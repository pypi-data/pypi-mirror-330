import os
import sys
from .debugger import Debugger

# Global instance to track debugged files
_debugger = None

def debug_and_run(api_key=None):
    """
    Decorator to debug the current file before running the function.
    """
    if api_key is None:
        # Try to get the API key from the environment
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key is None:
            raise ValueError(
                "Please provide a Gemini API key. "
                "You can pass it as an argument or set the GEMINI_API_KEY environment variable."
            )

    global _debugger
    if _debugger is None:
        _debugger = Debugger(api_key)

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                # Step 1: Debug the current file
                current_file = sys.argv[0]  # Get the path of the current script
                _debugger.debug_file(current_file)

                # Step 2: Execute the function
                return func(*args, **kwargs)
            except Exception as e:
                print(f"An error occurred: {e}")
        return wrapper
    return decorator