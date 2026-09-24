- Trees over strings. Representing formulas as Formula objects
  instead of manipulating raw strings everywhere means every function
  (evaluate, is_formula, printing) is a short, uniform recursive
  function instead of ad-hoc string surgery.
- Generators for models. Since the number of models over *n* variables
  grows as 2ⁿ, all_models is implemented as a generator rather than
  building a full list up front, keeping memory usage reasonable even for
  formulas with several variables.
- **tabulate for display.** Rather than hand-rolling column alignment for
  the truth table, the project relies on the well-tested tabulate
  package, keeping main() focused on logic rather than string
  formatting.

## How to run it

pip install -r requirements.txt
python semantic.py

You will be prompted to enter a formula (for example (p&q)), and the
program will print a full truth table for every variable used in it.
