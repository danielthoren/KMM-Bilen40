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
	DDRB = (1<<6);     //MISO as OUTPUT
	SPCR = (1<<SPE);   //Enable SPI
}

//Function to send and receive data for both master and slave
unsigned char spi_tranceiver (char data)
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
	LCDWriteString("Slave");
   
   char num = 0;
   char recieved = 0;
	while (1){
		recieved = spi_tranceiver(num);
		num++;
		LCDClear();
		LCDWriteString(&recieved);
	}
}

