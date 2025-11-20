# Web登录功能测试项目

## 项目概述
本项目在VSCode环境中完成Web登录功能的全面测试，包括手动测试用例设计、自动化测试执行、缺陷报告提交和测试报告生成。

## 项目结构
```
vscode_web_login_test/
├── test_cases/                 # 测试用例文档
│   └── login_test_cases.md
├── automation/                 # 自动化测试脚本
│   ├── login_test.py
│   ├── conftest.py
│   └── requirements.txt
├── defect_reports/             # 缺陷报告
│   └── defect_report_template.md
├── test_reports/               # 测试报告
│   └── test_report_template.md
├── screenshots/                # 测试截图
└── README.md                   # 项目说明
```

## 环境要求
- **VSCode版本**: 1.80.0+
- **Python版本**: 3.8+
- **浏览器**: Chrome 112.0+ / Firefox 111.0+
- **扩展插件**: Python、Pylance、Selenium IDE

## 安装步骤

### 1. 安装Python环境
```bash
# 检查Python版本
python --version

# 安装pip
python -m ensurepip --upgrade
```

### 2. 安装依赖包
```bash
cd automation
pip install -r requirements.txt
```

### 3. 安装浏览器驱动
- **Chrome**: 下载ChromeDriver (与Chrome版本匹配)
- **Firefox**: 下载geckodriver
- 将驱动文件添加到系统PATH

### 4. VSCode扩展配置
```json
{
    "python.pythonPath": "${workspaceFolder}/venv/bin/python",
    "python.testing.pytestArgs": [
        "automation"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true
}
```

## 使用说明

### 手动测试
1. 打开 `test_cases/login_test_cases.md`
2. 按照测试用例执行手动测试
3. 记录测试结果
4. 发现问题时填写缺陷报告

### 自动化测试
```bash
# 运行所有测试
cd automation
pytest login_test.py -v

# 运行指定测试用例
pytest login_test.py::TestLogin::test_valid_login -v

# 生成测试报告
pytest login_test.py --html=../test_reports/automation_report.html
```

### 生成测试报告
1. 收集手动测试结果
2. 运行自动化测试生成报告
3. 填写 `test_reports/test_report_template.md`
4. 生成最终测试报告

## 测试范围
- 用户登录功能
- 用户名/密码验证
- 错误处理机制
- 安全性测试
- 兼容性测试
- 性能测试

## 交付物
1. 测试用例文档
2. 自动化测试脚本
3. 缺陷报告
4. 测试报告
5. 测试截图

## 注意事项
1. 测试前确保测试环境准备就绪
2. 执行自动化测试前检查浏览器驱动配置
3. 及时记录测试过程中的问题
4. 保持测试数据的一致性
5. 定期备份测试结果