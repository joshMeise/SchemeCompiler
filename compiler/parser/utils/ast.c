/*
 * ast.c - 
 *
 * Josh Meise
 * 01-27-2026
 * Description: 
 *
 */

#include "ast.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

static void print_node(ast_node_t* node) {
    switch (node->type) {
        case fixnum:
            printf("%llu", node->data.fixnum_val);
            break;
        case boolean:
            if (node->data.bool_val) printf("True");
            else printf("False ");
            break;
        case character:
            if (node->data.character[strlen(node->data.character) - 1] == '\"') printf("\"#\\\\\\\"\"");
            else if (node->data.character[strlen(node->data.character) - 1] == '\n') printf("\"#\\\\\\n\"");
            else printf("\"#\\\\%s\"", node->data.character + 2);
            break;
        case expr:
            switch (node->data.expr_type) {
                case add1:
                    printf("\"add1\"");
                    break;
                case sub1:
                    printf("\"sub1\"");
                    break;
                case int_to_char:
                    printf("\"integer->char\"");
                    break;
                case char_to_int:
                    printf("\"char->integer\"");
                    break;
                case is_null:
                    printf("\"null?\"");
                    break;
                case is_zero:
                    printf("\"zero?\"");
                    break;
                case not_e:
                    printf("\"not\"");
                    break;
                case is_int:
                    printf("\"integer?\"");
                    break;
                case is_bool:
                    printf("\"boolean?\"");
                    break;
                case plus:
                    printf("\"+\"");
                    break;
                case minus:
                    printf("\"-\"");
                    break;
                case times:
                    printf("\"*\"");
                    break;
                case lt:
                    printf("\"<\"");
                    break;
                case gt:
                    printf("\">\"");
                    break;
                case leq:
                    printf("\"<=\"");
                    break;
                case geq:
                    printf("\">=\"");
                    break;
                case eq:
                    printf("\"=\"");
                    break;
                default:
                    fprintf(stderr, "Unknown expression type.\n");
            }
            break;
        default:
            printf("Unknown node type.\n");
    }
}

ast_node_t* create_node(data_type_t type, void* data, ast_node_t* left, ast_node_t* right) {
    ast_node_t* node;

    // Create node.
    if ((node = (ast_node_t *)malloc(sizeof(ast_node_t))) == NULL) {
        fprintf(stderr, "Memory allocation failed.\n");
        return NULL;
    }

    // Assign members.
    node->type = type;
    node->left = left;
    node->right = right;

    switch (type) {
        case fixnum:
            node->data.fixnum_val = *((int*)data);
            break;
        case boolean:
            node->data.bool_val = *((bool*)data);
            break;
        case character:
            if ((node->data.character = (char*)malloc(sizeof(char)*(strlen((char*)data) + 1))) == NULL) {
                fprintf(stderr, "Memory allocation failed.\n");
                return NULL;
            }
            strcpy(node->data.character, (char*)data);
            break;
        case expr:
            node->data.expr_type = *((expr_type_t*)data);
            break;
        default:
            fprintf(stderr, "Unknown node type.\n");
            free(node);
            return NULL;
    }

    return node;
}

/*
 * Prints out the AST for a given parse.
 * 
 * Args:
 *      - root (ast_node_t*): Pointer to root node of AST.
 *
 */
void print_tree(ast_node_t* root) {
    if (root == NULL)
        return;

    if (root->type == expr) {
        printf("[");
        print_node(root);
        printf(", ");
        print_tree(root->left);
        if (root->right != NULL) printf(", ");
        print_tree(root->right);
        printf("]");
    } else {
        print_tree(root->left);
        print_tree(root->right);
        print_node(root);
    }
}
