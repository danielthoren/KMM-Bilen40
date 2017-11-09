#define F_CPU 16000000

#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

void pwm_init()
{
// initialize TCCR0 as per requirement, say as follows
TCCR0A |= (0<<WGM01)|(1<<COM0A1)|(1<<WGM00);
TCCR0B |= (1<<WGM02)|(1<<CS01);
// make sure to make OC0 pin (pin PB3 for atmega32) as output pin
DDRB = (1<<4);
DDRA = (1<<2);
sei();

}

void main()
{
	PORTA = _BV(1);
	uint8_t duty;
	duty = 115;       // duty cycle = 45% of 255 = 114.75 = 115

	// initialize timer in PWM mode
	pwm_init();

	OCR0A = duty;
	_delay_ms(10);

		// run forever
		while(1)
		{
		OCR0A = 255;
		_delay_ms(10);
		OCR0A = 0;
		_delay_ms(10);
		OCR0A = 255;
		_delay_ms(10);
		OCR0A = 0;
		_delay_ms(10);
		}
}