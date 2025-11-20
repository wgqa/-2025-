def is_palindrome(s: str) -> bool:
    """
    判断一个字符串是否为回文
    
    回文是指正读和反读都一样的字符串，忽略大小写和非字母数字字符
    
    Args:
        s: 要判断的字符串
        
    Returns:
        如果是回文返回True，否则返回False
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    
    # 清理字符串：只保留字母数字字符，转换为小写
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    
    if not cleaned:
        return True  # 空字符串或只包含非字母数字字符的字符串视为回文
    
    # 判断是否为回文
    return cleaned == cleaned[::-1]