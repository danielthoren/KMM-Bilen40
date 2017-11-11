/*
 * sensormodul_spi.h
 *
 * Created: 2017-11-10 14:37:58
 *  Author: Daniel Thorén
 */ 

#include <avr/io.h>
#include <avr/interrupt.h>

//data sent from 'sensormodul' (A = AVR) to rasberry pi (=P)
struct sensormoduldata{
	volatile unsigned char sonar_data[4];
	volatile unsigned char lapsensor;
};

typedef struct sensormoduldata sensormodul_PA_data;

/************************************************************************/
/* Functions                                                             */
/************************************************************************/

void set_outgoing_data(sensormodul_PA_data data);
void spi_init (void);
void spi_tranciever(void);

