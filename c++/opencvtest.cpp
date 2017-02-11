#include <ctime>
#include <fstream>
#include <iostream>
#include <opencv2/highgui/highgui.hpp>
//#include <raspicam/raspicam.h>

#include "./include/laptopCamera.h"
#include "./include/raspberryPiCamera.h"

//using namespace cv; 
using namespace std;

int main()
{
    tuple<int, int> resolution (680, 1080);
    Camera* camera = new LaptopCamera();
    camera->initialize_camera(&resolution);

    Camera* piCamera = new RaspberryPiCamera();
    piCamera->initialize_camera(&resolution);
	// raspicam::RaspiCam Camera;
	// Camera.open();
	// Camera.grab();

	// unsigned char *data=new unsigned char[  Camera.getImageTypeSize ( raspicam::RASPICAM_FORMAT_RGB )];
 //    //extract the image in rgb format
 //    Camera.retrieve ( data,raspicam::RASPICAM_FORMAT_RGB );//get camera image
 //    //save
 //    std::ofstream outFile ( "raspicam_image.ppm",std::ios::binary );
 //    outFile<<"P6\n"<<Camera.getWidth() <<" "<<Camera.getHeight() <<" 255\n";
 //    outFile.write ( ( char* ) data, Camera.getImageTypeSize ( raspicam::RASPICAM_FORMAT_RGB ) );

 //    delete data;
 //    //Mat img = imread("testImage.jpg",CV_LOAD_IMAGE_COLOR);
 //    //imshow("opencvtest",img);
 //    //waitKey(0);

    return 0;
}