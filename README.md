# SchemeCompiler

## Big things:
- scheme_parse() currently outputs a list but compile_function() takes just an atomic value. Fix this.

## Questions:
- How do we handle integer overflow? Do we wish for it to be blocked by the parser or do we wish for overflow to behave in the same way it does in C?
- Do we want to catch errors on arguments in parser?
    - Thinking specifically of integer->char for now? What if int is too large? My Scheme implementation just returns the hex value then.

## TODO:
- Integeration tests.
