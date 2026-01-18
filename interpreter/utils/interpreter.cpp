/*
 * interpreter.cpp - 
 *
 * Josh Meise
 * 01-16-2026
 * Description: 
 *
 * Questions:
 * - What do we do with PC as we read off of stack?
 *
 */

#include "interpreter.h"
#include <stdexcept>
#include <span>
#include <iostream>
#include <format>

#define BPB 8
#define BPI 8

// enumerations of opcodes.
enum class OpCode : uint64_t {
    LOAD64 = 1,
    RETURN = 2
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
    int val = 0;
    for (auto& word : stack) {
        std::cout << std::format("0x{:016X}\n", word);
    }
    /*
    OpCode instr;
    uint64_t word;

    do {
        // Read instruction from the stack.
        word = readword();
        
        // Case value to instruction.
        instr = static_cast<OpCode>(word);
        
        switch (instr) {
            case OpCode::LOAD64:
                break;
            case OpCode::RETURN:
                break;
            default:
                throw std::logic_error("Opcode not yet implemented");
                break;
        }
    } while (instr != OpCode::RETURN);
    */
    return val;
}

// Construct interpreter based on a byte stream.
Interpreter::Interpreter(std::vector<uint8_t>& bytes) {
    int i;
    uint64_t word;

    // Add instructions to stack.
    for (i = 0; i < static_cast<int>(bytes.size()); i+= BPI) {
        word = word_from_bytes(std::span<uint8_t>(bytes.begin() + i, BPI));
        stack.push_back(word);
    }

    // Initialize program counter.
    pc = 0;
}

// Get instruction from stack.
uint64_t Interpreter::readword(void) {
    return stack[pc++];
}
