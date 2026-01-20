/*
 * interpreter.cpp - 
 *
 * Josh Meise
 * 01-16-2026
 * Description: 
 *
 */

#include "interpreter.h"
#include <stdexcept>
#include <span>
#include <iostream>
#include <format>

#define BPB 8
#define BPI 8
#define FIXNUM_SHIFT 2
#define CHAR_SHIFT 8
#define CHAR_MASK 255
#define CHAR_TAG 15

// enumerations of opcodes.
enum class OpCode : uint64_t {
    LOAD64 = 1,
    RETURN = 2,
    ADD1 = 3,
    SUB1 = 4,
    INT_TO_CHAR = 5
};

// Build insturction out of 4 bytes.
static uint64_t word_from_bytes(std::span<uint8_t> slice) {
    uint64_t val;
    int i;
    
    if (slice.size() != 8) throw std::invalid_argument("Argument must contain 8 bytes.\n");

    val = 0;
    for (i = 0; i < BPI; i++)
        val |= (slice[i] << i*BPB);
    
    return val;
}

// Default constructor.
Interpreter::Interpreter(void) {
    // Initialize program counter.
    pc = 0;
}

// Interpret a program, return once it reaches a return instruction.
uint64_t Interpreter::interpret(void) {
    OpCode instr;
    uint64_t word, val;

    do {
        // Read instruction.
        word = read_word();
        
        // Case value to instruction.
        instr = static_cast<OpCode>(word);
        
        switch (instr) {
            case OpCode::LOAD64:
                // Get the next word from the code and push onto the stack.
                word = read_word();
                push(word);
                break;
            case OpCode::RETURN:
                // Pop a value from stack and return the value.
                val = pop();
                break;
            case OpCode::ADD1:
                // Add 1 to the top value on the stack.
                add1();
                break;
            case OpCode::SUB1:
                // Subtract 1 from top value on stack.
                sub1();
                break;
            case OpCode::INT_TO_CHAR:
                // Convert to character.
                int_to_char();
                break;
            default:
                throw std::logic_error("Opcode not yet implemented");
                break;
        }
    } while (instr != OpCode::RETURN);

    return val;
}

// Construct interpreter based on a byte stream.
Interpreter::Interpreter(std::vector<uint8_t>& bytes) {
    int i;
    uint64_t word;

    // Add instructions to vector contsining code.
    for (i = 0; i < static_cast<int>(bytes.size()); i+= BPI) {
        word = word_from_bytes(std::span<uint8_t>(bytes.begin() + i, BPI));
        code.push_back(word);
    }

    // Initialize program counter.
    pc = 0;
}

// Get instruction from stack.
uint64_t Interpreter::read_word(void) {
    return code[pc++];
}

// Push value onto stack.
void Interpreter::push(uint64_t val) {
    stack.push(val);
}

// Pop value from stack.
uint64_t Interpreter::pop(void) {
    uint64_t val;

    val = stack.top();
    stack.pop();

    return val;
}

// Add 1 to the top value on the stack.
void Interpreter::add1(void) {
    // Add 4 due to shift.
    stack.top() += 4;
}

// Subtract 1 from the top value on the stack.
void Interpreter::sub1(void) {
    // Subtract 4 due to shift.
    stack.top() -= 4;
}

// Convert top valeu on stack from integer to character by adjusting tag.
void Interpreter::int_to_char(void) {
    // Shift and retag.
    stack.top() <<= (CHAR_SHIFT - FIXNUM_SHIFT);
    stack.top() &= ~CHAR_MASK;
    stack.top() |= CHAR_TAG;
}
