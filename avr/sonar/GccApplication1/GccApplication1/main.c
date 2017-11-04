// Interrupts funkar. Försöker få ett värde från timern. 
/////////////////////////////////////////////////////////////


#include <avr/io.h>
#include <avr/interrupt.h>

//Frequency
#define F_CPU 16000000

#include <util/delay.h>
#include <stdlib.h>

//Sonar trigger-pins
#define trig1 PD4

//Sonar echo-pins
#define echo1 PD0

int32_t sonar_data;

#define blue_led_on() PORTC |= _BV(0);

#define blue_led_off() PORTC &= ~_BV(0);
//Mode
int mode = 0;

void sonar_timer_interrupt();

void calc_sonar_data();

int main(void)
{

		
		DDRD = 0b00010000;
		_delay_ms(10);
		//Pins is now an output
		DDRC = 0b00000001;
		_delay_ms(10);
		PORTD |= _BV(0);
		
		
		//Turn on interrupt on PCMSK2 pins
		PCICR |= _BV(3);
		//Theses pins now trigger an interrupt
		PCMSK3 |= _BV(0);

		TCCR0B = 0;
	//Turn on global interrupt
	sei();
	
	
	while(1 == 1)
	{
			_delay_ms(10);
			if( mode == 0){
			//Triggerpin is high for 15uS
			PORTD|=_BV(4);
			_delay_us(15);
			PORTD &= ~_BV(4);
			mode = 1;
			_delay_ms(10);
			}

	}
}
//Interrupt function
ISR(PCINT3_vect)
{

	sonar_timer_interrupt(0);
}



void sonar_timer_interrupt(int sonar_nr){
	//LOW -> HIGH
	if( (PIND & (1 << PIND0)) == 1)
	{
		blue_led_on();
			// Raknare=0
			TCNT0=0;
			
			//Turn on counter
			TCCR0B |= (1 << CS02) | (0 << CS01) | (1 << CS00);
			}
	//HIGh -> LOW
	else{
				//Stops conter
				TCCR0B=0;
				int32_t pulse=TCNT0;
				calc_sonar_data(0, pulse);
				mode = 0;
				
	}
}

void calc_sonar_data(int sonar_nr, int32_t pulse){
	int cm;
	cm = (pulse*64)/58;
	if (pulse <= 200){
		blue_led_off();
	}
	sonar_data= cm;
}


//Take too long time too get data, reset
ISR (TIMER1_OVF_vect)
{
	//Stops counter
	TCCR1B=0;
	//////////////////////////////////////////
	//Reset everything
	//////////////////////////////////////////
}
