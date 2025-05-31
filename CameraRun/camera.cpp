
#include <iostream>
#include <opencv4/opencv2/opencv.hpp>


using namespace cv;
using namespace std;
typedef enum  {
    SUCCESS = 0,
    BAD_USAGE = -1,
    CAMERA_NOT_FOUND = -2

}error;
int main (int argc , const char ** argv)
{
    if(argc != 2)
    {
        std::cout <<"Bad Usage \n"<< std::endl;
        return BAD_USAGE;
    }
    int port = (int)(argv[1][0] - '0');
    VideoCapture cap;
    cap.setExceptionMode(true);
    cap.open(port, cv::CAP_V4L2);
    if(!cap.isOpened())
    {
        cout <<"Can't open camera .. verifiy port number and try again \n";
        return CAMERA_NOT_FOUND;
    }
    double fps = cap.get(CAP_PROP_FPS);
    double width = cap.get(CAP_PROP_FRAME_WIDTH);
    double height = cap.get(CAP_PROP_FRAME_HEIGHT);
    cout << "Resolution of the video : " << width << " x " << height << endl;
    cout << "Capped Frame rate =" << fps << endl;
    string&& window_name = "My Camera";
    namedWindow(move(window_name)); //create a window called "My Camera Feed"
 while (true)
 {
  Mat frame;
  Mat ResizedFrame;
  bool bSuccess = cap.read(frame); // read a new frame from video 

  //Breaking the while loop if the frames cannot be captured
  if (bSuccess == false) 
  {
   cout << "Video camera is disconnected" << endl;
   cin.get(); //Wait for any key press
   break;
  }
  cv::resize(std::move(frame), ResizedFrame, cv::Size(), 0.3, 0.3);
  //show the frame in the created window
  imshow(window_name, ResizedFrame);

  //wait for for 10 ms until any key is pressed.  
  //If the 'Esc' key is pressed, break the while loop.
  //If the any other key is pressed, continue the loop 
  //If any key is not pressed withing 10 ms, continue the loop 
  if (waitKey(10) == 27)
  {
   cout << "Esc key is pressed by user. Stoppig the video" << endl;
   break;
  }
 }

    return SUCCESS;
}