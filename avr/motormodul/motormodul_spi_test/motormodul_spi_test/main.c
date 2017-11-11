/*
 * motormodul_spi_test.c
 *
 * Created: 2017-11-11 12:14:31
 * Author : Daniel Thorén
 */ 

#include <avr/io.h>
#include <string.h>
#include <avr/interrupt.h>

#include "motormodul_spi.h"
#include "lcd.h"


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
	
		spi_init();
		sei();
		
		motormodul_AP_data data_out;
		motormodul_PA_data data_in;
		data_in.speed = 0xFF;
		data_out.curr_rpm = 42;
		get_set_spi_data(&data_in, data_out);

    /* Replace with your application code */
    while (1) 
    {
		data_in = get_set_spi_data(&data_in, data_out);
		if(data_in.speed != 0xFF){
			LCDClear();
			LCDWriteInt(data_in.speed, 3);
		}
    }
}

