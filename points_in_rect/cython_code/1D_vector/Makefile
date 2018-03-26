all:
	cython rect_in.pyx
	gcc -g -O3 -fpic -c rect_in.c `python-config --cflags`  -std=c99
	gcc rect_in.o -o rect_in.so -shared `python-config --ldflags` -std=c99
