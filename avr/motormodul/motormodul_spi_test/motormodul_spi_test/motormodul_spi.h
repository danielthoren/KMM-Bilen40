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

/*
sets the data that has been recieved from the pi in the pointer 'data_in' if the checksum checks out. Else sets the
'data_in' pointer to NULL (defined in stdlib.h). Also splits the 'data_out' and sends it over spi.
If the SS pin is low (transfer is ongoing) or the checksum is bad, then sets the speed parameter of 'data_in' to 0xFF

The recieved data is expected in the following order:
incomming[0] = speed;	incomming[1] = angle;

The outgoing data is sent in the following order:
outgoing[0] = curr_rpm
*/
void get_set_spi_data(motormodul_PA_data* data_in, motormodul_AP_data data_out);

//initializes the spi
void spi_init (void);

//only sets data if the SS pin is high, if it is low that means that a transfer is in progress.
//The data is saved in a buffer and set as outgoing data when SS goes high.
//When new data is available PORTD0 goes high until the pi has read the data, then it goes low again.
void spi_tranciever(void);

