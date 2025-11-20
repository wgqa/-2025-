#!/usr/bin/env python3
"""
Web登录功能自动化测试脚本
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLogin:
    """登录功能测试类"""
    
    @pytest.fixture(scope="class")
    def setup(self):
        """测试前置条件"""
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 15)
        self.test_url = "https://example.com/login"  # 替换为实际URL
        self.valid_user = ("testuser", "Test@123456")
        
        yield
        
        self.driver.quit()
    
    def test_valid_login(self, setup):
        """测试正确登录"""
        self.driver.get(self.test_url)
        
        # 输入用户名密码
        self.driver.find_element(By.ID, "username").send_keys(self.valid_user[0])
        self.driver.find_element(By.ID, "password").send_keys(self.valid_user[1])
        self.driver.find_element(By.ID, "loginBtn").click()
        
        # 验证登录成功
        welcome_msg = self.wait.until(
            EC.visibility_of_element_located((By.ID, "welcomeMessage"))
        )
        assert "欢迎" in welcome_msg.text
        assert self.valid_user[0] in welcome_msg.text
    
    def test_invalid_password(self, setup):
        """测试错误密码"""
        self.driver.get(self.test_url)
        
        self.driver.find_element(By.ID, "username").send_keys(self.valid_user[0])
        self.driver.find_element(By.ID, "password").send_keys("Wrong@123")
        self.driver.find_element(By.ID, "loginBtn").click()
        
        # 验证错误提示
        error_msg = self.wait.until(
            EC.visibility_of_element_located((By.ID, "errorMessage"))
        )
        assert "用户名或密码错误" in error_msg.text
    
    def test_empty_fields(self, setup):
        """测试空字段验证"""
        self.driver.get(self.test_url)
        
        # 直接点击登录
        self.driver.find_element(By.ID, "loginBtn").click()
        
        # 验证提示信息
        username_error = self.wait.until(
            EC.visibility_of_element_located((By.ID, "usernameError"))
        )
        password_error = self.driver.find_element(By.ID, "passwordError")
        
        assert "用户名不能为空" in username_error.text
        assert "密码不能为空" in password_error.text

if __name__ == "__main__":
    pytest.main(["-v", "login_test.py"])