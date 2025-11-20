"""
座位锁定系统测试脚本
Test script for Seat Lock System
"""

from app.seat_lock import SeatLockSystem
import time

def test_lock_and_expire():
    """测试锁定和过期功能"""
    s = SeatLockSystem()
    # 锁定座位A1
    assert s.lock("A1", "user1") == True
    # 手动设置过期时间为1秒前（模拟过期）
    s.locked_seats["A1"]["expire"] = time.time() - 1
    # 检查座位是否已过期（应该返回False）
    assert s.is_locked("A1") == False

def test_relock_after_expire():
    """测试过期后重新锁定功能"""
    s = SeatLockSystem()
    # 第一次锁定座位A1
    s.lock("A1", "user1")
    # 手动设置过期时间
    s.locked_seats["A1"]["expire"] = time.time() - 1
    # 过期后重新锁定座位A1给user2
    s.lock("A1", "user2")
    # 检查座位是否被成功锁定
    assert s.is_locked("A1") == True

def test_lock_seat_success():
    """测试正常锁定座位"""
    s = SeatLockSystem()
    result = s.lock("B2", "user3")
    assert result == True
    assert s.is_locked("B2") == True

def test_lock_already_locked_seat():
    """测试锁定已被锁定的座位"""
    s = SeatLockSystem()
    # 第一次锁定
    s.lock("C3", "user4")
    # 尝试再次锁定同一个座位
    result = s.lock("C3", "user5")
    assert result == False

def test_unlock_seat():
    """测试解锁座位功能"""
    s = SeatLockSystem()
    s.lock("D4", "user6")
    # 解锁座位
    result = s.unlock("D4")
    assert result == True
    assert s.is_locked("D4") == False

def test_unlock_unlocked_seat():
    """测试解锁未锁定的座位"""
    s = SeatLockSystem()
    result = s.unlock("E5")
    assert result == False

def test_extend_lock_time():
    """测试延长锁定时间"""
    s = SeatLockSystem()
    s.lock("F6", "user7")
    original_expire = s.locked_seats["F6"]["expire"]
    # 延长锁定时间30秒
    result = s.extend_lock("F6", 30)
    assert result == True
    assert s.locked_seats["F6"]["expire"] == original_expire + 30

def test_get_lock_info():
    """测试获取锁定信息"""
    s = SeatLockSystem()
    s.lock("G7", "user8")
    lock_info = s.get_lock_info("G7")
    assert lock_info is not None
    assert lock_info["user"] == "user8"
    assert "expire" in lock_info

def test_get_all_locked_seats():
    """测试获取所有锁定座位"""
    s = SeatLockSystem()
    s.lock("H8", "user9")
    s.lock("I9", "user10")
    locked_seats = s.get_all_locked_seats()
    assert len(locked_seats) == 2
    assert "H8" in locked_seats
    assert "I9" in locked_seats

if __name__ == "__main__":
    # 运行所有测试
    test_lock_and_expire()
    test_relock_after_expire()
    test_lock_seat_success()
    test_lock_already_locked_seat()
    test_unlock_seat()
    test_unlock_unlocked_seat()
    test_extend_lock_time()
    test_get_lock_info()
    test_get_all_locked_seats()
    print("所有测试通过！")