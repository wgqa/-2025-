import pytest
from bank import transfer


def test_transfer_normal():
    """正常转账分支"""
    a = {"balance": 100}
    b = {"balance": 50}
    assert transfer(a, b, 30) is True
    assert a["balance"] == 70
    assert b["balance"] == 80


def test_transfer_negative():
    """转账金额为负"""
    a = {"balance": 100}
    b = {"balance": 50}
    with pytest.raises(ValueError, match="转账金额必须为正数"):
        transfer(a, b, -10)


def test_transfer_insufficient_balance():
    """余额不足分支"""
    a = {"balance": 20}
    b = {"balance": 50}
    with pytest.raises(ValueError, match="余额不足"):
        transfer(a, b, 50)