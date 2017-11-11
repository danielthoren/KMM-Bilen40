/*
 * lcd_test.c
 *
 * Created: 2017-11-11 12:55:01
 * Author : Daniel Thorén
 */ 

#include <avr/io.h>

#include "lcd.h"


int main(void)
{
	   //Initialize LCD module
	   LCDInit(LS_BLINK | LS_ULINE);
	   
	   //Clear the screen
	   LCDClear();
	   
	   LCDWriteString("pandan dansar");
	
    /* Replace with your application code */
    while (1) 
    {
    }
}

