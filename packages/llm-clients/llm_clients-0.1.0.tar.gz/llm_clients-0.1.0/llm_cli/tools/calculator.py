"""
Calculator tool for evaluating expressions

A tool that supports:
1. Generating prompts to tell LLM to use <calculator> tags for arithmetic
2. Executing calculations inside <calculator> tags

The calculator supports:
- Basic arithmetic: +, -, *, /, //, %, **
- Scientific notation: 1e6, 1.2e-3
- All math module constants and functions (math.*)
- Parentheses for grouping

Example LLM response format:
    The result of 2 + 3 * 4 is <calculator>2 + 3 * 4</calculator>
    Ten divided by three is <calculator>10 / 3</calculator>
"""
import ast
import logging
import math
import xml.etree.ElementTree as ET

from llm_cli.tools import Tool
from llm_cli.tools.decorators import register_tool

logger = logging.getLogger(__name__)

@register_tool
class Calculator(Tool):
    """Tool for evaluating mathematical expressions"""
    
    def __init__(self):
        """Initialize tool and register XML tag handlers"""
        super().__init__()
        self.register_xml_tag('calculator', self._handle_calculator)
        self.verbose = False  # Initialize verbose flag
    
    @property
    def name(self) -> str:
        return "calculator"
        
    @property
    def description(self) -> str:
        return "Evaluates mathematical expressions using Python's math library"
        
    async def generate_prompt(self, input: str, **kwargs) -> str:
        """Generate a prompt instructing LLM to use calculator tags"""
        return (
            "You are a calculator tool that evaluates mathematical expressions using Python. "
            "You must wrap all expressions in <calculator> tags and use proper Python syntax.\n\n"
            "Important rules:\n"
            "1. All expressions are evaluated as Python code\n"
            "2. Math functions must be prefixed with 'math.' (e.g. use math.sin(), not sin())\n"
            "3. For angles in trigonometric functions, use math.radians() to convert degrees\n\n"
            "Examples:\n"
            "1. Basic arithmetic:\n"
            "   What is 2 + 3 * 4?\n"
            "   The result is <calculator>2 + 3 * 4</calculator>\n\n"
            "2. Using math functions (note the math. prefix):\n"
            "   Calculate sin(30°)\n"
            "   <calculator>math.sin(math.radians(30))</calculator>\n\n"
            "3. Complex calculations:\n"
            "   What is the square root of 16 plus log base 10 of 100?\n"
            "   <calculator>math.sqrt(16) + math.log10(100)</calculator>\n\n"
            "REMEMBER:\n"
            "- Always wrap expressions in <calculator> tags\n"
            "- Always use math. prefix for math functions (math.sin, math.cos, math.sqrt, etc.)\n\n"
            f"Now please help with this calculation: {input}"
        )
    
    async def execute(self, input: str, verbose: bool = False, **kwargs) -> str:
        """Execute the calculator tool"""
        self.verbose = verbose  # Set verbose flag from execute call
        return await super().execute(input, verbose=verbose, **kwargs)
    
    async def _handle_calculator(self, root: ET.Element) -> str:
        """Handle calculator XML tag"""
        try:
            # Get expression from tag content
            expr = root.text
            if not expr:
                raise ValueError("Empty expression")
            expr = expr.strip()
            if not expr:
                raise ValueError("Expression contains only whitespace")
                
            if self.verbose:
                logger.info(f"Evaluating expression: {expr}")
            
            # Parse and evaluate the expression safely with math module
            tree = ast.parse(expr, mode='eval')
            
            # Create safe environment with math module and basic functions
            safe_env = {
                # Math module for math.* functions
                'math': math,
                
                # Basic numeric functions
                'abs': abs,
                'float': float,
                'int': int,
                'pow': pow,
                'round': round,
            }
            
            result = eval(compile(tree, '<string>', 'eval'), {'__builtins__': {}}, safe_env)
            
            if self.verbose:
                logger.info(f"Result: {result}")
            
            # Format the result
            if isinstance(result, float):
                # Special handling for math constants
                if result == math.pi:
                    return str(math.pi)
                if result == math.e:
                    return str(math.e)
                
                # Round to 12 decimal places to avoid floating point artifacts
                result = round(result, 12)
                
                # Use scientific notation for very large/small numbers
                if abs(result) >= 1e6 or (result != 0 and abs(result) < 1e-4):
                    # Format with minimal precision and explicit + sign
                    formatted = f"{result:.6g}"  # Use general format with 6 sig figs
                    if 'e' in formatted:
                        base, exp = formatted.split('e')
                        if float(base) == int(float(base)):
                            base = str(int(float(base)))  # Remove .0 if integer
                        if not exp.startswith(('+', '-')):
                            exp = '+' + exp
                        return f"{base}e{exp}"
                    return formatted
                else:
                    # For regular floats, use full precision for constants like pi
                    # but format integers as .0
                    if result == int(result):
                        return f"{result:.1f}"
                    return f"{result:.12g}"  # Use 12 significant digits
            return str(result)
            
        except (ValueError, SyntaxError) as e:
            logger.error(f"Expression error: {e}")
            # Clean up syntax error message
            error = str(e)
            if "(<unknown>, line 1)" in error:
                error = error.replace(" (<unknown>, line 1)", "")
            # Remove any existing "Error: " prefix
            while error.startswith("Error: "):
                error = error[7:]
            return f"Error: {error}"
        except Exception as e:
            logger.error(f"Calculation error: {e}")
            error = str(e)
            # Remove any existing "Error: " prefix
            while error.startswith("Error: "):
                error = error[7:]
            return f"Error: {error}"