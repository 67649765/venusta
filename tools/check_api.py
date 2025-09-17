import urllib.request
import json

def check_url(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                return True, data
            else:
                return False, f"HTTP error: {response.status}"
    except Exception as e:
        return False, str(e)

print("=== API Status Check ===")

# 检查API健康状态
health_success, health_data = check_url("http://localhost:8000/health")
if health_success:
    print(f"✅ API Health: {health_data['status']}")
else:
    print(f"❌ API service check failed: {health_data}")

# 获取仪表板指标
metrics_success, metrics_data = check_url("http://localhost:8000/dashboard/metrics")
if metrics_success:
    print(f"✅ Dashboard: responses={metrics_data['responses']}, kappa={metrics_data['kappa']}, mae={metrics_data['mae']}")
else:
    print(f"❌ Dashboard check failed: {metrics_data}")

print("=== Check Complete ===")