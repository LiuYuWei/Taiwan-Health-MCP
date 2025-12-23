FROM python:3.10-slim

# 1. 設定基礎工作目錄為 /app (用來放置檔案)
WORKDIR /app

# 2. 安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. 複製資料 (這會放在 /app/data)
COPY data/ ./data/

# 4. 複製程式碼 (這會放在 /app/src)
COPY src/ ./src/

# 5. 【關鍵修改】切換工作目錄進入 /app/src
WORKDIR /app/src

# 6. 設定環境變數
ENV PYTHONUNBUFFERED=1

# 7. 【關鍵修改】因為已經在 src 裡面了，指令直接執行 server.py 即可
ENTRYPOINT ["python", "server.py"]