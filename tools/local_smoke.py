import pytest
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Running local smoke tests...")

# 直接运行pytest测试
if __name__ == "__main__":
    # 执行测试文件
    test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "api", "app", "tests", "test_smoke.py")
    if os.path.exists(test_file):
        result = pytest.main(["-q", test_file])
        if result == 0:
            print("✅ Local smoke tests passed successfully!")
        else:
            print("❌ Local smoke tests failed")
    else:
        print(f"❌ Test file not found: {test_file}")