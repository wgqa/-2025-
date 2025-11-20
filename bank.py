def transfer(account_a, account_b, amount):
    """
    从 account_a 向 account_b 转账 amount
    :return: True  转账成功
    :raises: ValueError 金额非法或余额不足
    """
    if amount <= 0:
        raise ValueError("转账金额必须为正数")

    if account_a['balance'] < amount:
        raise ValueError("余额不足")

    account_a['balance'] -= amount
    account_b['balance'] += amount
    return True