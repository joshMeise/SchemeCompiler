/*
 * utilities.cpp - 
 *
 * Josh Meise
 * 01-18-2026
 * Description: 
 *
 */

#include "utilities.h"

/*
 * Parses program arguments and sets input and output.
 * Defaults to setting input to stdin and output to stdout unless input/output file(s) specified as arguments to main().
 *
 * Args:
 * - argc (int): number of arguments to main()
 * - argv (char**): array of arguments to main()
 * - ifile (std::ifstream&): reference to input file pointer
 * - input (std::istream*&): reference to pointer to input stream, set to stdin by default
 * - ofile (std::ofstream&): reference to output file pointer
 * - output (std::ostream*&): reference to pointer to output stream, set to stdout by default
 *
 * Returns:
 * int: 0 for success, 1 for failure
 *
 */
int parse_args(int argc, char** argv, std::ifstream& ifile, std::istream*& input, std::ofstream& ofile, std::ostream*& output) {
    std::string arg;

    // Check arguments.
    if (argc != 1 && argc != 2 && argc != 3) {
        std::cout << "usage: ./interpret [infile.bc] [outfile.txt]\n";
        return 1;
    }

    // Open input and output files if provided.
    if (argc == 3) {
        ifile.open(argv[1], std::ios::binary);

        if (!ifile.is_open()) {
            std::cerr << "Failed to open file.\n";
            return 1;
        }
        
        input = &ifile;

        ofile.open(argv[2]);

        if (!ofile.is_open()) {
            std::cerr << "Failed to open file.\n";
            return 1;
        }

        output = &ofile;
    }
    // If no arguments are provided, use stdin and stdout.
    else if (argc == 1) {
        input = &std::cin;
        output = &std::cout;
    }
    // If two arguments are provided, determine if it was an input file or an output file.
    else if (argc == 2) {
        arg = std::string(argv[1]);

        // This is the case if an input file was provided.
        if (arg.length() >= 3 && arg.substr(arg.length() - 3) == ".bc") {
            ifile.open(argv[1], std::ios::binary);

            if (!ifile.is_open()) {
                std::cerr << "Failed to open file.\n";
                return 1;
            }

            input = &ifile;
            output = &std::cout;
        } 
        // THis is when an output file was provided.
        else if (arg.length() >= 4 && arg.substr(arg.length() - 4) == ".txt") {
            ofile.open(argv[1]);

            if (!ofile.is_open()) {
                std::cerr << "Failed to open file.\n";
                return 1;
            }

            input = &std::cin;
            output = &ofile;
        } 
        else {
            std::cout << "usage: ./interpret [infile.bc] [outfile.txt]\n";
            return 1;
        }
    }

    return 0;
}

/*
 * Prints out value returned by interpreter.
 * Checks type of value and prints based on type.
 *
 * Args:
 * - val (uint64_t): tagged pointer returned by interpreter
 * - output (std::ostream*&): reference to pointer to output stream to which to print
 *
 */
void print_val(uint64_t val, std::ostream*& output) {

    *output << "HI\n";
}
