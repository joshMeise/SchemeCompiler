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
#include <stack>

class Interpreter {
public:
    // Default constructor.
    Interpreter(void);

    // Construct interpreter based on byte stream.
    Interpreter(std::vector<uint8_t>& bytes);

    // Interpret program.
    uint64_t interpret(void);

private:
    // Member variables.
    std::vector<uint64_t> code;
    std::stack<uint64_t> stack;
    int pc;

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
};
