class SeatLockSystem:
    
    def __init__(self):
        self.locked_seats = {}
        self.timeout = 60
    
    def lock(self, seat_id, user):
        import time
        now = time.time()
        if seat_id in self.locked_seats and self.locked_seats[seat_id]['expire'] > now:
            return False
        self.locked_seats[seat_id] = {'user': user, 'expire': now + self.timeout}
        return True
    
    def is_locked(self, seat_id):
        import time
        now = time.time()
        if seat_id in self.locked_seats and self.locked_seats[seat_id]['expire'] > now:
            return True
        return False