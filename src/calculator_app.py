import tkinter as tk
from tkinter import ttk


class Calculator:
    """A simple desktop calculator application."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Current calculation
        self.current_input = ""
        self.result = 0
        
        # Create UI
        self.create_widgets()
    
    def create_widgets(self):
        """Create calculator UI components."""
        # Display
        self.display = tk.Entry(
            self.root,
            font=("Arial", 24),
            justify="right",
            bd=10
        )
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.display.insert(0, "0")
        
        # Button layout
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('CE', 5, 1), ('←', 5, 2), ('√', 5, 3),
        ]
        
        # Create buttons
        for (text, row, col) in buttons:
            btn = tk.Button(
                self.root,
                text=text,
                font=("Arial", 18),
                width=5,
                height=2,
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
    
    def on_button_click(self, char):
        """Handle button click events."""
        if char == '=':
            self.calculate()
        elif char == 'C':
            self.clear()
        elif char == 'CE':
            self.clear_entry()
        elif char == '←':
            self.backspace()
        elif char == '√':
            self.square_root()
        else:
            self.append_char(char)
    
    def append_char(self, char):
        """Add character to current input."""
        if self.current_input == "0" or self.current_input == "Error":
            self.current_input = ""
        
        self.current_input += char
        self.update_display(self.current_input)
    
    def calculate(self):
        """Evaluate the current expression."""
        try:
            # Evaluate the expression
            result = eval(self.current_input)
            self.result = result
            self.update_display(str(result))
            self.current_input = str(result)
        except ZeroDivisionError:
            self.update_display("Error: Division by zero")
            self.current_input = "Error"
        except Exception as e:
            self.update_display("Error")
            self.current_input = "Error"
    
    def clear(self):
        """Clear all input."""
        self.current_input = ""
        self.result = 0
        self.update_display("0")
    
    def clear_entry(self):
        """Clear current entry."""
        self.current_input = ""
        self.update_display("0")
    
    def backspace(self):
        """Remove last character."""
        if self.current_input:
            self.current_input = self.current_input[:-1]
            self.update_display(self.current_input if self.current_input else "0")
    
    def square_root(self):
        """Calculate square root of current number."""
        try:
            value = float(self.current_input) if self.current_input else 0
            if value < 0:
                self.update_display("Error: Negative number")
                self.current_input = "Error"
            else:
                result = value ** 0.5
                self.result = result
                self.update_display(str(result))
                self.current_input = str(result)
        except Exception:
            self.update_display("Error")
            self.current_input = "Error"
    
    def update_display(self, text):
        """Update the display with new text."""
        self.display.delete(0, tk.END)
        self.display.insert(0, text)
    
    def get_display_text(self):
        """Get current display text."""
        return self.display.get()


def main():
    """Run the calculator application."""
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
