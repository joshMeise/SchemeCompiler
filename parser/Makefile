CFLAGS=-Wall -Wpedantic
CC=gcc
BISON=bison
FLEX=flex
OFILES=ast.o parser.tab.o lex.yy.o parser_exec.o
EXEC=parser_exec

all: $(EXEC)

$(EXEC): $(OFILES)
	$(CC) $(CFLAGS) $^ -o $@

parser.tab.c parser.tab.h: parser.y
	$(BISON) -d parser.y

lex.yy.c: lexer.l parser.tab.h
	$(FLEX) lexer.l

%.o: %.c
	$(CC) $(CFLAGS) -c $<

clean:
	rm -rf *.o parser.tab.c parser.tab.h lex.yy.c $(EXEC)
