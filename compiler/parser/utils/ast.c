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

/*
 * Prints node information to stdout.
 *
 * Args:
 *      - node (ast_node_t*): pointer ot node to print.
 *
 */
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
        case empty_list:
            printf("[]");
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
                case if_e:
                    printf("\"if\"");
                    break;
                default:
                    fprintf(stderr, "Unknown expression type.\n");
            }
            break;
        default:
            printf("Unknown node type.\n");
    }
}

/*
 * Frees node and any data associated with node.
 *
 * Args:
 *      - node (ast_node_t*): pointer to node to be freed.
 *
 */
static void free_node(ast_node_t* node) {
    // If node's data was dynamically allocated, free it.
    switch (node->type) {
        case character:
            free(node->data.character);
            break;
        default:
            break;
    }
    
    if (node->children != NULL) free(node->children);
    free(node);
}

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
 *      - ast_node_t*: pointer to node created, NULL if error.
 */
ast_node_t* create_node(data_type_t type, void* data) {
    ast_node_t* node;

    // Create node.
    if ((node = (ast_node_t *)malloc(sizeof(ast_node_t))) == NULL) {
        fprintf(stderr, "Memory allocation failed.\n");
        return NULL;
    }

    // Assign members.
    node->type = type;
    node->num_children = 0;
    node->children = NULL;

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
        case empty_list:
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
 * Add child node to AST node.
 *
 * Args:
 *      - parent (ast_node_t*): parent to which to add the child node.
 *      - child (ast_node_t*): child node to add.
 *
 * Returns:
 *      - int: 0 if success, non-zero if error.
 */
int add_child_to_node(ast_node_t* parent, ast_node_t* child) {
    // Allocate/resize memory for children array.
    if (parent->num_children == 0) {
        if ((parent->children = (ast_node_t**)malloc(sizeof(ast_node_t*))) == NULL) {
            fprintf(stderr, "Memory allocation failed.");
            return 1;
        }
    } else {
        if ((parent->children = (ast_node_t**)realloc(parent->children, sizeof(ast_node_t*)*(parent->num_children + 1))) == NULL) {
            fprintf(stderr, "Memory allocation failed.");
            return 1;
        }
    }

    // Add child toa array of children.
    parent->children[(parent->num_children)++] = child;

    return 0;

}

/*
 * Prints out the AST for a given parse.
 * 
 * Args:
 *      - root (ast_node_t*): Pointer to root node of AST.
 */
void print_tree(ast_node_t* root) {
    int i;

    if (root == NULL) return;

    if (root->type == expr) {
        printf("[");
        print_node(root);
        printf(", ");

        for (i = 0; i < root->num_children; i++) {
            print_tree(root->children[i]);
            if (i != root->num_children - 1) printf(", ");
        }
        printf("]");
    } else {
        for (i = 0; i < root->num_children; i++) print_tree(root->children[i]);
        print_node(root);
    }
}

/*
 * Free memory allocated for an AST.
 * 
 * Args:
 *      - root (ast_node_t*): Pointer to root node of AST.
 */
void free_tree(ast_node_t* root) {
    int i;

    if (root == NULL) return ;
    
    for (i = 0; i < root->num_children; i++)
        free_tree(root->children[i]);
    free_node(root);
}
