#include "FaceDetector.hpp"

FaceDetector::FaceDetector(const std::string& protoPath, const std::string& modelPath) {
    net = cv::dnn::readNetFromCaffe(protoPath, modelPath);
}

FaceDetector::~FaceDetector() {
    stop();
}

void FaceDetector::start() {
    running = true;
    worker = std::thread(&FaceDetector::detectLoop, this);
}

void FaceDetector::stop() {
    running = false;
    if (worker.joinable()) {
        worker.join();
    }
}

void FaceDetector::updateFrame(const cv::Mat& frame) {
    std::lock_guard<std::mutex> lock(frameMutex);
    latestFrame = frame.clone();
}

std::vector<cv::Rect> FaceDetector::getFaces() {
    std::lock_guard<std::mutex> lock(resultMutex);
    return faces;
}

void FaceDetector::detectLoop() {
    while (running) {
        cv::Mat frame;

        {
            std::lock_guard<std::mutex> lock(frameMutex);
            if (latestFrame.empty()) {
                continue;
            }
            frame = latestFrame.clone();
        }

        cv::Mat blob = cv::dnn::blobFromImage(
            frame,
            1.0,
            cv::Size(300, 300),
            cv::Scalar(104.0, 177.0, 123.0)
        );

        net.setInput(blob);
        cv::Mat detections = net.forward();

        std::vector<cv::Rect> detectedFaces;

        cv::Mat detectionMat(
            detections.size[2],
            detections.size[3],
            CV_32F,
            detections.ptr<float>()
        );

        for (int i = 0; i < detectionMat.rows; i++) {
            float confidence = detectionMat.at<float>(i, 2);

            if (confidence > 0.5) {
                int x1 = static_cast<int>(detectionMat.at<float>(i, 3) * frame.cols);
                int y1 = static_cast<int>(detectionMat.at<float>(i, 4) * frame.rows);
                int x2 = static_cast<int>(detectionMat.at<float>(i, 5) * frame.cols);
                int y2 = static_cast<int>(detectionMat.at<float>(i, 6) * frame.rows);

                detectedFaces.push_back(cv::Rect(
                    cv::Point(x1, y1),
                    cv::Point(x2, y2)
                ));
            }
        }

        {
            std::lock_guard<std::mutex> lock(resultMutex);
            faces = detectedFaces;
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(30));
    }
}