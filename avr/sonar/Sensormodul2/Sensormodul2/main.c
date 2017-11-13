//Frequency
#define F_CPU 16000000
#include <stdio.h>
#include <util/delay.h>
#include <stdlib.h>
#include "sensormodul_spi.h"
#include <avr/io.h>
#include <avr/interrupt.h>

//Struct to send over spi
sensormodul_AP_data data;
//Temporary saved sonar data
volatile unsigned char sonar_data[4];
//Timer ticks
uint32_t pulse = 0;
//Whitch sensor
unsigned short sonar_nr;

#define blue_led_on() PORTC |= _BV(1);
#define blue_led_off() PORTC &= ~_BV(1);


//Which mode/sensor is active. 
int mode = 0;

//Interruptrutin for sonarsensorer, save pulses from timer1, from burst to receive signal.
void sonar_timer_interrupt();

//Convert pulses to cm. 
void calc_sonar_data(unsigned short sonar_nr, uint32_t pulse);

int main(void)
{
	//Init pins for sensormodul
	sensor_init();
	
	//Init SPI
	spi_init();
	
	//Enable globel interrupt
	sei();
	
	
	while(1 == 1)
	{
		_delay_ms(100);
		switch (mode)
		{
			case 0:
				//Triggerpin is high for 15uS
				PORTA|=_BV(1);
				_delay_us(15);
				PORTA &= ~_BV(1);
				mode = 5;
				_delay_ms(10);
				break;
			case 1:
				//Triggerpin is high for 15uS
				PORTB|=_BV(1);
				_delay_us(15);
				PORTB &= ~_BV(1);
				mode = 5;
				_delay_ms(10);
				break;
			case 2:
				//Triggerpin is high for 15uS
				PORTC|=_BV(1);
				_delay_us(15);
				PORTC &= ~_BV(1);
				mode = 5;
				_delay_ms(10);
				break;
			case 3:
				//Triggerpin is high for 15uS
				PORTD|=_BV(1);
				_delay_us(15);
				PORTD &= ~_BV(1);
				mode = 5;
				_delay_ms(10);
				break;
		}
		ready_to_send_spi();
		
}
}

void ready_to_send_spi(){
	if (mode == 6){
		cli();
		//data.sonar_data = sonar_data;
		set_outgoing_data(data);
		mode = 0;
		sei();
	}
}

void sensor_init(){
	
	//Pins is now an output and input
	DDRA = 0b00000010;
	DDRB = 0b00000010;
	DDRC = 0b00000010;
	DDRD = 0b00000010;
	_delay_ms(10);
	
	
	//Turn on interrupt on PCMSK2 pins
	PCICR |= _BV(3)| _BV(2)| _BV(1)| _BV(0);
	//Theses pins now trigger an interrupt
	PCMSK0 |= _BV(0);
	PCMSK1 |= _BV(0);
	PCMSK2 |= _BV(0);
	PCMSK3 |= _BV(2);

	TCCR1B = 0;
	//Turn on global interrupt
}


void sonar_timer_interrupt(int sonar_nr){
	
	switch (sonar_nr)
	{
		case 0:
		//LOW -> HIGH
		if( (PINA & (1 << PINA0)) == 1)
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
			calc_sonar_data(0, pulse);
			mode = 1;
			
		}break;
		case 1:
		//LOW -> HIGH
		if( (PINB & (1 << PINB0)) == 1)
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
			calc_sonar_data(0, pulse);
			mode = 2;
		}break;
		case 2:
		//LOW -> HIGH
		if( (PINC & (1 << PINC0)) == 1)
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
			calc_sonar_data(0, pulse);
			mode = 3;
		}break;
		case 3:
		//LOW -> HIGH
		if( (PIND & (1 << PIND2)) == 1)
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
			calc_sonar_data(0, pulse);
			mode = 6;
		}break;
	}
}

void calc_sonar_data(unsigned short sonar_nr, uint32_t pulse){
	uint32_t cm;
	cm = (pulse/480)+2;
	sonar_data[sonar_nr] = cm;
}


ISR(PCINT0_vect){sonar_timer_interrupt(0);}


ISR(PCINT1_vect){sonar_timer_interrupt(1);}


ISR(PCINT2_vect){sonar_timer_interrupt(2);}


ISR(PCINT3_vect){sonar_timer_interrupt(3);}



//Take too long time too get data, reset
ISR (TIMER1_OVF_vect)
{
	//Stops counter
	TCCR1B=0;
	mode = 0;
}

ISR(SPI_STC_vect){
	spi_tranciever();
}