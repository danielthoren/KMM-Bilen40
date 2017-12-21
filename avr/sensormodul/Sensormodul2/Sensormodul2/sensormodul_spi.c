/*
 * sensormodul_spi.c
 *
 * Created: 2017-11-10 14:28:31
 *  Author: Daniel Thorén
 */ 
#include <string.h>

#include "sensormodul_spi.h"

#define OUTGOING_PACKET_SIZE 6

volatile unsigned char outgoing[OUTGOING_PACKET_SIZE] = {0};
volatile short int tranciever_count=0;
sensormodul_AP_data outgoing_data;
sensormodul_AP_data buffer;

#define clear_lap()  PORTB &= ~_BV(3)
#define unclear_lap()  PORTB |= _BV(3)

//Calculates a simple XOR checksum for the outgoing package
unsigned char calc_outgoing_checksum(volatile unsigned char data[OUTGOING_PACKET_SIZE - 1]){
	unsigned char checksum = 0;
	for (int i = 0; i < (OUTGOING_PACKET_SIZE - 1); i++){
		checksum = checksum ^ data[i];
	}
	return checksum;
}

//converts the data of the incomming 'sensormodul_AP_data' to the 'outgoing' char array
void set_outgoing(sensormodul_AP_data data){
	memcpy((void*) outgoing, (void*) data.sonar_data, 4);
	outgoing[4] = data.lapsensor;
			
	outgoing[5] = calc_outgoing_checksum(outgoing);
	
	spi_tranciever();
}

void set_outgoing_data(sensormodul_AP_data data){
	if ((PINB & 0b00010000) != 0){
		set_outgoing(data);
		outgoing_data = data;
		
		PORTD |= 0b00000001;
	}
	else{
		buffer = data;
	}
}

// Initialize SPI Slave Device
void spi_init (void)
{
	DDRB |= (1 << DDB6);			//Set MISO as output
	DDRD |= _BV(0);			//Set pin 0 of PORTD as output, used to tell pi when new data is available
	PORTD &= 0b11111110;		//Inits pin 0 of PORTD to 0
	SPCR=(1<<SPE)|(1<<SPIE);	//Enable SPI && interrupt enable bit
	buffer.lapsensor = 0xFF;
}

//Checks if this is the end of the message, else sends next byte
void spi_tranciever(){
		
	if (tranciever_count == OUTGOING_PACKET_SIZE){
		tranciever_count = 0;
		PORTD &= 0b11111110;
	}
	else{
		SPDR = outgoing[tranciever_count];
		tranciever_count++;
	}
}