SHELL = /bin/bash

all:
	ls ../emsdk && \
	source ../emsdk/emsdk_env.sh && \
	em++ main.cpp -o index.html -sGL_UNSAFE_OPTS=0 -sASYNCIFY && \
	emdump --file index.html
