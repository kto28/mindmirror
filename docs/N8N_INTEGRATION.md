# MindMirror — n8n 整合指南

## 概覽

MindMirror 提供 3 個 Automation API，供 n8n 或其他自動化工具呼叫：

| Endpoint | 用途 |
|----------|------|
| `POST /api/automation/generate-quiz` | 根據主題生成測驗（草稿） |
| `POST /api/automation/publish-quiz` | 發布指定測驗 |
| `POST /api/automation/ingest-topic` | 接收主題 + 生成（合併操作） |

所有 automation API 需帶 `secret` 欄位，對應 `.env` 中的 `AUTOMATION_SECRET`。

## 每日自動生成流程

### 建議 n8n Workflow

```
[Cron Trigger: 每天 07:00] 
    → [HTTP Request: generate-quiz] 
    → [IF: success] 
        → [HTTP Request: publish-quiz]
        → [Slack/Email 通知: 已發布]
    → [ELSE]
        → [Slack/Email 通知: 生成失敗]
```

### Step 1: 生成測驗

**POST** `https://mindmirror.eddyto.com/api/automation/generate-quiz`

**Request Body:**
```json
{
  "topic": "社交電量恢復",
  "secret": "your-automation-secret"
}
```

**Response (200):**
```json
{
  "quiz_id": 4,
  "slug": "社交電量恢復-自我探索",
  "title": "你的社交電量恢復模式",
  "status": "draft",
  "question_count": 6
}
```

**Response (500 - 生成失敗):**
```json
{
  "detail": "Generation failed: OpenAI API error..."
}
```

### Step 2: 發布測驗

**POST** `https://mindmirror.eddyto.com/api/automation/publish-quiz`

**Request Body:**
```json
{
  "quiz_id": 4,
  "secret": "your-automation-secret"
}
```

**Response (200):**
```json
{
  "success": true,
  "quiz_id": 4,
  "status": "published"
}
```

### 合併操作: ingest-topic

如果不需要審核，可以用 `ingest-topic` 一步到位生成（但仍為 draft 狀態）：

**POST** `https://mindmirror.eddyto.com/api/automation/ingest-topic`

```json
{
  "topic": "金錢安全感",
  "secret": "your-automation-secret"
}
```

## 推薦主題列表

以下主題適合每日輪換：

| 類別 | 主題範例 |
|------|---------|
| 職場 | 工作壓力恢復、職場溝通風格、領導力傾向 |
| 關係 | 愛的語言、友誼模式、社交電量 |
| 生活 | 旅行偏好、消費風格、金錢安全感 |
| 成長 | 學習風格、決策傾向、時間管理 |
| 情緒 | 情緒調節方式、壓力應對策略、能量來源 |
| 自我 | 內在動力來源、價值觀探索、生活優先序 |

## Webhook 安全建議

1. **AUTOMATION_SECRET** 應為隨機長字串（至少 32 字元）
2. 在 n8n 中使用 Credentials 儲存 secret，不要 hardcode
3. 限制 n8n 伺服器的出口 IP，在 Nginx 層做 IP 白名單
4. 加上 rate limit：建議每日不超過 5 次 generate 呼叫
5. 監控 `generation_logs` 表，追蹤生成狀態和錯誤

## n8n HTTP Request 節點設定

```
Method: POST
URL: https://mindmirror.eddyto.com/api/automation/generate-quiz
Authentication: None (secret in body)
Body Content Type: JSON
Body:
{
  "topic": "{{ $json.topic }}",
  "secret": "{{ $credentials.mindmirror_secret }}"
}
```
