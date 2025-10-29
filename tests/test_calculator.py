import pytest
import tkinter as tk
from src.calculator_app import Calculator


@pytest.fixture
def calculator():
    """Create a calculator instance for testing."""
    root = tk.Tk()
    calc = Calculator(root)
    yield calc
    root.destroy()


class TestBasicOperations:
    """Test basic arithmetic operations."""
    
    @pytest.mark.ui
    def test_addition(self, calculator):
        """Test calculator can add two numbers."""
        calculator.append_char('5')
        calculator.append_char('+')
        calculator.append_char('3')
        calculator.calculate()
        
        assert calculator.get_display_text() == '8'
        assert calculator.result == 8
    
    @pytest.mark.ui
    def test_subtraction(self, calculator):
        """Test calculator can subtract numbers."""
        calculator.append_char('1')
        calculator.append_char('0')
        calculator.append_char('-')
        calculator.append_char('4')
        calculator.calculate()
        
        assert calculator.get_display_text() == '6'
        assert calculator.result == 6
    
    @pytest.mark.ui
    def test_multiplication(self, calculator):
        """Test calculator can multiply numbers."""
        calculator.append_char('6')
        calculator.append_char('*')
        calculator.append_char('7')
        calculator.calculate()
        
        assert calculator.get_display_text() == '42'
        assert calculator.result == 42
    
    @pytest.mark.ui
    def test_division(self, calculator):
        """Test calculator can divide numbers."""
        calculator.append_char('2')
        calculator.append_char('0')
        calculator.append_char('/')
        calculator.append_char('4')
        calculator.calculate()
        
        assert calculator.get_display_text() == '5.0'
        assert calculator.result == 5.0
    
    @pytest.mark.ui
    @pytest.mark.error_handling
    def test_division_by_zero(self, calculator):
        """Test calculator handles division by zero correctly."""
        calculator.append_char('1')
        calculator.append_char('0')
        calculator.append_char('/')
        calculator.append_char('0')
        calculator.calculate()
        
        display_text = calculator.get_display_text()
        assert "Error" in display_text or "Division by zero" in display_text


class TestAdvancedOperations:
    """Test advanced calculator features."""
    
    @pytest.mark.ui
    def test_square_root(self, calculator):
        """Test square root calculation."""
        calculator.current_input = '16'
        calculator.update_display('16')
        calculator.square_root()
        
        assert calculator.get_display_text() == '4.0'
        assert calculator.result == 4.0
    
    @pytest.mark.ui
    @pytest.mark.error_handling
    def test_square_root_negative(self, calculator):
        """Test square root of negative number shows error."""
        calculator.current_input = '-9'
        calculator.update_display('-9')
        calculator.square_root()
        
        display_text = calculator.get_display_text()
        assert "Error" in display_text
    
    @pytest.mark.ui
    def test_decimal_operations(self, calculator):
        """Test calculator works with decimal numbers."""
        calculator.append_char('3')
        calculator.append_char('.')
        calculator.append_char('5')
        calculator.append_char('+')
        calculator.append_char('2')
        calculator.append_char('.')
        calculator.append_char('5')
        calculator.calculate()
        
        assert float(calculator.get_display_text()) == 6.0


class TestUIFunctions:
    """Test UI control functions."""
    
    @pytest.mark.ui
    def test_clear_function(self, calculator):
        """Test clear button resets calculator."""
        calculator.append_char('1')
        calculator.append_char('2')
        calculator.append_char('3')
        calculator.clear()
        
        assert calculator.get_display_text() == '0'
        assert calculator.current_input == ''
    
    @pytest.mark.ui
    def test_clear_entry(self, calculator):
        """Test clear entry removes current input."""
        calculator.append_char('4')
        calculator.append_char('5')
        calculator.append_char('6')
        calculator.clear_entry()
        
        assert calculator.get_display_text() == '0'
        assert calculator.current_input == ''
    
    @pytest.mark.ui
    def test_backspace(self, calculator):
        """Test backspace removes last character."""
        calculator.append_char('1')
        calculator.append_char('2')
        calculator.append_char('3')
        calculator.backspace()
        
        assert calculator.current_input == '12'
        assert calculator.get_display_text() == '12'
    
    @pytest.mark.ui
    def test_multiple_operations(self, calculator):
        """Test chaining multiple operations."""
        calculator.append_char('5')
        calculator.append_char('+')
        calculator.append_char('3')
        calculator.calculate()
        
        # Result is 8, now multiply by 2
        calculator.append_char('*')
        calculator.append_char('2')
        calculator.calculate()
        
        assert calculator.get_display_text() == '16'


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    @pytest.mark.ui
    @pytest.mark.slow
    def test_very_large_numbers(self, calculator):
        """Test calculator handles large numbers."""
        calculator.current_input = '999999999'
        calculator.append_char('+')
        calculator.append_char('1')
        calculator.calculate()
        
        assert calculator.result == 1000000000
    
    @pytest.mark.ui
    def test_zero_operations(self, calculator):
        """Test operations with zero."""
        calculator.append_char('0')
        calculator.append_char('+')
        calculator.append_char('0')
        calculator.calculate()
        
        assert calculator.result == 0
    
    @pytest.mark.ui
    @pytest.mark.error_handling
    def test_invalid_expression(self, calculator):
        """Test calculator handles invalid expressions."""
        calculator.current_input = '5++'
        calculator.calculate()
        
        display_text = calculator.get_display_text()
        assert "Error" in display_text
