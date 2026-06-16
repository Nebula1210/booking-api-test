# 使用官方Python 3.11 精简镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件到容器中
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目所有文件到容器
COPY . .

# 设置环境变量（可选）
ENV PYTHONUNBUFFERED=1

# 默认运行 pytest，生成 Allure 原始数据到 /app/reports/allure_raw
# 注意：容器内不安装 allure，只生成原始数据，报告生成在宿主机完成
CMD ["pytest", "-v", "--alluredir=/app/reports/allure_raw"]