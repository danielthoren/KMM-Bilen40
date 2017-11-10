/*
 * sensormodul_spi_test.c
 *
 * Created: 2017-11-10 18:00:15
 * Author : Daniel Thorén
 */ 

#include <avr/io.h>
#include <avr/interrupt.h>

#include "lcd.h"
#include "sensormodul_spi.h"

ISR(SPI_STC_vect){
	spi_tranciever();
}

int main(void)
{
	spi_init();
	sei();
	sensormodul_PA_data data;
	
	
	
    /* Replace with your application code */
    while (1) 
    {
    }
}

