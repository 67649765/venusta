#!/bin/bash
# CI环境测试脚本
# 用于在CI/CD环境中运行VenusTA项目的冒烟测试

set -e  # 任何命令失败时立即退出

# 配置日志颜色
echo_color() {
    local color=$1
    local text=$2
    case $color in
        "green") echo "\033[32m$text\033[0m" ;;  # 绿色
        "red") echo "\033[31m$text\033[0m" ;;    # 红色
        "blue") echo "\033[34m$text\033[0m" ;;   # 蓝色
        "yellow") echo "\033[33m$text\033[0m" ;; # 黄色
        *) echo "$text" ;;  # 默认
    esac
}

# 检查Docker是否可用
check_docker() {
    echo_color "blue" "\n[1/4] 检查Docker环境..."
    if ! command -v docker &> /dev/null; then
        echo_color "red" "❌ Docker未安装，请先安装Docker"
        return 1
    fi
    
    if ! docker info &> /dev/null; then
        echo_color "red" "❌ Docker服务未启动，请先启动Docker服务"
        return 1
    fi
    
    echo_color "green" "✅ Docker环境正常"
    return 0
}

# 等待服务就绪
wait_for_services() {
    echo_color "blue" "\n[2/4] 等待服务就绪..."
    local max_wait=120  # 最大等待时间(秒)
    local wait_interval=5  # 检查间隔(秒)
    local elapsed=0
    
    while [ $elapsed -lt $max_wait ]; do
        # 检查API服务健康状态
        if curl -s http://localhost:8000/health | grep -q "status":"ok"; then
            echo_color "green" "✅ API服务已就绪"
            return 0
        fi
        
        echo_color "yellow" "服务尚未就绪，等待${wait_interval}秒... (已等待${elapsed}/${max_wait}秒)"
        sleep $wait_interval
        elapsed=$((elapsed + wait_interval))
    done
    
    echo_color "red" "❌ 服务在${max_wait}秒内未就绪，测试失败"
    return 1
}

# 运行CI冒烟测试
run_smoke_test() {
    echo_color "blue" "\n[3/4] 运行CI冒烟测试..."
    
    # 检查Python是否可用
    if ! command -v python3 &> /dev/null; then
        echo_color "red" "❌ Python3未安装，请先安装Python3"
        return 1
    fi
    
    # 检查测试脚本是否存在
    if [ ! -f tools/ci_smoke_test.py ]; then
        echo_color "red" "❌ 测试脚本 tools/ci_smoke_test.py 不存在"
        return 1
    fi
    
    # 安装依赖
    echo_color "blue" "安装测试依赖..."
    pip3 install --quiet requests argparse
    
    # 运行测试脚本
    if python3 tools/ci_smoke_test.py --api-base http://localhost:8000; then
        echo_color "green" "✅ CI冒烟测试通过"
        return 0
    else
        echo_color "red" "❌ CI冒烟测试失败"
        return 1
    fi
}

# 查看容器日志(如果测试失败)
check_container_logs() {
    echo_color "blue" "\n[4/4] 查看容器状态..."
    
    # 显示所有容器状态
    docker compose ps
    
    # 显示API容器日志的最后20行
    echo -e "\nAPI容器最后20行日志："
    docker compose logs --tail=20 api
    
    # 显示数据库容器日志的最后20行
    echo -e "\n数据库容器最后20行日志："
    docker compose logs --tail=20 db
}

# 主函数
main() {
    echo_color "blue" "开始VenusTA CI测试流程"
    echo_color "blue" "====================================="
    
    if check_docker; then
        if wait_for_services; then
            if run_smoke_test; then
                echo_color "green" "\n🎉 所有测试通过！VenusTA项目在CI环境中正常运行"
                echo_color "blue" "====================================="
                return 0
            fi
        fi
    fi
    
    # 如果测试失败，查看容器日志
    check_container_logs
    
    echo_color "red" "\n❌ VenusTA CI测试失败"
    echo_color "blue" "====================================="
    return 1
}

# 执行主函数
main

# 根据测试结果设置退出码
exit $?