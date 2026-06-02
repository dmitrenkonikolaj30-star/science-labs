#include "KeyProcessor.hpp"

bool KeyProcessor::isExitKey(int key) {
    return key == 27 || key == 'q' || key == 'Q';
}