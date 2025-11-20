# Flask服务容错性测试 - 数据库中断测试

## 项目简介
这是一个用于演示和测试Flask服务在数据库中断情况下容错能力的完整解决方案。该项目使用Docker容器化技术，模拟数据库故障场景，测试Web服务的稳定性和恢复能力。

## 项目结构
```
fault_tolerance_test/
├── app.py                # Flask支付服务应用
├── Dockerfile            # Docker构建文件
├── docker-compose.yml    # Docker Compose配置
├── requirements.txt      # Python依赖包
├── entrypoint.sh         # 应用启动脚本
├── init.sql              # 数据库初始化脚本
├── test_fault_tolerance.py  # 容错性测试脚本
├── TEST_PLAN.md          # 测试计划文档
├── README.md             # 项目说明文档
└── .vscode/              # VS Code配置
    └── launch.json       # 调试配置
```

## 功能特性

### 核心功能
- **支付服务**: 创建支付、查询支付、确认支付
- **健康检查**: 实时监控服务和数据库状态
- **容错机制**: 数据库操作重试、错误处理、自动恢复
- **数据一致性**: 确保支付数据的完整性

### 容错特性
- **自动重试**: 数据库操作失败时自动重试
- **优雅降级**: 数据库断开时返回友好错误
- **自动恢复**: 数据库恢复后服务自动恢复
- **数据保护**: 确保未完成的操作不会破坏数据

## 快速开始

### 环境要求
- Docker 20.10+
- Docker Compose 1.29+
- Python 3.9+
- VS Code (推荐)

### 安装步骤

#### 1. 克隆项目
```bash
git clone <项目地址>
cd fault_tolerance_test
```

#### 2. 启动服务
```bash
# 使用Docker Compose启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

#### 3. 验证服务
```bash
# 检查服务是否正常运行
curl http://localhost:5000/health

# 预期输出
# {"status":"healthy","database":"connected","timestamp":"..."}
```

#### 4. 测试支付功能
```bash
# 创建支付
curl -X POST http://localhost:5000/payment \
  -H "Content-Type: application/json" \
  -d '{"order_id": "TEST001", "amount": 100.00}'

# 查询支付
curl http://localhost:5000/payment/TEST001
```

### 使用VS Code开发

#### 1. 安装扩展
- Docker
- Python
- REST Client (推荐)

#### 2. 配置虚拟环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 3. 调试配置
使用`.vscode/launch.json`中的配置进行调试：
- **Python: 运行应用**: 启动Flask应用
- **Python: 运行测试**: 执行容错性测试

## 容错性测试

### 测试用例

#### 测试用例1: 正常操作
```bash
# 运行正常操作测试
python test_fault_tolerance.py --test normal
```

#### 测试用例2: 数据库中断测试
```bash
# 运行数据库中断测试
python test_fault_tolerance.py --test database-failure
```

#### 测试用例3: 完整测试套件
```bash
# 运行所有测试用例
python test_fault_tolerance.py --test all
```

### 手动测试

#### 1. 模拟数据库故障
```bash
# 停止数据库容器
docker stop fault_tolerance_test_db_1

# 测试服务响应
curl http://localhost:5000/payment \
  -H "Content-Type: application/json" \
  -d '{"order_id": "TEST002", "amount": 200.00}'

# 恢复数据库
docker start fault_tolerance_test_db_1

# 等待恢复后测试
sleep 20
curl http://localhost:5000/health
```

#### 2. 查看日志
```bash
# 查看应用日志
docker logs -f fault_tolerance_test_web_1

# 查看测试日志
tail -f fault_tolerance_test.log
```

## 项目配置

### Docker配置
```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/payment_db
      - PAYMENT_RETRY_ATTEMPTS=3
      - PAYMENT_RETRY_DELAY=2
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=payment_db
```

### Flask应用配置
```python
# app.py
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql://postgres:postgres@db:5432/payment_db'
)
app.config['PAYMENT_RETRY_ATTEMPTS'] = 3
app.config['PAYMENT_RETRY_DELAY'] = 2
```

## 测试报告

### 自动生成报告
```bash
# 运行测试并生成报告
python test_fault_tolerance.py --generate-report

# 查看报告
ls -la *.json *.html
```

### 报告内容
- **测试摘要**: 总用例数、通过率、总体状态
- **详细结果**: 每个测试用例的执行步骤和结果
- **错误信息**: 失败用例的详细错误信息
- **性能数据**: 响应时间、重试次数等统计信息

## 最佳实践

### 开发建议
1. **错误处理**: 始终使用try-except捕获数据库异常
2. **事务管理**: 重要操作使用数据库事务
3. **重试机制**: 对可能失败的操作添加重试逻辑
4. **健康检查**: 定期检查服务和依赖状态

### 部署建议
1. **监控告警**: 配置服务状态监控和告警
2. **日志管理**: 集中管理应用和数据库日志
3. **备份策略**: 定期备份数据库
4. **容灾部署**: 考虑多区域部署提高可用性

## 常见问题

### Q1: 服务启动失败
**A**: 检查Docker是否正常运行，查看日志定位问题：
```bash
docker-compose logs web
```

### Q2: 数据库连接失败
**A**: 检查数据库容器是否运行，网络配置是否正确：
```bash
docker-compose ps
docker network ls
```

### Q3: 测试脚本执行失败
**A**: 确保服务正常运行，检查Python环境和依赖：
```bash
pip list | grep -E "flask|sqlalchemy|requests"
```

### Q4: VS Code调试问题
**A**: 检查launch.json配置，确保Python路径正确：
```json
{
    "python.pythonPath": "${workspaceFolder}/venv/bin/python"
}
```

## 扩展功能

### 计划中的功能
- **更多数据库支持**: MySQL、SQLite等
- **分布式追踪**: 使用Jaeger追踪请求流程
- **性能监控**: Prometheus + Grafana监控
- **CI/CD集成**: GitHub Actions自动测试部署

## 技术栈

### 后端技术
- **Web框架**: Flask 2.0.1
- **ORM**: SQLAlchemy 2.5.1
- **数据库**: PostgreSQL 13
- **容器化**: Docker、Docker Compose

### 测试技术
- **测试框架**: pytest 6.2.5
- **HTTP客户端**: requests 2.26.0
- **Docker SDK**: docker 5.0.0
- **报告生成**: JSON、HTML

## 许可证
[MIT License](LICENSE)

## 联系方式
如有问题或建议，请联系：
- **项目维护者**: [姓名]
- **邮箱**: [邮箱地址]
- **项目地址**: [GitHub地址]

---
**项目版本**: 1.0  
**最后更新**: 2025年11月20日  
**文档状态**: 完整