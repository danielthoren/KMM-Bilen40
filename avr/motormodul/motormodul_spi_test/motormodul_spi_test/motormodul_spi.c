/*
 * sensormodul_spi.c
 *
 * Created: 2017-11-10 14:28:31
 *  Author: Daniel Thorén
 */ 
#include <string.h>
#include <stdlib.h>

#include "lcd.h"
#include "motormodul_spi.h"

#define OUTGOING_PACKET_SIZE 1
#define INCOMMING_PACKET_SIZE 2

volatile unsigned char outgoing[OUTGOING_PACKET_SIZE] = {0};
volatile unsigned char incomming[INCOMMING_PACKET_SIZE] = {0};
volatile short int tranciever_count=0;
motormodul_AP_data buffer;
motormodul_AP_data outgoing_data;
unsigned char data_retrieved = 0;
unsigned char data_set = 0;

//Calculates a simple XOR checksum for the outgoing package
unsigned char calc_outgoing_checksum(volatile unsigned char data[OUTGOING_PACKET_SIZE]){
	unsigned char checksum = 0;
	for (int i = 0; i < (OUTGOING_PACKET_SIZE - 1); i++){
		checksum = checksum ^ data[i];
	}
	return checksum;
}

//Calculates a simple XOR checksum for the incomming package
unsigned char calc_incomming_checksum(volatile unsigned char data[INCOMMING_PACKET_SIZE]){
		unsigned char checksum = 0;
		for (int i = 0; i < (OUTGOING_PACKET_SIZE - 1); i++){
			checksum = checksum ^ data[i];
		}
		return checksum;
}

//converts the data of the outgoing 'sensormodul_AP_data' to the 'outgoing' char array
void set_outgoing(motormodul_AP_data* data){
	outgoing[0] = data->curr_rpm;
	
	outgoing[1] = calc_outgoing_checksum(outgoing);
	
	SPDR = outgoing[0];
}
#include <stdlib.h>
//converts the incomming char array to a struct of type 'motormodul_PA_data'
void get_incomming(motormodul_PA_data* data){
	data->speed = incomming[0];
	data->angle = incomming[1];	
}

void get_set_spi_data(motormodul_PA_data* data_in, motormodul_AP_data data_out){
	//setting outgoing data
	if ((PORTB & 0b00001000) != 0){
		//dismantling struct to outgoing data
		set_outgoing(&data_out);
		outgoing_data = data_out;
		
		//signal pi that there is new data
		PORTD |= 0b00000001;
		
		//building up struct from incomming data
		if(calc_incomming_checksum(incomming) == incomming[INCOMMING_PACKET_SIZE - 1]){
			get_incomming(data_in);
		}
		else{
			data_in->speed = 0xFF;
		}
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
	DDRD = (1<DDD0);			//Set pin 0 on PORTD as output, used to signal rasberry pi when data is available
	PORTD &= 0b11111110;		//init pin 0 on PORTD to 0
	buffer.curr_rpm = 0xFF;
}

//Checks if this is the end of the message, else sends next byte
void spi_tranciever(){
	if (tranciever_count >= INCOMMING_PACKET_SIZE &&
		tranciever_count >= OUTGOING_PACKET_SIZE){
			
			PORTD &= 0b11111110;
			tranciever_count = 0;
			if(buffer.curr_rpm != 0xFF){
				set_outgoing(&buffer);
				//signal pi that there is new data
				buffer.curr_rpm = 0xFF;
			}
			else{
				set_outgoing(&outgoing_data);
			}
	}
	else{
		incomming[tranciever_count] = SPDR;
		tranciever_count++;
		SPDR = outgoing[tranciever_count];
	}
}