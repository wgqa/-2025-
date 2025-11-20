#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
容错性测试脚本 - 数据库中断测试
使用Docker模拟数据库故障，测试Flask服务的容错能力
"""

import os
import sys
import time
import json
import logging
import subprocess
import requests
import pytest
from datetime import datetime
from typing import Dict, List, Tuple

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fault_tolerance_test.log'),
        logging.StreamHandler()
    ]
)

class FaultToleranceTester:
    """容错性测试类"""
    
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.docker_compose_file = "docker-compose.yml"
        self.db_container_name = "fault_tolerance_test_db_1"
        self.web_container_name = "fault_tolerance_test_web_1"
        self.test_order_id = f"TEST_{int(time.time())}"
        self.test_amount = 150.75
        
    def run_command(self, command: str) -> Tuple[str, str, int]:
        """运行shell命令"""
        logging.info(f"执行命令: {command}")
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout, result.stderr, result.returncode
    
    def start_services(self) -> bool:
        """启动所有服务"""
        logging.info("启动Docker服务...")
        stdout, stderr, returncode = self.run_command(
            f"docker-compose -f {self.docker_compose_file} up -d"
        )
        
        if returncode != 0:
            logging.error(f"服务启动失败: {stderr}")
            return False
        
        # 等待服务启动完成
        time.sleep(30)
        return self.wait_for_services()
    
    def stop_services(self) -> bool:
        """停止所有服务"""
        logging.info("停止Docker服务...")
        stdout, stderr, returncode = self.run_command(
            f"docker-compose -f {self.docker_compose_file} down"
        )
        
        if returncode != 0:
            logging.error(f"服务停止失败: {stderr}")
            return False
        return True
    
    def restart_services(self) -> bool:
        """重启所有服务"""
        logging.info("重启Docker服务...")
        return self.stop_services() and self.start_services()
    
    def stop_database(self) -> bool:
        """停止数据库容器"""
        logging.info("停止数据库容器...")
        stdout, stderr, returncode = self.run_command(
            f"docker stop {self.db_container_name}"
        )
        
        if returncode != 0:
            logging.error(f"数据库停止失败: {stderr}")
            return False
        return True
    
    def start_database(self) -> bool:
        """启动数据库容器"""
        logging.info("启动数据库容器...")
        stdout, stderr, returncode = self.run_command(
            f"docker start {self.db_container_name}"
        )
        
        if returncode != 0:
            logging.error(f"数据库启动失败: {stderr}")
            return False
        
        # 等待数据库恢复
        time.sleep(20)
        return True
    
    def restart_database(self) -> bool:
        """重启数据库容器"""
        logging.info("重启数据库容器...")
        return self.stop_database() and self.start_database()
    
    def wait_for_services(self, timeout: int = 60) -> bool:
        """等待服务就绪"""
        logging.info("等待服务就绪...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{self.base_url}/health", timeout=5)
                if response.status_code == 200:
                    logging.info("服务已就绪")
                    return True
            except Exception as e:
                logging.warning(f"服务检查失败: {str(e)}")
            
            time.sleep(5)
        
        logging.error("服务启动超时")
        return False
    
    def create_payment(self, order_id: str = None, amount: float = None) -> Tuple[bool, Dict]:
        """创建支付请求"""
        order_id = order_id or self.test_order_id
        amount = amount or self.test_amount
        
        logging.info(f"创建支付请求: order_id={order_id}, amount={amount}")
        
        try:
            response = requests.post(
                f"{self.base_url}/payment",
                json={"order_id": order_id, "amount": amount},
                timeout=30
            )
            
            result = {
                "success": response.status_code in [200, 201],
                "status_code": response.status_code,
                "response": response.json(),
                "timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"支付请求结果: {json.dumps(result, indent=2)}")
            return result["success"], result
            
        except requests.exceptions.RequestException as e:
            error_result = {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            logging.error(f"支付请求异常: {str(e)}")
            return False, error_result
    
    def get_payment(self, order_id: str = None) -> Tuple[bool, Dict]:
        """查询支付状态"""
        order_id = order_id or self.test_order_id
        
        logging.info(f"查询支付状态: order_id={order_id}")
        
        try:
            response = requests.get(
                f"{self.base_url}/payment/{order_id}",
                timeout=10
            )
            
            result = {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "response": response.json(),
                "timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"查询结果: {json.dumps(result, indent=2)}")
            return result["success"], result
            
        except requests.exceptions.RequestException as e:
            error_result = {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            logging.error(f"查询异常: {str(e)}")
            return False, error_result
    
    def check_health(self) -> Tuple[bool, Dict]:
        """检查服务健康状态"""
        logging.info("检查服务健康状态...")
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            
            result = {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "database_status": response.json().get("database", "unknown"),
                "timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"健康检查结果: {json.dumps(result, indent=2)}")
            return result["success"], result
            
        except requests.exceptions.RequestException as e:
            error_result = {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            logging.error(f"健康检查异常: {str(e)}")
            return False, error_result
    
    def test_normal_operation(self) -> Dict:
        """测试正常操作流程"""
        logging.info("=== 开始正常操作测试 ===")
        
        test_result = {
            "test_case": "正常操作流程",
            "timestamp": datetime.now().isoformat(),
            "steps": []
        }
        
        try:
            # 步骤1: 检查服务健康状态
            step1_success, step1_result = self.check_health()
            test_result["steps"].append({
                "step": "检查服务健康状态",
                "success": step1_success,
                "result": step1_result
            })
            
            # 步骤2: 创建支付请求
            step2_success, step2_result = self.create_payment(
                order_id=f"NORMAL_{int(time.time())}",
                amount=100.00
            )
            test_result["steps"].append({
                "step": "创建支付请求",
                "success": step2_success,
                "result": step2_result
            })
            
            # 步骤3: 查询支付状态
            if step2_success:
                order_id = step2_result["response"]["payment"]["order_id"]
                step3_success, step3_result = self.get_payment(order_id)
            else:
                step3_success, step3_result = False, {"error": "跳过查询，创建支付失败"}
            
            test_result["steps"].append({
                "step": "查询支付状态",
                "success": step3_success,
                "result": step3_result
            })
            
            # 总结结果
            test_result["success"] = all([step1_success, step2_success, step3_success])
            test_result["status"] = "PASS" if test_result["success"] else "FAIL"
            
        except Exception as e:
            test_result["success"] = False
            test_result["status"] = "ERROR"
            test_result["error"] = str(e)
            logging.error(f"正常操作测试失败: {str(e)}")
        
        logging.info(f"正常操作测试结果: {test_result['status']}")
        return test_result
    
    def test_database_failure_during_payment(self) -> Dict:
        """测试支付过程中数据库中断"""
        logging.info("=== 开始支付过程中数据库中断测试 ===")
        
        test_result = {
            "test_case": "支付过程中数据库中断",
            "timestamp": datetime.now().isoformat(),
            "steps": []
        }
        
        try:
            # 步骤1: 确保服务正常
            step1_success, step1_result = self.check_health()
            test_result["steps"].append({
                "step": "检查初始服务状态",
                "success": step1_success,
                "result": step1_result
            })
            
            if not step1_success:
                raise Exception("初始服务状态异常")
            
            # 步骤2: 开始创建支付请求（在请求过程中中断数据库）
            logging.info("开始创建支付请求并中断数据库...")
            
            # 使用线程同时执行支付请求和数据库中断
            import threading
            
            payment_result = None
            payment_order_id = f"FAIL_{int(time.time())}"
            
            def create_payment_thread():
                nonlocal payment_result
                payment_result = self.create_payment(
                    order_id=payment_order_id,
                    amount=200.00
                )
            
            def stop_database_thread():
                # 等待1秒后中断数据库
                time.sleep(1)
                self.stop_database()
            
            # 启动线程
            payment_thread = threading.Thread(target=create_payment_thread)
            stop_thread = threading.Thread(target=stop_database_thread)
            
            payment_thread.start()
            stop_thread.start()
            
            payment_thread.join()
            stop_thread.join()
            
            step2_success, step2_result = payment_result
            test_result["steps"].append({
                "step": "支付过程中中断数据库",
                "success": not step2_success,  # 预期应该失败
                "result": step2_result
            })
            
            # 步骤3: 检查服务状态（应该显示数据库断开）
            step3_success, step3_result = self.check_health()
            test_result["steps"].append({
                "step": "检查数据库中断后的服务状态",
                "success": not step3_success,  # 预期应该不健康
                "result": step3_result
            })
            
            # 步骤4: 恢复数据库
            step4_success = self.start_database()
            test_result["steps"].append({
                "step": "恢复数据库",
                "success": step4_success,
                "result": {"message": "数据库恢复完成" if step4_success else "数据库恢复失败"}
            })
            
            # 步骤5: 等待服务恢复并检查
            if step4_success:
                time.sleep(30)
                step5_success, step5_result = self.check_health()
            else:
                step5_success, step5_result = False, {"error": "跳过检查，数据库未恢复"}
            
            test_result["steps"].append({
                "step": "检查服务恢复状态",
                "success": step5_success,
                "result": step5_result
            })
            
            # 步骤6: 验证数据一致性（查询之前的支付是否存在）
            if step5_success:
                step6_success, step6_result = self.get_payment(payment_order_id)
                # 如果支付失败，订单不应该存在
                step6_success = not step6_success
            else:
                step6_success, step6_result = False, {"error": "跳过验证，服务未恢复"}
            
            test_result["steps"].append({
                "step": "验证数据一致性",
                "success": step6_success,
                "result": step6_result
            })
            
            # 总结结果（关键步骤：步骤2、4、5、6应该成功）
            critical_steps = [
                step2_success,  # 支付应该失败
                step4_success,  # 数据库应该恢复
                step5_success,  # 服务应该恢复
                step6_success   # 数据应该一致
            ]
            
            test_result["success"] = all(critical_steps)
            test_result["status"] = "PASS" if test_result["success"] else "FAIL"
            
        except Exception as e:
            test_result["success"] = False
            test_result["status"] = "ERROR"
            test_result["error"] = str(e)
            logging.error(f"数据库中断测试失败: {str(e)}")
        
        logging.info(f"数据库中断测试结果: {test_result['status']}")
        return test_result
    
    def test_database_disconnected_payment(self) -> Dict:
        """测试数据库断开时的支付请求"""
        logging.info("=== 开始数据库断开时支付请求测试 ===")
        
        test_result = {
            "test_case": "数据库断开时支付请求",
            "timestamp": datetime.now().isoformat(),
            "steps": []
        }
        
        try:
            # 步骤1: 确保服务正常
            step1_success, step1_result = self.check_health()
            test_result["steps"].append({
                "step": "检查初始服务状态",
                "success": step1_success,
                "result": step1_result
            })
            
            if not step1_success:
                raise Exception("初始服务状态异常")
            
            # 步骤2: 停止数据库
            step2_success = self.stop_database()
            test_result["steps"].append({
                "step": "停止数据库",
                "success": step2_success,
                "result": {"message": "数据库停止完成" if step2_success else "数据库停止失败"}
            })
            
            if not step2_success:
                raise Exception("数据库停止失败")
            
            # 步骤3: 等待数据库完全停止
            time.sleep(10)
            
            # 步骤4: 尝试创建支付请求
            step4_success, step4_result = self.create_payment(
                order_id=f"DISCON_{int(time.time())}",
                amount=300.00
            )
            test_result["steps"].append({
                "step": "数据库断开时创建支付请求",
                "success": not step4_success,  # 预期应该失败
                "result": step4_result
            })
            
            # 步骤5: 检查错误处理是否正确
            error_handling_correct = False
            if not step4_success:
                response = step4_result.get("response", {})
                error_msg = response.get("error", "") or step4_result.get("error", "")
                error_handling_correct = "数据库" in error_msg or "503" in str(step4_result.get("status_code"))
            
            test_result["steps"].append({
                "step": "验证错误处理",
                "success": error_handling_correct,
                "result": {"error_message": error_msg}
            })
            
            # 步骤6: 恢复数据库
            step6_success = self.start_database()
            test_result["steps"].append({
                "step": "恢复数据库",
                "success": step6_success,
                "result": {"message": "数据库恢复完成" if step6_success else "数据库恢复失败"}
            })
            
            # 步骤7: 检查服务恢复
            if step6_success:
                time.sleep(30)
                step7_success, step7_result = self.check_health()
            else:
                step7_success, step7_result = False, {"error": "跳过检查，数据库未恢复"}
            
            test_result["steps"].append({
                "step": "检查服务恢复",
                "success": step7_success,
                "result": step7_result
            })
            
            # 总结结果
            critical_steps = [
                step2_success,          # 数据库应该停止成功
                not step4_success,      # 支付应该失败
                error_handling_correct, # 错误处理应该正确
                step6_success,          # 数据库应该恢复
                step7_success           # 服务应该恢复
            ]
            
            test_result["success"] = all(critical_steps)
            test_result["status"] = "PASS" if test_result["success"] else "FAIL"
            
        except Exception as e:
            test_result["success"] = False
            test_result["status"] = "ERROR"
            test_result["error"] = str(e)
            logging.error(f"数据库断开测试失败: {str(e)}")
        
        logging.info(f"数据库断开测试结果: {test_result['status']}")
        return test_result
    
    def test_retry_mechanism(self) -> Dict:
        """测试重试机制"""
        logging.info("=== 开始重试机制测试 ===")
        
        test_result = {
            "test_case": "数据库暂时不可用时的重试机制",
            "timestamp": datetime.now().isoformat(),
            "steps": []
        }
        
        try:
            # 步骤1: 确保服务正常
            step1_success, step1_result = self.check_health()
            test_result["steps"].append({
                "step": "检查初始服务状态",
                "success": step1_success,
                "result": step1_result
            })
            
            if not step1_success:
                raise Exception("初始服务状态异常")
            
            # 步骤2: 临时停止数据库
            logging.info("临时停止数据库2秒...")
            stop_result = self.run_command(f"docker stop {self.db_container_name}")
            
            # 等待1秒
            time.sleep(1)
            
            # 步骤3: 创建支付请求（应该触发重试）
            step3_success, step3_result = self.create_payment(
                order_id=f"RETRY_{int(time.time())}",
                amount=400.00
            )
            
            # 立即恢复数据库
            self.start_database()
            
            test_result["steps"].append({
                "step": "测试重试机制",
                "success": step3_success,  # 预期应该成功（重试后）
                "result": step3_result
            })
            
            # 步骤4: 检查重试是否生效
            retry_occurred = False
            if step3_success:
                # 检查日志中是否有重试信息
                with open("app.log", "r") as f:
                    log_content = f.read()
                    retry_occurred = "重试" in log_content or "retry" in log_content.lower()
            
            test_result["steps"].append({
                "step": "验证重试机制生效",
                "success": retry_occurred,
                "result": {"retry_occurred": retry_occurred}
            })
            
            # 步骤5: 验证数据一致性
            if step3_success:
                order_id = step3_result["response"]["payment"]["order_id"]
                step5_success, step5_result = self.get_payment(order_id)
            else:
                step5_success, step5_result = False, {"error": "跳过验证，支付失败"}
            
            test_result["steps"].append({
                "step": "验证数据一致性",
                "success": step5_success,
                "result": step5_result
            })
            
            # 总结结果
            critical_steps = [
                step3_success,  # 支付应该成功（重试后）
                retry_occurred, # 重试机制应该生效
                step5_success   # 数据应该一致
            ]
            
            test_result["success"] = all(critical_steps)
            test_result["status"] = "PASS" if test_result["success"] else "FAIL"
            
        except Exception as e:
            test_result["success"] = False
            test_result["status"] = "ERROR"
            test_result["error"] = str(e)
            logging.error(f"重试机制测试失败: {str(e)}")
            # 确保数据库恢复
            self.start_database()
        
        logging.info(f"重试机制测试结果: {test_result['status']}")
        return test_result
    
    def run_all_tests(self) -> Dict:
        """运行所有测试用例"""
        logging.info("=== 开始执行所有容错性测试 ===")
        
        test_summary = {
            "test_suite": "Flask服务容错性测试",
            "timestamp": datetime.now().isoformat(),
            "test_cases": [],
            "summary": {}
        }
        
        try:
            # 清理之前的环境
            self.stop_services()
            
            # 启动服务
            if not self.start_services():
                raise Exception("服务启动失败，无法执行测试")
            
            # 执行测试用例
            test_cases = [
                self.test_normal_operation,
                self.test_database_failure_during_payment,
                self.test_database_disconnected_payment,
                self.test_retry_mechanism
            ]
            
            for test_case in test_cases:
                result = test_case()
                test_summary["test_cases"].append(result)
            
            # 生成总结
            total_tests = len(test_summary["test_cases"])
            passed_tests = len([tc for tc in test_summary["test_cases"] if tc["status"] == "PASS"])
            failed_tests = len([tc for tc in test_summary["test_cases"] if tc["status"] == "FAIL"])
            error_tests = len([tc for tc in test_summary["test_cases"] if tc["status"] == "ERROR"])
            
            test_summary["summary"] = {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "error_tests": error_tests,
                "pass_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
                "overall_status": "PASS" if passed_tests == total_tests else "FAIL"
            }
            
            logging.info(f"=== 测试总结 ===")
            logging.info(f"总测试用例: {total_tests}")
            logging.info(f"通过: {passed_tests}")
            logging.info(f"失败: {failed_tests}")
            logging.info(f"错误: {error_tests}")
            logging.info(f"通过率: {test_summary['summary']['pass_rate']:.1f}%")
            logging.info(f"总体状态: {test_summary['summary']['overall_status']}")
            
        except Exception as e:
            logging.error(f"测试套件执行失败: {str(e)}")
            test_summary["error"] = str(e)
            test_summary["summary"] = {"overall_status": "ERROR"}
        
        finally:
            # 清理环境
            self.stop_services()
            
            # 保存测试报告
            self.save_test_report(test_summary)
        
        return test_summary
    
    def save_test_report(self, report_data: Dict):
        """保存测试报告"""
        report_filename = f"fault_tolerance_test_report_{int(time.time())}.json"
        
        try:
            with open(report_filename, "w", encoding="utf-8") as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            
            logging.info(f"测试报告已保存: {report_filename}")
            
            # 生成HTML报告
            self.generate_html_report(report_data, report_filename.replace(".json", ".html"))
            
        except Exception as e:
            logging.error(f"保存测试报告失败: {str(e)}")
    
    def generate_html_report(self, report_data: Dict, filename: str):
        """生成HTML报告"""
        html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask服务容错性测试报告</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.6;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background-color: #f5f5f5;
            border-radius: 8px;
        }}
        .summary {{
            background-color: #e8f4f8;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .test-case {{
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
        }}
        .test-case.pass {{
            border-color: #28a745;
            background-color: #f8f9fa;
        }}
        .test-case.fail {{
            border-color: #dc3545;
            background-color: #f8f9fa;
        }}
        .test-case.error {{
            border-color: #ffc107;
            background-color: #f8f9fa;
        }}
        .step {{
            margin-bottom: 15px;
            padding: 10px;
            background-color: #f9f9f9;
            border-radius: 4px;
        }}
        .status-pass {{
            color: #28a745;
            font-weight: bold;
        }}
        .status-fail {{
            color: #dc3545;
            font-weight: bold;
        }}
        .status-error {{
            color: #ffc107;
            font-weight: bold;
        }}
        .timestamp {{
            color: #666;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Flask服务容错性测试报告</h1>
        <p class="timestamp">测试时间: {report_data['timestamp']}</p>
    </div>

    <div class="summary">
        <h2>测试总结</h2>
        <p><strong>总测试用例:</strong> {report_data['summary']['total_tests']}</p>
        <p><strong>通过:</strong> <span class="status-pass">{report_data['summary']['passed_tests']}</span></p>
        <p><strong>失败:</strong> <span class="status-fail">{report_data['summary']['failed_tests']}</span></p>
        <p><strong>错误:</strong> <span class="status-error">{report_data['summary']['error_tests']}</span></p>
        <p><strong>通过率:</strong> {report_data['summary']['pass_rate']:.1f}%</p>
        <p><strong>总体状态:</strong> 
            <span class="status-{report_data['summary']['overall_status'].lower()}">
                {report_data['summary']['overall_status']}
            </span>
        </p>
    </div>

    <h2>测试用例详情</h2>
"""

        for test_case in report_data['test_cases']:
            html_content += f"""
    <div class="test-case {test_case['status'].lower()}">
        <h3>{test_case['test_case']}</h3>
        <p class="timestamp">执行时间: {test_case['timestamp']}</p>
        <p><strong>状态:</strong> <span class="status-{test_case['status'].lower()}">{test_case['status']}</span></p>
        
        <h4>测试步骤:</h4>
"""
            
            for i, step in enumerate(test_case['steps'], 1):
                step_status = "pass" if step['success'] else "fail"
                html_content += f"""
        <div class="step">
            <p><strong>步骤 {i}:</strong> {step['step']}</p>
            <p><strong>状态:</strong> <span class="status-{step_status}">{step_status.upper()}</span></p>
            <pre>{json.dumps(step['result'], ensure_ascii=False, indent=2)}</pre>
        </div>
"""
            
            if 'error' in test_case:
                html_content += f"""
        <div class="error">
            <p><strong>错误信息:</strong> {test_case['error']}</p>
        </div>
"""
            
            html_content += """
    </div>
"""

        html_content += """
</body>
</html>
        """
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html_content)
            logging.info(f"HTML报告已生成: {filename}")
        except Exception as e:
            logging.error(f"生成HTML报告失败: {str(e)}")

def main():
    """主函数"""
    try:
        tester = FaultToleranceTester()
        result = tester.run_all_tests()
        
        # 输出结果摘要
        print("\n" + "="*60)
        print("Flask服务容错性测试完成")
        print("="*60)
        print(f"测试时间: {result['timestamp']}")
        print(f"总测试用例: {result['summary']['total_tests']}")
        print(f"通过: {result['summary']['passed_tests']}")
        print(f"失败: {result['summary']['failed_tests']}")
        print(f"错误: {result['summary']['error_tests']}")
        print(f"通过率: {result['summary']['pass_rate']:.1f}%")
        print(f"总体状态: {result['summary']['overall_status']}")
        print("="*60)
        
        # 根据测试结果返回相应的退出码
        if result['summary']['overall_status'] == "PASS":
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        logging.info("测试被用户中断")
        sys.exit(1)
    except Exception as e:
        logging.error(f"测试执行失败: {str(e)}")
        print(f"测试执行失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()