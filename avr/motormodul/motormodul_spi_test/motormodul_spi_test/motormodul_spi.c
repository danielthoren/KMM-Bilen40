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
#define INCOMMING_PACKET_SIZE 2

volatile unsigned char outgoing[OUTGOING_PACKET_SIZE] = {0};
volatile unsigned char incomming[INCOMMING_PACKET_SIZE] = {0};
volatile short int recieved=0;
motormodul_AP_data buffer;
unsigned char data_retrieved = 0;
unsigned char data_set = 0;

unsigned char get_set_spi_data(motormodul_PA_data* data_in, motormodul_AP_data data_out){
	if ((PORTB & 0b00001000) != 0){
		//dismantling struct to outgoing data
		outgoing[0] = data_out.curr_rpm;
		
		//building up struct from incomming data
		data_in->speed = incomming[0];
		data_in->angle = incomming[1];
		
		//initializing spi transfer
		SPDR = outgoing[0];
	}
	else{
		buffer = data_out;
	}
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
	if (recieved == INCOMMING_PACKET_SIZE){
		if(buffer.curr_rpm != 0xFF){
			get_set_data(buffer);
			buffer.curr_rpm = 0xFF;
		}
		recieved = 0;
	}
	else{
		incomming[recieved] = SPDR;
		recieved++;
		SPDR = outgoing[recieved];
	}
}