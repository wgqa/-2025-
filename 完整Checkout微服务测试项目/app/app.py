"""
Checkout微服务
提供购物车结算功能的API接口
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/checkout", methods=["POST"])
def checkout():
    """
    结算接口
    接收购物车商品列表，计算总金额
    
    请求格式:
    {
        "items": [
            {"price": 10.99, "quantity": 2},
            {"price": 5.99, "quantity": 1}
        ]
    }
    
    成功响应 (200 OK):
    {
        "total": 27.97,
        "status": "ok"
    }
    
    错误响应 (400 Bad Request):
    {
        "error": "empty cart"
    }
    """
    try:
        # 尝试解析JSON数据
        try:
            data = request.get_json()
        except Exception as e:
            return jsonify({"error": "invalid json format"}), 400
        
        # 验证请求数据格式
        if not isinstance(data, dict):
            return jsonify({"error": "invalid request format"}), 400
            
        items = data.get("items", [])
        
        # 验证items字段是否为列表
        if not isinstance(items, list):
            return jsonify({"error": "items must be a list"}), 400
        
        # 检查购物车是否为空
        if not items:
            return jsonify({"error": "empty cart"}), 400
        
        # 计算总金额
        total = 0.0
        for item in items:
            # 验证每个商品的格式
            if not isinstance(item, dict):
                return jsonify({"error": "each item must be an object"}), 400
            
            # 获取价格和数量，设置默认值
            price = item.get("price", 0.0)
            quantity = item.get("quantity", 0)
            
            # 验证价格和数量的类型
            if not isinstance(price, (int, float)) or price < 0:
                return jsonify({"error": "price must be a non-negative number"}), 400
            
            if not isinstance(quantity, int) or quantity < 0:
                return jsonify({"error": "quantity must be a non-negative integer"}), 400
            
            # 累加总金额
            total += price * quantity
        
        # 保留两位小数
        total = round(total, 2)
        
        return jsonify({"total": total, "status": "ok"}), 200
        
    except Exception as e:
        return jsonify({"error": f"internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    """运行Flask应用"""
    app.run(debug=True, host="0.0.0.0", port=5000)