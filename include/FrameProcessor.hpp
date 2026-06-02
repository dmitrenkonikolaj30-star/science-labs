#ifndef FRAME_PROCESSOR_HPP
#define FRAME_PROCESSOR_HPP

#include <opencv2/opencv.hpp>

class FrameProcessor {
public:
    static cv::Mat process(const cv::Mat& frame);
};

#endif