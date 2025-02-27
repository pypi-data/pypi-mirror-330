import sys
from tppc.tppc import TPPCInterpreter  # Ensure this import matches your structure

def run():
    """Main entry point for the tppc CLI."""
    if len(sys.argv) < 2:
        print("Usage: tppc <filename.tpp>")
        sys.exit(1)
    
    filename = sys.argv[1]
    interpreter = TPPCInterpreter()
    interpreter.run(filename)

if __name__ == "__main__":
    run()
