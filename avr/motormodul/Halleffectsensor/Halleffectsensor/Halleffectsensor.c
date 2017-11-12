/*
 * Triggeronchange.c
 *
 * Created: 11/7/2017 2:33:23 PM
 *  Author: marli763
 */ 

#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include "lcd.h"
#define F_CPU 16000000
#define led_on()  PORTA |= _BV(1)
#define led_off()  PORTA &= ~_BV(1)
#define led_is_on() bit_is_set(PORTA,1)
#define timer_led_on() PORTA |= _BV(2)
#define timer_led_off() PORTA &= ~_BV(2)
#define timer_led_is_on() bit_is_set(PORTA,2)


volatile long ticks_elapsed;

volatile float time_elapsed;

volatile float rpm;

volatile int tot_overflow;

uint32_t current_ticks;

volatile long TIMER_TICKS = 65536;

volatile float seconds_per_tick = 0.000016;

void timer0_init()
{
	// set up timer with prescaler = 1024
	TCCR0B |= (1 << CS02)|(1 << CS00);
	TCCR0A = _BV(WGM00);  // Mode = PWM, phase correct
	
	// initialize counter
	TCNT0 = 0;
	
	// enable overflow interrupt
	TIMSK0 |= (1 << TOIE0);
}

void timer3_init()
{
	TCCR3A |= _BV(WGM32);
	TCCR3B |= _BV(CS32);//16MHz, 16 bit timer and 256 prescaler gives 0.95367431640625Hz
	
	TCNT3 = 0;
	
	TIMSK3 |= (1 << TOIE3);
}

void lcd_init()
{
	   //Initialize LCD module
	   LCDInit(LS_BLINK|LS_ULINE);
	   
	   //Clear the screen
	   LCDClear();
}

int main (void) {
	
		//Initialize LCD module
		LCDInit(LS_BLINK|LS_ULINE);
		
		//Clear the screen
		LCDClear();
		
		LCDWriteString("inited");
		
	// PINCHANGE INTERRUPT FOR MEASURING PULSES
	DDRA  = 0b11111110;

	PCICR |= (1 << PCIE0);    // set PCIE0 to enable PCMSK0 scan
	PCMSK0 |= (1 << PCINT0);  // set PCINT0 to trigger an interrupt on state change

	// TIMER INTERRUPT FOR MEASURING SPEED
	
	timer3_init();
	
	tot_overflow = 0;

	sei();                //sets the bit and switches interrupts on

	while(1) {
		count();
	}
}

void count() {
}

/*PULSE INTERRUPT
ISR(PCINT0_vect)
{
	pulses++;
	if (led_is_on())
	led_off();
	else
	led_on();
}*/

ISR(PCINT0_vect)
{	
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
	
	rpm = (float) 1/(time_elapsed*8) ;
	LCDWriteInt(rpm,6);
	//LCDWriteString("triggered");
}



/*ISR(TIMER3_OVF_vect)
{
	//Calculate REVS per minute http://eleccelerator.com/avr-timer-calculator/
	//
	rpm = pulses * 60 * 2; // pulses to minutes, 2
	pulses = 0; //reset pulses
	//send rpm to main unit
	if (timer_led_is_on())
	timer_led_off();
	else
	timer_led_on();
	}
}*/

ISR(TIMER3_OVF_vect)
{
	if (timer_led_is_on())
	timer_led_off();
	else
	timer_led_on();
	
	tot_overflow++;
}