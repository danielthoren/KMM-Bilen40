/*
 * sensormodul_spi_test.c
 *
 * Created: 2017-11-10 18:00:15
 * Author : Daniel Thorén
 */ 

#define F_CPU 16000000

#include <avr/io.h>
#include <avr/interrupt.h>
#include <string.h>
#include <util//delay.h>

#include "lcd.h"
#include "sensormodul_spi.h"

ISR(SPI_STC_vect){
	spi_tranciever();
}

int main(void)
{
	spi_init();
	sei();
	
	//Initialize LCD module
	LCDInit(LS_BLINK | LS_ULINE);
		 
	//Clear the screen
	LCDClear();
	
	sensormodul_AP_data data;
	
	data.lapsensor = 1;
	unsigned char tmp_data[4] = {13,55,3,7};
	memcpy((void*) data.sonar_data, (void*) tmp_data, 4);
	
	set_outgoing_data(data);
	
	_delay_ms(50);
	
	data.lapsensor = 1;
	unsigned char tmp_data2[4] = {1,3,3,7};
	memcpy((void*) data.sonar_data, (void*) tmp_data2, 4);
		
	set_outgoing_data(data);

    while (1) 
    {
	}
}

