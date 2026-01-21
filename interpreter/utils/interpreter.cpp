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
#define FIXNUM_MASK 3
#define FIXNUM_TAG 0
#define CHAR_SHIFT 8
#define CHAR_MASK 255
#define CHAR_TAG 15
#define BOOL_SHIFT 7
#define BOOL_MASK 127
#define BOOL_TAG 31
#define EMPTY_LIST_MASK 255
#define EMPTY_LIST_TAG 47

// enumerations of opcodes.
enum class OpCode : uint64_t {
    LOAD64 = 1,
    RETURN = 2,
    ADD1 = 3,
    SUB1 = 4,
    INT_TO_CHAR = 5,
    CHAR_TO_INT = 6,
    IS_NULL = 7,
    IS_ZERO = 8,
    NOT = 9,
    IS_INT = 10,
    IS_BOOL = 11,
    PLUS = 12,
    TIMES = 13,
    MINUS = 14,
    LT = 15,
    GT = 16,
    LEQ = 17,
    GEQ = 18,
    EQ = 19
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
            case OpCode::CHAR_TO_INT:
                // Convert to integer.
                char_to_int();
                break;
            case OpCode::IS_NULL:
                // Check if top value on stack is ().
                is_null();
                break;
            case OpCode::IS_ZERO:
                // Check if value is 0 and push true if so, false otherwise.
                is_zero();
                break;
            case OpCode::NOT:
                // Convert truthy to falsya dn vice versa.
                invert();
                break;
            case OpCode::IS_INT:
                // Check if value is an integer and push true if so, false otherwise.
                is_int();
                break;
            case OpCode::IS_BOOL:
                // Check if value is a boolean and push true if so, false otherwise.
                is_bool();
                break;
            case OpCode::PLUS:
                // Add values that are currenty on stack. Leave result on stack.
                plus();
                break;
            case OpCode::TIMES:
                // Multiply values that are currenty on stack. Leave result on stack.
                times();
                break;
            case OpCode::MINUS:
                // Minus values that are currenty on stack. Leave result on stack.
                minus();
                break;
            case OpCode::LT:
                // Check that values on stack are in ascending order (top to bottom).
                less_than();
                break;
            case OpCode::GT:
                // Check that values on stack are in descending order (top to bottom).
                greater_than();
                break;
            case OpCode::LEQ:
                // Check that values on stack are in non-decreasing order (top to bottom).
                less_than_equal();
                break;
            case OpCode::GEQ:
                // Check that values on stack are in non-increasing order (top to bottom).
                greater_than_equal();
                break;
            case OpCode::EQ:
                // Check that values on stack are equal to one another.
                equal();
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

// Convert top valeu on stack from character to integer by adjusting tag.
void Interpreter::char_to_int(void) {
    // Shift and retag.
    stack.top() >>= (CHAR_SHIFT - FIXNUM_SHIFT);
    stack.top() &= ~FIXNUM_MASK;
    stack.top() |= FIXNUM_TAG;
}

// Check if top value on stack is 0.
void Interpreter::is_zero(void) {
    // If top value is 0, convert to true, else convert to false.
    if (stack.top() >> FIXNUM_SHIFT == 0)
        stack.top() = ((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
    else
        stack.top() = ((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
}

// Check if top value on stack is ().
void Interpreter::is_null(void) {
    // If top value is (), convert to true, else convert to false.
    if ((stack.top() & EMPTY_LIST_MASK) == EMPTY_LIST_TAG)
        stack.top() = ((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
    else
        stack.top() = ((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
}

// Converts top value on stack to falsy if truthy and to truthy if falsy.
void Interpreter::invert(void) {
    // The boolean value false is the onl true false value.
    if (((stack.top() & BOOL_MASK) == BOOL_TAG) && ((stack.top() >> BOOL_SHIFT) == 0))
        stack.top() = ((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
    else
        stack.top() = ((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
}

// Check if top value on stack is integer.
void Interpreter::is_int(void) {
    // If top value is an integer, convert to true, else convert to false.
    if ((stack.top() & FIXNUM_MASK) == FIXNUM_TAG)
        stack.top() = ((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
    else
        stack.top() = ((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
}

// Check if top value on stack is boolean.
void Interpreter::is_bool(void) {
    // If top value is a boolean, convert to true, else convert to false.
    if ((stack.top() & BOOL_MASK) == BOOL_TAG)
        stack.top() = ((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
    else
        stack.top() = ((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
}

// Add values on stack leaving result on stack.
void Interpreter::plus(void) {
    uint64_t val;

    while (stack.size() > 1) {
        // Save top value in stack.
        val = stack.top();

        // Remove top element of stack.
        stack.pop();

        // Add removed value to top value on stack.
        stack.top() += val;
    }
}

// Multiply values on stack leaving result on stack.
void Interpreter::times(void) {
    uint64_t val;

    while (stack.size() > 1) {
        // Save top value in stack.
        val = stack.top();

        // Untag value.
        val >>= FIXNUM_SHIFT;

        // Remove top element of stack.
        stack.pop();

        // Untag current top value.
        stack.top() >>= FIXNUM_SHIFT;

        // Multiply removed value to top value on stack.
        stack.top() *= val;

        // Retag op value on stack.
        stack.top() <<= FIXNUM_SHIFT;
        stack.top() &= ~FIXNUM_MASK;
        stack.top() |= FIXNUM_TAG;
    }
}

// Subtract values on stack leaving result on stack.
void Interpreter::minus(void) {
    uint64_t val;

    // Subtract from top value on stack.
    val = stack.top() >> FIXNUM_SHIFT;
    stack.pop();

    while (stack.size() > 0) {
        // Subtract value.
        val -= (stack.top() >> FIXNUM_SHIFT);

        // Remove top element of stack.
        stack.pop();
    }

    // Retag value and push to top of stack.
    val <<= FIXNUM_SHIFT;
    val &= ~FIXNUM_MASK;
    val |= FIXNUM_TAG;
    push(val);
}

// Check that values on stack are in ascending order (top to bottom). Place truthy on stack if so.
void Interpreter::less_than(void) {
    bool less_than;
    uint64_t curr, prev;

    less_than = true;

    // Pop top value off stack.
    curr = pop();

    while (stack.size() > 0) {
        // Update previous and current.
        prev = curr;
        curr = pop();

        if (prev >= curr) less_than = false;

    }

    // If values are in ascending order, push truthy onto stack, else push falsy.
    if (less_than) push(((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);
    else push(((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);
}

// Check that values on stack are in descending order (top to bottom). Place truthy on stack if so.
void Interpreter::greater_than(void) {
    bool greater_than;
    uint64_t curr, prev;

    greater_than = true;

    // Pop top value off stack.
    curr = pop();

    while (stack.size() > 0) {
        // Update previous and current.
        prev = curr;
        curr = pop();
        
        if (prev <= curr) greater_than = false;

    }

    // If values are in descending order, push truthy onto stack, else push falsy.
    if (greater_than) push(((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);
    else push(((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);
}

// Check that values on stack are in non-decreasing order (top to bottom). Place truthy on stack if so.
void Interpreter::less_than_equal(void) {
    bool less_than;
    uint64_t curr, prev;

    less_than = true;

    // Pop top value off stack.
    curr = pop();

    while (stack.size() > 0) {
        // Update previous and current.
        prev = curr;
        curr = pop();
        
        if (prev > curr) less_than = false;

    }

    // If values are in ascending order, push truthy onto stack, else push falsy.
    if (less_than) push(((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);
    else push(((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);
}

// Check that values on stack are in non-increasing order (top to bottom). Place truthy on stack if so.
void Interpreter::greater_than_equal(void) {
    bool greater_than;
    uint64_t curr, prev;

    greater_than = true;

    // Pop top value off stack.
    curr = pop();

    while (stack.size() > 0) {
        // Update previous and current.
        prev = curr;
        curr = pop();
        
        if (prev < curr) greater_than = false;

    }

    // If values are in descending order, push truthy onto stack, else push falsy.
    if (greater_than) push(((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);
    else push(((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);
}

// Check that values on stack are equal. Place truthy on stack if so.
void Interpreter::equal(void) {
    bool equal;
    uint64_t curr, prev;

    equal = true;

    // Pop top value off stack.
    curr = pop();

    while (stack.size() > 0) {
        // Update previous and current.
        prev = curr;
        curr = pop();
        
        if (prev != curr) equal = false;

    }

    // If values are in descending order, push truthy onto stack, else push falsy.
    if (equal) push(((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);
    else push(((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);
}

