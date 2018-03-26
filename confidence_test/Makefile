all:
	cython perturb.pyx
	gcc -g -O3 -fpic -c perturb.c `python-config --cflags`  -lm
	gcc perturb.o -o perturb.so -shared `python-config --ldflags` -lm
