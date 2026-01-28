/*
 * lexer.l - lexer for Scheme program
 *
 * Josh Meise
 * 01-25-2026
 * Description: 
 *
 */

%option noinput
%option nounput

%{

#include "ast.h"
#include "parser.tab.h"

%}

%%

[0-9]+                          { yylval.ival = atoi(yytext); return NUMBER; }
"#t"|"#f"                       { yylval.sval = strdup(yytext); return BOOL; }
"#\\"[^`]                       { yylval.sval = strdup(yytext); return CHAR; }
"add1"                          { return ADD1; }
"sub1"                          { return SUB1; }
"integer->char"                 { return INT_TO_CHAR; }
"char->integer"                 { return CHAR_TO_INT; }
"null?"                         { return IS_NULL; }
"zero?"                         { return IS_ZERO; }
"not"                           { return NOT; }
"integer?"                      { return IS_INT; }
"boolean?"                      { return IS_BOOL; }
"+"                             { return PLUS; }
"-"                             { return MINUS; }
"*"                             { return TIMES; }
"<"                             { return LT; }
">"                             { return GT; }
"<="                            { return LEQ; }
">="                            { return GEQ; }
"="                             { return EQ; }
[ \r\t\n]
.                               { return yytext[0]; }

%%

int yywrap(void) {
    return 1;
}
