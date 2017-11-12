﻿/*
 * sensormodul_spi.c
 *
 * Created: 2017-11-10 14:28:31
 *  Author: Daniel Thorén
 */ 
#include <string.h>

#include "lcd.h"
#include "sensormodul_spi.h"

#define OUTGOING_PACKET_SIZE 6

volatile unsigned char outgoing[OUTGOING_PACKET_SIZE] = {0};
volatile short int tranciever_count=0;
sensormodul_AP_data buffer;

//Calculates a simple XOR checksum for the outgoing package
unsigned char calc_outgoing_checksum(volatile unsigned char data[OUTGOING_PACKET_SIZE - 1]){
	unsigned char checksum = 0;
	for (int i = 0; i < (OUTGOING_PACKET_SIZE - 1); i++){
		checksum = checksum ^ data[i];
	}
	return checksum;
}

void set_outgoing(sensormodul_AP_data data){
	memcpy((void*) outgoing, (void*) data.sonar_data, 4);
	outgoing[4] = data.lapsensor;
			
	outgoing[5] = calc_outgoing_checksum(outgoing);
}

void set_outgoing_data(sensormodul_AP_data data){
	if ((PINB & 0b00010000) != 0){
		set_outgoing(data);
		
		//initializing first transfer
		spi_tranciever();
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
	if (tranciever_count == OUTGOING_PACKET_SIZE){
		tranciever_count = 0;
		if (buffer.lapsensor != 0xFF){
			set_outgoing(buffer);
			
			SPDR = outgoing[0];
			tranciever_count++;
			buffer.lapsensor = 0xFF;
		}
		else{
			memcpy((void*) outgoing, 0, OUTGOING_PACKET_SIZE);
			
		}
	}
	else{
		SPDR = outgoing[tranciever_count];
		tranciever_count++;
	}
}