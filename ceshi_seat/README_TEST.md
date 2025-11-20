# 座位锁定系统测试指南

##  项目概述
本项目包含座位锁定系统的实现和对应的测试脚本，以及在VSCode中运行测试并生成HTML报告的完整指南。

##  项目结构
```
seat_lock_system/
├── app/
│   └── seat_lock.py          # 座位锁定系统实现
├── tests/
│   └── test_seat_lock.py     # 测试脚本
├── requirements.txt          # 项目依赖
└── README.md                 # 项目说明
```

##  在VSCode中运行测试的步骤

###  第一步：安装依赖
```bash
pip install -r requirements.txt
```

###  第二步：配置VSCode测试环境

1. **打开命令面板**：
   - Windows/Linux: Ctrl + Shift + P
   - macOS: Command + Shift + P

2. **选择测试配置**：
   - 输入并选择：`Python: Configure Tests`
   - 选择测试框架：`pytest`
   - 选择测试目录：`tests/`

###  第三步：运行测试并生成HTML报告

**方法一：使用命令行**
```bash
# 运行所有测试并生成HTML报告
pytest tests/ --html=report.html --self-contained-html

# 运行指定测试文件
pytest tests/test_seat_lock.py --html=report.html --self-contained-html

# 详细模式运行
pytest tests/ -v --html=report.html --self-contained-html
```

**方法二：使用VSCode界面**
1. 点击左侧的"测试"图标（烧瓶图标）
2. 点击"运行所有测试"按钮
3. 测试结果会显示在测试面板中

###  第四步：查看测试报告

1. 测试完成后，会生成 `report.html` 文件
2. 在VSCode中右键点击该文件，选择"Open with Live Server"
3. 或者直接用浏览器打开该文件
4. 报告包含：
   - 测试结果摘要
   - 每个测试用例的详细信息
   - 测试通过率统计
   - 测试时长信息

##  测试用例说明

本测试脚本包含以下测试用例：

###  基础功能测试
1. `test_lock_and_expire()` - 测试锁定和过期功能
2. `test_relock_after_expire()` - 测试过期后重新锁定
3. `test_lock_seat_success()` - 测试正常锁定座位
4. `test_lock_already_locked_seat()` - 测试锁定已锁定的座位

###  扩展功能测试
5. `test_unlock_seat()` - 测试解锁座位
6. `test_unlock_unlocked_seat()` - 测试解锁未锁定的座位
7. `test_extend_lock_time()` - 测试延长锁定时间
8. `test_get_lock_info()` - 测试获取锁定信息
9. `test_get_all_locked_seats()` - 测试获取所有锁定座位

##  预期测试结果

**成功结果**：
- 所有测试用例显示为绿色（PASSED）
- 生成的HTML报告显示通过率100%
- 控制台输出显示测试通过信息

**失败处理**：
- 如果测试失败，会显示具体的错误信息
- 检查代码逻辑或测试用例是否正确
- 根据错误提示进行调试

##  常见问题解决

### 1. 模块导入错误
```
ModuleNotFoundError: No module named 'app'
```
**解决方案**：确保在项目根目录下运行测试，或设置PYTHONPATH：
```bash
export PYTHONPATH=.
pytest tests/
```

### 2. 测试报告无法生成
**解决方案**：确保已安装pytest-html：
```bash
pip install pytest-html
```

### 3. VSCode无法找到测试
**解决方案**：
1. 检查测试文件是否以`test_`开头
2. 检查函数是否以`test_`开头
3. 重新配置测试环境

##  作业提交要求

根据课堂要求，您需要提交：
1. **测试代码**：`tests/test_seat_lock.py`
2. **HTML测试报告**：`report.html`
3. **运行截图**：显示所有测试通过的界面截图

确保：
- 所有测试用例都通过（显示绿色）
- HTML报告正确生成
- 截图清晰显示测试结果

##  总结

本指南提供了在VSCode中运行座位锁定系统测试的完整流程。通过编写测试脚本和生成HTML报告，您可以：
- 验证代码的正确性
- 确保功能的完整性
- 生成专业的测试报告
- 提高代码质量和可靠性

按照上述步骤操作，您将能够成功完成测试任务并获得满意的结果！