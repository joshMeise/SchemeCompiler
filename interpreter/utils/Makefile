CXXFLAGS=-Wall -Wpedantic -std=c++20
OFILES=interpreter.o utilities.o
CC=g++

all: $(OFILES)
	 ar cr ../lib/libutils.a $(OFILES)

%.o: %.c %.h
	$(CC) $(CXXFLAGS) -c $<

clean:
	rm -rf *.o ../lib/libutils.a
