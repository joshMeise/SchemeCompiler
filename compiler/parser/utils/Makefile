CFLAGS=-Wall -Wpedantic
CC=gcc
BISON=bison
FLEX=flex
OFILES=ast.o parser.tab.o lex.yy.o

all: ../lib/libutils.a

../lib/libutils.a: $(OFILES)
	ar cr ../lib/libutils.a $(OFILES)

parser.tab.c parser.tab.h: parser.y
	$(BISON) -d parser.y

lex.yy.c: lexer.l parser.tab.h
	$(FLEX) lexer.l

%.o: %.c
	$(CC) $(CFLAGS) -c $<

clean:
	rm -rf *.o parser.tab.c parser.tab.h lex.yy.c ../lib/libutils.a
