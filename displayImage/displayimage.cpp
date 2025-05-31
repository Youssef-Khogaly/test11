#include <iostream>
#include <opencv4/opencv2/opencv.hpp>
#include <stdio.h>
using namespace cv;
enum  error{
    SUCCESS = 0,
    BAD_USAGE = -1,
    FILE_NOT_FOUND = -2
};

int main(int argc , const char** argv )

{   
    using std::cout;
    using std::endl;
    using std::string;
    if(argc != 2)
    {
        cout << "Bad usage \n" << endl;
        return BAD_USAGE;
    }

    cv::Mat image = cv::imread(argv[1], cv::IMREAD_COLOR);
    cv::Mat reSizedImg{};
    if(image.empty())
    {
        cout << "couldn't open or find the image file" << endl;
        return FILE_NOT_FOUND;
    } 
    cv::resize(std::move(image), reSizedImg, cv::Size(), 0.3, 0.3);
    string && windowName = "image test";
    cv::namedWindow(windowName);
    cv::imshow(windowName,reSizedImg);
    waitKey(0);
    cv::destroyWindow(windowName);



    return SUCCESS;
}