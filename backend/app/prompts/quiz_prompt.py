"""OpenAI prompt builder for generating positive psychology quizzes."""

QUIZ_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "intro_text": {"type": "string"},
        "estimated_minutes": {"type": "integer"},
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question_text": {"type": "string"},
                    "options": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "option_text": {"type": "string"},
                                "value_code": {"type": "string"},
                                "score_map": {"type": "object"},
                            },
                            "required": ["option_text", "value_code", "score_map"],
                        },
                    },
                },
                "required": ["question_text", "options"],
            },
        },
        "result_profiles": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "title": {"type": "string"},
                    "short_label": {"type": "string"},
                    "description": {"type": "string"},
                    "strengths": {"type": "array", "items": {"type": "string"}},
                    "growth_tips": {"type": "array", "items": {"type": "string"}},
                    "encouragement": {"type": "string"},
                    "share_text": {"type": "string"},
                },
                "required": [
                    "code",
                    "title",
                    "short_label",
                    "description",
                    "strengths",
                    "growth_tips",
                    "encouragement",
                    "share_text",
                ],
            },
        },
    },
    "required": [
        "title",
        "summary",
        "intro_text",
        "estimated_minutes",
        "questions",
        "result_profiles",
    ],
}


def build_quiz_prompt(topic: str) -> list[dict]:
    """Build the OpenAI chat messages for quiz generation."""
    system_prompt = """你是一位資深正向心理學內容設計師，專門製作自我探索測驗。

你的任務是根據用戶提供的主題，生成一份正向、溫暖、有深度的自我探索心理測驗。

## 嚴格安全規則（必須遵守）

1. 絕對不可使用任何醫療診斷字眼：抑鬱症、焦慮症、人格障礙、精神病、創傷、PTSD、躁鬱等
2. 絕對不可使用羞辱式標籤：失敗、缺陷、不正常、有問題、軟弱等
3. 所有內容必須使用正向自我探索語氣：你的傾向、你的風格、你現階段的狀態、你可以進一步成長的方向
4. 不可涉及宗教、政治、性別歧視
5. 不可說教或過度空泛
6. 語氣溫暖、鼓勵、清晰，適合 20-45 歲成年人

## 輸出規格

你必須輸出一個 JSON 物件，包含以下欄位：
- title: 測驗標題（繁體中文，10-25字）
- summary: 測驗簡介（繁體中文，30-60字）
- intro_text: 開場引導語（繁體中文，50-100字，溫暖有吸引力）
- estimated_minutes: 預估作答時間（整數，通常 2-5）
- questions: 題目陣列（5-8 題）
- result_profiles: 結果類型陣列（恰好 4 種）

每條題目：
- question_text: 題目文字（繁體中文）
- options: 選項陣列（恰好 4 個選項）

每個選項：
- option_text: 選項文字（繁體中文）
- value_code: 選項代碼（英文，如 "a", "b", "c", "d"）
- score_map: 分數對應（JSON object，key 為 result profile code，value 為分數 0-3）

每個結果類型：
- code: 英文代碼（如 "explorer", "guardian"）
- title: 結果名稱（繁體中文，5-15字）
- short_label: 短標籤（繁體中文，2-6字）
- description: 結果描述（繁體中文，120-220字，正向、有深度）
- strengths: 你的優勢（繁體中文，恰好 3 條）
- growth_tips: 可提升方向（繁體中文，恰好 3 條，正面語氣）
- encouragement: 鼓勵語（繁體中文，30-60字）
- share_text: 分享文案（繁體中文，20-40字，適合社交分享）

## 重要提醒
- 每個選項的 score_map 必須包含所有 4 個 result profile code
- 分數範圍 0-3，確保不同選項有差異化的分數分佈
- 題目要有趣、生活化、容易代入
- 結果描述要有洞察力，讓人覺得「被理解了」
"""

    user_prompt = f"""請根據以下主題生成一份完整的自我探索心理測驗：

主題：{topic}

請直接輸出 JSON，不要加任何其他文字。"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
