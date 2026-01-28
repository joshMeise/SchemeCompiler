CFLAGS=-Wall -Wpedantic -std=c11 -I../utils -L../lib
LIBS=-lutils
EXECS=parser_exec
CC=gcc

all: $(EXECS)

$(EXECS): %: %.c
	$(CC) $(CFLAGS) $^ $(LIBS) -o $@

clean:
	rm -rf $(EXECS)
