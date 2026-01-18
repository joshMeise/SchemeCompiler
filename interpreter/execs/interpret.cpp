/*
 * interpret.cpp - 
 *
 * Josh Meise
 * 01-17-2026
 * Description: 
 *
 */

#include <interpreter.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <cstdint>

int main(int argc, char** argv) {
    std::ifstream ifile;
    std::istream* input;
    std::vector<uint8_t> bytes;
    char c;
    Interpreter interpreter;

    // Check arguments.
    if (argc != 1 && argc != 2) {
        std::cout << "usage: ./interpret [infile.bc]\n";
        return 1;
    }

    // Open file and set input to file else set input to byte stdin if no file provided.
    if (argc == 2) {
        ifile.open(argv[1], std::ios::binary);

        if (!ifile.is_open()) {
            std::cerr << "Failed to open file.\n";
            return 1;
        }
        
        input = &ifile;
    } else
        input = &std::cin;

    // Read bytes into vector.
    while ((c = input->get()) != EOF)
        bytes.push_back(static_cast<uint8_t>(c));

    ifile.close();

    // Construct interpreter.
    interpreter = Interpreter(bytes);

    interpreter.interpret();




    return 0;
}
