/*
 * sensormodul_spi.h
 *
 * Created: 2017-11-10 14:37:58
 *  Author: Daniel Thorén
 */ 

#include <avr/io.h>
#include <avr/interrupt.h>

//data sent from rasberry pi (=P) to motormodul (A = AVR)
struct motormodul_PA{
	//the speed of the engine, may be between 0-40 (3 is neutral)
	uint8_t speed;
	//the angle of the front wheels, may be between 1-180 (90 is neutral)
	uint8_t angle;
};

//data sent from 'motormodul' (A = AVR) to rasberry pi (=P)
struct motormodul_AP{
	uint8_t curr_rpm;
};

typedef struct motormodul_PA motormodul_PA_data;
typedef struct motormodul_AP motormodul_AP_data;

/************************************************************************/
/* Functions                                                             */
/************************************************************************/

//
unsigned char get_set_spi_data(motormodul_PA_data* data_in, motormodul_AP_data data_out);

//initializes the spi
void spi_init (void);

//This function must be called from the spi interrupt function. It takes the sent byte and saves it, then 
//updates the outgoing byte
void spi_tranciever(void);

