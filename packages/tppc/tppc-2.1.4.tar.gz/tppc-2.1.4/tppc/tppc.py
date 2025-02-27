import sys
import re

class TPPCInterpreter:
    def __init__(self):
        self.variables = {}  # Storage for variables
        self.functions = {}  # Storage for functions
    
    def parse(self, lines):
        """Parses the TPPC source code."""
        for line in lines:
            line = line.strip()
            
            if line.startswith("#") or line == "":
                continue  # Ignore comments and empty lines
            
            tokens = line.split()

            if tokens[0] == "print":
                self.handle_print(tokens)
            elif tokens[0] == "let":
                self.handle_variable_assignment(tokens)
            elif tokens[0] == "if":
                self.handle_if_statement(tokens)
            elif tokens[0] == "while":
                self.handle_while_loop(tokens)
            else:
                print(f"Syntax Error: Unknown command '{tokens[0]}'")
    
    def handle_print(self, tokens):
        """Handles print statements."""
        content = " ".join(tokens[1:])
        if content.startswith('"') and content.endswith('"'):
            print(content[1:-1])
        elif content in self.variables:
            print(self.variables[content])
        else:
            print(f"Error: Undefined variable '{content}'")
    
    def handle_variable_assignment(self, tokens):
        """Handles variable assignment: let x = 10"""
        if len(tokens) != 4 or tokens[2] != "=":
            print("Syntax Error: Invalid variable assignment")
            return
        var_name = tokens[1]
        value = tokens[3]
        if value.isdigit():
            self.variables[var_name] = int(value)
        elif value.replace(".", "", 1).isdigit():
            self.variables[var_name] = float(value)
        else:
            print(f"Error: Invalid value '{value}'")
    
    def handle_if_statement(self, tokens):
        """Handles simple if conditions"""
        if len(tokens) < 4:
            print("Syntax Error: Incomplete if statement")
            return
        
        condition_var = tokens[1]
        comparison_op = tokens[2]
        condition_value = tokens[3]

        if condition_var not in self.variables:
            print(f"Error: Undefined variable '{condition_var}'")
            return

        # Evaluate condition
        if self.evaluate_condition(condition_var, comparison_op, condition_value):
            print(" ".join(tokens[4:]))  # Execute inline statement
    
    def handle_while_loop(self, tokens):
        """Handles while loops"""
        print("While loops are not implemented yet.")
    
    def evaluate_condition(self, var, op, value):
        """Evaluates if conditions"""
        if var not in self.variables:
            return False

        try:
            var_value = self.variables[var]
            if value.isdigit():
                value = int(value)
            elif value.replace(".", "", 1).isdigit():
                value = float(value)

            if op == "==":
                return var_value == value
            elif op == "!=":
                return var_value != value
            elif op == "<":
                return var_value < value
            elif op == ">":
                return var_value > value
            elif op == "<=":
                return var_value <= value
            elif op == ">=":
                return var_value >= value
            else:
                print(f"Error: Unknown operator '{op}'")
                return False
        except:
            return False

    def run(self, filename):
        """Reads and executes a .tpp file"""
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
                self.parse(lines)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"Runtime Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: tppc.py <filename.tpp>")
    else:
        interpreter = TPPCInterpreter()
        interpreter.run(sys.argv[1])
