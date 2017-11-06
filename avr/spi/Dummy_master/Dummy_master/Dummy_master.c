/*
 * Dummy_master.c
 *
 * Created: 11/6/2017 2:22:22 PM
 *  Author: krisi211
 */ 


#include <avr/io.h>
#include <util/delay.h>

void init_master(){
	DDRB = (1 << DDB7) | (1 << DDB5);
	
	SPCR = (1<<SPE)|(1<<MSTR)|(1<<SPR0);
}

//Function to send and receive data for both master and slave
unsigned char spi_tranceiver (unsigned char data)
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
	init_master();
	while (1){
	_delay_ms(100);
    spi_tranceiver('A');
	_delay_ms(100);
	spi_tranceiver('B');
	_delay_ms(100);
	spi_tranceiver('C');
	_delay_ms(100);
	spi_tranceiver('D');
	}
}