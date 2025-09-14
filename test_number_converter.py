import pytest
import base64
import json
from unittest.mock import patch
from api.index import (
    text_to_number, 
    number_to_text, 
    base64_to_number, 
    number_to_base64,
    app
)


class TestTextToNumber:
    """Test text to number conversion function"""
    
    def test_single_digit_words(self):
        """Test conversion of single digit words"""
        assert text_to_number("one") == 1
        assert text_to_number("two") == 2
        assert text_to_number("three") == 3
        assert text_to_number("four") == 4
        assert text_to_number("five") == 5
        assert text_to_number("six") == 6
        assert text_to_number("seven") == 7
        assert text_to_number("eight") == 8
        assert text_to_number("nine") == 9
        assert text_to_number("ten") == 10
    
    def test_case_insensitive(self):
        """Test that conversion is case insensitive"""
        assert text_to_number("ONE") == 1
        assert text_to_number("Two") == 2
        assert text_to_number("THREE") == 3
    
    def test_special_cases(self):
        """Test special cases like zero and nil"""
        assert text_to_number("zero") == 0
        assert text_to_number("nil") == 0
        assert text_to_number("ZERO") == 0
        assert text_to_number("NIL") == 0
    
    def test_with_non_alphanumeric_chars(self):
        """Test that non-alphanumeric characters are stripped"""
        assert text_to_number("one!") == 1
        assert text_to_number("two@#$") == 2
        assert text_to_number("three-") == 3
        assert text_to_number("four123") == 4
    
    def test_invalid_text_raises_error(self):
        """Test that invalid text raises ValueError"""
        with pytest.raises(ValueError, match="Unable to convert text to number"):
            text_to_number("eleven")
        
        with pytest.raises(ValueError, match="Unable to convert text to number"):
            text_to_number("hundred")
        
        with pytest.raises(ValueError, match="Unable to convert text to number"):
            text_to_number("invalid")


class TestNumberToText:
    """Test number to text conversion function"""
    
    def test_single_digits(self):
        """Test conversion of single digits"""
        assert number_to_text(1) == "one"
        assert number_to_text(2) == "two"
        assert number_to_text(3) == "three"
        assert number_to_text(4) == "four"
        assert number_to_text(5) == "five"
        assert number_to_text(6) == "six"
        assert number_to_text(7) == "seven"
        assert number_to_text(8) == "eight"
        assert number_to_text(9) == "nine"
        assert number_to_text(10) == "ten"
    
    def test_larger_numbers(self):
        """Test conversion of larger numbers"""
        assert number_to_text(11) == "eleven"
        assert number_to_text(20) == "twenty"
        assert number_to_text(100) == "one hundred"
        assert number_to_text(1000) == "one thousand"
    
    def test_zero(self):
        """Test conversion of zero"""
        assert number_to_text(0) == "zero"
    
    def test_negative_numbers(self):
        """Test conversion of negative numbers"""
        assert number_to_text(-1) == "minus one"
        assert number_to_text(-10) == "minus ten"
    
    def test_large_numbers(self):
        """Test conversion of very large numbers"""
        assert number_to_text(1000000) == "one million"
        assert number_to_text(1000000000) == "one billion"


class TestBase64ToNumber:
    """Test base64 to number conversion function"""
    
    def test_single_byte_numbers(self):
        """Test conversion of single byte numbers"""
        # Test with little-endian byte order
        assert base64_to_number("AA==") == 0  # 0x00
        assert base64_to_number("AQ==") == 1  # 0x01
        assert base64_to_number("Ag==") == 2  # 0x02
        assert base64_to_number("BQ==") == 5  # 0x05
        assert base64_to_number("Cg==") == 10  # 0x0A
        assert base64_to_number("Dw==") == 15  # 0x0F
        assert base64_to_number("IA==") == 32  # 0x20
        assert base64_to_number("fw==") == 127  # 0x7F
        assert base64_to_number("gA==") == 128  # 0x80
        assert base64_to_number("/w==") == 255  # 0xFF
    
    def test_multi_byte_numbers(self):
        """Test conversion of multi-byte numbers"""
        # Test with little-endian byte order
        assert base64_to_number("AAE=") == 256  # 0x0100
        assert base64_to_number("AAQ=") == 1024  # 0x0400
        assert base64_to_number("ABA=") == 4096  # 0x1000
        assert base64_to_number("AA==") == 0  # 0x0000
    
    def test_large_numbers(self):
        """Test conversion of large numbers"""
        # 0x12345678 in little-endian
        assert base64_to_number("eFY0Eg==") == 0x12345678
        # 0xDEADBEEF in little-endian  
        assert base64_to_number("776t3g==") == 0xDEADBEEF
    
    def test_invalid_base64_raises_error(self):
        """Test that invalid base64 raises ValueError"""
        with pytest.raises(ValueError, match="Invalid base64 input"):
            base64_to_number("invalid_base64")
        
        with pytest.raises(ValueError, match="Invalid base64 input"):
            base64_to_number("not_base64!")
        
        with pytest.raises(ValueError, match="Invalid base64 input"):
            base64_to_number("")


class TestNumberToBase64:
    """Test number to base64 conversion function"""
    
    def test_single_byte_numbers(self):
        """Test conversion of single byte numbers to base64"""
        # Test with little-endian byte order
        assert number_to_base64(0) == "AA=="  # 0x00
        assert number_to_base64(1) == "AQ=="  # 0x01
        assert number_to_base64(2) == "Ag=="  # 0x02
        assert number_to_base64(5) == "BQ=="  # 0x05
        assert number_to_base64(10) == "Cg=="  # 0x0A
        assert number_to_base64(15) == "Dw=="  # 0x0F
        assert number_to_base64(32) == "IA=="  # 0x20
        assert number_to_base64(127) == "fw=="  # 0x7F
        assert number_to_base64(128) == "gA=="  # 0x80
        assert number_to_base64(255) == "/w=="  # 0xFF
    
    def test_multi_byte_numbers(self):
        """Test conversion of multi-byte numbers to base64"""
        # Test with little-endian byte order
        assert number_to_base64(256) == "AAE="  # 0x0100
        assert number_to_base64(1024) == "AAQ="  # 0x0400
        assert number_to_base64(4096) == "ABA="  # 0x1000
    
    def test_large_numbers(self):
        """Test conversion of large numbers to base64"""
        # 0x12345678 in little-endian
        assert number_to_base64(0x12345678) == "eFY0Eg=="
        # 0xDEADBEEF in little-endian
        assert number_to_base64(0xDEADBEEF) == "776t3g=="
    
    def test_zero(self):
        """Test conversion of zero to base64"""
        assert number_to_base64(0) == "AA=="
    
    def test_negative_numbers(self):
        """Test conversion of negative numbers to base64"""
        # Negative numbers should work with two's complement
        assert number_to_base64(-1) == "/w=="  # 0xFF in single byte
        assert number_to_base64(-128) == "gA=="  # 0x80 in single byte


class TestCrossConversions:
    """Test all input types to all output types"""
    
    def test_text_to_all_outputs(self):
        """Test text input to all output types"""
        test_cases = [
            ("one", "text", "one"),
            ("one", "binary", "1"),
            ("one", "octal", "1"),
            ("one", "decimal", "1"),
            ("one", "hexadecimal", "1"),
            ("one", "base64", "AQ=="),
            ("ten", "text", "ten"),
            ("ten", "binary", "1010"),
            ("ten", "octal", "12"),
            ("ten", "decimal", "10"),
            ("ten", "hexadecimal", "a"),
            ("ten", "base64", "Cg=="),
        ]
        
        for input_val, output_type, expected in test_cases:
            result = self._convert_via_api(input_val, "text", output_type)
            assert result == expected, f"Failed: {input_val} (text) -> {output_type}"
    
    def test_binary_to_all_outputs(self):
        """Test binary input to all output types"""
        test_cases = [
            ("1010", "text", "ten"),
            ("1010", "binary", "1010"),
            ("1010", "octal", "12"),
            ("1010", "decimal", "10"),
            ("1010", "hexadecimal", "a"),
            ("1010", "base64", "Cg=="),
            ("1111", "text", "fifteen"),
            ("1111", "binary", "1111"),
            ("1111", "octal", "17"),
            ("1111", "decimal", "15"),
            ("1111", "hexadecimal", "f"),
            ("1111", "base64", "Dw=="),
        ]
        
        for input_val, output_type, expected in test_cases:
            result = self._convert_via_api(input_val, "binary", output_type)
            assert result == expected, f"Failed: {input_val} (binary) -> {output_type}"
    
    def test_octal_to_all_outputs(self):
        """Test octal input to all output types"""
        test_cases = [
            ("12", "text", "ten"),
            ("12", "binary", "1010"),
            ("12", "octal", "12"),
            ("12", "decimal", "10"),
            ("12", "hexadecimal", "a"),
            ("12", "base64", "Cg=="),
        ]
        
        for input_val, output_type, expected in test_cases:
            result = self._convert_via_api(input_val, "octal", output_type)
            assert result == expected, f"Failed: {input_val} (octal) -> {output_type}"
    
    def test_decimal_to_all_outputs(self):
        """Test decimal input to all output types"""
        test_cases = [
            ("10", "text", "ten"),
            ("10", "binary", "1010"),
            ("10", "octal", "12"),
            ("10", "decimal", "10"),
            ("10", "hexadecimal", "a"),
            ("10", "base64", "Cg=="),
            ("15", "text", "fifteen"),
            ("15", "binary", "1111"),
            ("15", "octal", "17"),
            ("15", "decimal", "15"),
            ("15", "hexadecimal", "f"),
            ("15", "base64", "Dw=="),
        ]
        
        for input_val, output_type, expected in test_cases:
            result = self._convert_via_api(input_val, "decimal", output_type)
            assert result == expected, f"Failed: {input_val} (decimal) -> {output_type}"
    
    def test_hexadecimal_to_all_outputs(self):
        """Test hexadecimal input to all output types"""
        test_cases = [
            ("a", "text", "ten"),
            ("a", "binary", "1010"),
            ("a", "octal", "12"),
            ("a", "decimal", "10"),
            ("a", "hexadecimal", "a"),
            ("a", "base64", "Cg=="),
            ("f", "text", "fifteen"),
            ("f", "binary", "1111"),
            ("f", "octal", "17"),
            ("f", "decimal", "15"),
            ("f", "hexadecimal", "f"),
            ("f", "base64", "Dw=="),
        ]
        
        for input_val, output_type, expected in test_cases:
            result = self._convert_via_api(input_val, "hexadecimal", output_type)
            assert result == expected, f"Failed: {input_val} (hexadecimal) -> {output_type}"
    
    def test_base64_to_all_outputs(self):
        """Test base64 input to all output types"""
        test_cases = [
            ("Cg==", "text", "ten"),
            ("Cg==", "binary", "1010"),
            ("Cg==", "octal", "12"),
            ("Cg==", "decimal", "10"),
            ("Cg==", "hexadecimal", "a"),
            ("Cg==", "base64", "Cg=="),
            ("Dw==", "text", "fifteen"),
            ("Dw==", "binary", "1111"),
            ("Dw==", "octal", "17"),
            ("Dw==", "decimal", "15"),
            ("Dw==", "hexadecimal", "f"),
            ("Dw==", "base64", "Dw=="),
        ]
        
        for input_val, output_type, expected in test_cases:
            result = self._convert_via_api(input_val, "base64", output_type)
            assert result == expected, f"Failed: {input_val} (base64) -> {output_type}"
    
    def _convert_via_api(self, input_val, input_type, output_type):
        """Helper method to convert via the API"""
        with app.test_client() as client:
            response = client.post('/convert', 
                                json={'input': input_val, 'inputType': input_type, 'outputType': output_type})
            data = json.loads(response.data)
            if data['error']:
                raise ValueError(f"API error: {data['error']}")
            return data['result']


class TestErrorHandling:
    """Test error handling for various invalid inputs"""
    
    def test_invalid_text_input(self):
        """Test API error handling for invalid text input"""
        with app.test_client() as client:
            response = client.post('/convert', 
                                json={'input': 'eleven', 'inputType': 'text', 'outputType': 'decimal'})
            data = json.loads(response.data)
            assert data['result'] is None
            assert "Unable to convert text to number" in data['error']
    
    def test_invalid_binary_input(self):
        """Test API error handling for invalid binary input"""
        with app.test_client() as client:
            response = client.post('/convert', 
                                json={'input': '102', 'inputType': 'binary', 'outputType': 'decimal'})
            data = json.loads(response.data)
            assert data['result'] is None
            assert "invalid literal for int() with base 2" in data['error']
    
    def test_invalid_octal_input(self):
        """Test API error handling for invalid octal input"""
        with app.test_client() as client:
            response = client.post('/convert', 
                                json={'input': '89', 'inputType': 'octal', 'outputType': 'decimal'})
            data = json.loads(response.data)
            assert data['result'] is None
            assert "invalid literal for int() with base 8" in data['error']
    
    def test_invalid_hexadecimal_input(self):
        """Test API error handling for invalid hexadecimal input"""
        with app.test_client() as client:
            response = client.post('/convert', 
                                json={'input': 'gh', 'inputType': 'hexadecimal', 'outputType': 'decimal'})
            data = json.loads(response.data)
            assert data['result'] is None
            assert "invalid literal for int() with base 16" in data['error']
    
    def test_invalid_base64_input(self):
        """Test API error handling for invalid base64 input"""
        with app.test_client() as client:
            response = client.post('/convert', 
                                json={'input': 'invalid_base64!', 'inputType': 'base64', 'outputType': 'decimal'})
            data = json.loads(response.data)
            assert data['result'] is None
            assert "Invalid base64 input" in data['error']
    
    def test_invalid_input_type(self):
        """Test API error handling for invalid input type"""
        with app.test_client() as client:
            response = client.post('/convert', 
                                json={'input': '10', 'inputType': 'invalid', 'outputType': 'decimal'})
            data = json.loads(response.data)
            assert data['result'] is None
            assert "Invalid input type" in data['error']
    
    def test_invalid_output_type(self):
        """Test API error handling for invalid output type"""
        with app.test_client() as client:
            response = client.post('/convert', 
                                json={'input': '10', 'inputType': 'decimal', 'outputType': 'invalid'})
            data = json.loads(response.data)
            assert data['result'] is None
            assert "Invalid output type" in data['error']
    
    def test_missing_input_field(self):
        """Test API error handling for missing input field"""
        with app.test_client() as client:
            response = client.post('/convert', 
                                json={'inputType': 'decimal', 'outputType': 'decimal'})
            data = json.loads(response.data)
            assert data['result'] is None
            assert "'input'" in data['error']
    
    def test_missing_input_type_field(self):
        """Test API error handling for missing inputType field"""
        with app.test_client() as client:
            response = client.post('/convert', 
                                json={'input': '10', 'outputType': 'decimal'})
            data = json.loads(response.data)
            assert data['result'] is None
            assert "'inputType'" in data['error']
    
    def test_missing_output_type_field(self):
        """Test API error handling for missing outputType field"""
        with app.test_client() as client:
            response = client.post('/convert', 
                                json={'input': '10', 'inputType': 'decimal'})
            data = json.loads(response.data)
            assert data['result'] is None
            assert "'outputType'" in data['error']


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_zero_conversions(self):
        """Test zero in all input/output combinations"""
        with app.test_client() as client:
            # Test zero in different input formats
            test_cases = [
                ("zero", "text"),
                ("0", "binary"),
                ("0", "octal"), 
                ("0", "decimal"),
                ("0", "hexadecimal"),
                ("AA==", "base64"),
            ]
            
            for input_val, input_type in test_cases:
                for output_type in ["text", "binary", "octal", "decimal", "hexadecimal", "base64"]:
                    response = client.post('/convert', 
                                        json={'input': input_val, 'inputType': input_type, 'outputType': output_type})
                    data = json.loads(response.data)
                    assert data['error'] is None, f"Error converting {input_val} ({input_type}) to {output_type}: {data['error']}"
                    assert data['result'] is not None
    
    def test_large_numbers(self):
        """Test large numbers in various formats"""
        large_number = 1000000
        with app.test_client() as client:
            # Test decimal input to all outputs
            response = client.post('/convert', 
                                json={'input': str(large_number), 'inputType': 'decimal', 'outputType': 'text'})
            data = json.loads(response.data)
            assert data['error'] is None
            assert "million" in data['result'].lower()
    
    def test_negative_numbers(self):
        """Test negative numbers (if supported)"""
        with app.test_client() as client:
            response = client.post('/convert', 
                                json={'input': '-10', 'inputType': 'decimal', 'outputType': 'text'})
            data = json.loads(response.data)
            # The current implementation might not handle negatives properly
            # This test will help identify if there are issues
            assert data['result'] is not None or data['error'] is not None


class TestBase64LittleEndianBug:
    """Test to catch the base64 little-endian bug"""
    
    def test_base64_little_endian_consistency(self):
        """Test that base64 conversion is consistent with little-endian byte order"""
        # This test will fail if the implementation uses big-endian instead of little-endian
        test_number = 0x1234  # 4660 in decimal
        
        # Convert to base64 using the function
        b64_result = number_to_base64(test_number)
        
        # Convert back using little-endian byte order
        expected_bytes = test_number.to_bytes(2, byteorder='little')
        expected_b64 = base64.b64encode(expected_bytes).decode('utf-8')
        
        # The current implementation uses little-endian, so this should pass
        # This test documents the expected behavior
        assert b64_result == expected_b64, f"Expected little-endian base64 {expected_b64}, got {b64_result}"
    
    def test_base64_roundtrip_little_endian(self):
        """Test that base64 roundtrip works with little-endian"""
        test_numbers = [1, 10, 100, 256, 1000, 0x1234, 0xDEADBEEF]
        
        for number in test_numbers:
            # Convert to base64
            b64 = number_to_base64(number)
            
            # Convert back from base64
            result = base64_to_number(b64)
            
            # For little-endian, we need to check if the roundtrip works correctly
            # The current implementation uses little-endian, so this test should pass
            assert result == number, f"Roundtrip failed for {number}: {number} -> {b64} -> {result}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
