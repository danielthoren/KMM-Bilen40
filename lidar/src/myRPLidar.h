/* Till stora delar kopierade  från ultrasimple frame grabber.
 *
 * Tänkt att fungera som ett interface mot pythonwrappern.
 * Här ska alltså alla funktionsanrop defineras som görs mot
 * lidarmodulen
 *
 * //ALex
 */
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include "rplidar.h" //RPLIDAR standard sdk, all-in-one header


////////////////////////////////////
// Används vid översättnign från C++ data till numpy array i python.
#include <vector>
////////////////////////////////////
using namespace rp::standalone::rplidar;
namespace rp {namespace standalone {namespace rplidar {
  class RPlidar {
  public:
    //attrib
    RPlidarDriver * drv;
    //funcs
    RPlidar();
    ~RPlidar();
    bool setup();
    std::vector<std::vector<float> > grabData();
    void _startMotor();
    void _startScan();
    void _stop();
    void _stopMotor();
  };
}
}}
