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
    expr
} data_type_t;

typedef union {
    bool bool_val;
    uint64_t fixnum_val;
    expr_type_t expr_type;
} data_t;

typedef struct ast_node {
    data_t data;
    data_type_t type;
    struct ast_node* left;
    struct ast_node* right;
} ast_node_t;

ast_node_t* create_node(data_type_t type, void* data, ast_node_t* left, ast_node_t* right);

void print_tree(ast_node_t* node);
