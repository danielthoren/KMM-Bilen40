/*
 * motormodul_v1.c
 *
 * Created: 11/12/2017 4:28:20 PM
 *  Author: marli763, krisi211, gussö811
 */



/* --- TODO TODO TODO TODO TODO TODO ---
 * Fix data types when calculating RPM/RPS
 * Comment properly
 * Merge with master
 * Incorporate RPM into scale
 * Remove lcd compability (?)
 *
*/

#define F_CPU 16000000

#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include "motormodul_spi.h"

#include "lcd.h"

// DEBUG LED
#define led_on()  PORTA |= _BV(1)
#define led_off()  PORTA &= ~_BV(1)
#define led_is_on() bit_is_set(PORTA,1)
#define timer_led_on() PORTA |= _BV(2)
#define timer_led_off() PORTA &= ~_BV(2)
#define timer_led_is_on() bit_is_set(PORTA,2)

//		--- PWM ---
const int natural = 3000;		//Pulse is 1,5 ms
const int max_left = 3900;		//Ish max right (pulse should be 2 ms)
const int max_right = 2100;		//Ish max left (pulse should be 1ms)
const int max_speed;			//FIND ITS VALUE
const int min_speed = 3170;		//FIND ITS VALUE
int turn;						//Turn < natural => right, turn > natural => left
int scale_speed;

//		--- HALLEFFECT ---
volatile uint32_t ticks_elapsed;	//ticks since last timer-intr
volatile uint32_t time_elapsed;	//ticks (ys) converted into time
volatile uint8_t rpm;				//revolutions per minute
volatile uint32_t tot_overflow = 0; //unset when ready
volatile uint32_t current_ticks;
volatile uint32_t TIMER_TICKS = 65536;
volatile uint32_t micro_seconds_per_tick = 16;
int new_rpm;

motormodul_PA_data data_in;
 
//data sent from 'motormodul' (A = AVR) to raspberry pi (=P)
motormodul_AP_data data_out;

void timer3_init()
{
	//		--- TIMER FOR HALL EFFECT SENSOR SETUP ---
	TCCR3A |= _BV(WGM32);
	TCCR3B |= _BV(CS32);		//16MHz, 16 bit timer and 256 prescaler gives 0.95367431640625Hz
	TCNT3 = 0;					// Reset counter
	TIMSK3 |= (1 << TOIE3);
}

void pwm_init()
{
	//		--- PWM SETUP ---
	//Pin set-up
	DDRD |= _BV(5);				//Pin 19, styrservot ()
	DDRD |= _BV(4);				//Pin 18, motor
	//timer set-up
	TCCR1A |= _BV(1) | _BV(7) | _BV(5);
	TCCR1B |= _BV(3)| _BV(4) | _BV(1);
	ICR1 = 40000;
	//send out neutral mode
	turn = natural;
	scale_speed = natural;
	OCR1A = turn;
	OCR1B = scale_speed;
	 led_on();
	_delay_ms(5000);			// delay so that the motor control receives it's neutral properly
	 led_off();
}

void halleffect_init()
{
	//		--- HALL EFFECT SETUP ---
	// PINCHANGE INTERRUPT FOR MEASURING PULSES
	DDRA  = 0b11111110;
	PCICR |= (1 << PCIE0);		// set PCIE0 to enable PCMSK0 scan
	PCMSK0 |= (1 << PCINT0);	// set PCINT0 to trigger an interrupt on state change
	tot_overflow = 0;
}
void lcd_init(){
		//		--- LCD SETUP ---
		//Initialize LCD module
		LCDInit(LS_BLINK|LS_ULINE);
		
		//Clear the screen
		LCDClear();
		
		LCDWriteString("STARTING");
}
void scale(){
	if(data_in.angle <= 180 && data_in.angle >= 0)
	{
		turn = (int)((10 *data_in.angle) + 2100);
	}
	else if(data_in.angle == 90){ turn = natural;} 
	else
	{
		turn = turn;
	}
	//Update speed limits,
	//Probable max speed = 40000
	if(data_in.speed <= 200 && data_in.speed >= 101)
	{
		scale_speed = (int)(3180 + (data_in.speed - 100));
	}
	else if (data_in.speed <= 99 && data_in.speed >= 0)
	{	
		scale_speed = (int)(2820 + (data_in.speed - 100));
	}
	else if (data_in.speed == 100){scale_speed = natural;}
	else{
		scale_speed = scale_speed;
	}
	
}
//      --- P algorithm ---
	float pGain = 0.001;						//Default value
	float currVal = 3000;						// latest input , current value


void p_loop()
{	
	float currOutVal = currVal;
	float setVal = (float)scale_speed;		// the desired value of the controller
	float errorVal = setVal - currVal;		// calculate proportional term
	float pTerm = pGain * errorVal ;		// calculate the new output
	currVal = currOutVal + pTerm ;
}


int main(void)
{
	//		--- Initialize timers & 'modules' ---
	//lcd_init();
	pwm_init();
	halleffect_init();
	spi_init();
	timer3_init();

	sei();
	
	//		--- Main loop, receive tasks from master ---
    while(1)
    {
		
		data_out.curr_rpm = rpm;
		set_spi_data(data_out);
		if(get_data_available()){
			get_spi_data(&data_in);
			pGain = data_in.pGain;
			scale();
			}
		p_loop();
		OCR1A = turn;
		OCR1B = (int)currVal;
    }
}


ISR(PCINT0_vect)
{
	//		--- Pin change interrupt for hall effect sensor ---
	// Just measure on incoming magnet, not outgoing
	if( PINA & ((1 << PIND0) == 1)){
		
		// Debug LED
		if (led_is_on())
			led_off();
		else
			led_on();
	
		// RPM Calculations TODO: CHANGE DATA TYPES
		current_ticks = TCNT3;
		ticks_elapsed = (tot_overflow * TIMER_TICKS) + current_ticks;
		time_elapsed = ticks_elapsed * micro_seconds_per_tick;//seconds
		tot_overflow = 0;		//Reset registered overflows and timer counter
		TCNT3 = 0;
	
		rpm = (uint8_t) (60000000/(time_elapsed*4));//60*1.000.000 minute and scale microseconds
	}
}


ISR(TIMER3_OVF_vect)
{
	//		--- Timer interupt (0.953~ Hz) ---
	
	// Debug LED (Not connected to board currently 24/11)
	if (timer_led_is_on())
	timer_led_off();
	else
	timer_led_on();
	
	tot_overflow++;
	if(tot_overflow >= 2){
		rpm = 0;
		new_rpm=1;
		
	}
}
