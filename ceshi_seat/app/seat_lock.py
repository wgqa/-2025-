"""
座位锁定系统
Seat Lock System
"""

import time

class SeatLockSystem:
    """
    座位锁定系统
    用于管理座位的锁定状态，支持设置锁定超时时间
    """
    
    def __init__(self, timeout: int = 60):
        """
        初始化座位锁定系统
        
        Args:
            timeout: 锁定超时时间（秒），默认为60秒
        """
        self.locked_seats = {}  # 存储锁定的座位信息
        self.timeout = timeout  # 锁定超时时间
    
    def lock(self, seat_id: str, user: str) -> bool:
        """
        锁定指定座位
        
        Args:
            seat_id: 座位ID
            user: 锁定座位的用户
            
        Returns:
            bool: 如果锁定成功返回True，如果座位已被锁定返回False
        """
        now = time.time()
        
        # 检查座位是否已被锁定且未过期
        if seat_id in self.locked_seats and self.locked_seats[seat_id]['expire'] > now:
            return False
        
        # 锁定座位
        self.locked_seats[seat_id] = {
            'user': user,
            'expire': now + self.timeout
        }
        return True
    
    def is_locked(self, seat_id: str) -> bool:
        """
        检查座位是否处于锁定状态
        
        Args:
            seat_id: 座位ID
            
        Returns:
            bool: 如果座位已锁定且未超时返回True，否则返回False
        """
        now = time.time()
        
        # 检查座位是否已被锁定且未过期
        if seat_id in self.locked_seats and self.locked_seats[seat_id]['expire'] > now:
            return True
        
        # 如果座位已过期，从锁定列表中移除
        if seat_id in self.locked_seats:
            del self.locked_seats[seat_id]
            
        return False
    
    def unlock(self, seat_id: str) -> bool:
        """
        解锁指定座位
        
        Args:
            seat_id: 座位ID
            
        Returns:
            bool: 如果解锁成功返回True，如果座位未锁定返回False
        """
        if seat_id in self.locked_seats:
            del self.locked_seats[seat_id]
            return True
        return False
    
    def extend_lock(self, seat_id: str, extend_time: int) -> bool:
        """
        延长座位锁定时间
        
        Args:
            seat_id: 座位ID
            extend_time: 延长的时间（秒）
            
        Returns:
            bool: 如果延长成功返回True，如果座位未锁定返回False
        """
        if seat_id in self.locked_seats:
            self.locked_seats[seat_id]['expire'] += extend_time
            return True
        return False
    
    def get_lock_info(self, seat_id: str) -> dict or None:
        """
        获取座位锁定信息
        
        Args:
            seat_id: 座位ID
            
        Returns:
            dict or None: 如果座位已锁定返回锁定信息字典，否则返回None
        """
        return self.locked_seats.get(seat_id)
    
    def get_all_locked_seats(self) -> list:
        """
        获取所有已锁定的座位ID列表
        
        Returns:
            list: 已锁定的座位ID列表
        """
        return list(self.locked_seats.keys())