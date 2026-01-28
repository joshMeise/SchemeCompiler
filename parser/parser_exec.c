/*
 * parser_exec.c --
 *
 * Josh Meise
 * 01-25-2026
 * Description: 
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include "ast.h"

extern int yyparse(void);
extern int yylex_destroy(void);
extern FILE* yyin;
extern ast_node_t* root;

int main(int argc, char** argv) {
    int ret;

    yyin = stdin;

    ret = yyparse();

    print_tree(root);
    printf("\n");

    // Clean up.
    yylex_destroy();

    if (ret == 0) exit(EXIT_SUCCESS);
    else exit(EXIT_FAILURE);
}
