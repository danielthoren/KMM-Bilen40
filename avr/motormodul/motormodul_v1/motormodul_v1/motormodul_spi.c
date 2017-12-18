/*
 * sensormodul_spi.c
 *
 * Created: 2017-11-10 14:28:31
 *  Author: Daniel Thorén
 */ 
#include <string.h>
#include <stdlib.h>
#include <stdlib.h>

#include "lcd.h"
#include "motormodul_spi.h"

#define OUTGOING_PACKET_SIZE 2
#define INCOMMING_PACKET_SIZE 4

volatile unsigned char outgoing[OUTGOING_PACKET_SIZE] = {0};
volatile unsigned char incomming[INCOMMING_PACKET_SIZE] = {0};
volatile short int tranciever_count=0;
motormodul_AP_data buffer;
motormodul_AP_data outgoing_data;
unsigned char data_set = 0;
unsigned char data_available;

unsigned char get_data_available(){
	return data_available;
}

//Calculates a simple XOR checksum for the incomming package
unsigned char calc_checksum(volatile unsigned char data[], int size){
		unsigned char checksum = 0;
		for (int i = 0; i < (size); i++){
			checksum = checksum ^ data[i];
		}
		return checksum;
}

//converts the data of the outgoing 'sensormodul_AP_data' to the 'outgoing' char array
void set_outgoing(motormodul_AP_data* data){
	outgoing[0] = data->curr_rpm;
	
	outgoing[1] = calc_checksum(outgoing, OUTGOING_PACKET_SIZE);
	
	SPDR = outgoing[0];
}

//converts the incomming char array to a struct of type 'motormodul_PA_data'
void get_incomming(motormodul_PA_data* data){
	data->speed = incomming[0];
	data->angle = incomming[1];
	data->pGain = incomming[2];
}

void set_spi_data(motormodul_AP_data data){
	if ((PINB & 0b00010000) != 0){
		//dismantling struct to outgoing data
		memcpy((void*) &outgoing_data, (void*) &data, sizeof(data));
		set_outgoing(&data);
	}
	else{
		buffer = data;
	}
}

void get_spi_data(motormodul_PA_data* data){
	//building up struct from incomming data
	data_available = 0;
	if(calc_checksum(incomming, INCOMMING_PACKET_SIZE - 1) == incomming[INCOMMING_PACKET_SIZE - 1]){
		get_incomming(data);
	}
	memcpy((void*) incomming, 0, sizeof(incomming));
}

// Initialize SPI Slave Device
void spi_init (void)
{
	DDRB |= (1 << DDB6);		//Set MISO as output
	SPCR |= (1<<SPE)|(1<<SPIE);	//Enable SPI && interrupt enable bit
	PORTD &= 0b11111110;		//Inits pin 0 of PORTD to 0
	data_available = 0;
	buffer.curr_rpm = 0xFF;
}

//only sets data if the SS pin is high, if it is low that means that a transfer is in progress.
//The data is saved in a buffer and set as outgoing data when SS goes high.
//When new data is available PORTD0 goes high until the pi has read the data, then it goes low again.
void spi_tranciever(){
	//If SS line is low then message is still being trancieved. Else there might have been a lost bit or
	//involentary reset of the other side, thus aborting current message and getting ready for a new one
	tranciever_count++;
	if (tranciever_count >= INCOMMING_PACKET_SIZE &&
	tranciever_count >= OUTGOING_PACKET_SIZE){
		//getting the last byte of the incomming package
		incomming[tranciever_count-1] = SPDR;
		data_available = 1;
		tranciever_count = 0;
		memcpy((void*) outgoing, 0, OUTGOING_PACKET_SIZE);
		if(buffer.curr_rpm != 0xFF){
			set_outgoing(&buffer);
			buffer.curr_rpm = 0xFF;
		}
		else{
			set_outgoing(&outgoing_data);
		}
	}
	else{
		incomming[tranciever_count-1] = SPDR;
		if(tranciever_count >= OUTGOING_PACKET_SIZE){
			SPDR = 0xFF;
		}
		else{
			SPDR = outgoing[tranciever_count];
		}
	}
}

ISR(SPI_STC_vect){
	spi_tranciever();
}