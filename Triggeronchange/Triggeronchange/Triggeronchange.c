/*
 * Triggeronchange.c
 *
 * Created: 11/7/2017 2:33:23 PM
 *  Author: marli763
 */ 

#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#define led_on()  PORTA |= _BV(1)
#define led_off()  PORTA &= ~_BV(1)
#define led_is_on() bit_is_set(PORTA,1)
#define timer_led_on() PORTA |= _BV(2)
#define timer_led_off() PORTA &= ~_BV(2)
#define timer_led_is_on() bit_is_set(PORTA,2)

volatile int pulses;
volatile int rpm;

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

int main (void) {
	// PINCHANGE INTERRUPT FOR MEASURING PULSES
	DDRA  = 0b11111110;

	PCICR |= (1 << PCIE0);    // set PCIE0 to enable PCMSK0 scan
	PCMSK0 |= (1 << PCINT0);  // set PCINT0 to trigger an interrupt on state change

	// TIMER INTERRUPT FOR MEASURING SPEED
	
	timer0_init();
	
	pulses = 0;

	sei();                //sets the bit and switches interrupts on

	while(1) {
		count();
	}
}

void count() {
	// main program loop
}

//PULSE INTERRUPT
ISR(PCINT0_vect)
{
	pulses++;
}

ISR(TIMER0_OVF_vect)
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