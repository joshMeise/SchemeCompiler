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

#define BPB 8
#define BPI 4

// Enumerations of opcodes.
enum class OpCodes : uint64_t {
    LOAD64 = 1,
    RETURN = 2
};

// Build insturction out of 4 bytes.
static uint64_t word_from_bytes(std::span<uint8_t> slice) {
    if (slice.size() != 4) throw std::invalid_argument("Argument must contain 4 bytes.\n");

    return slice[0] | (slice[1] << BPB) | (slice[2] <<2*BPB) | (slice[3] << 3*BPB);
}

// Default constructor.
Interpreter::Interpreter(void) {
    // Initialize program counter.
    pc = 0;
}

// Interpret a program, return once it reaches a return instruction.

// Construct interpreter based on a byte stream.
Interpreter::Interpreter(std::vector<uint8_t>& bytes) {
    int i;
    uint64_t word;

    // Add instructions to stack.
    for (i = 0; i < bytes.size(); i+= BPI) {
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
