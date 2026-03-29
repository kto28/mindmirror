"""Seed script — inserts 3 demo quizzes with full questions, options, and result profiles."""

import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from app.core.database import SessionLocal, engine, Base
from app.models.quiz import Quiz, Question, QuestionOption, ResultProfile

Base.metadata.create_all(bind=engine)

SEED_QUIZZES = [
    {
        "title": "你的旅行人格是什麼？",
        "slug": "travel-personality",
        "topic": "旅行偏好",
        "summary": "透過 6 道情境題，探索你內在的旅行風格與生活態度。",
        "intro_text": "每個人的旅行方式，都藏著一面真實的自己。無論你是喜歡背包獨行，還是享受精心策劃的行程，這份測驗將幫助你更了解自己在面對未知時的傾向與力量。準備好了嗎？",
        "estimated_minutes": 3,
        "status": "published",
        "publish_date": date.today() - timedelta(days=2),
        "questions": [
            {
                "question_text": "朋友突然約你明天出發去旅行，你的第一反應是？",
                "options": [
                    {"option_text": "太棒了！馬上收拾行李出發", "value_code": "a", "score_map": {"adventurer": 3, "planner": 0, "soulseeker": 1, "connector": 1}},
                    {"option_text": "讓我先查查天氣和住宿", "value_code": "b", "score_map": {"adventurer": 0, "planner": 3, "soulseeker": 1, "connector": 1}},
                    {"option_text": "看看那裡有什麼特別的體驗", "value_code": "c", "score_map": {"adventurer": 1, "planner": 0, "soulseeker": 3, "connector": 1}},
                    {"option_text": "先問問還有誰要一起去", "value_code": "d", "score_map": {"adventurer": 1, "planner": 0, "soulseeker": 0, "connector": 3}},
                ],
            },
            {
                "question_text": "到了一個完全陌生的城市，你最想做的事是？",
                "options": [
                    {"option_text": "隨意走進巷弄探索", "value_code": "a", "score_map": {"adventurer": 3, "planner": 0, "soulseeker": 2, "connector": 0}},
                    {"option_text": "打開地圖找最佳路線", "value_code": "b", "score_map": {"adventurer": 0, "planner": 3, "soulseeker": 0, "connector": 1}},
                    {"option_text": "去當地人推薦的隱藏景點", "value_code": "c", "score_map": {"adventurer": 1, "planner": 0, "soulseeker": 3, "connector": 1}},
                    {"option_text": "找間咖啡廳和旁邊的人聊天", "value_code": "d", "score_map": {"adventurer": 0, "planner": 0, "soulseeker": 1, "connector": 3}},
                ],
            },
            {
                "question_text": "旅途中遇到計劃外的狀況（例如迷路），你會？",
                "options": [
                    {"option_text": "反而覺得更有趣，享受意外", "value_code": "a", "score_map": {"adventurer": 3, "planner": 0, "soulseeker": 2, "connector": 0}},
                    {"option_text": "冷靜地重新規劃路線", "value_code": "b", "score_map": {"adventurer": 0, "planner": 3, "soulseeker": 0, "connector": 1}},
                    {"option_text": "把它當作一次人生體驗", "value_code": "c", "score_map": {"adventurer": 1, "planner": 0, "soulseeker": 3, "connector": 1}},
                    {"option_text": "向路人求助，順便交個朋友", "value_code": "d", "score_map": {"adventurer": 0, "planner": 0, "soulseeker": 0, "connector": 3}},
                ],
            },
            {
                "question_text": "旅行結束後，你最珍惜的是什麼？",
                "options": [
                    {"option_text": "那些意想不到的冒險經歷", "value_code": "a", "score_map": {"adventurer": 3, "planner": 0, "soulseeker": 1, "connector": 1}},
                    {"option_text": "完美執行計劃的成就感", "value_code": "b", "score_map": {"adventurer": 0, "planner": 3, "soulseeker": 0, "connector": 0}},
                    {"option_text": "旅途中的感悟和啟發", "value_code": "c", "score_map": {"adventurer": 0, "planner": 0, "soulseeker": 3, "connector": 1}},
                    {"option_text": "認識的新朋友和分享的故事", "value_code": "d", "score_map": {"adventurer": 0, "planner": 0, "soulseeker": 1, "connector": 3}},
                ],
            },
            {
                "question_text": "如果可以選一種旅行方式度過一個月，你會選？",
                "options": [
                    {"option_text": "一個人環遊世界", "value_code": "a", "score_map": {"adventurer": 3, "planner": 1, "soulseeker": 2, "connector": 0}},
                    {"option_text": "精心安排的主題深度遊", "value_code": "b", "score_map": {"adventurer": 0, "planner": 3, "soulseeker": 1, "connector": 0}},
                    {"option_text": "在一個小鎮慢慢生活", "value_code": "c", "score_map": {"adventurer": 0, "planner": 0, "soulseeker": 3, "connector": 1}},
                    {"option_text": "和朋友們一起公路旅行", "value_code": "d", "score_map": {"adventurer": 1, "planner": 0, "soulseeker": 0, "connector": 3}},
                ],
            },
            {
                "question_text": "你覺得旅行最大的意義是什麼？",
                "options": [
                    {"option_text": "突破舒適圈，挑戰自我", "value_code": "a", "score_map": {"adventurer": 3, "planner": 0, "soulseeker": 1, "connector": 0}},
                    {"option_text": "增長見識，豐富知識", "value_code": "b", "score_map": {"adventurer": 0, "planner": 3, "soulseeker": 1, "connector": 0}},
                    {"option_text": "找到內心的平靜和方向", "value_code": "c", "score_map": {"adventurer": 0, "planner": 0, "soulseeker": 3, "connector": 1}},
                    {"option_text": "建立連結，分享快樂", "value_code": "d", "score_map": {"adventurer": 0, "planner": 0, "soulseeker": 0, "connector": 3}},
                ],
            },
        ],
        "result_profiles": [
            {
                "code": "adventurer",
                "title": "自由探險家",
                "short_label": "探險家",
                "description": "你是一個天生的探險家，對未知充滿好奇與熱情。你不害怕改變，反而在變化中找到能量和靈感。你相信最好的風景往往在計劃之外，而最深刻的體驗來自於勇敢踏出第一步。你的冒險精神不僅體現在旅行中，更滲透在日常生活的每個選擇裡。你用行動證明：人生最美的風景，永遠在下一個轉角。",
                "strengths": ["勇於面對未知，適應力極強", "充滿創造力和行動力", "能在挑戰中找到樂趣和成長"],
                "growth_tips": ["有時可以稍微放慢腳步，享受當下的寧靜", "嘗試為重要的事情做一些基本規劃", "記得在冒險之餘，也照顧好自己的身心"],
                "encouragement": "你的勇氣是許多人羨慕的禮物。繼續探索吧，世界因為像你這樣的人而更加精彩！",
                "share_text": "我是「自由探險家」✈️ 未知的旅途就是我最好的目的地！",
            },
            {
                "code": "planner",
                "title": "品質策劃師",
                "short_label": "策劃師",
                "description": "你是一個注重品質的策劃師，善於將想法轉化為完美的行動方案。你相信好的準備是成功的一半，而你的細心和條理讓身邊的人都感到安心。你不是害怕冒險，而是選擇用智慧和策略來面對挑戰。你的規劃能力不僅讓旅行更順暢，也讓生活中的每個目標都能一步步實現。",
                "strengths": ["邏輯清晰，做事有條不紊", "善於資源整合和時間管理", "可靠且值得信賴，是團隊的定心丸"],
                "growth_tips": ["偶爾給自己一些「留白」的空間，享受即興的樂趣", "練習在不完美中找到美好", "嘗試信任直覺，不一定每件事都需要完美計劃"],
                "encouragement": "你的用心和負責是一種珍貴的力量。相信自己，即使計劃改變，你也有能力應對一切！",
                "share_text": "我是「品質策劃師」📋 完美的旅程從完美的計劃開始！",
            },
            {
                "code": "soulseeker",
                "title": "心靈漫遊者",
                "short_label": "漫遊者",
                "description": "你是一個深度的心靈漫遊者，旅行對你來說不只是移動身體，更是一場內在的探索。你善於在平凡中發現不平凡，在安靜的時刻找到深刻的感悟。你追求的不是打卡景點，而是真實的體驗和內心的觸動。你的敏感和洞察力讓你能看見別人看不見的美，也讓你的人生充滿了深度和意義。",
                "strengths": ["高度的觀察力和感受力", "善於自我反思和內在成長", "能在平凡中創造有意義的體驗"],
                "growth_tips": ["有時候可以更主動地與他人分享你的感受", "平衡內在世界和外在行動", "不要把太多時間花在思考上，有時行動本身就是答案"],
                "encouragement": "你的深度思考是一份獨特的禮物。繼續保持對世界的敏感，你的內在旅程同樣精彩！",
                "share_text": "我是「心靈漫遊者」🌿 每一次旅行都是一場內在的對話。",
            },
            {
                "code": "connector",
                "title": "溫暖連結者",
                "short_label": "連結者",
                "description": "你是一個天生的連結者，善於在旅途中建立真摯的人際關係。對你來說，最美的風景不是山水，而是人與人之間的溫暖。你有一種讓人感到舒適和被接納的能力，走到哪裡都能找到朋友。你相信分享讓快樂加倍，而旅行中最珍貴的收穫，就是那些真誠的人際連結。",
                "strengths": ["高度的同理心和社交能力", "善於傾聽和理解他人", "能在任何環境中建立溫暖的人際關係"],
                "growth_tips": ["記得也留一些時間給自己，享受獨處的時光", "嘗試在不熟悉的情境中也保持自信", "學習在付出的同時，也接受他人的關心"],
                "encouragement": "你的溫暖是這個世界最需要的力量。繼續用你的真誠感染身邊的人吧！",
                "share_text": "我是「溫暖連結者」💛 旅行中最美的風景是遇見你們！",
            },
        ],
    },
    {
        "title": "你的社交電量恢復模式",
        "slug": "social-energy-recovery",
        "topic": "社交電量",
        "summary": "了解你在社交之後如何為自己充電，找到最適合你的能量恢復方式。",
        "intro_text": "社交是生活中重要的一部分，但每個人在社交後恢復能量的方式都不同。有人需要獨處，有人需要運動，有人需要創作。這份測驗將幫助你發現自己的充電模式，讓你在繁忙的社交生活中更好地照顧自己。",
        "estimated_minutes": 3,
        "status": "published",
        "publish_date": date.today() - timedelta(days=1),
        "questions": [
            {
                "question_text": "參加了一場熱鬧的聚會後，你最想做的事是？",
                "options": [
                    {"option_text": "窩在沙發上安靜看書或追劇", "value_code": "a", "score_map": {"quiet": 3, "active": 0, "creative": 1, "social_light": 0}},
                    {"option_text": "去跑步或做瑜伽", "value_code": "b", "score_map": {"quiet": 0, "active": 3, "creative": 0, "social_light": 1}},
                    {"option_text": "畫畫、寫日記或聽音樂", "value_code": "c", "score_map": {"quiet": 1, "active": 0, "creative": 3, "social_light": 0}},
                    {"option_text": "和一兩個親近的人輕鬆聊天", "value_code": "d", "score_map": {"quiet": 0, "active": 0, "creative": 0, "social_light": 3}},
                ],
            },
            {
                "question_text": "連續幾天高強度社交後，你的身體通常會？",
                "options": [
                    {"option_text": "感覺很疲倦，只想待在家", "value_code": "a", "score_map": {"quiet": 3, "active": 0, "creative": 1, "social_light": 0}},
                    {"option_text": "反而想活動一下身體", "value_code": "b", "score_map": {"quiet": 0, "active": 3, "creative": 0, "social_light": 1}},
                    {"option_text": "腦子裡會冒出很多想法想記錄", "value_code": "c", "score_map": {"quiet": 0, "active": 0, "creative": 3, "social_light": 1}},
                    {"option_text": "想找信任的人說說心裡話", "value_code": "d", "score_map": {"quiet": 0, "active": 0, "creative": 0, "social_light": 3}},
                ],
            },
            {
                "question_text": "週末只有半天空閒，你會選擇？",
                "options": [
                    {"option_text": "一個人泡在浴缸裡放空", "value_code": "a", "score_map": {"quiet": 3, "active": 0, "creative": 1, "social_light": 0}},
                    {"option_text": "去戶外散步或爬山", "value_code": "b", "score_map": {"quiet": 1, "active": 3, "creative": 0, "social_light": 0}},
                    {"option_text": "嘗試一個新的手作或烘焙", "value_code": "c", "score_map": {"quiet": 0, "active": 0, "creative": 3, "social_light": 1}},
                    {"option_text": "約最好的朋友喝下午茶", "value_code": "d", "score_map": {"quiet": 0, "active": 0, "creative": 0, "social_light": 3}},
                ],
            },
            {
                "question_text": "什麼樣的環境最能讓你感到放鬆？",
                "options": [
                    {"option_text": "安靜的房間，柔和的燈光", "value_code": "a", "score_map": {"quiet": 3, "active": 0, "creative": 1, "social_light": 0}},
                    {"option_text": "開闊的戶外，清新的空氣", "value_code": "b", "score_map": {"quiet": 0, "active": 3, "creative": 1, "social_light": 0}},
                    {"option_text": "有音樂和工具的創作空間", "value_code": "c", "score_map": {"quiet": 0, "active": 0, "creative": 3, "social_light": 0}},
                    {"option_text": "溫馨的小聚會，幾個好朋友", "value_code": "d", "score_map": {"quiet": 0, "active": 0, "creative": 0, "social_light": 3}},
                ],
            },
            {
                "question_text": "你覺得「充電完成」的感覺是？",
                "options": [
                    {"option_text": "內心很平靜，思緒清晰", "value_code": "a", "score_map": {"quiet": 3, "active": 1, "creative": 1, "social_light": 0}},
                    {"option_text": "身體有活力，精神飽滿", "value_code": "b", "score_map": {"quiet": 0, "active": 3, "creative": 0, "social_light": 1}},
                    {"option_text": "有了新的靈感和動力", "value_code": "c", "score_map": {"quiet": 0, "active": 0, "creative": 3, "social_light": 1}},
                    {"option_text": "感覺被理解和支持", "value_code": "d", "score_map": {"quiet": 0, "active": 0, "creative": 0, "social_light": 3}},
                ],
            },
        ],
        "result_profiles": [
            {
                "code": "quiet",
                "title": "寧靜充電型",
                "short_label": "寧靜型",
                "description": "你是一個在安靜中找到力量的人。社交活動雖然讓你享受，但你的能量主要來自獨處的時光。你善於在安靜的環境中整理思緒、恢復元氣。這不是內向或害羞，而是你擁有一個豐富的內在世界，需要空間來沉澱和重新連結自己。當你給自己足夠的安靜時間，你會發現自己變得更有能量去面對世界。",
                "strengths": ["深度思考能力強", "善於自我覺察和情緒調節", "在安靜中能產生深刻的洞見"],
                "growth_tips": ["為自己設定固定的獨處充電時間", "學習溫和地向他人表達你需要安靜的空間", "在獨處時嘗試正念冥想，效果會更好"],
                "encouragement": "安靜不是逃避，而是你最有力量的充電方式。好好珍惜這份能在寧靜中找到自己的能力！",
                "share_text": "我是「寧靜充電型」🌙 安靜是我最好的充電方式！",
            },
            {
                "code": "active",
                "title": "活力運動型",
                "short_label": "活力型",
                "description": "你是一個透過身體活動來恢復能量的人。當社交讓你感到疲倦時，運動和戶外活動是你最好的解藥。你的身體和心靈有著緊密的連結，當身體動起來，你的心情也跟著飛揚。你不需要激烈的運動，哪怕只是散步或伸展，都能讓你重新找到平衡。這種身心合一的充電方式，讓你總是充滿活力。",
                "strengths": ["身心連結強，善於透過身體釋放壓力", "行動力強，恢復速度快", "正向積極，感染力強"],
                "growth_tips": ["在運動之外，也嘗試靜態的放鬆方式", "注意不要用過度運動來逃避情緒", "嘗試瑜伽或太極等身心整合的練習"],
                "encouragement": "你的活力是會傳染的正能量！繼續用運動來照顧自己，你的身體會感謝你。",
                "share_text": "我是「活力運動型」⚡ 動起來就是我的充電秘訣！",
            },
            {
                "code": "creative",
                "title": "靈感創作型",
                "short_label": "創作型",
                "description": "你是一個透過創作來恢復能量的人。社交之後，你的內在世界會累積許多感受和想法，而創作就是你表達和釋放的管道。無論是寫字、畫畫、做手工還是彈琴，這些創造性的活動讓你重新與自己連結。你擁有豐富的想像力和敏感度，這讓你能把日常的感受轉化為美好的作品。",
                "strengths": ["豐富的想像力和表達能力", "善於將感受轉化為有意義的作品", "高度的敏感力讓你能捕捉生活中的美"],
                "growth_tips": ["不要追求完美，享受創作的過程本身", "嘗試不同的創作媒介，找到最適合你的表達方式", "偶爾也和他人分享你的作品，你會得到意想不到的回饋"],
                "encouragement": "你的創造力是一份珍貴的禮物。繼續用你的方式記錄和表達這個世界吧！",
                "share_text": "我是「靈感創作型」🎨 創作是我最好的心靈充電站！",
            },
            {
                "code": "social_light",
                "title": "輕社交暖心型",
                "short_label": "暖心型",
                "description": "你是一個在親密的小圈子中恢復能量的人。大型社交可能讓你消耗，但和一兩個知心好友的深度對話卻能讓你重新充滿電。你重視的不是社交的廣度，而是深度。你需要的是真誠的傾聽和理解，而不是熱鬧的氛圍。這種選擇性的社交方式，讓你既能享受人際的溫暖，又不會過度消耗自己。",
                "strengths": ["善於維護深度的人際關係", "高度的同理心和傾聽能力", "能在小圈子中創造安全和溫暖的氛圍"],
                "growth_tips": ["確保你的傾聽者也有人傾聽你", "嘗試拓展一些新的友誼圈", "在付出關心的同時，也記得接受他人的關愛"],
                "encouragement": "你對真誠連結的重視，是這個快速世界中最珍貴的品質。繼續珍惜那些深度的友誼！",
                "share_text": "我是「輕社交暖心型」☕ 和知心好友的深度對話就是最好的充電！",
            },
        ],
    },
    {
        "title": "你的金錢安全感風格",
        "slug": "money-security-style",
        "topic": "金錢安全感",
        "summary": "探索你與金錢的內在關係，了解你的財務安全感來源與理財傾向。",
        "intro_text": "金錢不只是數字，它反映了我們的價值觀、安全感和生活態度。每個人對金錢的感受和使用方式都不同，而了解自己的金錢風格，是邁向財務自在的第一步。這份測驗沒有對錯，只有更深的自我理解。",
        "estimated_minutes": 3,
        "status": "published",
        "publish_date": date.today(),
        "questions": [
            {
                "question_text": "收到一筆意外獎金，你的第一個念頭是？",
                "options": [
                    {"option_text": "太好了，先存起來以備不時之需", "value_code": "a", "score_map": {"guardian": 3, "grower": 1, "experiencer": 0, "sharer": 0}},
                    {"option_text": "研究一下哪些投資管道適合", "value_code": "b", "score_map": {"guardian": 0, "grower": 3, "experiencer": 1, "sharer": 0}},
                    {"option_text": "犒賞自己，去做一直想做的事", "value_code": "c", "score_map": {"guardian": 0, "grower": 0, "experiencer": 3, "sharer": 1}},
                    {"option_text": "和家人朋友分享，請大家吃飯", "value_code": "d", "score_map": {"guardian": 0, "grower": 0, "experiencer": 1, "sharer": 3}},
                ],
            },
            {
                "question_text": "看到銀行帳戶餘額下降時，你的感受是？",
                "options": [
                    {"option_text": "會焦慮，馬上檢查哪裡可以節省", "value_code": "a", "score_map": {"guardian": 3, "grower": 1, "experiencer": 0, "sharer": 0}},
                    {"option_text": "不太擔心，因為錢放在其他投資裡", "value_code": "b", "score_map": {"guardian": 0, "grower": 3, "experiencer": 0, "sharer": 1}},
                    {"option_text": "有點在意但覺得花得值得就好", "value_code": "c", "score_map": {"guardian": 0, "grower": 0, "experiencer": 3, "sharer": 1}},
                    {"option_text": "如果是花在重要的人身上就不心疼", "value_code": "d", "score_map": {"guardian": 0, "grower": 0, "experiencer": 0, "sharer": 3}},
                ],
            },
            {
                "question_text": "對你來說，「財務自由」意味著什麼？",
                "options": [
                    {"option_text": "不用擔心突發狀況的安全感", "value_code": "a", "score_map": {"guardian": 3, "grower": 1, "experiencer": 0, "sharer": 0}},
                    {"option_text": "資產持續增長的成就感", "value_code": "b", "score_map": {"guardian": 0, "grower": 3, "experiencer": 1, "sharer": 0}},
                    {"option_text": "可以自由選擇生活方式", "value_code": "c", "score_map": {"guardian": 0, "grower": 0, "experiencer": 3, "sharer": 1}},
                    {"option_text": "有能力照顧身邊重要的人", "value_code": "d", "score_map": {"guardian": 1, "grower": 0, "experiencer": 0, "sharer": 3}},
                ],
            },
            {
                "question_text": "朋友向你推薦一個新的理財產品，你會？",
                "options": [
                    {"option_text": "先觀望，等確認安全再說", "value_code": "a", "score_map": {"guardian": 3, "grower": 1, "experiencer": 0, "sharer": 0}},
                    {"option_text": "仔細研究風險和回報率", "value_code": "b", "score_map": {"guardian": 1, "grower": 3, "experiencer": 0, "sharer": 0}},
                    {"option_text": "如果能帶來好的體驗就考慮", "value_code": "c", "score_map": {"guardian": 0, "grower": 0, "experiencer": 3, "sharer": 0}},
                    {"option_text": "看看朋友的經驗再決定", "value_code": "d", "score_map": {"guardian": 0, "grower": 0, "experiencer": 1, "sharer": 3}},
                ],
            },
            {
                "question_text": "如果明天不用工作了，你會？",
                "options": [
                    {"option_text": "先確保存款足夠支撐一段時間", "value_code": "a", "score_map": {"guardian": 3, "grower": 1, "experiencer": 0, "sharer": 0}},
                    {"option_text": "用時間研究新的被動收入方式", "value_code": "b", "score_map": {"guardian": 0, "grower": 3, "experiencer": 1, "sharer": 0}},
                    {"option_text": "去實現一直沒時間做的夢想", "value_code": "c", "score_map": {"guardian": 0, "grower": 0, "experiencer": 3, "sharer": 1}},
                    {"option_text": "花更多時間陪伴家人朋友", "value_code": "d", "score_map": {"guardian": 0, "grower": 0, "experiencer": 0, "sharer": 3}},
                ],
            },
        ],
        "result_profiles": [
            {
                "code": "guardian",
                "title": "穩健守護者",
                "short_label": "守護者",
                "description": "你是一個重視安全和穩定的人，金錢對你來說首先代表著安全感和保障。你會謹慎地管理每一分錢，確保自己和家人在任何情況下都能安心。你的理財方式偏向保守，但這絕對不是膽小，而是一種深思熟慮的智慧。你知道穩定的基礎才能支撐更大的夢想，這種踏實的態度讓你在財務上始終保持安全的距離。",
                "strengths": ["財務紀律性強，善於儲蓄和預算管理", "風險意識高，能避開不必要的損失", "給身邊的人帶來安全感和穩定感"],
                "growth_tips": ["可以將一小部分資金嘗試低風險的投資增長", "允許自己偶爾享受金錢帶來的快樂", "不必過度擔心未來，你已經做得很好了"],
                "encouragement": "你的穩健是最堅實的力量。在安全的基礎上，你有能力去探索更多可能性！",
                "share_text": "我是「穩健守護者」🛡️ 安全感是我最重視的財務基礎！",
            },
            {
                "code": "grower",
                "title": "智慧增長者",
                "short_label": "增長者",
                "description": "你是一個善於讓金錢為自己工作的人。你不滿足於單純的儲蓄，而是積極尋找讓資產增長的方式。你對投資和理財有著天然的興趣和洞察力，善於分析和研究各種機會。你的目標不是炫富，而是通過智慧的理財來實現更大的人生自由。你知道金錢是工具，而你擅長使用這個工具。",
                "strengths": ["善於學習和研究理財知識", "能夠理性分析風險和機會", "有長期規劃的眼光和耐心"],
                "growth_tips": ["不要讓理財佔據所有的注意力，生活還有更多面向", "學會享受當下，不必所有決定都以回報率衡量", "偶爾也可以做一些「不划算但快樂」的消費"],
                "encouragement": "你的理財智慧是許多人學習的榜樣。繼續成長，但也記得享受這段旅程！",
                "share_text": "我是「智慧增長者」📈 讓錢為我工作是我的理財哲學！",
            },
            {
                "code": "experiencer",
                "title": "體驗優先者",
                "short_label": "體驗者",
                "description": "你是一個相信金錢應該服務於生活體驗的人。對你來說，最好的投資就是投資在豐富的人生經歷上。你不是衝動消費，而是清楚知道什麼體驗對你有價值。你相信回憶比物品更珍貴，而那些用金錢換來的美好體驗，會成為你人生中最有價值的資產。",
                "strengths": ["清楚自己的價值觀和生活優先順序", "善於創造有意義的生活體驗", "對金錢的態度健康且正面"],
                "growth_tips": ["建立一個基本的緊急預備金，讓自己更安心", "在享受體驗的同時，也為未來做一些規劃", "偶爾檢視消費是否真正帶來了滿足感"],
                "encouragement": "你懂得生活的本質不在於擁有多少，而在於體驗多少。這份智慧讓你的人生格外精彩！",
                "share_text": "我是「體驗優先者」✨ 最好的投資就是投資在精彩的人生體驗上！",
            },
            {
                "code": "sharer",
                "title": "慷慨分享者",
                "short_label": "分享者",
                "description": "你是一個天生慷慨的人，金錢對你來說最大的價值在於能夠照顧和回饋身邊的人。你相信分享讓富足加倍，而你的付出總是發自真心。你不一定是最富有的人，但你絕對是最富有愛的人。你用金錢表達關懷的方式，讓身邊的人感受到溫暖和被重視。",
                "strengths": ["高度的同理心和關懷能力", "善於用行動表達愛和感謝", "在付出中找到真正的快樂和滿足"],
                "growth_tips": ["確保在照顧他人之前，先照顧好自己的財務需求", "學會接受別人的回饋和幫助", "設定合理的付出界限，慷慨也需要可持續"],
                "encouragement": "你的慷慨讓這個世界更溫暖。記住，照顧好自己，才能持續地照顧別人！",
                "share_text": "我是「慷慨分享者」🤝 分享讓快樂和富足都加倍！",
            },
        ],
    },
]


def seed():
    db = SessionLocal()
    try:
        for quiz_data in SEED_QUIZZES:
            existing = db.query(Quiz).filter(Quiz.slug == quiz_data["slug"]).first()
            if existing:
                print(f"  Skip: '{quiz_data['slug']}' already exists")
                continue

            quiz = Quiz(
                title=quiz_data["title"],
                slug=quiz_data["slug"],
                topic=quiz_data["topic"],
                summary=quiz_data["summary"],
                intro_text=quiz_data["intro_text"],
                estimated_minutes=quiz_data["estimated_minutes"],
                status=quiz_data["status"],
                publish_date=quiz_data["publish_date"],
            )
            db.add(quiz)
            db.flush()

            for qi, q in enumerate(quiz_data["questions"]):
                question = Question(
                    quiz_id=quiz.id,
                    question_text=q["question_text"],
                    order_index=qi,
                )
                db.add(question)
                db.flush()
                for oi, opt in enumerate(q["options"]):
                    option = QuestionOption(
                        question_id=question.id,
                        option_text=opt["option_text"],
                        option_value_code=opt["value_code"],
                        score_payload=opt["score_map"],
                        order_index=oi,
                    )
                    db.add(option)

            for rp in quiz_data["result_profiles"]:
                profile = ResultProfile(
                    quiz_id=quiz.id,
                    code=rp["code"],
                    title=rp["title"],
                    short_label=rp["short_label"],
                    description=rp["description"],
                    strengths=rp["strengths"],
                    growth_tips=rp["growth_tips"],
                    encouragement=rp["encouragement"],
                    share_text=rp["share_text"],
                )
                db.add(profile)

            db.commit()
            print(f"  ✓ Seeded: '{quiz_data['title']}'")

        print("\nSeed complete!")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
