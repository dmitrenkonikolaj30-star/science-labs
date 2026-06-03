#include <iostream>
#include <opencv2/opencv.hpp>

#include "CameraProvider.hpp"
#include "KeyProcessor.hpp"
#include "FrameProcessor.hpp"
#include "FaceDetector.hpp"

int main() {
    CameraProvider camera(0);

    if (!camera.isOpened()) {
        std::cerr << "Помилка: не вдалося відкрити камеру." << std::endl;
        return -1;
    }

    FaceDetector detector(
        "deploy.prototxt",
        "res10_300x300_ssd_iter_140000.caffemodel"
    );

    detector.start();

    std::cout << "Камеру відкрито успішно." << std::endl;
    std::cout << "Для виходу натисніть Esc або Q." << std::endl;

    while (true) {
        cv::Mat frame = camera.getFrame();

        if (frame.empty()) {
            std::cerr << "Помилка: не вдалося отримати кадр." << std::endl;
            break;
        }

        detector.updateFrame(frame);

        auto faces = detector.getFaces();

        for (const auto& face : faces) {
            cv::rectangle(
                frame,
                face,
                cv::Scalar(0, 255, 0),
                2
            );
        }

        cv::Mat processedFrame = FrameProcessor::process(frame);

        cv::imshow("Original Frame with Face Detection", frame);
        cv::imshow("Processed Frame", processedFrame);

        int key = cv::waitKey(30);

        if (KeyProcessor::isExitKey(key)) {
            break;
        }
    }

    detector.stop();
    cv::destroyAllWindows();

    return 0;
}