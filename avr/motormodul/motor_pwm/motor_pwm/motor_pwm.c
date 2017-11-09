/*
 * motor_pwm.c
 *
 * Created: 11/9/2017 9:04:09 AM
 *  Author: marli763
 */ 

#define F_CPU 16000000
#include <avr/io.h>
#include <avr/delay.h>
#include <avr/interrupt.h>

int natural = 3000;
int duty = 3200;

int main(void)
{
	//Pin set-up
	DDRD |= _BV(5);
	
	//timer set-up
	TCCR1A |= _BV(1) | _BV(7);
	TCCR1B |= _BV(3)| _BV(4) | _BV(1);
	ICR1 = 40000;
	//send out neutral mode
	OCR1A = natural;
	_delay_ms(5000);

	
    while(1)
    {
        //Read tasks from main unit, perform
		
		//test pwm

		OCR1A = duty;
		_delay_ms(5000);
		OCR1A = natural;
		_delay_ms(5000);
	}
	
}