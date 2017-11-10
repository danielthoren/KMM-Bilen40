﻿/*
 * sensormodul_spi.c
 *
 * Created: 2017-11-10 14:28:31
 *  Author: Daniel Thorén
 */ 
#include "lcd.h"

#define OUTGOING_PACKET_SIZE 5

volatile unsigned char outgoing[OUTGOING_PACKET_SIZE] = {0};
volatile short int recieved=0;
struct sensormodul_PA_data outgoing_data;
struct sensormodul_PA_data buffer;

struct sensormodul_PA_data{
	int8_t sonar_data[4];
	char lapsensor;
};

void set_outgoing_data(struct sensormodul_PA_data data){
	if ((PORTB & 0b00001000) != 0){
		outgoing_data = data;
	}
	else{
		buffer = data;
	}
}

// Initialize SPI Slave Device
void spi_init_spi (void)
{
	DDRB = (1 << DDB6);			//Set MISO as output
	SPCR=(1<<SPE)|(1<<SPIE);	//Enable SPI && interrupt enable bit
	buffer.lapsensor = 0;
}

//Checks if this is the end of the message, else sends next byte
void spi_tranciever(){
	if (recieved == OUTGOING_PACKET_SIZE){
		if (buffer.lapsensor != 0){
			outgoing_data = buffer;
			buffer.lapsensor = 0;
		}
	}
	else{
		SPDR = outgoing[recieved++];
	}
}