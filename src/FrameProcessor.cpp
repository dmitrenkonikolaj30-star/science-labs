#include "FrameProcessor.hpp"

cv::Mat FrameProcessor::process(const cv::Mat& frame) {
    cv::Mat gray;

    cv::cvtColor(
        frame,
        gray,
        cv::COLOR_BGR2GRAY
    );

    return gray;
}