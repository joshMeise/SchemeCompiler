/*
 * utilities.h - 
 *
 * Josh Meise
 * 01-18-2026
 * Description: 
 *
 */

#pragma once
#include <iostream>
#include <fstream>
#include <cstdint>

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
int parse_args(int argc, char** argv, std::ifstream& ifile, std::istream*& input, std::ofstream& ofile, std::ostream*& output);

/*
 * Prints out value returned by interpreter.
 * Checks type of value and prints based on type.
 *
 * Args:
 * - val (uint64_t): tagged pointer returned by interpreter
 * - output (std::ostream*&): reference to pointer to output stream to which to print
 *
 */
void print_val(uint64_t val, std::ostream*& output);
