/* Author: Alexander Zeijlon */
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
#include "memeRPlidar.h"

#include <unistd.h>
#ifndef _countof
#define _countof(_Array) (int)(sizeof(_Array) / sizeof(_Array[0]))
#endif
namespace rp {namespace standalone { namespace rplidar {
  static inline void delay(_word_size_t ms){
      while (ms>=1000){
          usleep(1000*1000);
          ms-=1000;
      };
      if (ms!=0)
          usleep(ms*1000);
  }

  bool checkRPLIDARHealth(RPlidarDriver * drv)
  {
      u_result     op_result;
      rplidar_response_device_health_t healthinfo;


      op_result = drv->getHealth(healthinfo);
      if (IS_OK(op_result)) { // the macro IS_OK is the preperred way to judge whether the operation is succeed.
          printf("RPLidar health status : %d\n", healthinfo.status);
          if (healthinfo.status == RPLIDAR_STATUS_ERROR) {
              fprintf(stderr, "Error, rplidar internal error detected. Please reboot the device to retry.\n");
              // enable the following code if you want rplidar to be reboot by software
              // drv->reset();
              return false;
          } else {
              return true;
          }

      } else {
          fprintf(stderr, "Error, cannot retrieve the lidar health code: %x\n", op_result);
          return false;
      }
  }

  #include <signal.h>
  bool ctrl_c_pressed;
  void ctrlc(int)
  {
      ctrl_c_pressed = true;
  }

  bool memeRPlidar::setup() {
      const char * opt_com_path = NULL;
      _u32         opt_com_baudrate = 115200;
      u_result     op_result;
      printf("Ultra simple LIDAR data grabber for RPLIDAR.\n"
             "Version: "RPLIDAR_SDK_VERSION"\n");

      opt_com_path = "/dev/ttyUSB0";

      // create the driver instance
      /*RPlidarDriver **/ drv = RPlidarDriver::CreateDriver(RPlidarDriver::DRIVER_TYPE_SERIALPORT);

      if (!drv) {
          fprintf(stderr, "insufficent memory, exit\n");
          exit(-2);
      }

      // make connection...
      if (IS_FAIL(drv->connect(opt_com_path, opt_com_baudrate))) {
          fprintf(stderr, "Error, cannot bind to the specified serial port %s.\n"
              , opt_com_path);
          goto on_finished;
      }

      rplidar_response_device_info_t devinfo;
	  
      op_result = drv->getDeviceInfo(devinfo);

      if (IS_FAIL(op_result)) {
          fprintf(stderr, "Error, cannot get device info.\n");
          goto on_finished;
      }

      // print out the device serial number, firmware and hardware version number..
      printf("RPLIDAR S/N: ");
      for (int pos = 0; pos < 16 ;++pos) {
          printf("%02X", devinfo.serialnum[pos]);
      }

      printf("\n"
              "Firmware Ver: %d.%02d\n"
              "Hardware Rev: %d\n"
              , devinfo.firmware_version>>8
              , devinfo.firmware_version & 0xFF
              , (int)devinfo.hardware_version);

      if (!checkRPLIDARHealth(drv)) {
          goto on_finished;
      }

      return true;

      on_finished:
      RPlidarDriver::DisposeDriver(drv);
      return false;
  }

  std::vector<std::vector<float> > memeRPlidar::grabData() {
    u_result     op_result;
    std::vector<std::vector<float> > tot;
    rplidar_response_measurement_node_t nodes[360*2];
    size_t count = _countof(nodes);

    op_result = drv->grabScanData(nodes, count);

    if (IS_OK(op_result)) {
      drv-> ascendScanData(nodes, count);
      for (int pos = 0; pos < (int)count; pos++) {
        std::vector<float> measurement;
        measurement.push_back( (float) (nodes[pos].sync_quality & RPLIDAR_RESP_MEASUREMENT_SYNCBIT)); /*  ?"S ":"  " */
        measurement.push_back( (float) ((nodes[pos].angle_q6_checkbit >> RPLIDAR_RESP_MEASUREMENT_ANGLE_SHIFT)/64.0f));
        measurement.push_back( (float) (nodes[pos].distance_q2/4.0f));
        measurement.push_back( (float) (nodes[pos].sync_quality >> RPLIDAR_RESP_MEASUREMENT_QUALITY_SHIFT));
        tot.push_back(measurement);
      }
    }
    return tot;
  }

  std::vector<std::vector<float> > memeRPlidar::grabNonZeroData() {
    u_result     op_result;
    std::vector<std::vector<float> > tot;
    rplidar_response_measurement_node_t nodes[360*2];
    size_t count = _countof(nodes);

    op_result = drv->grabScanData(nodes, count);

    if (IS_OK(op_result)) {
      drv-> ascendScanData(nodes, count);
      for (int pos = 0; pos < (int)count; pos++) {
        std::vector<float> measurement;
        measurement.push_back( (float) (nodes[pos].sync_quality & RPLIDAR_RESP_MEASUREMENT_SYNCBIT)); /*  ?"S ":"  " */
        measurement.push_back( (float) ((nodes[pos].angle_q6_checkbit >> RPLIDAR_RESP_MEASUREMENT_ANGLE_SHIFT)/64.0f));
        measurement.push_back( (float) (nodes[pos].distance_q2/4.0f));
        measurement.push_back( (float) (nodes[pos].sync_quality >> RPLIDAR_RESP_MEASUREMENT_QUALITY_SHIFT));
	if (measurement.at(3) > 0) {
	  tot.push_back(measurement);
	}
        
      }
    }
    return tot;
  }

  void memeRPlidar::startMotor() {
    drv->startMotor();
  }
  void memeRPlidar::startScan() {
    drv->startScan();
  }
  void memeRPlidar::stopMotor() {
    drv->stopMotor();
  }
  void memeRPlidar::stop() {
    drv->stop();
  }
  memeRPlidar::memeRPlidar() {
    std::cout << "Creating RPlidar object, running setup()" << std::endl;
    memeRPlidar::setup();
  }
  memeRPlidar::~memeRPlidar() {
    std::cout << "Disposing of lidar driver." << std::endl;
    RPlidarDriver::DisposeDriver(drv);
  }
}}}
