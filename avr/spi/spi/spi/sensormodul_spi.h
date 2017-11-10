/*
 * sensormodul_spi.h
 *
 * Created: 2017-11-10 14:37:58
 *  Author: Daniel Thorén
 */ 

#include <avr/io.h>
#include <avr/interrupt.h>

//data sent from 'sensormodul' (A = AVR) to rasberry pi (=P)
struct sensormodul_PA_data{
	int8_t sonar_data[4];
	char lapsensor;
};

/************************************************************************/
/* Functions                                                             */
/************************************************************************/

void set_outgoing_data(struct sensormodul_PA_data data);
void spi_init_slave (void);

