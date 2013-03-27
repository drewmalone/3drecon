all:
	g++ -o rectify rectify.cpp `pkg-config --cflags --libs opencv`

clean:
	rm stereo_calibrate
 
