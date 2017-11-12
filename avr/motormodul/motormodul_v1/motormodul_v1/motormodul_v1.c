/*
 * motormodul_v1.c
 *
 * Created: 11/12/2017 4:28:20 PM
 *  Author: marli763, krisi211, gussö811
 */ 

#define F_CPU 16000000

#include <avr/io.h>
#include <avr/delay.h>
#include <avr/interrupt.h>

#include "lcd.h"

// DEBUG LED
#define led_on()  PORTA |= _BV(1)
#define led_off()  PORTA &= ~_BV(1)
#define led_is_on() bit_is_set(PORTA,1)
#define timer_led_on() PORTA |= _BV(2)
#define timer_led_off() PORTA &= ~_BV(2)
#define timer_led_is_on() bit_is_set(PORTA,2)

//		--- PWM ---
const int natural = 3000; //Pulse is 1,5 ms
const int max_left = 3900; //Ish max right (pulse should be 2 ms)
const int max_right = 2100; //Ish max left (pulse should be 1ms)
const int max_speed; //FIND ITS VALUE
const int min_speed = 3170; //FIND ITS VALUE
int turn; //Turn < natural => right, turn > natural => left
int speed;
uint8_t scale_turn;
uint8_t scale_speed;

//		--- HALLEFFECT ---
volatile long ticks_elapsed;
volatile float time_elapsed;
volatile float rpm;
volatile int tot_overflow;
uint32_t current_ticks;
volatile long TIMER_TICKS = 65536;
volatile float seconds_per_tick = 0.000016;



//Timer3 initiate for Hall effect
void timer3_init()
{
	TCCR3A |= _BV(WGM32);
	TCCR3B |= _BV(CS32);//16MHz, 16 bit timer and 256 prescaler gives 0.95367431640625Hz
	
	TCNT3 = 0;
	
	TIMSK3 |= (1 << TOIE3);
}

void pwm_init()
{
	//		--- PWM SETUP ---
	//Pin set-up
	DDRD |= _BV(5); //Pinne 19, styrservot
	DDRD |= _BV(4); //Pinne 18, motorn
	//timer set-up
	TCCR1A |= _BV(1) | _BV(7) | _BV(5);
	TCCR1B |= _BV(3)| _BV(4) | _BV(1);
	ICR1 = 40000;
}

void halleffect_init()
{
	//		--- HALL EFFECT SETUP ---
	// PINCHANGE INTERRUPT FOR MEASURING PULSES
	DDRA  = 0b11111110;
	PCICR |= (1 << PCIE0);    // set PCIE0 to enable PCMSK0 scan
	PCMSK0 |= (1 << PCINT0);  // set PCINT0 to trigger an interrupt on state change
	tot_overflow = 0;
}
/*
void scale(){
	if(scale_turn <= 180 && scale_turn >= 1)
	{
		turn = (10 *scale_turn) + 2100;
	}
	else
	{
		turn = natural;
	}
	//Uppdatera granser för hastighet,
	//maxhastighet troligen innan speed = 40000
	if(scale_speed <= 40 && scale_speed >= 1)
	{
		speed = (1000*scale_speed);
	}
	else
	{
		speed = natural;
	}
	
}*/

int main(void)
{
	//		--- LCD SETUP ---
	//Initialize LCD module
	LCDInit(LS_BLINK|LS_ULINE);
			
	//Clear the screen
	LCDClear();
			
	LCDWriteString("STARTING");
	
	pwm_init();
	halleffect_init();
	// TIMER INTERRUPT FOR MEASURING SPEED
	timer3_init();

	sei();
	
	//send out neutral mode
	turn = natural;
	speed = natural;
	OCR1A = turn;
	OCR1B = speed;
	_delay_ms(5000);
	
	speed = 3230;
	
    while(1)
    {
	    OCR1A = turn;
	    OCR1B = speed;
    }
}


ISR(PCINT0_vect)
{
	if( PINA & (1 << PIND0) == 1){
	LCDClear();
	if (led_is_on())
	led_off();
	else
	led_on();
	
	current_ticks = TCNT3;
	ticks_elapsed = (tot_overflow * TIMER_TICKS) + current_ticks;
	time_elapsed = (float) ticks_elapsed * seconds_per_tick;//seconds
	
	tot_overflow = 0;
	TCNT3 = 0;
	
	rpm = (float) (1/(time_elapsed*4)) ;
	LCDWriteInt(rpm,6);
	}
	//LCDWriteString("triggered");
}


ISR(TIMER3_OVF_vect)
{
	if (timer_led_is_on())
	timer_led_off();
	else
	timer_led_on();
	
	tot_overflow++;
}