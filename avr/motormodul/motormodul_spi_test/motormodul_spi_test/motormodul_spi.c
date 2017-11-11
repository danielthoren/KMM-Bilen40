/*
 * sensormodul_spi.c
 *
 * Created: 2017-11-10 14:28:31
 *  Author: Daniel Thorén
 */ 
#include <string.h>

#include "lcd.h"
#include "motormodul_spi.h"

#define OUTGOING_PACKET_SIZE 1
#define INCOMMING_PACKET_SIZE 1

volatile unsigned char outgoing[OUTGOING_PACKET_SIZE] = {0};
volatile unsigned char incomming[INCOMMING_PACKET_SIZE] = {0};
volatile short int recieved=0;
motormodul_AP_data buffer;

void set_outgoing_data(motormodul_AP_data data){
	if ((PORTB & 0b00001000) != 0){
		outgoing[0] = data.curr_rpm;
	}
	else{
		buffer = data;
	}
}

motormodul_PA_data get_incomming_data(){
	motormodul_PA_data data;
	if ((PORTB & 0b00001000) != 0){
		data.speed = incomming[0];
		incomming[0] = 0xFF;
	}
	else{
		data.speed = 0xFF;
	}
	return data;
}

// Initialize SPI Slave Device
void spi_init (void)
{
	DDRB = (1 << DDB6);			//Set MISO as output
	SPCR=(1<<SPE)|(1<<SPIE);	//Enable SPI && interrupt enable bit
	buffer.curr_rpm = 0xFF;
	incomming[0] = 0xFF;
}

//Checks if this is the end of the message, else sends next byte
void spi_tranciever(){
	if (recieved == OUTGOING_PACKET_SIZE){
		if (buffer.curr_rpm != 0xFF){
			set_outgoing_data(buffer);
			buffer.curr_rpm = 0xFF;
			recieved = 0;
		}
	}
	else{
		incomming[recieved] = SPDR;
		SPDR = outgoing[recieved++];
	}
}