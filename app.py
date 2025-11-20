from flask import Flask, request, jsonify
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# 模拟库存
inventory = {"book": 10}

@app.route("/order", methods=["POST"])
def order():
    """下单接口：扣减库存"""
    item = request.json.get("item")
    qty  = request.json.get("qty", 1)

    if item not in inventory:
        return jsonify({"error": "不存在的商品"}), 400

    if inventory[item] < qty:
        return jsonify({"error": "库存不足"}), 400

    inventory[item] -= qty
    return jsonify({"success": True, "剩余库存": inventory[item]})

# ---- 2. 新增最小登录模块 ----
@app.route("/login")
def login():
    # 返回带“登录”二字的简单页面
    return render_template_string("""
        <html>
          <head><title>登录</title></head>
          <body>
            <h2>用户登录</h2>
            <form method="post" action="/do_login">
              用户名：<input name="user"><br>
              密码  ：<input type="password" name="pwd"><br>
              <button type="submit">登录</button>
            </form>
          </body>
        </html>
    """)

# 可选：处理登录（测试用不到，可留空）
@app.route("/do_login", methods=["POST"])
def do_login():
    return jsonify({"msg": "登录成功"})

if __name__ == "__main__":
    app.run(debug=True)