/*
 * HallEffectSensor.c
 *
 * Created: 11/6/2017 1:36:05 PM
 *  Author: marli763
 */ 


#include <avr/io.h>
#define led_on()  PORTD |= _BV(0)
#define led_off()  PORTD &= ~_BV(0)
#define led_is_on() bit_is_set(PORTD,0)

volatile int pulses = 0;

volatile int rpm;

int main (void) {
	// TIMER INTERRUPT FOR MEASURING SPEED
	DDRB  = 0b11111111;   // All outputs

	TIMSK0 = _BV(OCIE0A);  // Enable Interrupt TimerCounter0 Compare Match A (SIG_OUTPUT_COMPARE0A)
	TCCR0A = _BV(WGM00);  // Mode = PWM, Phase Correct
	TCCR0B = _BV(CS02) | _BV(CS00);   // Clock/1024, 0.001024 seconds per tick
	OCR0A = 244;          // 0.001024*244 ~= .25 SIG_OUTPUT_COMPARE0A will be triggered 8 times per second.

	DDRD &= ~(1 << DDD2);     // Clear the PD2 pin
	// PD2 (PCINT0 pin) is now an input

	// EXTERNAL INTERRUPT FOR MEASURING PULSES
	PORTD |= (1 << PORTD2);    // turn On the Pull-up
	// PD2 is now an input with pull-up enabled

	EICRA |= (1 << ISC00);    // set INT0 to trigger on ANY logic change
	EIMSK |= (1 << INT0);     // Turns on INT0

	sei();                //sets the bit and switches interrupts on

	while(1) {
		count();
	}
}

void count() {
	// main program loop
}

//PULSE INTERRUPT
ISR(PCINT0_vect) {
	if (led_is_on())
	{
		led_off();
	}
	else {
		led_on();
	}
}
//SEND RPM TO MAIN UNIT

ISR(SIG_OUTPUT_COMPARE0A) {
	//rpm = pulses * 60 * 4 / 2;
	//pulses = 0;
	//Send RPM
}
