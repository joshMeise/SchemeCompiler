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
};
