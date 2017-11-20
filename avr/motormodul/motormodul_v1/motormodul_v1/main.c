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

/*
ISR(SPI_STC_vect){
	spi_tranciever();
}*/

int main(void)
{
		spi_init();
		
		sei();
		
		//Initialize LCD module
		LCDInit(LS_BLINK | LS_ULINE);
		
		//Clear the screen
		LCDClear();
		
		motormodul_AP_data data_out;
		data_out.curr_rpm = 42;
		set_spi_data(data_out);

    while (1) 
    {
		// OBS!!!! data_available never gets high for some reason?
		//LCDWriteInt(data_available, 1);
		if(get_data_available()){
			motormodul_PA_data data;
			data.angle = 0;
			data.speed = 0;
			get_spi_data(&data);
			LCDWriteString(" ");
			LCDWriteInt(data.angle, 3);
			LCDWriteString(" ");
			LCDWriteInt(data.speed, 3);
		}
    }
}

