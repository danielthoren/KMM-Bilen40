/*
 * spi.c
 *
 * Created: 2017-11-03 10:48:11
 * Author : Daniel Thorén
 */ 

#include <avr/io.h>

#include "lcd.h"
#include "myutils.h"

// Initialize SPI Slave Device
void spi_init_slave (void)
{
	DDRB = (1 << DDB6);	//Set MISO as output
	SPCR = (1 << SPE);	//Enable interrupts and set AVR as slave
}

//Function to send and receive data for both master and slave
char spi_tranceiver (unsigned char data)
{
	// Load data into the buffer
	SPDR = data;
	
	//Wait until transmission complete
	while(!(SPSR & (1<<SPIF) ));
	
	// Return received data
	return(SPDR);
}

int main(void)
{
   //Initialize LCD module
   LCDInit(LS_BLINK|LS_ULINE);
   
   //Clear the screen
   LCDClear();
   
	//initialize spi
	spi_init_slave();
	LCDWriteString(" Slave");
   
   LCDClear();
	while (1){
		LCDWriteString(&recieved);
	}
}

