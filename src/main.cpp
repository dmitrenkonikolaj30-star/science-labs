#include <iostream>
#include <opencv2/opencv.hpp>

#include "CameraProvider.hpp"
#include "KeyProcessor.hpp"
#include "FrameProcessor.hpp"

int main() {
    CameraProvider camera(0);

    if (!camera.isOpened()) {
        std::cerr << "Помилка: не вдалося відкрити камеру." << std::endl;
        return -1;
    }

    std::cout << "Камеру відкрито успішно." << std::endl;
    std::cout << "Для виходу натисніть Esc або Q." << std::endl;

    while (true) {
        cv::Mat frame = camera.getFrame();

        if (frame.empty()) {
            std::cerr << "Помилка: не вдалося отримати кадр." << std::endl;
            break;
        }

        cv::Mat processedFrame = FrameProcessor::process(frame);

        cv::imshow("Original Frame", frame);
        cv::imshow("Processed Frame", processedFrame);

        int key = cv::waitKey(30);

        if (KeyProcessor::isExitKey(key)) {
            break;
        }
    }

    cv::destroyAllWindows();

    return 0;
}