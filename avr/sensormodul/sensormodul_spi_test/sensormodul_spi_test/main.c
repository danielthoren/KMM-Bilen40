/*
 * sensormodul_spi_test.c
 *
 * Created: 2017-11-10 18:00:15
 * Author : Daniel Thorén
 */ 

#include <avr/io.h>
#include <avr/interrupt.h>
#include <string.h>

#include "lcd.h"
#include "sensormodul_spi.h"

ISR(SPI_STC_vect){
	spi_tranciever();
}

int main(void)
{
	spi_init();
	sei();
	sensormodul_AP_data data;
	
	data.lapsensor = 1;
	unsigned char tmp_data[4] = {13,55,3,7};
	memcpy((void*) &data.sonar_data, (void*) &tmp_data, 4);
	
	set_outgoing_data(data);
	
    /* Replace with your application code */
    while (1) 
    {
    }
}

