#ifndef Camera_h
#define Camera_h

#include <tuple>

using namespace std;

class Camera
{
public:
	virtual void initialize_camera(tuple<int, int>* resolution) = 0;
	virtual void capture_image() = 0;
	virtual void capture_video(int seconds, int frames_per_second) = 0;
	virtual void shutdown() = 0;
};

#endif