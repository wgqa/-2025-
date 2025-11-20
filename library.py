# library.py
class UserNotExistError(Exception):
    """用户不存在异常"""
    pass

class BookNotExistError(Exception):
    """图书不存在异常"""
    pass

class NoStockError(Exception):
    """库存为0异常"""
    pass

# 模拟数据库
USERS = {"1001": "Alice", "1002": "Bob"}
BOOKS = {
    "978-7-111-54320-0": {"title": "Python编程", "stock": 2},
    "978-7-111-12345-6": {"title": "算法导论", "stock": 0},
}

def borrow_book(user_id: str, book_isbn: str):
    """
    借书主逻辑
    :param user_id: 用户编号
    :param book_isbn: 图书ISBN
    :raises: 对应异常
    """
    if user_id not in USERS:
        raise UserNotExistError(f"用户{user_id}不存在")

    if book_isbn not in BOOKS:
        raise BookNotExistError(f"图书{book_isbn}不存在")

    if BOOKS[book_isbn]["stock"] <= 0:
        raise NoStockError(f"图书{book_isbn}库存为0")

    # 借书成功
    BOOKS[book_isbn]["stock"] -= 1
    return True