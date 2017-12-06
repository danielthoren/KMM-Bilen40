//Frequency
#define F_CPU 16000000
#include <stdio.h>
#include <util/delay.h>
#include <stdlib.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <string.h>

#include "sensormodul_spi.h"

//Struct to send over spi
sensormodul_AP_data data;
//Temporary saved sonar data
//volatile unsigned char sonar_data[4];
//Timer ticks
//uint32_t pulse = 0;
//Whitch sensor

#define blue_led_on() PORTC |= _BV(1);
#define blue_led_off() PORTC &= ~_BV(1);

//Which mode/sensor is active.
//enum Modes {sonar1=0,sonar2=1, sonar3=2, sonar4=3, sensor_active=4, send_data=5};
//enum Modes mode = sonar1;

//Interruptrutin for sonarsensorer, save pulses from timer1, from burst to receive signal.
//void sonar_timer_interrupt();

//Convert pulses to cm. 
//void calc_sonar_data(int sonar, uint32_t pulse);
//Init SPI
void send_spi();
//Init for sensormodul
//void sensor_init();
//Init for lap sensor
void lapsensor_init();
//Might have to be changed to clear instead of set
#define clear_lap()  PORTB &= ~_BV(3)
#define unclear_lap()  PORTB |= _BV(3)

int main(void)
{
	//Init spi
	spi_init();
	
	//Init sensormodule
	//sensor_init();
	
	//Init lap sensor
	lapsensor_init();
	data.lapsensor = 0;
	
	//Enable globel interrupt
	sei();
	

	while(1 == 1)
	{
		_delay_ms(10);
	}
}

void lapsensor_init(){
	//Pin B2 will serve as the interrupt pin
	//Pin B3 will serve as a clear to the lap sensor
	
	//16bit Timer Set-up for lapcounter
	TCCR3A |= _BV(WGM32);
	TCCR3B |= _BV(CS32) |_BV(CS30);		//16MHz, 16 bit timer and 1024 prescaler gives 0.95367431640625Hz
	TCNT3 = 0;					// Reset counter
	TIMSK3 |= (1 << TOIE3);
	EICRA |= _BV(ISC21) | _BV(ISC20);
	EIMSK |= _BV(INT2);
	DDRB |= 0b00001000;
	DDRB &= 0b11111011;	
	unclear_lap();
}


void send_spi(){
	data.sonar_data[0] = 0;
	data.sonar_data[1] = 0;
	data.sonar_data[2] = 0;
	data.sonar_data[3] = 0;
	set_outgoing_data(data);
}

ISR(TIMER3_OVF_vect)
{		
		data.lapsensor = 0;
		clear_lap();
		unclear_lap();
}

//Send data to master
ISR(SPI_STC_vect){
	spi_tranciever();
}

	
ISR(INT2_vect){
		//if (bit_is_set(PORTB,2))
		
			data.lapsensor = 1;
			TCNT3 = 0;
			send_spi();
			//clear_lap();
			//_delay_ms(10);
			//unclear_lap();
		
}


























/*
void sonar_timer_interrupt(int sonar){
	//Echo pin interrupt
	switch (sonar)
	{	case 0:
		//LOW -> HIGH
		if( (PINA & (1 << PINA0)) == 1)
		{
			// Raknare=0
			TCNT1=0;
			TCCR1B |= _BV(0);
		}
		//HIGh -> LOW
		else{
			//Stops conter
			TCCR1B &= ~_BV(0);
			TCCR3B &= ~_BV(0);
			pulse=TCNT1;
			calc_sonar_data(sonar, pulse);
			mode = sonar2;
		}break;
		case 1:
		//LOW -> HIGH
		if( (PINB & (1 << PINB0)) == 1)
		{
			// Raknare=0
			TCNT1=0;
			TCCR1B |= _BV(0);
		}
		//HIGh -> LOW
		else{
			//Stops conter
			TCCR1B &= ~_BV(0);
			TCCR3B &= ~_BV(0);
			pulse=TCNT1;
			calc_sonar_data(sonar, pulse);
			mode = sonar3;
		}break;
		case 2:
		//LOW -> HIGH
		if( (PINC & (1 << PINC0)) == 1)
		{
			// Raknare=0
			TCNT1=0;
			TCCR1B |= _BV(0);
		}
		//HIGh -> LOW
		else{
			//Stops conter
			TCCR1B &= ~_BV(0);
			TCCR3B &= ~_BV(0);
			pulse=TCNT1;
			calc_sonar_data(sonar, pulse);
			mode = sonar4;
		}break;
		case 3:
		//LOW -> HIGH
		if( (PIND & (1 << PIND2)) == 1)
		{
			// Raknare=0
			TCNT1=0;
			TCCR1B |= _BV(0);
		}
		//HIGh -> LOW
		else{
			//Stops conter
			TCCR1B &= ~_BV(0);
			TCCR3B &= ~_BV(0);
			pulse=TCNT1;
			calc_sonar_data(sonar, pulse);
			mode = send_data;
		}break;
	}
}
//Calculate distance with timer value and speed of sound
void calc_sonar_data(int sonar, uint32_t pulse){
	//Longer then 86 cm, invalid,w value
	if (pulse > 50000){
		sonar_data[sonar] = 0xFF;
	}
	else{
		uint32_t cm;
		cm = (pulse/580);
	sonar_data[sonar] = cm;}
}

//Sonar 1 interrupt
ISR(PCINT0_vect){sonar_timer_interrupt(0);}

//Sonar 2 interrupt
ISR(PCINT1_vect){sonar_timer_interrupt(1);}

//Sonar 3 interrupt
ISR(PCINT2_vect){sonar_timer_interrupt(2);}

//Sonar 4 interrupt
ISR(PCINT3_vect){sonar_timer_interrupt(3);}


//Take too long time too get data, reset
ISR (TIMER3_COMPA_vect)
{
	//Stops counter
	TCCR1B &= ~_BV(0);
	TCCR3B &= ~_BV(0);
	//Take next sensor
	if (mode > 3){
		mode = sonar1;
		}
	else{mode = mode + 1;
		}
	
}

ISR (TIMER3_OVF_vect)
{
	//Stops counter
	TCCR1B &= ~_BV(0);
	TCCR3B &= ~_BV(0);
	TCNT3=0;
	//Take next sensor
	if (mode > 3){
		mode = sonar1;
	}
	else{mode = mode + 1;
	}
	
}


//Collectad data sent to spi module
void ready_to_send_spi(){
	if (mode == send_data){
		memcpy((void*) data.sonar_data, (void*) sonar_data, 4);
		set_outgoing_data(data);
		//start over
		mode = sonar1;
	}
}

void sensor_init(){
	
	//Pins is now an output
	DDRA |= 0b00000010;
	DDRB |= 0b00001110;		//B2 & B3 is for the lap sensor
	DDRC |= 0b00000010;
	DDRD |= 0b00000010;
	//Pins is now an input
	DDRA &= 0b11111110;
	DDRB &= 0b11111110;
	DDRC &= 0b11111110;
	DDRD &= 0b11111011;
	
	_delay_ms(10);
	
	
	//Turn on interrupt on PCMSK pins
	PCICR |= _BV(3)| _BV(2)| _BV(1)| _BV(0);
	//Theses pins now trigger an interrupt
	PCMSK0 |= _BV(0);
	PCMSK1 |= _BV(0);
	PCMSK2 |= _BV(0);
	PCMSK3 |= _BV(2);

	//Timer interrupt enable when timer hits 50000
	TIMSK3 |= _BV(0);	TCCR3B |= _BV(3);	TCCR3B &= ~_BV(0);	OCR3A = 50000;
	//Timer stopped
	TCCR1B &= ~_BV(0);
}
*/