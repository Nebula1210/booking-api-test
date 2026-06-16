import subprocess
import sys


def run_command(cmd):
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def main():
    # 确保在项目根目录执行
    print("Starting test execution...")

    # 1. 运行测试
    run_command(["pytest", "-v", "--alluredir=reports/allure_raw"])

    # 2. 生成报告
    run_command(["allure", "generate", "reports/allure_raw", "-o", "reports/allure_html", "--clean"])

    # 3. 打开报告
    run_command(["allure", "open", "reports/allure_html"])


if __name__ == "__main__":
    main()
