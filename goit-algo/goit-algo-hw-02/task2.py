from collections import deque


def is_palindrome(s):
    """
    Check if the given string is a palindrome.

    A palindrome is a string that reads the same forwards and backwards.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string is a palindrome, False otherwise.
    """
    # Normalize the string by removing spaces and converting to lowercase
    normalized_str = ''.join(s.split()).lower()
    
    dq = deque(normalized_str)
    while len(dq) > 1:
        if dq.popleft() != dq.pop():
            return False
    return True

def test_palindrome(s: str):
    """Друкує розширений результат перевірки"""
    result = is_palindrome(s)
    if result:
        print(f'"{s}" ➜ паліндром ✅')
    else:
        print(f'"{s}" ➜ не паліндром ❌')


# Приклади викликів
test_palindrome("abbA")                      # паліндром
test_palindrome("racecar")                   # паліндром
test_palindrome("A man a plan a canal Panama")  # паліндром
test_palindrome("No lemon no melon")        # паліндром
test_palindrome("abcd")                     # не паліндром
test_palindrome("python")                   # не паліндром
test_palindrome("Hello World")              # не паліндром