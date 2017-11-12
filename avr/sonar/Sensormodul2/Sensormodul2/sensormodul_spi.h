﻿/*
 * sensormodul_spi.h
 *
 * Created: 2017-11-10 14:37:58
 *  Author: Daniel Thorén
 */ 

#include <avr/io.h>
#include <avr/interrupt.h>

//data sent from 'sensormodul' (A = AVR) to rasberry pi (=P)
struct sensormodul_AP{
	volatile unsigned char sonar_data[4];
	volatile unsigned char lapsensor;
};

typedef struct sensormodul_AP sensormodul_AP_data;

/************************************************************************/
/* Functions                                                             */
/************************************************************************/

//only sets data if the SS pin is high, if it is low that means that a transfer is in progress.
//The data is saved in a buffer and set as outgoing data when SS goes high.
//When new data is available PORTD0 goes high until the pi has read the data, then it goes low again.
void set_outgoing_data(sensormodul_AP_data data);

//initializes the spi
void spi_init (void);

//Handles the transfer, this function must be called every time the "ISR(SPI_STC_vect)" interrupt function is called
void spi_tranciever(void);

