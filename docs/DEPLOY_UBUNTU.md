# MindMirror — Ubuntu Server 部署指南

## 前置需求

- Ubuntu 22.04 LTS
- 域名 `mindmirror.eddyto.com` 已指向伺服器 IP
- SSH root / sudo 存取

## 1. 安裝系統依賴

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git build-essential nginx certbot python3-certbot-nginx

# Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Python 3.11
sudo apt install -y python3.11 python3.11-venv python3-pip

# PostgreSQL
sudo apt install -y postgresql postgresql-contrib
```

## 2. 設定 PostgreSQL

```bash
sudo -u postgres psql
```

```sql
CREATE USER mindmirror WITH PASSWORD 'your-secure-password';
CREATE DATABASE mindmirror OWNER mindmirror;
GRANT ALL PRIVILEGES ON DATABASE mindmirror TO mindmirror;
\q
```

## 3. 部署後端

```bash
# 建立應用目錄
sudo mkdir -p /opt/mindmirror
sudo chown $USER:$USER /opt/mindmirror
cd /opt/mindmirror

# 複製檔案 (從本機)
# scp -r ./backend user@server:/opt/mindmirror/

cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 設定環境變數
cp .env.example .env
nano .env
# 填入:
# DATABASE_URL=postgresql://mindmirror:your-secure-password@localhost:5432/mindmirror
# ADMIN_PASSWORD=your-admin-password
# JWT_SECRET=your-random-secret-string
# OPENAI_API_KEY=sk-your-key
# CORS_ORIGINS=https://mindmirror.eddyto.com
# AUTOMATION_SECRET=your-webhook-secret

# 初始化 DB + seed
python seed.py
```

### 建立 systemd service (後端)

```bash
sudo tee /etc/systemd/system/mindmirror-api.service << 'EOF'
[Unit]
Description=MindMirror FastAPI Backend
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/mindmirror/backend
Environment=PATH=/opt/mindmirror/backend/venv/bin
EnvironmentFile=/opt/mindmirror/backend/.env
ExecStart=/opt/mindmirror/backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable mindmirror-api
sudo systemctl start mindmirror-api
sudo systemctl status mindmirror-api
```

## 4. 部署前端

```bash
cd /opt/mindmirror/frontend

# 設定環境
cp .env.example .env.local
echo "NEXT_PUBLIC_API_URL=https://mindmirror.eddyto.com" > .env.local

npm install
npm run build
```

### 使用 PM2 管理前端

```bash
sudo npm install -g pm2

cd /opt/mindmirror/frontend
pm2 start npm --name "mindmirror-web" -- start -- -p 3000
pm2 save
pm2 startup systemd
```

## 5. 設定 Nginx

```bash
sudo tee /etc/nginx/sites-available/mindmirror << 'EOF'
server {
    listen 80;
    server_name mindmirror.eddyto.com;

    # API proxy
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
    }

    # Frontend proxy
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/mindmirror /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 6. 設定 SSL (Let's Encrypt)

```bash
sudo certbot --nginx -d mindmirror.eddyto.com
```

自動續期:
```bash
sudo certbot renew --dry-run
```

## 7. 驗證

```bash
# 檢查後端
curl https://mindmirror.eddyto.com/api/health

# 檢查前端
curl -s https://mindmirror.eddyto.com | head -20
```

## 常用維運命令

```bash
# 查看後端日誌
sudo journalctl -u mindmirror-api -f

# 查看前端日誌
pm2 logs mindmirror-web

# 重啟後端
sudo systemctl restart mindmirror-api

# 重啟前端
pm2 restart mindmirror-web

# 更新部署
cd /opt/mindmirror && git pull
cd backend && source venv/bin/activate && pip install -r requirements.txt
sudo systemctl restart mindmirror-api
cd ../frontend && npm install && npm run build && pm2 restart mindmirror-web
```
