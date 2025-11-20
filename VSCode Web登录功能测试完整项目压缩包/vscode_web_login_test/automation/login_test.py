#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web登录功能自动化测试脚本
在VSCode环境中执行Web登录功能的自动化测试
"""

import pytest
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('login_test.log'),
        logging.StreamHandler()
    ]
)

class TestLogin:
    """Web登录功能测试类"""
    
    @pytest.fixture(scope="class")
    def setup(self):
        """测试前置条件"""
        logging.info("开始初始化测试环境...")
        
        # 配置Chrome浏览器选项
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        
        # 初始化WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 15)
        
        # 测试数据
        self.test_url = "https://example.com/login"  # 请替换为实际的登录页面URL
        self.valid_username = "testuser"
        self.valid_password = "Test@123456"
        self.invalid_username = "wronguser"
        self.invalid_password = "Wrong@123"
        
        logging.info("测试环境初始化完成")
        yield
        logging.info("开始清理测试环境...")
        self.driver.quit()
        logging.info("测试环境清理完成")
    
    def capture_screenshot(self, test_name):
        """截图功能"""
        screenshot_path = f"../screenshots/{test_name}_{int(time.time())}.png"
        self.driver.save_screenshot(screenshot_path)
        logging.info(f"截图已保存: {screenshot_path}")
        return screenshot_path
    
    def test_valid_login(self, setup):
        """测试用例：正确用户名密码登录"""
        logging.info("开始执行测试用例：正确用户名密码登录")
        
        try:
            # 打开登录页面
            self.driver.get(self.test_url)
            logging.info(f"打开登录页面: {self.test_url}")
            
            # 输入用户名
            username_input = self.wait.until(
                EC.visibility_of_element_located((By.ID, "username"))
            )
            username_input.clear()
            username_input.send_keys(self.valid_username)
            logging.info(f"输入用户名: {self.valid_username}")
            
            # 输入密码
            password_input = self.driver.find_element(By.ID, "password")
            password_input.clear()
            password_input.send_keys(self.valid_password)
            logging.info("输入密码: ******")
            
            # 点击登录按钮
            login_button = self.driver.find_element(By.ID, "loginBtn")
            login_button.click()
            logging.info("点击登录按钮")
            
            # 验证登录成功
            welcome_message = self.wait.until(
                EC.visibility_of_element_located((By.ID, "welcomeMessage"))
            )
            
            assert "欢迎" in welcome_message.text, "登录成功提示不正确"
            assert self.valid_username in welcome_message.text, "用户名显示不正确"
            
            # 验证页面跳转
            assert "dashboard" in self.driver.current_url, "页面未跳转到主页"
            
            logging.info("测试用例执行成功")
            self.capture_screenshot("valid_login_success")
            
        except Exception as e:
            logging.error(f"测试用例执行失败: {str(e)}")
            self.capture_screenshot("valid_login_failure")
            raise
    
    def test_invalid_username_login(self, setup):
        """测试用例：错误用户名登录"""
        logging.info("开始执行测试用例：错误用户名登录")
        
        try:
            self.driver.get(self.test_url)
            
            # 输入错误用户名
            username_input = self.wait.until(
                EC.visibility_of_element_located((By.ID, "username"))
            )
            username_input.clear()
            username_input.send_keys(self.invalid_username)
            
            # 输入正确密码
            password_input = self.driver.find_element(By.ID, "password")
            password_input.clear()
            password_input.send_keys(self.valid_password)
            
            # 点击登录
            self.driver.find_element(By.ID, "loginBtn").click()
            
            # 验证错误提示
            error_message = self.wait.until(
                EC.visibility_of_element_located((By.ID, "errorMessage"))
            )
            
            assert "用户名或密码错误" in error_message.text, "错误提示不正确"
            assert self.test_url in self.driver.current_url, "页面不应该跳转"
            
            logging.info("测试用例执行成功")
            self.capture_screenshot("invalid_username_login")
            
        except Exception as e:
            logging.error(f"测试用例执行失败: {str(e)}")
            self.capture_screenshot("invalid_username_login_failure")
            raise
    
    def test_invalid_password_login(self, setup):
        """测试用例：错误密码登录"""
        logging.info("开始执行测试用例：错误密码登录")
        
        try:
            self.driver.get(self.test_url)
            
            # 输入正确用户名
            username_input = self.wait.until(
                EC.visibility_of_element_located((By.ID, "username"))
            )
            username_input.clear()
            username_input.send_keys(self.valid_username)
            
            # 输入错误密码
            password_input = self.driver.find_element(By.ID, "password")
            password_input.clear()
            password_input.send_keys(self.invalid_password)
            
            # 点击登录
            self.driver.find_element(By.ID, "loginBtn").click()
            
            # 验证错误提示
            error_message = self.wait.until(
                EC.visibility_of_element_located((By.ID, "errorMessage"))
            )
            
            assert "用户名或密码错误" in error_message.text, "错误提示不正确"
            assert self.test_url in self.driver.current_url, "页面不应该跳转"
            
            logging.info("测试用例执行成功")
            self.capture_screenshot("invalid_password_login")
            
        except Exception as e:
            logging.error(f"测试用例执行失败: {str(e)}")
            self.capture_screenshot("invalid_password_login_failure")
            raise
    
    def test_empty_fields_validation(self, setup):
        """测试用例：空字段验证"""
        logging.info("开始执行测试用例：空字段验证")
        
        try:
            self.driver.get(self.test_url)
            
            # 直接点击登录按钮（不输入任何内容）
            self.driver.find_element(By.ID, "loginBtn").click()
            
            # 验证用户名空字段提示
            username_error = self.wait.until(
                EC.visibility_of_element_located((By.ID, "usernameError"))
            )
            assert "用户名不能为空" in username_error.text, "用户名空字段提示不正确"
            
            # 验证密码空字段提示
            password_error = self.driver.find_element(By.ID, "passwordError")
            assert "密码不能为空" in password_error.text, "密码空字段提示不正确"
            
            logging.info("测试用例执行成功")
            self.capture_screenshot("empty_fields_validation")
            
        except Exception as e:
            logging.error(f"测试用例执行失败: {str(e)}")
            self.capture_screenshot("empty_fields_validation_failure")
            raise
    
    def test_remember_me_functionality(self, setup):
        """测试用例：记住密码功能"""
        logging.info("开始执行测试用例：记住密码功能")
        
        try:
            self.driver.get(self.test_url)
            
            # 输入用户名密码并勾选记住我
            self.driver.find_element(By.ID, "username").send_keys(self.valid_username)
            self.driver.find_element(By.ID, "password").send_keys(self.valid_password)
            
            remember_me_checkbox = self.driver.find_element(By.ID, "rememberMe")
            if not remember_me_checkbox.is_selected():
                remember_me_checkbox.click()
            
            self.driver.find_element(By.ID, "loginBtn").click()
            
            # 验证登录成功
            self.wait.until(
                EC.visibility_of_element_located((By.ID, "welcomeMessage"))
            )
            
            # 退出系统
            self.driver.find_element(By.ID, "logoutBtn").click()
            logging.info("退出系统")
            
            # 重新打开登录页面
            self.driver.get(self.test_url)
            logging.info("重新打开登录页面")
            
            # 验证用户名是否被记住
            username_input = self.wait.until(
                EC.visibility_of_element_located((By.ID, "username"))
            )
            
            assert username_input.get_attribute("value") == self.valid_username, "用户名未被记住"
            
            # 验证密码是否为空
            password_input = self.driver.find_element(By.ID, "password")
            assert password_input.get_attribute("value") == "", "密码不应该被记住"
            
            logging.info("测试用例执行成功")
            self.capture_screenshot("remember_me_functionality")
            
        except Exception as e:
            logging.error(f"测试用例执行失败: {str(e)}")
            self.capture_screenshot("remember_me_functionality_failure")
            raise
    
    def test_sql_injection_protection(self, setup):
        """测试用例：SQL注入防护"""
        logging.info("开始执行测试用例：SQL注入防护")
        
        try:
            self.driver.get(self.test_url)
            
            # 输入SQL注入字符串
            sql_injection_username = "' OR 1=1 --"
            self.driver.find_element(By.ID, "username").send_keys(sql_injection_username)
            self.driver.find_element(By.ID, "password").send_keys("任意密码")
            
            self.driver.find_element(By.ID, "loginBtn").click()
            
            # 验证是否防御成功
            error_message = self.wait.until(
                EC.visibility_of_element_located((By.ID, "errorMessage"))
            )
            
            # 应该显示正常的错误提示，而不是登录成功
            assert "用户名或密码错误" in error_message.text or "格式不正确" in error_message.text
            assert "dashboard" not in self.driver.current_url, "SQL注入攻击成功，系统存在安全漏洞"
            
            logging.info("测试用例执行成功")
            self.capture_screenshot("sql_injection_protection")
            
        except Exception as e:
            logging.error(f"测试用例执行失败: {str(e)}")
            self.capture_screenshot("sql_injection_protection_failure")
            raise
    
    def test_consecutive_login_failures(self, setup):
        """测试用例：连续登录失败锁定"""
        logging.info("开始执行测试用例：连续登录失败锁定")
        
        try:
            self.driver.get(self.test_url)
            
            # 连续3次使用错误密码登录
            for attempt in range(3):
                self.driver.find_element(By.ID, "username").send_keys(self.valid_username)
                self.driver.find_element(By.ID, "password").send_keys(f"WrongPass{attempt}")
                self.driver.find_element(By.ID, "loginBtn").click()
                
                if attempt < 2:
                    # 前两次应该显示普通错误
                    error_message = self.wait.until(
                        EC.visibility_of_element_located((By.ID, "errorMessage"))
                    )
                    assert "用户名或密码错误" in error_message.text
                    
                    # 清空输入框
                    self.driver.find_element(By.ID, "username").clear()
                    self.driver.find_element(By.ID, "password").clear()
                else:
                    # 第三次应该显示锁定提示
                    lock_message = self.wait.until(
                        EC.visibility_of_element_located((By.ID, "lockMessage"))
                    )
                    assert "连续3次登录失败" in lock_message.text
                    assert "账号已锁定" in lock_message.text
                    assert "15分钟" in lock_message.text
            
            logging.info("测试用例执行成功")
            self.capture_screenshot("consecutive_login_failures")
            
        except Exception as e:
            logging.error(f"测试用例执行失败: {str(e)}")
            self.capture_screenshot("consecutive_login_failures_failure")
            raise
    
    def test_login_performance(self, setup):
        """测试用例：登录响应时间"""
        logging.info("开始执行测试用例：登录响应时间")
        
        try:
            self.driver.get(self.test_url)
            
            # 记录开始时间
            start_time = time.time()
            
            # 输入用户名密码
            self.driver.find_element(By.ID, "username").send_keys(self.valid_username)
            self.driver.find_element(By.ID, "password").send_keys(self.valid_password)
            
            # 点击登录并记录时间
            login_button = self.driver.find_element(By.ID, "loginBtn")
            login_button.click()
            
            # 等待页面加载完成
            self.wait.until(
                EC.visibility_of_element_located((By.ID, "welcomeMessage"))
            )
            
            # 计算响应时间
            response_time = time.time() - start_time
            logging.info(f"登录响应时间: {response_time:.2f}秒")
            
            # 验证响应时间是否在可接受范围内
            assert response_time < 2.0, f"登录响应时间过长: {response_time:.2f}秒"
            
            logging.info("测试用例执行成功")
            self.capture_screenshot("login_performance")
            
        except Exception as e:
            logging.error(f"测试用例执行失败: {str(e)}")
            self.capture_screenshot("login_performance_failure")
            raise

if __name__ == "__main__":
    # 运行所有测试用例
    pytest.main([
        "-v",
        "--html=../test_reports/automation_report.html",
        "--self-contained-html",
        "login_test.py"
    ])