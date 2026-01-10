# SchemeCompiler

## Questions:
- What do we expect scheme_parse() to return? Should it return the AST (list of lists) or just an atomic value?
- How do we handle integer overflow? Do we wish for it to be blocked by the parser or do we wish for overflow to behave in the same way it does in C?
