/*
 * spi.c
 *
 * Created: 2017-11-03 10:48:11
 * Author : Daniel Thorén
 */ 

#include <avr/io.h>
#include <avr/interrupt.h>
#include <string.h>

#include "lcd.h"
#include "myutils.h"

//data sent from rasberry pi (=P) to motormodul (A = AVR)
struct motormodul_PA_data{
	int8_t speed;
	};
	
//data sent from 'motormodul' (A = AVR) to rasberry pi (=P)
struct motormodul_AP_data{
	int8_t curr_rpm;
	};

void split_int32(int32_t input, unsigned char output[4]){
	output[0] = (input >> 24) & 0xFF;
	output[1] = (input >> 16) & 0xFF;
	output[2] = (input >> 8) & 0xFF;
	output[3] = input & 0xFF;
}

int32_t build_int32(unsigned char input[4]){
	int32_t num = 0;
	num = (uint32_t)input[0] << 24 |
	(uint32_t)input[1] << 16 |
	(uint32_t)input[2] << 8  |
	(uint32_t)input[3];
	return num;
}

//Spi interrupt routine
ISR(SPI_STC_vect){
	spi_tranciever();
}

int main(void)
{
	//enabling interrupts
	sei();
	
   //Initialize LCD module
   LCDInit(LS_BLINK | LS_ULINE);
   
   //Clear the screen
   LCDClear();
   
	//initialize spi
	spi_init_spi();

	while (1){
	}
}
/*
//Checks if this is the end of the message, else sends next byte
void spi_tranciever(){
	if (recieved == OUTGOING_PACKET_SIZE){
		if (buffer != NULL){
			outgoing_data = buffer;
			buffer = NULL;
		}
		interpret_message();
	}
	else{
		incomming[recieved] = SPDR;
		SPDR = outgoing[recieved++];
	}
}
*/

