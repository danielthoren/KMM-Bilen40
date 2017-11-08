/*
 * spi.c
 *
 * Created: 2017-11-03 10:48:11
 * Author : Daniel Thorén
 */ 

#include <avr/io.h>
#include <avr/interrupt.h>

#include "lcd.h"
#include "myutils.h"

#define BUFFSIZE 20

volatile unsigned char incomming[BUFFSIZE] = {0};
volatile unsigned char outgoing[BUFFSIZE] = {0};
volatile short int recieved=0;

// Initialize SPI Slave Device
void spi_init_slave (void)
{
	DDRB = (1 << DDB6);			//Set MISO as output
	SPCR=(1<<SPE)|(1<<SPIE);	//Enable SPI && interrupt enable bit
}

//Function to send and receive data for both master and slave
unsigned char spi_tranceiver2 (unsigned char data)
{
	// Load data into the buffer
	SPDR = data;
	
	//Wait until transmission complete
	while(!(SPSR & (1<<SPIF) ));
	
	// Return received data
	return(SPDR);
}

//interprets the message and resets the spi bus
void interpret_message(){
	LCDWriteString((char*)&incomming[0]);
	recieved = 0;
}

//Checks if this is the end of message, if not then stores it and sends the next byte
void spi_tranciever(){
	if (SPDR == 0x00){
		interpret_message();
	}
	else{
		incomming[recieved] = SPDR;
		SPDR = outgoing[recieved++];
	}
}

//Spi interrupt routine
ISR(SPI_STC_vect){
	
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
   
	while (1){
	}
}

