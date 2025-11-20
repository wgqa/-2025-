"""
Checkout微服务测试脚本
系统测试计划与测试用例实现
"""

import pytest
import requests
import json
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app.app import app as flask_app

# 测试配置
BASE_URL = "http://localhost:5000"

class TestCheckoutService:
    """Checkout微服务系统测试类"""
    
    @classmethod
    def setup_class(cls):
        """测试类初始化：启动Flask测试服务器"""
        # 配置测试模式
        flask_app.config['TESTING'] = True
        cls.client = flask_app.test_client()
        
        print("=== Checkout微服务测试开始 ===")
    
    @classmethod
    def teardown_class(cls):
        """测试类清理"""
        print("\n=== Checkout微服务测试结束 ===")
    
    def test_checkout_normal_case(self):
        """
        测试1：正常结算场景
        描述：购物车包含多个商品，验证总金额计算正确性
        """
        print("\n测试1：正常结算场景")
        
        # 测试数据
        payload = {
            "items": [
                {"price": 10.99, "quantity": 2},
                {"price": 5.99, "quantity": 1},
                {"price": 3.50, "quantity": 4}
            ]
        }
        
        # 发送请求
        response = self.client.post(
            "/checkout",
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 200
        result = response.get_json()
        assert result["status"] == "ok"
        
        # 重新计算：10.99*2 = 21.98, 5.99*1 = 5.99, 3.50*4 = 14.00
        # 总和：21.98 + 5.99 = 27.97 + 14.00 = 41.97
        assert result["total"] == 41.97
        
        print("✓ 正常结算场景测试通过")
    
    def test_checkout_empty_cart(self):
        """
        测试2：空购物车场景
        描述：购物车为空时，验证返回400错误
        """
        print("\n测试2：空购物车场景")
        
        # 测试数据：空购物车
        payload = {"items": []}
        
        # 发送请求
        response = self.client.post(
            "/checkout",
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 400
        result = response.get_json()
        assert result["error"] == "empty cart"
        
        print("✓ 空购物车场景测试通过")
    
    def test_checkout_single_item(self):
        """
        测试3：单个商品结算场景
        描述：购物车只包含一个商品
        """
        print("\n测试3：单个商品结算场景")
        
        # 测试数据
        payload = {"items": [{"price": 99.99, "quantity": 1}]}
        
        # 发送请求
        response = self.client.post(
            "/checkout",
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 200
        result = response.get_json()
        assert result["total"] == 99.99
        
        print("✓ 单个商品结算场景测试通过")
    
    def test_checkout_multiple_quantities(self):
        """
        测试4：多数量商品结算场景
        描述：验证大量商品数量的计算正确性
        """
        print("\n测试4：多数量商品结算场景")
        
        # 测试数据
        payload = {"items": [{"price": 1.50, "quantity": 100}]}
        
        # 发送请求
        response = self.client.post(
            "/checkout",
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 200
        result = response.get_json()
        assert result["total"] == 150.00
        
        print("✓ 多数量商品结算场景测试通过")
    
    def test_checkout_invalid_price(self):
        """
        测试5：无效价格场景
        描述：验证对负数价格的处理
        """
        print("\n测试5：无效价格场景")
        
        # 测试数据：负数价格
        payload = {"items": [{"price": -10.00, "quantity": 1}]}
        
        # 发送请求
        response = self.client.post(
            "/checkout",
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 400
        result = response.get_json()
        assert "price must be a non-negative number" in result["error"]
        
        print("✓ 无效价格场景测试通过")
    
    def test_checkout_invalid_quantity(self):
        """
        测试6：无效数量场景
        描述：验证对负数和非整数数量的处理
        """
        print("\n测试6：无效数量场景")
        
        # 测试数据1：负数数量
        payload1 = {"items": [{"price": 10.00, "quantity": -2}]}
        response1 = self.client.post(
            "/checkout",
            data=json.dumps(payload1),
            content_type='application/json'
        )
        assert response1.status_code == 400
        
        # 测试数据2：非整数数量
        payload2 = {"items": [{"price": 10.00, "quantity": 2.5}]}
        response2 = self.client.post(
            "/checkout",
            data=json.dumps(payload2),
            content_type='application/json'
        )
        assert response2.status_code == 400
        
        print("✓ 无效数量场景测试通过")
    
    def test_checkout_invalid_request_format(self):
        """
        测试7：无效请求格式场景
        描述：验证对错误请求格式的处理
        """
        print("\n测试7：无效请求格式场景")
        
        # 测试数据1：非JSON格式
        response1 = self.client.post(
            "/checkout",
            data="not json data",
            content_type='text/plain'
        )
        assert response1.status_code == 400
        
        # 测试数据2：items不是列表
        payload2 = {"items": "not a list"}
        response2 = self.client.post(
            "/checkout",
            data=json.dumps(payload2),
            content_type='application/json'
        )
        assert response2.status_code == 400
        
        # 测试数据3：item不是对象
        payload3 = {"items": ["not an object"]}
        response3 = self.client.post(
            "/checkout",
            data=json.dumps(payload3),
            content_type='application/json'
        )
        assert response3.status_code == 400
        
        print("✓ 无效请求格式场景测试通过")
    
    def test_checkout_float_precision(self):
        """
        测试8：浮点数精度场景
        描述：验证价格计算的浮点数精度处理
        """
        print("\n测试8：浮点数精度场景")
        
        # 测试数据：可能产生精度问题的价格
        payload = {
            "items": [
                {"price": 0.1, "quantity": 3},  # 0.3
                {"price": 0.2, "quantity": 2}   # 0.4
            ]
        }
        
        # 发送请求
        response = self.client.post(
            "/checkout",
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # 验证响应：0.3 + 0.4 = 0.7
        assert response.status_code == 200
        result = response.get_json()
        assert result["total"] == 0.70
        
        print("✓ 浮点数精度场景测试通过")
    
    def test_checkout_large_order(self):
        """
        测试9：大额订单场景
        描述：验证对大额订单的处理能力
        """
        print("\n测试9：大额订单场景")
        
        # 测试数据：大量商品
        items = [{"price": i * 0.1, "quantity": i} for i in range(1, 101)]
        payload = {"items": items}
        
        # 发送请求
        response = self.client.post(
            "/checkout",
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 200
        result = response.get_json()
        
        # 计算预期结果：sum(i*0.1 * i) for i in 1..100 = 0.1 * sum(i²)
        # sum(i²) from 1 to n = n(n+1)(2n+1)/6
        # sum(1² to 100²) = 100*101*201/6 = 338350
        # 0.1 * 338350 = 33835.0
        expected_total = 33835.0
        assert result["total"] == expected_total
        
        print("✓ 大额订单场景测试通过")

if __name__ == "__main__":
    """运行测试"""
    pytest.main(["-v", "test_checkout.py"])