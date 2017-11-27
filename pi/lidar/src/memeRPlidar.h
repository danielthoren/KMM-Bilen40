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
namespace rp {namespace standalone {namespace rplidar {
  class memeRPlidar {
  public:
    //attrib
    RPlidarDriver * drv;
    //funcs
    memeRPlidar();
    ~memeRPlidar();
    bool setup();
    std::vector<std::vector<float> > grabNonZeroData();
    std::vector<std::vector<float> > grabData();
    void startMotor();
    void startScan();
    void stop();
    void stopMotor();
  };
}}}
