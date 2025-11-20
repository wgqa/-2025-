# Checkout微服务测试项目

## 项目概述
这是一个为Checkout微服务编写的系统测试项目，包含完整的测试计划和自动化测试脚本。

## 项目结构
```
checkout_service/
├── app/
│   └── app.py          # Checkout微服务实现
├── tests/
│   └── test_checkout.py # 系统测试脚本
├── TEST_PLAN.md        # 系统测试计划文档
├── requirements.txt    # 项目依赖
└── README.md           # 项目说明
```

## 功能说明

### Checkout微服务
提供购物车结算功能的API接口：
- **URL**: /checkout
- **方法**: POST
- **格式**: JSON
- **功能**: 接收商品列表，计算总金额并返回结果

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行应用
```bash
# 方式1：直接运行
python app/app.py

# 方式2：使用Flask命令
export FLASK_APP=app/app.py
export FLASK_ENV=development
flask run
```

### 3. 运行测试
```bash
# 运行所有测试
pytest tests/test_checkout.py -v

# 运行测试并生成HTML报告
pytest tests/test_checkout.py -v --html=report.html

# 运行指定测试用例
pytest tests/test_checkout.py::TestCheckoutService::test_checkout_normal_case -v
```

## 测试用例说明

### 包含9个测试场景：

1. **正常结算场景** - 验证基本功能
2. **空购物车场景** - 验证异常处理
3. **单个商品结算场景** - 验证边界情况
4. **多数量商品结算场景** - 验证大量商品处理
5. **无效价格场景** - 验证数据验证
6. **无效数量场景** - 验证数据验证
7. **无效请求格式场景** - 验证错误处理
8. **浮点数精度场景** - 验证计算精度
9. **大额订单场景** - 验证系统性能

## API使用示例

### 请求示例
```python
import requests
import json

url = "http://localhost:5000/checkout"
data = {
    "items": [
        {"price": 10.99, "quantity": 2},
        {"price": 5.99, "quantity": 1}
    ]
}

response = requests.post(url, json=data)
print(response.json())
```

### 成功响应
```json
{
    "total": 27.97,
    "status": "ok"
}
```

### 错误响应
```json
{
    "error": "empty cart"
}
```

## 测试报告

运行测试后会生成详细的测试报告，包含：
- 测试用例执行结果
- 测试通过率统计
- 详细的错误信息
- 测试执行时间

## 技术特点

### 测试框架优势
- **自动化测试**: 使用Pytest实现自动化测试
- **全面覆盖**: 涵盖功能、异常、边界场景
- **易于维护**: 模块化的测试代码结构
- **详细报告**: 支持HTML格式测试报告

### 微服务优势
- **轻量级**: 使用Flask框架，部署简单
- **RESTful**: 符合REST API设计规范
- **错误处理**: 完善的错误处理机制
- **数据验证**: 严格的输入数据验证

## 部署说明

### 开发环境
```bash
# 本地开发
python app/app.py

# 开发测试
pytest tests/test_checkout.py -v
```

### 生产环境
```bash
# 使用Gunicorn部署
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app.app:app"

# 健康检查
curl http://localhost:5000/health
```

## 维护说明

### 新增测试用例
1. 在`tests/test_checkout.py`中添加新的测试方法
2. 遵循现有的测试用例命名规范
3. 确保测试覆盖率的完整性

### 功能扩展
1. 在`app/app.py`中添加新的API端点
2. 编写相应的测试用例
3. 更新测试计划文档

## 问题解决

### 常见问题
1. **端口被占用**: 更换端口或停止占用端口的进程
2. **依赖冲突**: 使用虚拟环境隔离依赖
3. **测试失败**: 检查代码逻辑或测试数据

### 技术支持
如需技术支持，请提供：
- 完整的错误信息
- 测试数据
- 环境配置信息

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| 1.0 | 2025-11-19 | 初始版本，包含基础功能和测试 |

## 许可证

本项目采用MIT许可证，详情请参考LICENSE文件。