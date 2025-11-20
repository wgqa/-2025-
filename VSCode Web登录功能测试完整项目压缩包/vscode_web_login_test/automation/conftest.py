#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pytest配置文件
为Web登录功能测试提供全局配置和fixture
"""

import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@pytest.fixture(scope="session")
def browser_type(request):
    """获取浏览器类型，默认Chrome"""
    return request.config.getoption("--browser", default="chrome")

@pytest.fixture(scope="session")
def headless_mode(request):
    """获取无头模式配置，默认False"""
    return request.config.getoption("--headless", default=False)

@pytest.fixture(scope="session")
def base_url(request):
    """获取基础URL"""
    return request.config.getoption("--base-url", default="https://example.com")

@pytest.fixture(scope="session")
def driver(browser_type, headless_mode, base_url):
    """全局WebDriver fixture"""
    logging.info(f"初始化{browser_type}浏览器...")
    
    driver = None
    try:
        if browser_type.lower() == "chrome":
            chrome_options = Options()
            if headless_mode:
                chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            # 添加实验性选项
            chrome_options.add_experimental_option(
                "excludeSwitches", ["enable-automation"]
            )
            chrome_options.add_experimental_option(
                "prefs", {"credentials_enable_service": False}
            )
            
            driver = webdriver.Chrome(options=chrome_options)
            
        elif browser_type.lower() == "firefox":
            firefox_options = FirefoxOptions()
            if headless_mode:
                firefox_options.add_argument("--headless")
            driver = webdriver.Firefox(options=firefox_options)
            
        elif browser_type.lower() == "edge":
            from selenium.webdriver.edge.options import Options as EdgeOptions
            edge_options = EdgeOptions()
            if headless_mode:
                edge_options.add_argument("--headless=new")
            driver = webdriver.Edge(options=edge_options)
            
        else:
            raise ValueError(f"不支持的浏览器类型: {browser_type}")
        
        # 设置隐式等待
        driver.implicitly_wait(10)
        logging.info(f"{browser_type}浏览器初始化完成")
        
        # 访问基础URL
        driver.get(base_url)
        logging.info(f"访问基础URL: {base_url}")
        
        yield driver
        
    finally:
        if driver:
            logging.info("关闭浏览器...")
            driver.quit()
            logging.info("浏览器已关闭")

@pytest.fixture(scope="function")
def clean_driver(driver):
    """每次测试前清理浏览器状态"""
    yield driver
    
    # 清理cookies和localStorage
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    
    # 刷新页面
    driver.refresh()
    logging.info("浏览器状态已清理")

@pytest.fixture(scope="function")
def login_page(driver, base_url):
    """登录页面fixture"""
    login_url = f"{base_url}/login"
    driver.get(login_url)
    logging.info(f"导航到登录页面: {login_url}")
    return driver

@pytest.fixture(scope="session")
def test_data():
    """测试数据fixture"""
    return {
        "valid_user": {
            "username": "testuser",
            "password": "Test@123456"
        },
        "invalid_user": {
            "username": "wronguser",
            "password": "Wrong@123"
        },
        "admin_user": {
            "username": "admin",
            "password": "Admin@123456"
        }
    }

def pytest_addoption(parser):
    """添加命令行选项"""
    parser.addoption(
        "--browser",
        action="store",
        help="浏览器类型: chrome, firefox, edge"
    )
    
    parser.addoption(
        "--headless",
        action="store_true",
        help="启用无头模式"
    )
    
    parser.addoption(
        "--base-url",
        action="store",
        help="测试基础URL"
    )

def pytest_configure(config):
    """配置pytest"""
    # 设置测试报告标题
    config._metadata["项目名称"] = "Web登录功能测试"
    config._metadata["测试环境"] = config.getoption("--browser")
    config._metadata["基础URL"] = config.getoption("--base-url")
    
    # 创建截图目录
    screenshot_dir = "../screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
        logging.info(f"创建截图目录: {screenshot_dir}")

def pytest_html_report_title(report):
    """设置HTML报告标题"""
    report.title = "Web登录功能自动化测试报告"

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    """自定义测试报告"""
    outcome = yield
    report = outcome.get_result()
    
    # 添加测试用例属性到报告
    if hasattr(item, "funcargs"):
        driver = item.funcargs.get("driver")
        if driver and report.when == "call" and report.failed:
            # 失败时自动截图
            try:
                import time
                screenshot_name = f"failure_{item.name}_{int(time.time())}.png"
                screenshot_path = f"../screenshots/{screenshot_name}"
                driver.save_screenshot(screenshot_path)
                logging.info(f"测试失败截图: {screenshot_path}")
                
                # 将截图添加到HTML报告
                if hasattr(report, "extra"):
                    report.extra.append(pytest_html.extras.image(screenshot_path))
            except Exception as e:
                logging.error(f"截图失败: {str(e)}")

# 导入pytest-html插件（如果安装）
try:
    import pytest_html
except ImportError:
    logging.warning("pytest-html插件未安装，HTML报告功能受限")