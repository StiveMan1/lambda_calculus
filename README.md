# Lambda Calculus Compiler

This Python script serves as a compiler for a subset of lambda calculus expressions. Lambda calculus is a formal system
for expressing computations based on function abstraction and application using variable binding and substitution.

## Functionality

The script includes several functions to parse lambda calculus expressions from input, analyze variable scopes and
bindings, perform variable substitution, and print the resulting expression.

## Components

### 1. Tokenization (split_tokens):

* Splits the input string into tokens including lambda (λ), parentheses, dots (.), and identifiers.

### 2. Parsing Functions:

* `get_identifier(list, pos)`: Retrieves identifiers from the token list.
* `application_expr(list, pos)`: Parses application expressions.
* `function_expr(list, pos)`: Parses function expressions (λ abstraction).
* `scope_expr(list, pos)`: Parses scope expressions enclosed in parentheses.

### 3. Expression Analysis:

* `get_expr_low(list, pos)`: Determines the lowest precedence expression.
* `get_expr(list, pos)`: Retrieves the entire lambda calculus expression.

### 4. Variable Scoping and Substitution:

* `set_free(graph, list)`: Sets free variable counts within the expression graph.
* `re_set_free(graph, list, new_list)`: Updates free variable counts after substitution.
* `un_set_free(graph, list)`: Unsets free variables within the expression graph.
* `repalace_graph(graph, argFrom, argTo, list)`: Replaces occurrences of a variable with another expression.
* `find_graph(graph, list)`: Finds and replaces occurrences of a variable within the expression graph.

### 5. Output:

* `print_graph(graph)`: Converts the expression graph back into a readable string format.

## Usage

To compile a lambda calculus expression, provide the input directly to the `data` variable and execute the script. The
script will tokenize the input, parse it into an expression graph, analyze variable scopes, perform substitutions, and
print the resulting lambda calculus expression.

## Example:

```python
from copy import deepcopy as copy

data = input()  # Provide your lambda calculus expression here
list = split_tokens(data)
print(list)
graph = get_expr(list, 0)[1]
print(graph)
graph = set_free(graph, [])
print(print_graph(graph))
graph = find_graph(graph, [])
print(print_graph(graph))
```

## Notes

* This compiler assumes a subset of lambda calculus and may need extension for more complex expressions or additional
  features.
* Variable scoping and substitution are handled recursively through the expression graph structure.
* Ensure input adheres to lambda calculus syntax to avoid parsing errors.
  For detailed explanation and understanding of each function's role, refer to the inline comments within the script.