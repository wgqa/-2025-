#!/bin/bash
# entrypoint.sh - Flask应用启动脚本

set -e

echo "Starting Flask Payment Service..."

# 等待数据库启动
echo "Waiting for database to be ready..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is ready!"

# 初始化数据库
echo "Initializing database..."
python -c "from app import init_database; init_database()"

# 启动应用
echo "Starting application..."
exec gunicorn --bind 0.0.0.0:5000 --workers 4 app:app