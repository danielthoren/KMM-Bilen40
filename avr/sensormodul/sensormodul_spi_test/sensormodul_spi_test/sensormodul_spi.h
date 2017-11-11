/*
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
void set_outgoing_data(sensormodul_AP_data data);
void spi_init (void);
void spi_tranciever(void);

