/*
 * TimerTest.c
 *
 * Created: 2017-11-04 11:12:45
 * Author : Gustaf
 */ 

#include <avr/io.h>
#include "lcd.h"
#include "myutils.h"

#define F_CPU 16000000
int main(void)
{
	
	 //Initialize LCD module
	 LCDInit(LS_ULINE);
	 
	 //Clear the screen
	 LCDClear();
	 
	 // Raknare=0
	 TCNT0=0;
	 
	 //Turn on counter
	 TCCR0B |= (1 << CS02) | (0 << CS01) | (1 << CS00);
	 
	 int32_t pulse;
	 
    while (1) 
    {
		pulse=TCNT0;
		_delay_ms(10);
		LCDWriteInt(pulse, 4);
		
    }
}

