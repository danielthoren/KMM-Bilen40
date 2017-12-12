/* Author: Alexander Zeijlon
 * Header file for the C++ parts of the lidar code that's wrapped into a python module.
 * 
 * The files that i have written are all starting with the name "meme", all other
 * files are taken directly from the RPLIDAR SDK.
 * 
 * The actual functionality has been borrowed from the official RPLIDAR SDK's
 * "ultra_simple_grabber"-app.
 * The SDK can be found at https://download.slamtec.com/api/download
 */

/*
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include "rplidar.h"
#include <vector>

namespace rp {namespace standalone {namespace rplidar {
  class memeRPlidar {
  public:
    // attributes
    RPlidarDriver * drv;
    
    // functions
    memeRPlidar();
    
    ~memeRPlidar();
    
    // Initiates the RPLIDAR driver.
    bool setup();
    
    // Returns a 2D vector containing a full 360 degree measurement.
    // All elems have non zero quality meas.
    std::vector< std::vector<float> > grabNonZeroData();
    
    // Returns a 2D vector containing a full 360 degree measurement.
    std::vector< std::vector<float> > grabData();
    
    void startMotor();
    
    void startScan();
    
    // Stop scanning.
    void stop();
    
    void stopMotor();
  };
}}}
