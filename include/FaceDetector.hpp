#pragma once

#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include <thread>
#include <mutex>
#include <atomic>
#include <vector>

class FaceDetector {
private:
    cv::dnn::Net net;
    std::thread worker;
    std::mutex frameMutex;
    std::mutex resultMutex;
    std::atomic<bool> running{false};

    cv::Mat latestFrame;
    std::vector<cv::Rect> faces;

    void detectLoop();

public:
    FaceDetector(const std::string& protoPath, const std::string& modelPath);
    ~FaceDetector();

    void start();
    void stop();
    void updateFrame(const cv::Mat& frame);
    std::vector<cv::Rect> getFaces();
};