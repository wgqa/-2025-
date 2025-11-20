# test_library.py
import pytest
from library import borrow_book, UserNotExistError, BookNotExistError, NoStockError, BOOKS

def test_borrow_success():
    """正常借书"""
    isbn = "978-7-111-54320-0"
    original = BOOKS[isbn]["stock"]
    assert borrow_book("1001", isbn) is True
    assert BOOKS[isbn]["stock"] == original - 1

def test_user_not_exist():
    """用户不存在"""
    with pytest.raises(UserNotExistError):
        borrow_book("9999", "978-7-111-54320-0")

def test_book_not_exist():
    """图书不存在"""
    with pytest.raises(BookNotExistError):
        borrow_book("1001", "000-0-000-00000-0")

def test_no_stock():
    """库存为0"""
    with pytest.raises(NoStockError):
        borrow_book("1001", "978-7-111-12345-6")

def test_borrow_twice_reduce_stock():
    """连续借两本，库存递减"""
    isbn = "978-7-111-54320-0"
    BOOKS[isbn]["stock"] = 2  # 先重置
    borrow_book("1001", isbn)
    borrow_book("1002", isbn)
    assert BOOKS[isbn]["stock"] == 0