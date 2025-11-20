#!/bin/bash
# Web登录功能测试执行脚本
# 在VSCode环境中执行自动化测试的便捷脚本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
AUTOMATION_DIR="${PROJECT_ROOT}/automation"
TEST_REPORTS_DIR="${PROJECT_ROOT}/test_reports"
SCREENSHOTS_DIR="${PROJECT_ROOT}/screenshots"

# 检查目录是否存在
check_directories() {
    echo -e "${YELLOW}检查项目目录结构...${NC}"
    
    # 创建必要的目录
    mkdir -p "${TEST_REPORTS_DIR}"
    mkdir -p "${SCREENSHOTS_DIR}"
    mkdir -p "${AUTOMATION_DIR}/logs"
    
    echo -e "${GREEN}目录检查完成${NC}"
}

# 检查Python环境
check_python() {
    echo -e "${YELLOW}检查Python环境...${NC}"
    
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}错误: Python3未安装${NC}"
        exit 1
    fi
    
    if ! command -v pip3 &> /dev/null; then
        echo -e "${RED}错误: pip3未安装${NC}"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo -e "${GREEN}Python版本: ${PYTHON_VERSION}${NC}"
}

# 安装依赖包
install_dependencies() {
    echo -e "${YELLOW}安装依赖包...${NC}"
    
    cd "${AUTOMATION_DIR}"
    pip3 install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}依赖包安装完成${NC}"
    else
        echo -e "${RED}依赖包安装失败${NC}"
        exit 1
    fi
}

# 运行所有测试
run_all_tests() {
    echo -e "${YELLOW}开始运行所有测试...${NC}"
    
    cd "${AUTOMATION_DIR}"
    
    # 生成报告文件名（包含时间戳）
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    REPORT_FILE="${TEST_REPORTS_DIR}/automation_report_${TIMESTAMP}.html"
    
    # 运行测试
    pytest login_test.py \
        -v \
        --html="${REPORT_FILE}" \
        --self-contained-html \
        --cov=. \
        --cov-report=html:"${TEST_REPORTS_DIR}/coverage_report" \
        --cov-report=xml:"${TEST_REPORTS_DIR}/coverage.xml"
    
    TEST_EXIT_CODE=$?
    
    if [ ${TEST_EXIT_CODE} -eq 0 ]; then
        echo -e "${GREEN}所有测试通过！${NC}"
    else
        echo -e "${RED}部分测试失败，请查看报告${NC}"
    fi
    
    echo -e "${YELLOW}测试报告已生成: ${REPORT_FILE}${NC}"
    echo -e "${YELLOW}覆盖率报告已生成: ${TEST_REPORTS_DIR}/coverage_report/index.html${NC}"
    
    return ${TEST_EXIT_CODE}
}

# 运行指定测试用例
run_specific_test() {
    local test_case=$1
    
    if [ -z "${test_case}" ]; then
        echo -e "${RED}请指定测试用例名称${NC}"
        echo -e "${YELLOW}示例: ./run_tests.sh run-specific TestLogin::test_valid_login${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}开始运行测试用例: ${test_case}${NC}"
    
    cd "${AUTOMATION_DIR}"
    
    pytest login_test.py::${test_case} -v
    
    TEST_EXIT_CODE=$?
    
    if [ ${TEST_EXIT_CODE} -eq 0 ]; then
        echo -e "${GREEN}测试用例通过！${NC}"
    else
        echo -e "${RED}测试用例失败${NC}"
    fi
    
    return ${TEST_EXIT_CODE}
}

# 清理测试环境
clean_environment() {
    echo -e "${YELLOW}清理测试环境...${NC}"
    
    # 清理截图
    rm -rf "${SCREENSHOTS_DIR}"/*
    echo -e "清理截图目录"
    
    # 清理日志
    rm -rf "${AUTOMATION_DIR}/logs"/*
    echo -e "清理日志文件"
    
    # 清理测试报告（保留最近5个）
    ls -tp "${TEST_REPORTS_DIR}/"automation_report_*.html | grep -v '/$' | tail -n +6 | xargs -I {} rm -- {}
    echo -e "清理旧测试报告"
    
    echo -e "${GREEN}环境清理完成${NC}"
}

# 显示帮助信息
show_help() {
    echo -e "${GREEN}Web登录功能测试执行脚本${NC}"
    echo -e ""
    echo -e "${YELLOW}用法: ./run_tests.sh [命令] [参数]${NC}"
    echo -e ""
    echo -e "${YELLOW}命令列表:${NC}"
    echo -e "  ${GREEN}install${NC}           安装依赖包"
    echo -e "  ${GREEN}run-all${NC}           运行所有测试用例"
    echo -e "  ${GREEN}run-specific [用例名]${NC} 运行指定测试用例"
    echo -e "  ${GREEN}clean${NC}            清理测试环境"
    echo -e "  ${GREEN}check-env${NC}         检查测试环境"
    echo -e "  ${GREEN}help${NC}             显示帮助信息"
    echo -e ""
    echo -e "${YELLOW}示例:${NC}"
    echo -e "  ./run_tests.sh install"
    echo -e "  ./run_tests.sh run-all"
    echo -e "  ./run_tests.sh run-specific TestLogin::test_valid_login"
    echo -e "  ./run_tests.sh clean"
}

# 检查测试环境
check_environment() {
    echo -e "${YELLOW}检查测试环境...${NC}"
    
    check_directories
    check_python
    
    # 检查浏览器驱动
    if command -v chromedriver &> /dev/null; then
        CHROME_DRIVER_VERSION=$(chromedriver --version | awk '{print $2}')
        echo -e "${GREEN}ChromeDriver版本: ${CHROME_DRIVER_VERSION}${NC}"
    else
        echo -e "${YELLOW}ChromeDriver未找到，将使用webdriver-manager自动管理${NC}"
    fi
    
    echo -e "${GREEN}环境检查完成${NC}"
}

# 主函数
main() {
    case "$1" in
        install)
            check_python
            install_dependencies
            ;;
        run-all)
            check_directories
            run_all_tests
            ;;
        run-specific)
            shift
            check_directories
            run_specific_test "$@"
            ;;
        clean)
            clean_environment
            ;;
        check-env)
            check_environment
            ;;
        help)
            show_help
            ;;
        *)
            echo -e "${RED}未知命令: $1${NC}"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"