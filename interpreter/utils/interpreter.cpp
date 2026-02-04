/*
 * interpreter.cpp - 
 *
 * Josh Meise
 * 01-16-2026
 * Description: 
 *
 * Implementation notes;
 * - Characters in string are untagged and placed straight from instructions onto heap (not going via stack).
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
#define PAIR_SHIFT 3
#define PAIR_MASK 7
#define PAIR_TAG 1
#define STR_SHIFT 3
#define STR_MASK 7
#define STR_TAG 3
#define VEC_SHIFT 3
#define VEC_MASK 7
#define VEC_TAG 2

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
    EQ = 19,
    POP_JUMP_IF_FALSE = 20,
    JUMP_OVER_ELSE = 21,
    LET = 22,
    GET_FROM_ENV = 23,
    END_LET = 24,
    CONS = 25,
    CAR = 26,
    CDR = 27,
    STR = 28,
    STR_REF = 29,
    STR_SET = 30,
    STR_APP = 31,
    VEC = 32,
    VEC_REF = 33,
    VEC_SET = 34,
    VEC_APP = 35
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
    // Initialize program counter and heap pointer.
    pc = 0;
    heap_ptr = 0;
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

    // Initialize program counter and heap pointer.
    pc = 0;
    heap_ptr = 0;
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
            case OpCode::POP_JUMP_IF_FALSE:
                // Check top value on stack and direct control accordingly.
                pop_jump_if_false();
                break;
            case OpCode::JUMP_OVER_ELSE:
                // Jump over alternate if condition was satisfied.
                jump_over_else();
                break;
            case OpCode::LET:
                // Load the given number of values from stack into environment.
                let();
                break;
            case OpCode::GET_FROM_ENV:
                // Load given value from stack into environment.
                get_from_env();
                break;
            case OpCode::END_LET:
                // Clean up environment associated with binding.
                end_let();
                break;
            case OpCode::CONS:
                // Create cons cell on heap.
                create_cons();
                break;
            case OpCode::CAR:
                // Pull first value in corresponding cons cell.
                car();
                break;
            case OpCode::CDR:
                // Get second value from corresponding cons cell.
                cdr();
                break;
            case OpCode::STR:
                // Place string contents onto heap.
                create_str();
                break;
            case OpCode::STR_REF:
                // Get character from string.
                str_ref();
                break;
            case OpCode::STR_SET:
                // Set character in string.
                str_set();
                break;
            case OpCode::STR_APP:
                // Concatenate strings.
                str_append();
                break;
            case OpCode::VEC:
                // Place vector contents onto heap.
                create_vec();
                break;
            case OpCode::VEC_REF:
                // Get character from vectors.
                vec_ref();
                break;
            case OpCode::VEC_SET:
                // Set character in vectors.
                vec_set();
                break;
            case OpCode::VEC_APP:
                // Concatenate vectors.
                vec_append();
                break;
            default:
                throw std::runtime_error("Opcode not yet implemented.\n");
                break;
        }
    } while (instr != OpCode::RETURN);

    return val;
}

// Prints out value returned by interpreter.
void Interpreter::print_val(uint64_t val, std::ostream*& output) {
    uint64_t i;

    if ((val & FIXNUM_MASK) == FIXNUM_TAG)
        *output << (val >> FIXNUM_SHIFT);
    else if ((val & BOOL_MASK) == BOOL_TAG)
        if (val >> BOOL_SHIFT == 1) *output << "#t";
        else if (val >> BOOL_SHIFT == 0) *output << "#f";
        else *output << "Error.\n";
    else if ((val & CHAR_MASK) == CHAR_TAG) {
        if ((val >> CHAR_SHIFT) == '\n') *output << "#\\newline";
        else *output << std::format("#\\{:c}", (val >> CHAR_SHIFT));
    } 
    else if ((val & EMPTY_LIST_MASK) == EMPTY_LIST_TAG) *output << "()";
    else if ((val & PAIR_MASK) == PAIR_TAG) {
        *output << "(";
        print_val(heap[val >> PAIR_SHIFT], output);
        *output << " . ";
        print_val(heap[(val >> PAIR_SHIFT) + 1], output);
        *output << ")";
    }
    else if ((val & STR_MASK) == STR_TAG) {
        *output << "\"";
        for (i = heap[val >> STR_SHIFT]; i >= 1; i--) *output << static_cast<char>(heap[(val >> STR_SHIFT) + i]);
        *output << "\"";
    }
    else if ((val & VEC_MASK) == VEC_TAG) {
        *output << "#( ";
        for (i = heap[val >> VEC_SHIFT]; i >= 1; i--) {
            print_val(heap[(val >> VEC_SHIFT) + i], output);
            *output << " ";
        }
        *output << ")";
    }
    else
        throw std::runtime_error("Invlaid type.\n");
}

// Get instruction from stack.
uint64_t Interpreter::read_word(void) {
    return code[pc++];
}

// Push value onto stack.
void Interpreter::push(uint64_t val) {
    stack.push_back(val);
}

// Pop value from stack.
uint64_t Interpreter::pop(void) {
    uint64_t val;

    val = stack.back();
    stack.pop_back();

    return val;
}

// Add 1 to the top value on the stack.
void Interpreter::add1(void) {
    // Add 4 due to shift.
    stack.back() += 4;
}

// Subtract 1 from the top value on the stack.
void Interpreter::sub1(void) {
    // Subtract 4 due to shift.
    stack.back() -= 4;
}

// Convert top valeu on stack from integer to character by adjusting tag.
void Interpreter::int_to_char(void) {
    // Shift and retag.
    stack.back() <<= (CHAR_SHIFT - FIXNUM_SHIFT);
    stack.back() &= ~CHAR_MASK;
    stack.back() |= CHAR_TAG;
}

// Convert top valeu on stack from character to integer by adjusting tag.
void Interpreter::char_to_int(void) {
    // Shift and retag.
    stack.back() >>= (CHAR_SHIFT - FIXNUM_SHIFT);
    stack.back() &= ~FIXNUM_MASK;
    stack.back() |= FIXNUM_TAG;
}

// Check if top value on stack is 0.
void Interpreter::is_zero(void) {
    // If top value is 0, convert to true, else convert to false.
    if (stack.back() >> FIXNUM_SHIFT == 0)
        stack.back() = ((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
    else
        stack.back() = ((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
}

// Check if top value on stack is ().
void Interpreter::is_null(void) {
    // If top value is (), convert to true, else convert to false.
    if ((stack.back() & EMPTY_LIST_MASK) == EMPTY_LIST_TAG)
        stack.back() = ((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
    else
        stack.back() = ((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
}

// Converts top value on stack to falsy if truthy and to truthy if falsy.
void Interpreter::invert(void) {
    // The boolean value false is the onl true false value.
    if (((stack.back() & BOOL_MASK) == BOOL_TAG) && ((stack.back() >> BOOL_SHIFT) == 0))
        stack.back() = ((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
    else
        stack.back() = ((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
}

// Check if top value on stack is integer.
void Interpreter::is_int(void) {
    // If top value is an integer, convert to true, else convert to false.
    if ((stack.back() & FIXNUM_MASK) == FIXNUM_TAG)
        stack.back() = ((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
    else
        stack.back() = ((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
}

// Check if top value on stack is boolean.
void Interpreter::is_bool(void) {
    // If top value is a boolean, convert to true, else convert to false.
    if ((stack.back() & BOOL_MASK) == BOOL_TAG)
        stack.back() = ((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
    else
        stack.back() = ((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG;
}

// Add values on stack leaving result on stack.
void Interpreter::plus(void) {
    uint64_t val;

    // Pop two values off stack and add them.
    val = pop() >> FIXNUM_SHIFT;
    val += pop() >> FIXNUM_SHIFT;

    // Push result bakc onto stack.
    push(((val << FIXNUM_SHIFT) & ~FIXNUM_MASK) | FIXNUM_TAG);
}

// Multiply values on stack leaving result on stack.
void Interpreter::times(void) {
    uint64_t val;

    // Pop two values off stack and multiply them.
    val = pop() >> FIXNUM_SHIFT;
    val *= pop() >> FIXNUM_SHIFT;

    // Push result bakc onto stack.
    push(((val << FIXNUM_SHIFT) & ~FIXNUM_MASK) | FIXNUM_TAG);
}

// Subtract values on stack leaving result on stack.
void Interpreter::minus(void) {
    uint64_t val_1, val_2, val;

    // Pop two values off stack and subtract them.
    val_1 = pop() >> FIXNUM_SHIFT;
    val_2 = pop() >> FIXNUM_SHIFT;
    val = val_2 - val_1;

    // Push result bakc onto stack.
    push(((val << FIXNUM_SHIFT) & ~FIXNUM_MASK) | FIXNUM_TAG);
}

// Check that values on stack are in ascending order (top to bottom). Place truthy on stack if so.
void Interpreter::less_than(void) {
    uint64_t val_1, val_2;

    // Pop two values off of stack.
    val_1 = pop() >> FIXNUM_SHIFT;
    val_2 = pop() >> FIXNUM_SHIFT;

    // Compare values and push result onto stack.
    if (val_2 < val_1) push(((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);
    else push(((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);
}

// Check that values on stack are in descending order (top to bottom). Place truthy on stack if so.
void Interpreter::greater_than(void) {
    uint64_t val_1, val_2;

    // Pop two values off of stack.
    val_1 = pop() >> FIXNUM_SHIFT;
    val_2 = pop() >> FIXNUM_SHIFT;

    // Compare values and push result onto stack.
    if (val_2 > val_1) push(((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);
    else push(((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);
}

// Check that values on stack are in non-decreasing order (top to bottom). Place truthy on stack if so.
void Interpreter::less_than_equal(void) {
    uint64_t val_1, val_2;

    // Pop two values off of stack.
    val_1 = pop() >> FIXNUM_SHIFT;
    val_2 = pop() >> FIXNUM_SHIFT;

    // Compare values and push result onto stack.
    if (val_2 <= val_1) push(((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);
    else push(((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);

}

// Check that values on stack are in non-increasing order (top to bottom). Place truthy on stack if so.
void Interpreter::greater_than_equal(void) {
    uint64_t val_1, val_2;

    // Pop two values off of stack.
    val_1 = pop() >> FIXNUM_SHIFT;
    val_2 = pop() >> FIXNUM_SHIFT;

    // Compare values and push result onto stack.
    if (val_2 >= val_1) push(((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);
    else push(((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);

}

// Check that values on stack are equal. Place truthy on stack if so.
void Interpreter::equal(void) {
    uint64_t val_1, val_2;

    // Pop two values off of stack.
    val_1 = pop() >> FIXNUM_SHIFT;
    val_2 = pop() >> FIXNUM_SHIFT;

    // Compare values and push result onto stack.
    if (val_2 == val_1) push(((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);
    else push(((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG);
}

// Move to alternate if test was satisfied.
void Interpreter::pop_jump_if_false(void) {
    uint64_t val;

    val = pop();

    // If false on top of stack, jump over consequent; else just mvoe past offset.
    if (((val & BOOL_MASK) == BOOL_TAG) && (val >> BOOL_SHIFT == 0)) pc += read_word();
    else pc += 1;
}

// Move past alternate if test was not satisfied.
void Interpreter::jump_over_else(void) {
    // Increment porgram counter by given amount.
    pc += read_word();
}

// Create a new environment for the binding and load the given number of values from the stack into the environment.
void Interpreter::let(void) {
    uint64_t num_bindings;
    int i;

    // Get number of bindings to load.
    num_bindings = read_word();

    // Create environment for given number of bindings.
    env.push_back(std::vector<uint64_t>(num_bindings));

    // Place values from stack into environment.
    for (i = 0; i < num_bindings; i++)
        env.back()[num_bindings - i - 1] = pop();

}

// Get a value from the environment onto stack.
void Interpreter::get_from_env(void) {
    // Push value from given index of environment onto stack.
    push(env.back()[read_word()]);
}

// Clean up binding's environment.
void Interpreter::end_let(void) {
    // Remove environment at the back of environment vector.
    env.pop_back();
}

// Create cons cell.
void Interpreter::create_cons(void) {
    // Pop values off stack and place onto heap.
    heap.push_back(pop());
    heap.push_back(pop());

    // Place cons cell's heap location onto stack.
    push(((heap_ptr << PAIR_SHIFT) & ~PAIR_MASK) | PAIR_TAG);

    // Increment heap pointer.
    heap_ptr += 2;
}

// Place first value in corresponding cons cell onto stack.
void Interpreter::car(void) {
    uint64_t cons, heap_ind;

    // Read value of corresponding cons cell from stack.
    cons = pop();

    // Extract heap location.
    heap_ind = cons >> PAIR_SHIFT;

    // Push car value onto stack.
    push(heap[heap_ind]);
}

// Place second value in corresponding cons cell onto stack.
void Interpreter::cdr(void) {
    uint64_t cons, heap_ind;

    // Read value of corresponding cons cell from stack.
    cons = pop();

    // Extract heap location.
    heap_ind = cons >> PAIR_SHIFT;

    // Push car value onto stack.
    push(heap[heap_ind + 1]);
}

// Place string contents onto heap and address of string onto stack.
void Interpreter::create_str(void) {
    uint64_t len, i;

    // Get string length.
    len = read_word();

    // Place length onto heap.
    heap.push_back(len);

    // Place characters onto heap.
    for (i = 0; i < len; i++) heap.push_back(pop() >> CHAR_SHIFT);

    // Place location of string in heap onto stack.
    push(((heap_ptr << STR_SHIFT) & ~STR_MASK) | STR_TAG);

    // Advance heap ppinter.
    heap_ptr += (len + 1);
}

// Place character at given location on top of stack.
void Interpreter::str_ref(void) {
    uint64_t loc, str_loc, val, len;

    // Get location off the top of the stack.
    loc = pop() >> FIXNUM_SHIFT;

    // Get string location off the stack.
    str_loc = pop() >> STR_SHIFT;

    // Get length of string.
    len = heap[str_loc];

    // Ensure location is within string.
    if (loc >= len) throw std::runtime_error("Invalid index.\n");

    // Set character at location and place onto stack.
    val = heap[str_loc + len - loc];

    push(((val << CHAR_SHIFT) & ~CHAR_MASK) | CHAR_TAG);
}

// Set character at given location to given value and place string location on top of stack.
void Interpreter::str_set(void) {
    uint64_t loc, str_loc, val, len;

    // Get character value from stack.
    val = pop() >> CHAR_SHIFT;

    // Get string index from stack.
    loc = pop() >> FIXNUM_SHIFT;

    // Get string's heap index from stack.
    str_loc = pop() >> STR_SHIFT;

    // Get length of string.
    len = heap[str_loc];

    // Ensure location is within string.
    if (loc >= len) throw std::runtime_error("Invalid index.\n");

    // Set character at location and place onto stack.
    heap[str_loc + len - loc] = val;

    // Place string's heap value back onto stack.
    push(((str_loc << STR_SHIFT) & ~STR_MASK) | STR_TAG);
}

// Create new string which is a single string appended to another.
void Interpreter::str_append(void) {
    uint64_t str_loc_1, str_loc_2, i, tot_len, len_1, len_2;

    // Pull strings' heap locations off of stack.
    str_loc_2 = pop() >> STR_SHIFT;
    str_loc_1 = pop() >> STR_SHIFT;

    // Get lengths of each string.
    len_1 = heap[str_loc_1];
    len_2 = heap[str_loc_2];

    // Find length of new string.
    tot_len = len_1 + len_2;

    // Place total length onto heap.
    heap.push_back(tot_len);

    // Place characters into string.
    for (i = 1; i <= heap[str_loc_2]; i++) heap.push_back(heap[str_loc_2 + i]);
    for (i = 1; i <= heap[str_loc_1]; i++) heap.push_back(heap[str_loc_1 + i]);

    // Place new string's heap value back onto stack.
    push(((heap_ptr << STR_SHIFT) & ~STR_MASK) | STR_TAG);

    // Advance heap ppinter.
    heap_ptr += (tot_len + 1);
}

// Place vector contents onto heap and address of vector onto stack.
void Interpreter::create_vec(void) {
    uint64_t len, i;

    // Get number of items.
    len = read_word();

    // Place number of items onto heap.
    heap.push_back(len);

    // Place items onto heap.
    for (i = 0; i < len; i++) heap.push_back(pop());

    // Place location of vector in heap onto stack.
    push(((heap_ptr << VEC_SHIFT) & ~VEC_MASK) | VEC_TAG);

    // Advance heap ppinter.
    heap_ptr += (len + 1);
}

// Place item at given location on top of stack.
void Interpreter::vec_ref(void) {
    uint64_t loc, vec_loc, val, len;

    // Get location off the top of the stack.
    loc = pop() >> FIXNUM_SHIFT;

    // Get vector location off the stack.
    vec_loc = pop() >> VEC_SHIFT;

    // Get length of vector.
    len = heap[vec_loc];

    // Ensure location is within vector.
    if (loc >= len) throw std::runtime_error("Invalid index.\n");

    // Set item at location and place onto stack.
    val = heap[vec_loc + len - loc];

    push(val);
}

// Set item at given location to given index and place vector location on top of stack.
void Interpreter::vec_set(void) {
    uint64_t loc, vec_loc, val, len;

    // Get item from stack.
    val = pop();

    // Get vector index from stack.
    loc = pop() >> FIXNUM_SHIFT;

    // Get vector's heap index from stack.
    vec_loc = pop() >> VEC_SHIFT;

    // Get length of vector.
    len = heap[vec_loc];

    // Ensure location is within vector.
    if (loc >= len) throw std::runtime_error("Invalid index.\n");

    // Set character at location and place onto stack.
    heap[vec_loc + len - loc] = val;

    // Place vector's heap value back onto stack.
    push(((vec_loc << VEC_SHIFT) & ~VEC_MASK) | VEC_TAG);
}

// Create new vector which is a single vector appended to another.
void Interpreter::vec_append(void) {
    uint64_t vec_loc_1, vec_loc_2, i, tot_len, len_1, len_2;

    // Pull vectors' heap locations off of stack.
    vec_loc_2 = pop() >> VEC_SHIFT;
    vec_loc_1 = pop() >> VEC_SHIFT;

    // Get lengths of each vector.
    len_1 = heap[vec_loc_1];
    len_2 = heap[vec_loc_2];

    // Find length of new vector.
    tot_len = len_1 + len_2;

    // Place total length onto heap.
    heap.push_back(tot_len);

    // Place characters into vector.
    for (i = 1; i <= heap[vec_loc_2]; i++) heap.push_back(heap[vec_loc_2 + i]);
    for (i = 1; i <= heap[vec_loc_1]; i++) heap.push_back(heap[vec_loc_1 + i]);

    // Place new vector's heap value back onto stack.
    push(((heap_ptr << VEC_SHIFT) & ~VEC_MASK) | VEC_TAG);

    // Advance heap ppinter.
    heap_ptr += (tot_len + 1);
}

