#!/usr/bin/env python3
import os
import sys
import json
import time
import requests
import logging
import argparse
from typing import Dict, Any, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('ci_smoke_test')

# 默认配置
DEFAULT_API_BASE = 'http://api:8000'  # CI环境中使用容器名称
DEFAULT_TIMEOUT = 15
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_INTERVAL = 5

class CISmokeTester:
    def __init__(self, api_base: str, timeout: int, max_retries: int, retry_interval: int):
        self.api_base = api_base
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.test_results = {
            'api_health': False,
            'generate_exam': False,
            'grade_item': False,
            'dashboard': False,
            'review': False,
            'overall_result': False,
            'execution_time': 0
        }
        
    def retry(func):
        def wrapper(self, *args, **kwargs):
            retries = 0
            while retries < self.max_retries:
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= self.max_retries:
                        raise
                    logger.warning(f"尝试 {retries}/{self.max_retries} 失败: {str(e)}. 等待 {self.retry_interval} 秒后重试...")
                    time.sleep(self.retry_interval)
        return wrapper

    @retry
    def check_api_health(self) -> bool:
        """检查API服务健康状态"""
        try:
            url = f"{self.api_base}/health"
            response = requests.get(url, timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'ok':
                    logger.info("✅ API服务健康状态正常")
                    self.test_results['api_health'] = True
                    return True
            logger.error(f"❌ API服务健康检查失败: 状态码 {response.status_code}, 响应 {response.text}")
            return False
        except Exception as e:
            logger.error(f"❌ API服务连接失败: {str(e)}")
            raise

    @retry
    def generate_exam(self) -> Optional[Dict[str, Any]]:
        """生成测试试卷"""
        try:
            url = f"{self.api_base}/exams/generate"
            payload = {
                "grade": "junior",
                "subject": "math",
                "chapter": "quadratic",
                "knowledge_points": ["graph_properties"],
                "item_type_ratio": {"single_choice": 1, "subjective": 1},
                "difficulty": 3,
                "num_items": 2
            }
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'paper_id' in data and 'item_ids' in data:
                    logger.info(f"✅ 试卷生成成功: paper_id={data['paper_id']}")
                    self.test_results['generate_exam'] = True
                    return data
            logger.error(f"❌ 试卷生成失败: 状态码 {response.status_code}, 响应 {response.text}")
            return None
        except Exception as e:
            logger.error(f"❌ 试卷生成异常: {str(e)}")
            raise

    @retry
    def grade_item(self, paper_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """对测试试卷进行评分"""
        try:
            if not paper_data or not paper_data.get('item_ids'):
                logger.error("❌ 无效的试卷数据")
                return None
            
            url = f"{self.api_base}/grading/grade"
            item_id = paper_data['item_ids'][0]
            payload = {
                "user_id": 1,
                "paper_id": paper_data['paper_id'],
                "item_id": item_id,
                "answer": "2",
                "steps": ["axis", "vertex"]
            }
            
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'score' in data:
                    logger.info(f"✅ 答案评分成功: score={data['score']}")
                    self.test_results['grade_item'] = True
                    return data
            logger.error(f"❌ 评分失败: 状态码 {response.status_code}, 响应 {response.text}")
            return None
        except Exception as e:
            logger.error(f"❌ 评分异常: {str(e)}")
            raise

    @retry
    def get_dashboard(self) -> Optional[Dict[str, Any]]:
        """获取仪表板数据"""
        try:
            url = f"{self.api_base}/dashboard/metrics"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ 仪表板数据获取成功: responses={data.get('responses', 0)}")
                self.test_results['dashboard'] = True
                return data
            logger.error(f"❌ 仪表板数据获取失败: 状态码 {response.status_code}, 响应 {response.text}")
            return None
        except Exception as e:
            logger.error(f"❌ 仪表板数据获取异常: {str(e)}")
            raise

    @retry
    def generate_review(self, paper_id: int) -> Optional[Dict[str, Any]]:
        """生成试卷讲评"""
        try:
            url = f"{self.api_base}/review"
            payload = {"user_id": 1, "paper_id": paper_id}
            
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ 讲评生成成功")
                self.test_results['review'] = True
                return data
            logger.error(f"❌ 讲评生成失败: 状态码 {response.status_code}, 响应 {response.text}")
            return None
        except Exception as e:
            logger.error(f"❌ 讲评生成异常: {str(e)}")
            raise

    def run(self) -> bool:
        """运行完整的CI冒烟测试"""
        start_time = time.time()
        
        try:
            # 1. 检查API健康状态
            self.check_api_health()
            
            # 2. 生成试卷
            paper_data = self.generate_exam()
            if not paper_data:
                return False
            
            # 3. 评分
            grade_data = self.grade_item(paper_data)
            if not grade_data:
                return False
            
            # 4. 获取仪表板数据
            self.get_dashboard()
            
            # 5. 生成讲评
            self.generate_review(paper_data['paper_id'])
            
            # 计算总体结果（前三个步骤为关键步骤）
            critical_success = (self.test_results['api_health'] and 
                                self.test_results['generate_exam'] and 
                                self.test_results['grade_item'])
            
            self.test_results['overall_result'] = critical_success
            
        except Exception as e:
            logger.error(f"❌ 测试执行异常: {str(e)}")
            self.test_results['overall_result'] = False
        
        # 记录执行时间
        self.test_results['execution_time'] = round(time.time() - start_time, 2)
        
        # 输出测试结果摘要
        self.print_summary()
        
        return self.test_results['overall_result']
        
    def print_summary(self):
        """打印测试结果摘要"""
        logger.info("\n========= 测试结果摘要 ========")
        logger.info(f"API健康检查: {'✅ 成功' if self.test_results['api_health'] else '❌ 失败'}")
        logger.info(f"试卷生成: {'✅ 成功' if self.test_results['generate_exam'] else '❌ 失败'}")
        logger.info(f"答案评分: {'✅ 成功' if self.test_results['grade_item'] else '❌ 失败'}")
        logger.info(f"仪表板数据: {'✅ 成功' if self.test_results['dashboard'] else '❌ 失败'}")
        logger.info(f"讲评生成: {'✅ 成功' if self.test_results['review'] else '❌ 失败'}")
        logger.info(f"执行时间: {self.test_results['execution_time']}秒")
        logger.info(f"总体结果: {'✅ 测试通过' if self.test_results['overall_result'] else '❌ 测试失败'}")
        logger.info("==============================")

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='VenusTA CI环境冒烟测试脚本')
    parser.add_argument('--api-base', type=str, default=DEFAULT_API_BASE,
                        help=f'API基础URL (默认: {DEFAULT_API_BASE})')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT,
                        help=f'请求超时时间(秒) (默认: {DEFAULT_TIMEOUT})')
    parser.add_argument('--max-retries', type=int, default=DEFAULT_MAX_RETRIES,
                        help=f'最大重试次数 (默认: {DEFAULT_MAX_RETRIES})')
    parser.add_argument('--retry-interval', type=int, default=DEFAULT_RETRY_INTERVAL,
                        help=f'重试间隔(秒) (默认: {DEFAULT_RETRY_INTERVAL})')
    
    args = parser.parse_args()
    
    logger.info(f"开始CI环境冒烟测试 (API_BASE: {args.api_base})")
    
    tester = CISmokeTester(
        api_base=args.api_base,
        timeout=args.timeout,
        max_retries=args.max_retries,
        retry_interval=args.retry_interval
    )
    
    success = tester.run()
    
    # 根据测试结果设置退出码
    sys.exit(0 if success else 1)