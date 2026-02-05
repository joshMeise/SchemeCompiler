/*
 * interpret.cpp - 
 *
 * Josh Meise
 * 01-17-2026
 * Description: 
 *
 */

#include <interpreter.h>
#include <utilities.h>
#include <vector>

int main(int argc, char** argv) {
    std::ifstream ifile;
    std::istream* input;
    std::ofstream ofile;
    std::ostream* output;
    std::vector<uint8_t> bytes;
    char c;
    Interpreter interpreter;
    uint64_t val;

    // Parse arguments and set input and output sources.
    if (parse_args(argc, argv, ifile, input, ofile, output) != 0) return 1;

    // Read bytes into vector.
    while ((c = input->get()) != EOF)
        bytes.push_back(static_cast<uint8_t>(c));

    // Construct interpreter.
    interpreter = Interpreter(bytes);

    // Interpret program.
    val = interpreter.interpret();

    // Print out return value.
    interpreter.print_val(val, output);
    *output << std::endl;

    // Clean up.
    if (ifile.is_open()) ifile.close();
    if (ofile.is_open()) ofile.close();

    return 0;
}
