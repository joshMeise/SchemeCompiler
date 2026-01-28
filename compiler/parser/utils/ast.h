/*
 * ast.h - builds AST for Scheme expression
 *
 * Josh Meise
 * 01-26-2026
 * Description:
 * Functions to be caled in Bison parser for Scheme to build AST.
 *
 */

#pragma once
#include <inttypes.h>
#include <stdbool.h>

typedef enum {
    add1,
    sub1,
    int_to_char,
    char_to_int,
    is_null,
    is_zero,
    not_e,
    is_int,
    is_bool,
    plus,
    minus,
    times,
    lt,
    gt,
    leq,
    geq,
    eq,
    if_e
} expr_type_t;

typedef enum {
    fixnum,
    boolean,
    character,
    empty_list,
    expr
} data_type_t;

typedef union {
    bool bool_val;
    uint64_t fixnum_val;
    char* character;
    expr_type_t expr_type;
} data_t;

typedef struct ast_node {
    data_t data;
    data_type_t type;
    int num_children;
    struct ast_node** children;
} ast_node_t;

/*
 * Creates a new AST node.
 *
 * Args:
 *      - type (data_type_t): node type
 *      - data (void*): pointer to type of data contained in node
 *
 * Returns:
 *      - ast_node_t*: pointer to node created, NULL if error.
 */
ast_node_t* create_node(data_type_t type, void* data);

/*
 * Add child to AST node.
 *
 * Args:
 *      - parent (ast_node_t*): parent to which to add the child node.
 *      - child (ast_node_t*): child node to add.
 *
 * Returns:
 *      - int: 0 if success, non-zero if error.
 */
int add_child_to_node(ast_node_t* parent, ast_node_t* child);

/*
 * Prints out the AST for a given parse.
 * 
 * Args:
 *      - root (ast_node_t*): Pointer to root node of AST.
 */
void print_tree(ast_node_t* node);

/*
 * Free memory allocated for an AST.
 * 
 * Args:
 *      - root (ast_node_t*): Pointer to root node of AST.
 */
void free_tree(ast_node_t* root);
