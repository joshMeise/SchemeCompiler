/*
 * interpreter.h - 
 *
 * Josh Meise
 * 01-16-2026
 * Description: 
 *
 */

#pragma once
#include <stack>
#include <cstdint>
#include <vector>
#include <iostream>

class Interpreter {
public:
    // Default constructor.
    Interpreter(void);

    // Construct interpreter based on byte stream.
    Interpreter(std::vector<uint8_t>& bytes);

    // Interpret program.
    uint64_t interpret(void);

    // Print out value.
    void print_val(uint64_t val, std::ostream*& output);

private:
    // Member variables.
    std::vector<uint64_t> code;
    std::vector<uint64_t> stack;
    int pc;
    std::vector<std::vector<uint64_t>> env;
    std::vector<uint64_t> heap;
    uint64_t heap_ptr;

    // Get instruction.
    uint64_t read_word(void);

    // Push value onto stack.
    void push(uint64_t val);

    // Pop value from stack.
    uint64_t pop(void);

    // Add 1 to top value on stack.
    void add1(void);

    // Subtract 1 from top value on stack.
    void sub1(void);

    // Convert top valeu on stack from integer to character by adjusting tag
    void int_to_char(void);

    // Convert top value on stack from character to integer by adjusting tag
    void char_to_int(void);

    // Check if top value on stack is 0.
    void is_zero(void);

    // Check if top value on stack is ().
    void is_null(void);

    // Converts top value on stack to falsy if truthy and to truthy if falsy.
    void invert(void);

    // Check if top value on stack is integer.
    void is_int(void);

    // Check if top value on stack is boolean.
    void is_bool(void);

    // Add values on stack leaving result on stack.
    void plus(void);

    // Multiply values on stack leaving result on stack.
    void times(void);

    // Subtract values on stack leaving result on stack.
    void minus(void);

    // Check that values on stack are in ascending order (top to bottom). Place truthy on stack if so.
    void less_than(void);

    // Check that values on stack are in descending order (top to bottom). Place truthy on stack if so.
    void greater_than(void);

    // Check that values on stack are in non-decreasing order (top to bottom). Place truthy on stack if so.
    void less_than_equal(void);

    // Check that values on stack are in non-increasing order (top to bottom). Place truthy on stack if so.
    void greater_than_equal(void);

    // Check that values on stack are equal. Place truthy on stack if so.
    void equal(void);

    // Move to alternate if test was satisfied.
    void pop_jump_if_false(void);

    // Move past alternate if test was not satisfied.
    void jump_over_else(void);
    
    // Create a new environment for the binding and load the given number of values from the stack into the environment.
    void let(void);

    // Get a value from the environment onto stack.
    void get_from_env(void);

    // Clean up binding's environment.
    void end_let(void);

    // Create cons cell.
    void create_cons(void);
};
