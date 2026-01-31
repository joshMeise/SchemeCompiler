# parser.py - 
#
# Josh Meise
# 01-08-2026
# Description: 
#
# Citations:
# - Google's AI tool for the suggestion of the use of regex and then Python's regex documentation for the implementation.

from typing import Union
import re

WSP = [' ', '\n', '\t', '\r']
ILLEGAL_CHARS = ['`']

class Parser:
    """
    Class to handle parsing of Scheme program input text.

    Checks syntax of Scheme programs.
    Produces a list of tokens for use by compiler.

    Attributes:
        source (str): Scheme source program to be parsed.
        pos (int): Current position of parser in Scheme source program.
        length (int): Length of Scheme program.
    """

    def __init__(self, source: str):
        """
        Initializes the Parser object.

        Args:
            source (str): Scheme source code to be parsed.
        """
        self.source = source
        self.pos = 0
        self.length = len(source)

    def parse(self):
        """
        Parses input strings of various objects.

        Returns:
            Atomic element or abstract syntax tree in the form of a Python list.

        Raises:
            EOFError: Unexpectedly reaches end of file.
            NotImplementedError: Non-integer value being parsed.
        """
        self.skip_whitespace()
        match self.peek():
            case '':
                raise EOFError("unexpected end of input.")
            case c if c.isdigit():
                val = self.parse_number()
            case '#':
                val = self.parse_boolean_or_char()
            case '(':
                val = self.parse_expression()
            case c:
                raise NotImplementedError(f"found {c}.")

        # Ensure that whitespace follows.
        self.skip_whitespace()

        # If end of input expression is of invalid format.
        if self.peek() != '':
            raise TypeError("Invalid type.")

        return val

    def parse_expression(self) -> list:
        """
        Parses expression from string.

        Returns:
            list: AST containing expressiont aht have been parsed.

        Raises:
            TypeError: Invalid expression.
            NotImplementedError: Parse function for type not yet implemented.
        """
        # Consume opening parens.
        self.pos += 1

        # Skip whitespace.
        self.skip_whitespace()

        ast = []

        match self.peek():
            case ')':
                return self.parse_empty_list()
            # Contains another expression.
            case '(':
                ast.append(self.parse_expression())
            case _:
                match self.peek_word():
                    case "add1":
                        return self.parse_unary_int_arg("add1")
                    case "sub1":
                        return self.parse_unary_int_arg("sub1")
                    case "integer->char":
                        return self.parse_unary_int_arg("integer->char")
                    case "char->integer":
                        return self.parse_unary_char_arg("char->integer")
                    case "null?":
                        return self.parse_unary_any_arg("null?")
                    case "zero?":
                        return self.parse_unary_int_arg("zero?")
                    case "not":
                        return self.parse_unary_any_arg("not")
                    case "integer?":
                        return self.parse_unary_any_arg("integer?")
                    case "boolean?":
                        return self.parse_unary_any_arg("boolean?")
                    case "+":
                        return self.parse_binary_int_args("+")
                    case "*":
                        return self.parse_binary_int_args("*")
                    case "-":
                        return self.parse_binary_int_args("-")
                    case "<":
                        return self.parse_binary_int_args("<")
                    case ">":
                        return self.parse_binary_int_args(">")
                    case "<=":
                        return self.parse_binary_int_args("<=")
                    case ">=":
                        return self.parse_binary_int_args(">=")
                    case "=":
                        return self.parse_binary_int_args("=")
                    case "let":
                        return self.parse_let()
                    case "if":
                        return self.parse_if()
                    case w:
                        raise NotImplementedError(f"Expression {w} not implemented.")

        return ast

    def peek(self) -> str:
        """
        Get character at the front of input string.

        Returns:
            str: Character at front of input string.
        """
        # Return no character if end of input has been reached.
        if self.pos == self.length:
            return ''

        # Return front character in input string.
        c = self.source[self.pos]
        return c

    def peek_word(self) -> str:
        """
        Get word at the front of input string.

        Returns:
            str: Word at front of input string.
        """
        # Return no word if end of input has been reached.
        if self.pos == self.length:
            return ''

        # Return front word in input string.
        w = self.source[self.pos::].split(' ')[0]
        return w
    
    def skip_whitespace(self):
        """
        Removes leading whitespace in source code.
        """
        while self.peek() in WSP:
            self.pos += 1

    def parse_empty_list(self) -> list:
        """
        Parses empty list.

        Returns:
            list: Empty list.

        Raises:
            TypeError: Invalid empty list.
        """
        # Consume closing parens.
        self.pos += 1
        
        return []

    def parse_number(self) -> int:
        """
        Parses positive integer values from digit string.

        Returns:
            int: Integer value of string that has been parsed.

        Raises:
            TypeError: Non-digit found in integer string.
        """
        # Build ingeter from digit string.
        num = 0
        while self.peek().isdigit():
            num *= 10
            num += int(self.source[self.pos])
            self.pos += 1

        # Consume whitespace.
        self.skip_whitespace()

        return num

    def parse_boolean_or_char(self) -> Union[str, bool]:
        """
        Parses boolean or character value from string.

        Returns:
            bool: Boolean value of string that has been parsed.
            str: Character value that was parsed.

        Raises:
            TypeError: Non-boolean or non-character found in string starting with #.
        """
        # Skip over '#'.
        self.pos += 1
        
        if self.peek() == 't' or self.peek() == 'T' or self.peek() == 'f' or self.peek() == 'F':
            return self.parse_boolean()
        elif self.peek() == '\\':
            return self.parse_char()
        else:
            raise TypeError("Invalid boolean or character type.")

    def parse_boolean(self) -> bool:
        """
        Parses boolean value from string.

        Returns:
            bool: Boolean value that has been parsed.

        Raises:
            TypeError: Non-boolean value found in string.
        """
        if self.peek() == 't' or self.peek() == 'T':
            ret_val = True
        elif self.peek() == 'f' or self.peek() == 'F':
            ret_val = False
        else:
            raise TypeError("Invalid boolean type.")
        
        self.pos += 1

        return ret_val

    def parse_char(self) -> str:
        """
        Parses character value from string.

        Returns:
            str: Character value that has been parsed.

        Raises:
            TypeError: Non-character value or illegal character value found in string.
        """
        # Skip over backslash.
        self.pos += 1

        if self.peek() in ILLEGAL_CHARS:
            raise TypeError("Illegal character.")
    
        ret_val = self.peek()
        
        self.pos += 1

        return "#\\" + ret_val

    def parse_binding(self) -> str:
        """
        Parses binding value from string.

        Returns:
            str: Binding value that has been parsed.

        Raises:
            TypeError: Non-binding value or illegal binding value found in string.
        """
        # Skip over 'b'.
        self.pos += 1

        # Build ingeter from digit string.
        num = 0
        while self.peek().isdigit():
            num *= 10
            num += int(self.source[self.pos])
            self.pos += 1
        
        # Ensure that a space or closing parens follows.
        if self.peek() != ' ' and self.peek() != ')':
            raise TypeError("Invalid binding name.")

        return "b" + str(num)

    def parse_unary_int_arg(self, exp_name: str) -> list:
        """
        Parses unary exression (exp_name e) with integer argument from string.

        Returns:
            list: [exp_name, e].

        Raises:
            TypeError: Invalid expression.
        """
        exp = []

        # Skip over exp_name.
        self.pos += len(exp_name)

        exp.append(exp_name)

        # Consume whitespace.
        self.skip_whitespace()

        # Ensure that number follows.
        match self.peek():
            # Parse number and add to expression.
            case c if c.isdigit():
                num = self.parse_number()
                exp.append(num)
            # Append nested expression to list of expression to list of expressions.
            case '(':
                exp.append(self.parse_expression())
            case 'b':
                exp.append(self.parse_binding())
            case _:
                raise TypeError(f"Invalid argument to {exp_name} expression.")
        
        # Consume whitespace.
        self.skip_whitespace()

        # If not closing parens, the expresion is invalid.
        if self.peek() != ')':
            raise TypeError(f"Invalid argument to {exp_name} expression.")

        # Skip closing parens.
        if self.peek() != '' and self.peek() == ')':
            self.pos += 1
        else:
            raise TypeError(f"{exp_name} expression missing closing parens.")

        return exp

    def parse_unary_char_arg(self, exp_name: str) -> list:
        """
        Parses unary exression (exp_name e) with character argument from string.

        Returns:
            list: [exp_name, e].

        Raises:
            TypeError: Invalid expression.
        """
        exp = []

        # Skip over exp_name.
        self.pos += len(exp_name)

        exp.append(exp_name)

        # Consume whitespace.
        self.skip_whitespace()

        # Ensure that number follows.
        match self.peek():
            # Parse character or boolean and add to expression.
            case '#':
                # Skip over '#'.
                self.pos += 1
                arg = self.parse_char()
                exp.append(arg)
            # Append nested expression to list of expression to list of expressions.
            case '(':
                exp.append(self.parse_expression())
            case 'b':
                exp.append(self.parse_binding())
            case _:
                raise TypeError(f"Invalid argument to {exp_name} expression.")
        
        # Consume whitespace.
        self.skip_whitespace()

        # If not closing parens, the expresion is invalid.
        if self.peek() != ')':
            raise TypeError(f"Invalid argument to {exp_name} expression.")

        # Skip closing parens.
        if self.peek() != '' and self.peek() == ')':
            self.pos += 1
        else:
            raise TypeError(f"{exp_name} expression missing closing parens.")

        return exp

    def parse_unary_any_arg(self, exp_name: str) -> list:
        """
        Parses unary exression (exp_name e) with any type of argument from string.

        Returns:
            list: [exp_name, e].

        Raises:
            TypeError: Invalid expression.
        """
        exp = []

        # Skip over exp_name.
        self.pos += len(exp_name)

        exp.append(exp_name)

        # Consume whitespace.
        self.skip_whitespace()

        # Ensure that number follows.
        match self.peek():
            # Parse number and add to expression.
            case c if c.isdigit():
                num = self.parse_number()
                exp.append(num)
            # Parse character or boolean and add to expression.
            case '#':
                arg = self.parse_boolean_or_char()
                exp.append(arg)
            # Append nested expression to list of expression to list of expressions.
            case '(':
                exp.append(self.parse_expression())
            case 'b':
                exp.append(self.parse_binding())
            case _:
                raise TypeError(f"Invalid argument to {exp_name} expression.")
        
        # Consume whitespace.
        self.skip_whitespace()

        # If not closing parens, the expresion is invalid.
        if self.peek() != ')':
            raise TypeError(f"Invalid argument to {exp_name} expression.")

        # Skip closing parens.
        if self.peek() != '' and self.peek() == ')':
            self.pos += 1
        else:
            raise TypeError(f"{exp_name} expression missing closing parens.")

        return exp

    def parse_binary_int_args(self, exp_name: str) -> list:
        """
        Parses binary expression (exp_name e1 e2 ...) with integer arguments from string.

        Returns:
            list: [exp_name, e1, e2, ...].

        Raises:
            TypeError: Invalid expression.
        """
        exp = []

        # Skip over exp_name.
        self.pos += len(exp_name)

        exp.append(exp_name)

        # Consume whitespace.
        self.skip_whitespace()

        # Parse two numbers that follow exp_name.
        match self.peek():
            # Parse number and add to expression.
            case c if c.isdigit():
                num = self.parse_number()
                exp.append(num)
            # Append nested expression to list of expression to list of expressions.
            case '(':
                exp.append(self.parse_expression())
            case 'b':
                exp.append(self.parse_binding())
            case _:
                raise TypeError(f"Invalid argument to {exp_name} expression.")

        # Consume whitespace.
        self.skip_whitespace()

        match self.peek():
            # Parse number and add to expression.
            case c if c.isdigit():
                num = self.parse_number()
                exp.append(num)
            # Append nested expression to list of expression to list of expressions.
            case '(':
                exp.append(self.parse_expression())
            case 'b':
                exp.append(self.parse_binding())
            case _:
                raise TypeError(f"Invalid argument to {exp_name} expression.")

        # Consume whitespace.
        self.skip_whitespace()

        # Skip closing parens.
        if self.peek() != '' and self.peek() == ')':
            self.pos += 1
        else:
            raise TypeError(f"{exp_name} expression missing closing parens.")

        return exp

    def parse_let_and_if_helper(self) -> list:
        """
        Parses test, consequent and alternate of if expressions.

        Returns:
            list: AST of expression that has been parsed.

        Raises:
            NotImplementedError: Invalid leading character is found.
        """
        # Consume whitespace.
        self.skip_whitespace()
    
        # Parse expression.
        match self.peek():
            case '':
                raise EOFError("unexpected end of input.")
            case c if c.isdigit():
                val = self.parse_number()
            case '#':
                val = self.parse_boolean_or_char()
            case '(':
                val = self.parse_expression()
            case 'b':
                val = self.parse_binding()
            case c:
                raise NotImplementedError(f"found {c}.")

        # Comsume any trailing whitespace.
        self.skip_whitespace()

        return val

    def parse_if(self) -> list:
        """
        Parses conditional statement in the form of (if test conseq altern).

        Returns:
            list: ["if", test, conseq, altern]
        """
        exp = []

        # Add "if" to expression and skip over it.
        exp.append("if")
        self.pos += len("if")

        # Parse test, consequent and alternate, respectively.
        exp.append(self.parse_let_and_if_helper())
        exp.append(self.parse_let_and_if_helper())
        exp.append(self.parse_let_and_if_helper())

        # Skip over closing parens.
        if self.peek() != ')':
            raise TypeError("Invalid if format.")
        else:
            self.pos += 1

        return exp

    def parse_let(self) -> list:
        """
        Parses a let binding in the form of (let ((a e1) (b e2) ...) en).

        Returns:
            list: [e1, e2, ..., ["let", en(with offsets)]]
        """
        exp = []
        env = []
        bindings = []

        # Skip over let.
        self.pos += len("let")

        # Consume whitespace before bindings start.
        self.skip_whitespace()

        # Skip over parens tht opens bindings.
        if self.peek() != '(':
            raise TypeError("Invalid let binding.")
        else:
            self.pos += 1

        # Skip whitespace before opening parens of first binding.
        self.skip_whitespace()

        # Parse all bindings.
        while self.peek() != ')':
            # Consume opening parens.
            if self.peek() != '(':
                raise TypeError("Invalid let binding.")
            else:
                self.pos += 1

            # Skip whitespace before binding name.
            self.skip_whitespace()

            # Add binding name to list of bindings.
            name = self.peek_word()
            if name in bindings:
                raise TypeError("Invalid let binding.")
            bindings.append(name)
            self.pos += len(name)

            # Get AST for expression.
            exp.append(self.parse_let_and_if_helper())

            # Skip over closing parens.
            if self.peek() != ')':
                raise TypeError("Invalid let binding.")
            else:
                self.pos += 1

            # Consume any whitespace prior to any potential binding closing.
            self.skip_whitespace()

        # Skip over closing parens of bindings.
        if self.peek() != ')':
            raise TypeError("Invalid let binding.")
        else:
            self.pos += 1

        # Replace any references to bindings with the binding code.
        for i, binding_name in enumerate(bindings):
            # Define a regex pattern for the old binding name.
            # r'\b' is used to exclude consideration of parens as part of a word.
            regex = r'\b' + binding_name + r'\b'
            
            # New binding name.
            binding = f"b{i}"
            
            # Replace variable name with binding name.
            # Only replace in let's body otherwise it throws self.pos off if replacements occur prior to position of self.pos.
            self.source = self.source[0:self.pos] + re.sub(regex, binding, self.source[self.pos:])

        # Update the length of the string now that bindings have been added.
        self.length = len(self.source)

        # Add "let" to body portion.
        env.append("let")
    
        # Append number of bindings to env.
        env.append(len(bindings))

        # Parse body of let.
        env.append(self.parse_let_and_if_helper())

        # Skip whitespace prior to closing of let binding.
        self.skip_whitespace()

        # Consume final closing parens of let binding.
        if self.peek() != ')':
            raise TypeError("Invalid let binding.")
        else:
            self.pos += 1

        # Append body to espression.
        exp.append(env)

        return exp

def scheme_parse(source: str) -> list:
    """
    Wrapper around parsing function for Scheme programs.

    Args:
        source (str): Scheme source program.

    Returns:
        list: Abstract syntax tree in the form of a Python list.
    """
    return Parser(source).parse()

if __name__ == "__main__":
    print(scheme_parse("(let ((a 5) (b (+ 4 5)))  (+ (+ a b) b))"))
