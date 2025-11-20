import pytest
from palindrome import is_palindrome

def test_empty_string():
    """测试空字符串"""
    assert is_palindrome("") == True

def test_single_character():
    """测试单个字符"""
    assert is_palindrome("a") == True
    assert is_palindrome("5") == True

def test_basic_palindromes():
    """测试基本回文"""
    assert is_palindrome("racecar") == True
    assert is_palindrome("level") == True
    assert is_palindrome("madam") == True

def test_non_palindromes():
    """测试非回文"""
    assert is_palindrome("hello") == False
    assert is_palindrome("python") == False
    assert is_palindrome("test") == False

def test_case_insensitive():
    """测试大小写不敏感"""
    assert is_palindrome("RaceCar") == True
    assert is_palindrome("Madam") == True
    assert is_palindrome("A man a plan a canal Panama") == True

def test_ignore_non_alphanumeric():
    """测试忽略非字母数字字符"""
    assert is_palindrome("A man, a plan, a canal: Panama") == True
    assert is_palindrome("race a car") == False
    assert is_palindrome("No 'x' in Nixon") == True

def test_numbers_and_symbols():
    """测试数字和符号"""
    assert is_palindrome("12321") == True
    assert is_palindrome("12345") == False
    # 修复：使用真正的回文
    assert is_palindrome("12a21") == True
    assert is_palindrome("1a2a1") == True
    assert is_palindrome("123a321") == True

def test_mixed_types():
    """测试混合类型输入"""
    with pytest.raises(TypeError):
        is_palindrome(123)
    
    with pytest.raises(TypeError):
        is_palindrome(None)
    
    with pytest.raises(TypeError):
        is_palindrome([1, 2, 1])

def test_special_characters():
    """测试特殊字符"""
    assert is_palindrome("!!!") == True
    assert is_palindrome("abba!!!") == True
    assert is_palindrome("a@b@a") == True

def test_long_palindrome():
    """测试长回文"""
    long_palindrome = "a" * 1000
    assert is_palindrome(long_palindrome) == True
    
    long_non_palindrome = "a" * 999 + "b"
    assert is_palindrome(long_non_palindrome) == False