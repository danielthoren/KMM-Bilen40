// Interrupts funkar. Försöker få ett värde från timern. 
/////////////////////////////////////////////////////////////


#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>
//Frequency
#define F_CPU 16000000

#include <util/delay.h>
#include <stdlib.h>

//Sonar trigger-pins
#define trig1 PD4

//Sonar echo-pins
#define echo1 PD0

long double sonar_data = 0;
double pulse = 0;
unsigned short sonar_nr;

#define blue_led_on() PORTA |= _BV(1);

#define blue_led_off() PORTA &= ~_BV(1);
//Mode
int mode = 0;

void sonar_timer_interrupt();

void calc_sonar_data(unsigned short sonar_nr, double pulse);

int main(void)
{

		
		DDRD = 0b00010000;
		_delay_ms(10);
		//Pins is now an output
		DDRA = 0b00000010;
		_delay_ms(10);
		PORTD |= _BV(0);
		
		
		//Turn on interrupt on PCMSK2 pins
		PCICR |= _BV(3);
		//Theses pins now trigger an interrupt
		PCMSK3 |= _BV(0);

		TCCR1B = 0;
		
		  //Counter interrupt
		  TIMSK1 |= (1 << TOIE0);
		  
	  			
	//Turn on global interrupt
	sei();
	
	
	while(1 == 1)
	{		_delay_ms(10);
			if( mode == 0){
			//Triggerpin is high for 15uS
			PORTD|=_BV(4);
			_delay_us(15);
			PORTD &= ~_BV(4);
			mode = 1;
			}
			if(sonar_data < 30){
				blue_led_on();
			}
			else{
				blue_led_off();
			}
	}
}
//Interrupt function
ISR(PCINT3_vect)
{	
	sonar_timer_interrupt();
}



void sonar_timer_interrupt(){
	//LOW -> HIGH
	if( (PIND & (1 << PIND0)) == 1)
	{
			// Raknare=0
			TCNT1=0;
			TCCR1B = (0 << CS12) | (0 << CS11) | (1 << CS10);
			}

			
	//HIGh -> LOW
	else{
				//Stops conter
				TCCR1B = (0 << CS12) | (0 << CS11) | (0 << CS10);
				pulse=TCNT1;
				sonar_nr = 0;
				calc_sonar_data(sonar_nr, pulse);
				mode = 0;
				
	}
}

void calc_sonar_data(unsigned short sonar_nr, double pulse){
	sonar_data = pulse/58;
}


//Take too long time too get data, reset
ISR (TIMER1_OVF_vect)
{
	//Stops counter
	mode = 0;
	//////////////////////////////////////////
	//Reset everything
	//////////////////////////////////////////
}
