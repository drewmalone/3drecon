#include "cv.h"
#include "cxmisc.h"
#include "highgui.h"
#include "cvaux.h"
#include <vector>
#include <string>
#include <algorithm>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

using namespace std;

int main(int argc, char *argv[])
{
    if (argc != 3) {
        printf("%d", argc);
        printf("Please use: ./rectify [left] [right]\n");
    }

    IplImage* img1=cvLoadImage(argv[1],0);
    IplImage* img2=cvLoadImage(argv[2],0);

    CvSize imageSize = cvGetSize(img1);

    CvMat* mx1 = cvCreateMat( imageSize.height,
        imageSize.width, CV_32F );
    CvMat* my1 = cvCreateMat( imageSize.height,
        imageSize.width, CV_32F );
    CvMat* mx2 = cvCreateMat( imageSize.height,
        imageSize.width, CV_32F );
    CvMat* my2 = cvCreateMat( imageSize.height,
        imageSize.width, CV_32F );

    CvMat* img1r = cvCreateMat( imageSize.height,
        imageSize.width, CV_8U );
    CvMat* img2r = cvCreateMat( imageSize.height,
        imageSize.width, CV_8U );

    mx1 = (CvMat *) cvLoad("mx1.xml");
    my1 = (CvMat *) cvLoad("my1.xml");
    mx2 = (CvMat *) cvLoad("mx2.xml");
    my2 = (CvMat *) cvLoad("my2.xml");

    cvRemap( img1, img1r, mx1, my1 );
    cvRemap( img2, img2r, mx2, my2 );	

    cvSaveImage("left_rectified.png", img1r);
    cvSaveImage("right_rectified.png", img2r);
}
