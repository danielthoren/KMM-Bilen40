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
	uint8_t speed;
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

//Sets the outgoing data to 'data' if no transmission os ongoing, else saves the 'data' in a buffer
//and sets said buffer as outgoing data when the transmission is done
void set_outgoing_data(motormodul_AP_data data);

//Returns the data recieved from rasberry if no ongoing transmission is happening, else returns 
//a 'motormodul_PA_data' instance where 'speed' is set to 255 (0xFF) (This value should thus be ignored) 
motormodul_PA_data get_incomming_data();

//initializes the spi
void spi_init (void);

//This function must be called from the spi interrupt function. It takes the sent byte and saves it, then 
//updates the outgoing byte
void spi_tranciever(void);

