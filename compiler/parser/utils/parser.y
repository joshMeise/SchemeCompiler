/*
 * syntax.y - parser for a Scheme program
 *
 * Josh Meise
 * 01-25-2026
 * Description: 
 *
 */

%{

#include <stdio.h>
#include <string.h>
#include "ast.h"

extern int yylex(void);

int yyerror(char*);
ast_node_t* root;

%}

%union {
    int ival;
    char* sval;
    ast_node_t* nval;
}

%token <ival> NUMBER
%token <sval> BOOL CHAR IDENTIFIER
%token ADD1 SUB1 INT_TO_CHAR CHAR_TO_INT IS_NULL IS_ZERO NOT IS_INT IS_BOOL PLUS MINUS TIMES LT GT LEQ GEQ EQ IF LET

%type <nval> s add1 sub1 int_to_char char_to_int is_null is_zero not is_int is_bool plus minus times lt gt leq geq eq integer boolean character empty_list if let

%start s

%%

s: integer                                  { $$ = $1; root = $$; }
 | boolean                                  { $$ = $1; root = $$; }
 | character                                { $$ = $1; root = $$; }
 | empty_list                               { $$ = $1; root = $$; }
 | add1                                     { $$ = $1; root = $$; }
 | sub1                                     { $$ = $1; root = $$; }
 | int_to_char                              { $$ = $1; root = $$; }
 | char_to_int                              { $$ = $1; root = $$; }
 | is_null                                  { $$ = $1; root = $$; }
 | is_zero                                  { $$ = $1; root = $$; }
 | not                                      { $$ = $1; root = $$; }
 | is_int                                   { $$ = $1; root = $$; }
 | is_bool                                  { $$ = $1; root = $$; }
 | plus                                     { $$ = $1; root = $$; }
 | minus                                    { $$ = $1; root = $$; }
 | times                                    { $$ = $1; root = $$; }
 | lt                                       { $$ = $1; root = $$; }
 | gt                                       { $$ = $1; root = $$; }
 | leq                                      { $$ = $1; root = $$; }
 | geq                                      { $$ = $1; root = $$; }
 | eq                                       { $$ = $1; root = $$; }
 | if                                       { $$ = $1; root = $$; }
 | let                                      { $$ = $1; root = $$; }
 ;

integer: NUMBER                             { uint64_t data = $1; $$ = create_node(fixnum, (void*)&data); }
       ;

boolean: BOOL                               { bool val; if (!(strcmp($1, "#t")) || !strcmp($1, "#T")) val = true; else val = false; $$ = create_node(boolean, (void*)&val); free($1); }
       ;

character: CHAR                             { $$ = create_node(character, (void*)$1); free($1); }
         ;

empty_list: '(' ')'                         { $$ = create_node(empty_list, NULL); }
          ;

add1: '(' ADD1 s ')'                        { expr_type_t type = add1; $$ = create_node(expr, (void*)&type); add_child_to_node($$, $3); }
    ;

sub1: '(' SUB1 s ')'                        { expr_type_t type = sub1; $$ = create_node(expr, (void*)&type); add_child_to_node($$, $3); }
    ;

int_to_char: '(' INT_TO_CHAR s ')'          { expr_type_t type = int_to_char; $$ = create_node(expr, (void*)&type); add_child_to_node($$, $3); }
           ;

char_to_int: '(' CHAR_TO_INT s ')'          { expr_type_t type = char_to_int; $$ = create_node(expr, (void*)&type); add_child_to_node($$, $3); }
           ;

is_null: '(' IS_NULL s ')'                  { expr_type_t type = is_null; $$ = create_node(expr, (void*)&type); add_child_to_node($$, $3); }
       ;

is_zero: '(' IS_ZERO s ')'                  { expr_type_t type = is_zero; $$ = create_node(expr, (void*)&type); add_child_to_node($$, $3); }
       ;

not: '(' NOT s ')'                          { expr_type_t type = not_e; $$ = create_node(expr, (void*)&type); add_child_to_node($$, $3); }
   ;

is_int: '(' IS_INT s ')'                    { expr_type_t type = is_int; $$ = create_node(expr, (void*)&type); add_child_to_node($$, $3); }
      ;

is_bool: '(' IS_BOOL s ')'                  { expr_type_t type = is_bool; $$ = create_node(expr, (void*)&type); add_child_to_node($$, $3); }
       ;

plus: '(' PLUS s s ')'                      { expr_type_t type = plus; $$ = create_node(expr, (void*)&type); add_child_to_node($$, $3); add_child_to_node($$, $4); }
    ;

minus: '(' MINUS s s ')'                    { expr_type_t type = minus; $$ = create_node(expr, (void*)&type); add_child_to_node($$, $3); add_child_to_node($$, $4); }
     ;

times: '(' TIMES s s ')'                    { expr_type_t type = times; $$ = create_node(expr, (void*)&type); add_child_to_node($$, $3); add_child_to_node($$, $4); }
     ;

lt: '(' LT s s ')'                          { expr_type_t type = lt; $$ = create_node(expr, (void*)&type); add_child_to_node($$, $3); add_child_to_node($$, $4); }
  ;

gt: '(' GT s s ')'                          { expr_type_t type = gt; $$ = create_node(expr, (void*)&type); add_child_to_node($$, $3); add_child_to_node($$, $4); }
  ;

leq: '(' LEQ s s ')'                        { expr_type_t type = leq; $$ = create_node(expr, (void*)&type); add_child_to_node($$, $3); add_child_to_node($$, $4); }
   ; 

geq: '(' GEQ s s ')'                        { expr_type_t type = geq; $$ = create_node(expr, (void*)&type); add_child_to_node($$, $3); add_child_to_node($$, $4); }
   ; 

eq: '(' EQ s s ')'                          { expr_type_t type = eq; $$ = create_node(expr, (void*)&type); add_child_to_node($$, $3); add_child_to_node($$, $4); }
    ; 

if: '(' IF s s s ')'                        { expr_type_t type = if_e; $$ = create_node(expr, (void*)&type); add_child_to_node($$, $3); add_child_to_node($$, $4); add_child_to_node($$, $5); }
    ;

let: '(' LET '(' bindings ')' s ')'         { printf("HERE\n"); }
   ;

bindings: bindings binding                  { printf("HORO\n"); }
        | binding
        ;

binding: '(' IDENTIFIER s ')'
       ;

%%

int yyerror(char* s) {
    fprintf(stderr, "%s\n", s);
    return 1;
}
