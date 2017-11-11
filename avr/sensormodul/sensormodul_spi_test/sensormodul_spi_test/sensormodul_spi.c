/*
 * sensormodul_spi.c
 *
 * Created: 2017-11-10 14:28:31
 *  Author: Daniel Thorén
 */ 
#include <string.h>

#include "lcd.h"
#include "sensormodul_spi.h"

#define OUTGOING_PACKET_SIZE 5

volatile unsigned char outgoing[OUTGOING_PACKET_SIZE] = {0};
volatile short int recieved=0;
sensormodul_PA_data buffer;

void set_outgoing_data(sensormodul_PA_data data){
	if ((PORTB & 0b00001000) != 0){
		memcpy((void*) &outgoing, (void*) &data.sonar_data, 4);
		outgoing[4] = data.lapsensor;
	}
	else{
		buffer = data;
	}
}

// Initialize SPI Slave Device
void spi_init (void)
{
	DDRB = (1 << DDB6);			//Set MISO as output
	SPCR=(1<<SPE)|(1<<SPIE);	//Enable SPI && interrupt enable bit
	buffer.lapsensor = 0xFF;
}

//Checks if this is the end of the message, else sends next byte
void spi_tranciever(){
	if (recieved == OUTGOING_PACKET_SIZE){
		if (buffer.lapsensor != 0xFF){
			set_outgoing_data(buffer);
			buffer.lapsensor = 0xFF;
		}
	}
	else{
		SPDR = outgoing[recieved++];
	}
}