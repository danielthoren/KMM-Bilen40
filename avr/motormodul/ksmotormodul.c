/*
 * Servo_pwm.c
 *
 * Created: 11/11/2017 2:36:31 PM
 *  Author: krisi211
 */ 

#define F_CPU 16000000
#include <avr/io.h>
#include <avr/delay.h>
#include <avr/interrupt.h>

const int natural = 3000; //Pulse is 1,5 ms

const int max_left = 3900; //Ish max right (pulse should be 2 ms)
const int max_right = 2100; //Ish max left (pulse should be 1ms)
const int max_speed; //Ta reda på varde
int turn; //Turn < natural => right, turn > natural => left
int speed;
uint8_t scale_turn;
uint8_t scale_speed;

void scale(){
	if(scale_turn <= 180 && scale_turn >= 1)
	{
		turn = (10 *scale_turn) + 2100;
	}
	else
	{
		turn = natural;
	}
	//Uppdatera granser för hastighet, 
	//maxhastighet troligen innan speed = 40000 
	if(scale_speed <= 40 && scale_speed >= 1)
	{
		speed = (1000*scale_speed);
	}
	else 
	{
		speed = natural;
	}
	
}

int main(void)
{
	//Pin set-up
	DDRD |= _BV(5); //Pinne 19, styrservot
	DDRD |= _BV(4); //Pinne 18, motorn

	//timer set-up
	TCCR1A |= _BV(1) | _BV(7) | _BV(5);
	TCCR1B |= _BV(3)| _BV(4) | _BV(1);
	ICR1 = 40000;
	//send out neutral mode
	turn = natural;
	speed = natural;
	OCR1A = turn;
	OCR1B = speed;
	_delay_ms(5000);

	while(1)
	{
		scale();
		OCR1A = turn;
		OCR1B = speed;
		
	}

}
