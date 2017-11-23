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
	unsigned char speed;
	//the angle of the front wheels, may be between 1-180 (90 is neutral)
	unsigned char angle;
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

/*
Splits the 'data_out' and sends it over spi.

The outgoing data is sent in the following order:
outgoing[0] = curr_rpm
*/
void set_spi_data(motormodul_AP_data data);

/*
sets the data that has been recieved from the pi in the pointer 'data_in' if the checksum checks out. If new data has not
been recieved then does nothing.

The recieved data is expected in the following order:
incomming[0] = speed;	incomming[1] = angle;
*/
void get_spi_data(motormodul_PA_data* data);

//initializes the spi
void spi_init (void);

//Interrupt that is called when a new byte has been transferred over spi
ISR(SPI_STC_vect);

