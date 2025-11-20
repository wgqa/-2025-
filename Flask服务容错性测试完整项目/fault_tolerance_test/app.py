#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask支付服务应用
用于容错性测试的示例应用
"""

import os
import time
import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql://postgres:postgres@db:5432/payment_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PAYMENT_RETRY_ATTEMPTS'] = 3
app.config['PAYMENT_RETRY_DELAY'] = 2  # 重试延迟时间（秒）

db = SQLAlchemy(app)

class Payment(db.Model):
    """支付记录表"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, success, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'amount': self.amount,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class DatabaseHealth:
    """数据库健康检查类"""
    
    @staticmethod
    def is_healthy():
        """检查数据库连接是否健康"""
        try:
            # 执行一个简单的查询
            db.session.execute('SELECT 1')
            db.session.commit()
            return True
        except OperationalError as e:
            logging.error(f"数据库连接异常: {str(e)}")
            return False
        except Exception as e:
            logging.error(f"数据库健康检查失败: {str(e)}")
            return False

def with_retry(max_attempts=3, delay=2):
    """重试装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except OperationalError as e:
                    attempts += 1
                    logging.warning(f"数据库操作失败 (尝试 {attempts}/{max_attempts}): {str(e)}")
                    
                    if attempts >= max_attempts:
                        logging.error(f"达到最大重试次数 ({max_attempts})，操作失败")
                        raise
                    
                    logging.info(f"等待 {delay} 秒后重试...")
                    time.sleep(delay)
                except Exception as e:
                    logging.error(f"操作失败: {str(e)}")
                    raise
        return wrapper
    return decorator

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    db_healthy = DatabaseHealth.is_healthy()
    
    status = 'healthy' if db_healthy else 'unhealthy'
    code = 200 if db_healthy else 503
    
    return jsonify({
        'status': status,
        'database': 'connected' if db_healthy else 'disconnected',
        'timestamp': datetime.utcnow().isoformat()
    }), code

@app.route('/payment', methods=['POST'])
@with_retry(
    max_attempts=app.config['PAYMENT_RETRY_ATTEMPTS'],
    delay=app.config['PAYMENT_RETRY_DELAY']
)
def create_payment():
    """创建支付请求"""
    try:
        data = request.get_json()
        
        # 验证请求数据
        if not data or 'order_id' not in data or 'amount' not in data:
            return jsonify({'error': '缺少必要参数: order_id 和 amount 是必需的'}), 400
        
        order_id = data['order_id']
        amount = float(data['amount'])
        
        if amount <= 0:
            return jsonify({'error': '金额必须大于0'}), 400
        
        # 检查订单是否已存在
        existing_payment = Payment.query.filter_by(order_id=order_id).first()
        if existing_payment:
            return jsonify({
                'error': '订单已存在',
                'payment': existing_payment.to_dict()
            }), 409
        
        # 创建新的支付记录
        payment = Payment(
            order_id=order_id,
            amount=amount,
            status='pending'
        )
        
        db.session.add(payment)
        db.session.commit()
        
        logging.info(f"创建支付成功: order_id={order_id}, amount={amount}")
        
        return jsonify({
            'success': True,
            'message': '支付创建成功',
            'payment': payment.to_dict()
        }), 201
        
    except OperationalError as e:
        db.session.rollback()
        logging.error(f"数据库操作失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': '数据库连接异常',
            'message': '支付处理失败，请稍后重试'
        }), 503
    except Exception as e:
        db.session.rollback()
        logging.error(f"支付处理失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '支付处理失败'
        }), 500

@app.route('/payment/<order_id>', methods=['GET'])
def get_payment(order_id):
    """查询支付状态"""
    try:
        payment = Payment.query.filter_by(order_id=order_id).first()
        
        if not payment:
            return jsonify({'error': '支付记录不存在'}), 404
        
        return jsonify({
            'success': True,
            'payment': payment.to_dict()
        }), 200
        
    except OperationalError as e:
        logging.error(f"数据库查询失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': '数据库连接异常',
            'message': '查询失败，请稍后重试'
        }), 503
    except Exception as e:
        logging.error(f"查询失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '查询失败'
        }), 500

@app.route('/payment/<order_id>/confirm', methods=['POST'])
@with_retry(
    max_attempts=app.config['PAYMENT_RETRY_ATTEMPTS'],
    delay=app.config['PAYMENT_RETRY_DELAY']
)
def confirm_payment(order_id):
    """确认支付"""
    try:
        payment = Payment.query.filter_by(order_id=order_id).first()
        
        if not payment:
            return jsonify({'error': '支付记录不存在'}), 404
        
        if payment.status == 'success':
            return jsonify({
                'success': True,
                'message': '支付已确认',
                'payment': payment.to_dict()
            }), 200
        
        # 更新支付状态
        payment.status = 'success'
        db.session.commit()
        
        logging.info(f"支付确认成功: order_id={order_id}")
        
        return jsonify({
            'success': True,
            'message': '支付确认成功',
            'payment': payment.to_dict()
        }), 200
        
    except OperationalError as e:
        db.session.rollback()
        logging.error(f"数据库操作失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': '数据库连接异常',
            'message': '确认失败，请稍后重试'
        }), 503
    except Exception as e:
        db.session.rollback()
        logging.error(f"确认支付失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '确认失败'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({'error': '接口不存在'}), 404

@app.errorhandler(500)
def server_error(error):
    """500错误处理"""
    return jsonify({'error': '服务器内部错误'}), 500

def init_database():
    """初始化数据库"""
    with app.app_context():
        try:
            db.create_all()
            logging.info("数据库初始化成功")
        except Exception as e:
            logging.error(f"数据库初始化失败: {str(e)}")
            raise

if __name__ == '__main__':
    # 初始化数据库
    init_database()
    
    # 启动应用
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    logging.info(f"Flask应用启动: http://{host}:{port}")
    app.run(host=host, port=port, debug=True)