/*
 * ast.h - 
 *
 * Josh Meise
 * 01-26-2026
 * Description: 
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
    eq
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
    struct ast_node* left;
    struct ast_node* right;
} ast_node_t;

/*
 * Creates a new AST node.
 *
 * Args:
 *      - type (data_type_t): node type
 *      - data (void*): pointer to type of data contained in node
 *      - left (ast_node_t*): node's left child.
 *      - right (ast_node_t*): node's right child.
 *
 * Returns:
 *      - ast_node_t*: pointer to node created.
 *      - NULL: if error.
 */
ast_node_t* create_node(data_type_t type, void* data, ast_node_t* left, ast_node_t* right);

/*
 * Prints out the AST for a given parse.
 * 
 * Args:
 *      - root (ast_node_t*): Pointer to root node of AST.
 *
 */
void print_tree(ast_node_t* node);

/*
 * Free memory allocated for an AST.
 * 
 * Args:
 *      - root (ast_node_t*): Pointer to root node of AST.
 *
 */
void free_tree(ast_node_t* root);
