FROM python:3.10-slim

# 1. 設定基礎工作目錄為 /app (用來放置檔案)
WORKDIR /app

# 2. 安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. 複製原始碼
COPY src/ /app/src/

# 4. 【關鍵修改】切換工作目錄進入 /app/src
WORKDIR /app/src

# 5. 設定環境變數
ENV PYTHONUNBUFFERED=1

# 6. 執行伺服器
ENTRYPOINT ["python", "server.py"]