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

<<<<<<< HEAD
#define BUFFSIZE 30
=======
>>>>>>> ae0282b4bb2f1600d213303e670a759f01b0c18a


<<<<<<< HEAD
// Initialize SPI Slave Device
void spi_init_slave (void)
{
	DDRB = (1 << DDB6);			//Set MISO as output
	SPCR=(1<<SPE)|(1<<SPIE);	//Enable SPI && interrupt enable bit
}

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

//interprets the message and resets the spi bus
void interpret_message(){
	unsigned char int_char[4];
	memcpy((char*) int_char, (char*) incomming, 4);
	int32_t msg = build_int32(int_char);
	LCDClear();
	LCDWriteInt((int) msg, 4);
	recieved = 0;
	memset((void*) outgoing, 0x00, sizeof(outgoing));
	memset((void*) incomming, 0x00, sizeof(outgoing));
}

//Checks if this is the end of message, if not then stores it and sends the next byte
void spi_tranciever(){
	if (recieved == 4){
		interpret_message();
	}
	else{
		incomming[recieved] = SPDR;
		SPDR = outgoing[recieved++];
	}
=======
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
>>>>>>> ae0282b4bb2f1600d213303e670a759f01b0c18a
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
	spi_init_slave();
	
	unsigned char data[4];
	split_int32((int32_t) 3455, data);
<<<<<<< HEAD
	memcpy((void*) incomming, (void*) data, 4);
	
	/*
	
	LCDWriteString(" ");
	unsigned char testData[4] = {0};
	memcpy((void*) testData, (void*) outgoing, 4);
	int32_t temp = build_int32(testData);
	LCDWriteInt((int) temp, 4);
	*/
	unsigned char testData[4] = {0};
	memcpy((void*) testData, (void*) incomming, 4);
	interpret_message();
=======
	memcpy((void*) outgoing, (void*) data, 4);
	
>>>>>>> ae0282b4bb2f1600d213303e670a759f01b0c18a
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

