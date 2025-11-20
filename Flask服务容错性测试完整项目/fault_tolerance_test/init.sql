-- init.sql - 数据库初始化脚本

-- 创建支付表（如果不存在）
CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(50) UNIQUE NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_payments_order_id ON payments(order_id);
CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status);

-- 插入测试数据
INSERT INTO payments (order_id, amount, status) VALUES 
('TEST001', 100.00, 'success'),
('TEST002', 200.50, 'pending'),
('TEST003', 50.75, 'failed')
ON CONFLICT (order_id) DO NOTHING;

-- 创建数据库健康检查函数
CREATE OR REPLACE FUNCTION health_check()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

-- 显示初始化完成信息
SELECT 'Database initialized successfully' AS message;