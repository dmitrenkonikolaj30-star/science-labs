#ifndef CAMERA_PROVIDER_HPP
#define CAMERA_PROVIDER_HPP

#include <opencv2/opencv.hpp>

class CameraProvider {
private:
    cv::VideoCapture cap;

public:
    CameraProvider(int cameraIndex = 0);
    bool isOpened() const;
    cv::Mat getFrame();
};

#endif