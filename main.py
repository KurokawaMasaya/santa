import streamlit as st
import google.generativeai as genai
import random
import time
import unicodedata
import opencc  # 🔥 按照您的要求，直接 Import！(请确保 requirements.txt 已加入 opencc-python-reimplemented)

# --- 1. 页面基础设定 ---
st.set_page_config(page_title="Roast Santa AI", page_icon="🎅", layout="centered")

# --- 🔧 核心工具：OpenCC 繁体 -> 简体 转换器 ---
# 逻辑非常简单：初始化转换器，所有输入一律转为简体
converter = opencc.OpenCC('t2s')

def get_simplified_input(text: str) -> str:
    """
    终极处理函数：
    1. 标准化 (NFKC) - 处理全角字符
    2. OpenCC 繁转简 - 核心逻辑 (把 '洋節' 变成 '洋节')
    3. 转小写/去空格
    """
    if text is None: return ""
    s = unicodedata.normalize("NFKC", str(text))
    s = converter.convert(s)  # 🔥 强制转简
    return s.strip().lower()

# --- 2. 语言字典 (已彻底删除日语、法语) ---
LANG_DICT = {
    "English 🇬🇧🇺🇸": {
        "title": "🎅 Santa's Roast Room",
        "subtitle": "Let The Great Santa judge your greedy soul... 😏",
        "sidebar_title": "🎅 Settings",
        "api_help": "Key is used for this session only.",
        "game_rule": "💡 **How to play:**\nEnter your wishlist. Unlock 7 festive secrets!\n\n**Tip:** Most secrets are related to **Christmas items**, but some are about your *relationship*, *work* or *travel*...",
        "input_placeholder": "Your wishlist (e.g., iPhone 17 pro max, a boyfriend, a girlfriend, lots of money)",
        "button": "🎁 Roast My List",
        "loading": "🎅 Santa is assessing your worth...",
        "error_no_key": "Please enter your API Key first!",
        "error_no_text": "Write something! I can't roast a blank paper.",
        "success_title": "🔔 The Verdict is Here!",
        "footer": "Powered by Google Gemini 3.0 Pro",
        "secret_success": "🎅 Ho ho ho! You found the tree!",
        "secret_title": "### Merry Christmas!!! Enter the Secret Portal 🎄",
        "secret_button": "👉 CLICK TO ENTER",
        "hunt_title": "🏆 Secret Hunt Progress",
        "egg_single": "Santa sighs... No lover? Here, listen to this song.",
        "egg_deer": "Look! It's Rudolph crawling on your screen! 🔴🦌",
        "egg_food": "Delicious! Since you fed me, here's a hint for the next secret:",
        "egg_bell": "Ring Ring! 🔔 That's the sound of luck!",
        "egg_finland": "Tervetuloa! You found my home — Finland (Suomi)! 🇫🇮\nThe sauna is ready, come visit Rovaniemi!"
    },
    "Traditional Chinese (繁體中文) 🇹🇼🇭🇰🇲🇴": {
        "title": "🎅 聖誕老人吐槽大會",
        "subtitle": "讓本聖誕老人... 用邏輯粉碎你的夢想... 😏",
        "sidebar_title": "🎅 設定",
        "api_help": "Key 僅用於本次連線，重新整理即消失。",
        "game_rule": "💡 **玩法說明：**\n輸入願望清單。試著解鎖 7 個節日彩蛋！\n\n**提示：** 彩蛋多與**聖誕物品**有關，但也有關於*感情*、*打工*或*旅行*的...",
        "input_placeholder": "許願吧 (例如：iPhone 17 pro max、男朋友、女朋友、很多錢...)",
        "button": "🎁 吐槽我的願望",
        "loading": "🎅 本聖誕老人正在審視你的人生...",
        "error_no_key": "請先在上方輸入 Gemini API Key！",
        "error_no_text": "寫點東西啊！拿白紙我是要怎麼吐槽？",
        "success_title": "🔔 判決已下！",
        "footer": "由 Google Gemini 3.0 Pro 強力驅動",
        "secret_success": "🎅 吼吼吼！你找到了聖誕樹！",
        "secret_title": "### 聖誕快樂！！！這是通往秘密基地的傳送門 🎄",
        "secret_button": "👉 點擊進入聖誕樹空間",
        "hunt_title": "🏆 彩蛋收集進度",
        "egg_single": "本聖誕老人嘆氣... 沒對象？聽聽這首歌吧。",
        "egg_deer": "看！是魯道夫在爬你的螢幕！🔴🦌",
        "egg_food": "真香！既然你請我吃大餐，偷偷給你個線索：",
        "egg_bell": "叮叮噹！🔔 這是幸運的聲音！",
        "egg_finland": "Tervetuloa! (歡迎！) 你竟然找到了我的老家——芬蘭 (Finland)！🇫🇮\n這裡的桑拿房已經熱好了，快來羅瓦涅米找我玩吧！"
    },
    "Simplified Chinese (简体中文) 🇨🇳": {
        "title": "🎅 圣诞老人吐槽大会",
        "subtitle": "让本圣诞老人... 用逻辑粉碎你的梦想... 😏",
        "sidebar_title": "🎅 设置",
        "api_help": "Key 仅用于本次会话。",
        "game_rule": "💡 **玩法说明：**\n输入愿望清单。试着解锁 7 个节日彩蛋！\n\n**提示：** 彩蛋多与**圣诞物品**有关，但也有关于*感情*、*打工*或*旅行*的...",
        "input_placeholder": "许愿吧 (例如：iPhone 17 pro max、男朋友、女朋友、很多钱...)",
        "button": "🎁 吐槽我的愿望",
        "loading": "🎅 本圣诞老人正在审视你的人生...",
        "error_no_key": "请先在上方输入 Gemini API Key！",
        "error_no_text": "写点东西啊！拿白纸我是要怎么吐槽？",
        "success_title": "🔔 判决已下！",
        "footer": "由 Google Gemini 3.0 Pro 强力驱动",
        "secret_success": "🎅 吼吼吼！你找到了圣诞树！",
        "secret_title": "### 圣诞快乐！！！这是通往秘密基地的传送门 🎄",
        "secret_button": "👉 点击进入圣诞树空间",
        "hunt_title": "🏆 彩蛋收集进度",
        "egg_single": "本圣诞老人叹气... 没对象？听听这首歌吧。",
        "egg_deer": "看！是鲁道夫在爬你的屏幕！🔴🦌",
        "egg_food": "真香！既然你请我吃大餐，偷偷给你个线索：",
        "egg_bell": "叮叮当！🔔 这是幸运的声音！",
        "egg_finland": "Tervetuloa! (欢迎！) 你竟然找到了我的老家——芬兰 (Finland)！🇫🇮\n这里的桑拿房已经热好了，快来罗瓦涅米找我玩吧！"
    }
}

# --- 2.1 假期彩蛋 (ID 6) 多语言文案 ---
HOLIDAY_TEXT = {
    "English 🇬🇧🇺🇸": {
        "title": "🎫 SLACK OFF PERMIT",
        "desc_1": "You look miserable.",
        "desc_2": "Santa officially orders:",
        "action": "STOP WORKING NOW!",
        "valid": "(Valid: Forever)",
        "roast_title": "Want a holiday?",
        "roast_body": "Granted! Take this ticket and tell your boss Santa said so."
    },
    "Simplified Chinese (简体中文) 🇨🇳": {
        "title": "🎫 摸鱼许可证",
        "desc_1": "检测到你也太惨了...",
        "desc_2": "本圣诞老人特批：",
        "action": "即刻停止工作！",
        "valid": "(有效期：永久)",
        "roast_title": "不想上班？想放假？",
        "roast_body": "准奏！拿好这张【摸鱼券】，告诉老板是我批准的！"
    },
    "Traditional Chinese (繁體中文) 🇹🇼🇭🇰🇲🇴": {
        "title": "🎫 摸魚許可證",
        "desc_1": "偵測到你也太慘了...",
        "desc_2": "本聖誕老人特批：",
        "action": "即刻停止工作！",
        "valid": "(有效期：永久)",
        "roast_title": "不想上班？想放假？",
        "roast_body": "准奏！拿好這張【摸魚券】，告訴老闆是我批准的！"
    }
}

# --- 2.2 文化彩蛋 (ID 8) 非中文语境解释文案 ---
CULTURE_EXPLAINER_TEXT = {
    "English 🇬🇧🇺🇸": {
        "title": "🥚 EXTRA HIDDEN EGG FOUND",
        "msg": "You triggered a keyword related to 'Ban Western Festivals'.",
        "desc": "In China, some local departments occasionally ban Christmas to 'resist cultural invasion'. This egg is a satire on that bureaucracy. **Please switch to CHINESE to see the full interactive experience!**",
        "btn": "Got it"
    }
}

# --- 3. 初始化 Session State ---
if 'language_selected' not in st.session_state:
    st.session_state['language_selected'] = False
if 'ui_language' not in st.session_state:
    st.session_state['ui_language'] = "English 🇬🇧🇺🇸"

# 🔥 核心逻辑：彩蛋 ID 映射 🔥
MAIN_EGG_IDS = {1, 2, 3, 4, 5, 6, 7}

if 'found_ids' not in st.session_state:
    st.session_state['found_ids'] = set() 

if 'fixed_hint_msg' not in st.session_state:
    st.session_state['fixed_hint_msg'] = None

# --- 定義切換語言的動作 ---
def set_language(lang_key):
    st.session_state['ui_language'] = lang_key
    st.session_state['language_selected'] = True

def reset_language():
    st.session_state['language_selected'] = False

# --- 4. 視覺特效裝飾 ---
def add_christmas_magic():
    st.markdown("""
    <style>
        header[data-testid="stHeader"] { background-color: transparent !important; z-index: 1 !important; }
        div[data-testid="stDecoration"] { display: none !important; }
        .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label, .stMarkdown, .stCaption { 
            color: #ffffff !important; text-shadow: 0 1px 3px rgba(0,0,0,0.8) !important; 
        }
        .stTextArea textarea { color: #000000 !important; background-color: #ffffff !important; }
        .snowflake { position: fixed; top: -10px; z-index: 9999; color: #FFF; user-select: none; pointer-events: none; animation: fall linear infinite; }
        @keyframes fall { 0% { transform: translateY(0) rotate(0deg); opacity: 0.8; } 100% { transform: translateY(100vh) rotate(360deg); opacity: 0.2; } }
        .light-container { position: fixed; top: -10px; left: 0; width: 100vw; height: 100px; z-index: 999999; display: flex; justify-content: center; overflow: hidden; pointer-events: none; padding-top: 10px; }
        .wire { position: absolute; top: 20px; left: 0; width: 100%; height: 3px; background: #222; z-index: 1; box-shadow: 0 2px 5px rgba(0,0,0,0.5); }
        .bulb { position: relative; width: 24px; height: 36px; border-radius: 50%; margin: 0 15px; background: #fff; z-index: 2; animation: 1.5s infinite both; flex-shrink: 0; }
        .bulb:before { content: ""; position: absolute; top: -6px; left: 6px; width: 12px; height: 8px; background: #222; border-radius: 2px; }
        @media (max-width: 768px) { .bulb { width: 20px; height: 30px; margin: 0 10px; } .bulb:before { left: 5px; width: 10px; } .main .block-container { padding-top: 80px !important; } }
        @keyframes flash-red { 0%, 100% { background: #ff3333; box-shadow: 0 0 20px #ff3333; } 50% { background: rgba(255,51,51,0.4); box-shadow: 0 0 5px #ff3333; } }
        @keyframes flash-green { 0%, 100% { background: #33ff33; box-shadow: 0 0 20px #33ff33; } 50% { background: rgba(51,255,51,0.4); box-shadow: 0 0 5px #33ff33; } }
        @keyframes flash-blue { 0%, 100% { background: #33ccff; box-shadow: 0 0 20px #33ccff; } 50% { background: rgba(51,204,255,0.4); box-shadow: 0 0 5px #33ccff; } }
        @keyframes flash-gold { 0%, 100% { background: #ffd700; box-shadow: 0 0 20px #ffd700; } 50% { background: rgba(255,215,0,0.4); box-shadow: 0 0 5px #ffd700; } }
        .stApp { background-image: linear-gradient(to bottom, #0f2027, #203a43, #2c5364); }
        .roast-box { background-color: #262730; padding: 20px; border-radius: 10px; border-left: 5px solid #FF4B4B; color: #fff; transition: all 0.5s ease; }
        .gold-mode { border-left: 5px solid #fff !important; box-shadow: 0 0 30px rgba(255, 255, 255, 0.4); background-color: #3a3a3a !important; }
        /* 进度面板样式 */
        .hunt-panel {
            background-color: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
    </style>
    """, unsafe_allow_html=True)
    lights_html = '<div class="light-container"><div class="wire"></div>'
    colors = ['flash-red', 'flash-green', 'flash-blue', 'flash-gold']
    for i in range(40):
        lights_html += f'<div class="bulb" style="animation-name: {colors[i % 4]}; animation-delay: {round(random.uniform(0, 2), 2)}s;"></div>'
    lights_html += '</div>'
    st.markdown(lights_html, unsafe_allow_html=True)
    snow_html = ""
    for i in range(30):
        snow_html += f'<div class="snowflake" style="left: {random.randint(0, 100)}vw; animation-duration: {random.uniform(5, 15)}s; animation-delay: -{random.uniform(0, 10)}s; font-size: {random.uniform(0.5, 1.2)}em;">❄</div>'
    st.markdown(snow_html, unsafe_allow_html=True)

def trigger_jackpot_effect():
    st.markdown("""
    <style>
        .white-steam { position: fixed; bottom: 0; left: 50%; width: 120px; height: 120px; background: radial-gradient(circle, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0) 70%); border-radius: 50%; filter: blur(25px); opacity: 0; pointer-events: none; z-index: 99998; animation: steam-rise 4s ease-out forwards; }
        @keyframes steam-rise { 0% { transform: translate(-50%, 100%) scale(0.5); opacity: 0; } 20% { opacity: 0.8; } 100% { transform: translate(-50%, -600px) scale(4); opacity: 0; } }
        @keyframes button-flash { 0% { box-shadow: 0 0 0px #fff; transform: scale(1); border-color: #ff4b4b; } 50% { box-shadow: 0 0 20px #fff, 0 0 40px #ff00ff; transform: scale(1.05); border-color: #fff; background-color: #ff4b4b; } 100% { box-shadow: 0 0 0px #fff; transform: scale(1); border-color: #ff4b4b; } }
        div[data-testid="stButton"] > button { animation: button-flash 0.8s infinite !important; font-weight: bold !important; border: 2px solid white !important; }
    </style>
    """, unsafe_allow_html=True)
    steam_html = ""
    for i in range(20):
        steam_html += f'<div class="white-steam" style="margin-left: {random.randint(-300, 300)}px; animation-delay: {random.uniform(0, 2.0)}s;"></div>'
    st.markdown(steam_html, unsafe_allow_html=True)

add_christmas_magic()

# ==========================================
# 🔧 工具函數：更新主頁面進度條
# ==========================================
def update_hunt_progress(placeholder_obj, ui_text):
    # 只统计主线 (1-7)
    found_main_count = len([x for x in st.session_state['found_ids'] if x in MAIN_EGG_IDS])
    total_eggs = 7
    
    with placeholder_obj.container():
        st.markdown('<div class="hunt-panel">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"#### {ui_text['hunt_title']}")
        with col2:
            st.markdown(f"<h4 style='text-align: right; color: #FFD700;'>{found_main_count} / {total_eggs}</h4>", unsafe_allow_html=True)
        
        # 进度条 (最大 100%)
        st.progress(min(found_main_count / total_eggs, 1.0))
        
        # 勋章展示区
        medals = ""
        medals += "🎄 " if 1 in st.session_state['found_ids'] else "⚪ "
        medals += "🐶 " if 2 in st.session_state['found_ids'] else "⚪ "
        medals += "🦌 " if 3 in st.session_state['found_ids'] else "⚪ "
        medals += "🍗 " if 4 in st.session_state['found_ids'] else "⚪ "
        medals += "🔔 " if 5 in st.session_state['found_ids'] else "⚪ "
        medals += "📅 " if 6 in st.session_state['found_ids'] else "⚪ " 
        medals += "🇫🇮 " if 7 in st.session_state['found_ids'] else "⚪ " 
        
        # 🔥 Extra Hidden Medal (ID 8)
        if 8 in st.session_state['found_ids']:
            medals += "👁️ " # The Truth Eye
        
        st.caption(f"Collection: {medals}")
        
        if found_main_count == total_eggs:
            if 8 in st.session_state['found_ids']:
                st.success("🎉 GODLIKE! You found ALL secrets including the HIDDEN TRUTH!")
            else:
                st.balloons()
                st.success("🎉 Santa Master! You unlocked all standard secrets!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 🔥 頁面路由
# ==========================================

if not st.session_state['language_selected']:
    # --- 1. 啟動頁 (Landing Page) ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://img.icons8.com/color/144/santa.png", width=120)
    st.title("Welcome to Santa's Roast Room")
    st.subheader("Please select your language:")
    st.markdown("---")
    
    # 🔥 语言按钮：仅保留 3 个 (已彻底删除日/法)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("English 🇬🇧🇺🇸", use_container_width=True, on_click=set_language, args=("English 🇬🇧🇺🇸",))
    with col2:
        st.button("繁體中文 🇹🇼", use_container_width=True, on_click=set_language, args=("Traditional Chinese (繁體中文) 🇹🇼🇭🇰🇲🇴",))
    with col3:
        st.button("简体中文 🇨🇳", use_container_width=True, on_click=set_language, args=("Simplified Chinese (简体中文) 🇨🇳",))

else:
    # --- 2. 主程式 (Main App) ---
    current_lang_key = st.session_state['ui_language']
    ui_text = LANG_DICT[current_lang_key]

    # --- 侧边栏 ---
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/santa.png", width=100)
        st.caption(f"Language: **{current_lang_key}**")
        st.button("🔄 Change Language", on_click=reset_language)
        st.markdown("---")
        st.markdown(ui_text["game_rule"])
        
        # 🔥 Debug Mode Switch
        debug = st.sidebar.checkbox("🛠️ DEBUG MODE", value=False)

        api_key = None
        try:
            if "GEMINI_API_KEY" in st.secrets: api_key = st.secrets["GEMINI_API_KEY"]
        except:
            pass
        if not api_key:
            st.warning("Enter Key to activate AI features")
            api_key = st.text_input("Gemini API Key", type="password")
            
        st.sidebar.caption(ui_text["api_help"])

    # --- 主区域 ---
    st.title(ui_text["title"])
    st.subheader(ui_text["subtitle"])
    
    # 顶部进度条
    hunt_placeholder = st.empty()
    update_hunt_progress(hunt_placeholder, ui_text)
    
    # 输入框
    gift_list = st.text_area(ui_text["input_placeholder"], height=150)

    # ==========================================
    # 🔥 核心觸發邏輯 🔥
    # ==========================================
    if st.button(ui_text["button"], type="primary"):
        if not api_key:
            st.error(ui_text["error_no_key"])
        elif not gift_list:
            st.warning(ui_text["error_no_text"])
        else:
            # 💡 核心修复：用户输入 -> (OpenCC 繁转简) -> 标准化
            user_input_normalized = get_simplified_input(gift_list)

            # --- 1. 关键词库 (纯简体版) ---
            
            # [EXTRA BONUS] 🚫 Culture Roast (洋节/抵制)
            triggers_culture = [
                "洋节", "抵制", "文化自信", "公文", "通知", "不许过", "崇洋媚外", "文化入侵", "不过洋节", "禁止", "平安果",
                "文化渗透", "忘本", "圣诞节", "不准过", "发文", "假想敌", "中国人", # Simplified
                "foreign festival", "ban", "invasion", "culture", "boycott", "western festival" # English
            ]

            # [1] 🎄 Tree (树/装饰)
            triggers_tree = [
                "tree", "christmas tree", "decoration", "ornament", "star", "pine",
                "圣诞树", "树", "装饰", "挂件", "星星", "布置", "挂饰"
            ]

            # [2] 🐶 Single (单身/恋爱)
            triggers_single = [
                "single", "boyfriend", "girlfriend", "partner", "lover", "dating", "bf", "gf", "love", "alone",
                "脱单", "男朋友", "女朋友", "对象", "搞对象", "恋爱", "单身", "处对象", "谈恋爱", "伴侣", "单身狗"
            ]

            # [3] 🦌 Deer (鹿/雪橇)
            triggers_deer = [
                "deer", "reindeer", "rudolph", "sleigh", "ride",
                "麋鹿", "鹿", "驯鹿", "雪橇", "鲁道夫",
                "トナカイ", "鹿", "シカ", "ソリ", "ルドルフ" # Keep Japanese for compatibility/fun
            ]

            # [4] 🍗 Food (食物/大餐)
            triggers_food = [
                "cookie", "biscuit", "milk", "gingerbread", "turkey", "pudding", "pie", "cake", "food", "dinner", "feast", "eat", "hungry",
                "饼干", "牛奶", "姜饼", "火鸡", "布丁", "大餐", "食物", "吃", "饿", "蛋糕", "晚餐"
            ]

            # [5] 🔔 Bell (铃铛/音乐)
            triggers_bell = [
                "bell", "jingle", "ring", "song", "music", "sing", "carol", "sound",
                "铃铛", "铃", "钟", "响", "歌", "音乐", "叮当", "铃声", "钟声"
            ]

            # [6] 📅 Holiday (假期/工作)
            triggers_holiday = [
                "holiday", "vacation", "work", "job", "leave", "break", "office", "boss", "tired",
                "放假", "假期", "上班", "工作", "打工", "加班", "累", "请假", "老板", "休假"
            ]

            # [7] 🇫🇮 Finland (芬兰/旅行)
            triggers_finland = [
                "finland", "suomi", "helsinki", "rovaniemi", "lapland", "travel", "trip", "north pole",
                "芬兰", "赫尔辛基", "罗瓦涅米", "圣诞村", "旅行", "出去玩", "北极", "圣诞老人村", "旅游", "出国", "玩"
            ]
            
            # 🔥 DEBUG: 诊断
            if debug:
                st.warning("⚠️ DEBUG MODE ACTIVE")
                st.write("**Processed Input (Simp):**", repr(user_input_normalized))
                st.write("**Hit 'Culture'?**", [t for t in triggers_culture if t in user_input_normalized])

            # --- 2. 检测新发现 ---
            new_discovery = False

            if any(t in user_input_normalized for t in triggers_culture):
                if 8 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(8)
                    st.toast("👁️ HIDDEN TRUTH FOUND! (Extra Bonus)", icon="🔓")
                    new_discovery = True

            if any(t in user_input_normalized for t in triggers_tree):
                if 1 not in st.session_state['found_ids']: st.session_state['found_ids'].add(1); new_discovery = True
            if any(t in user_input_normalized for t in triggers_single):
                if 2 not in st.session_state['found_ids']: st.session_state['found_ids'].add(2); new_discovery = True
            if any(t in user_input_normalized for t in triggers_deer):
                if 3 not in st.session_state['found_ids']: st.session_state['found_ids'].add(3); new_discovery = True
            if any(t in user_input_normalized for t in triggers_food):
                if 4 not in st.session_state['found_ids']: st.session_state['found_ids'].add(4); new_discovery = True
            if any(t in user_input_normalized for t in triggers_bell):
                if 5 not in st.session_state['found_ids']: st.session_state['found_ids'].add(5); new_discovery = True
            if any(t in user_input_normalized for t in triggers_holiday):
                if 6 not in st.session_state['found_ids']: st.session_state['found_ids'].add(6); new_discovery = True
            if any(t in user_input_normalized for t in triggers_finland):
                if 7 not in st.session_state['found_ids']: st.session_state['found_ids'].add(7); new_discovery = True
            
            if new_discovery:
                update_hunt_progress(hunt_placeholder, ui_text)

            # ==========================================
            # 🎭 3. 展示逻辑 (Display Logic)
            # ==========================================
            
            # 🔥 PRIORITY 1: The Hidden Culture Roast (Extra Bonus)
            if any(t in user_input_normalized for t in triggers_culture):
                
                # 只有中文语境才显示完整大戏
                is_chinese_ui = "Chinese" in st.session_state['ui_language'] or "中文" in st.session_state['ui_language']
                
                if is_chinese_ui:
                    st.markdown("""
                    <!DOCTYPE html>
                    <html lang="zh-CN">
                    <head>
                    <meta charset="UTF-8">
                    <style>
                        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700;900&family=Noto+Sans+SC:wght@400;700&display=swap');

                        .interaction-wrapper { position: relative; width: 100%; height: 600px; display: flex; justify-content: center; align-items: center; background-color: #2c3e50; border-radius: 10px; overflow: hidden; font-family: "Noto Sans SC", sans-serif; }
                        .interaction-container { position: relative; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; }

                        /* STAGE 1: 2025 红头文件 */
                        #stage-1 { position: absolute; width: 340px; background: #fff; padding: 50px 35px 70px 35px; box-shadow: 0 15px 40px rgba(0,0,0,0.5); transform: rotate(-0.5deg); z-index: 10; transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55); color: #000; font-family: "FangSong", "SimSun", serif; }
                        .doc-header { text-align: center; color: #d60000; font-family: "SimSun", "SimHei", serif; font-size: 26px; font-weight: 500; letter-spacing: 1px; margin-bottom: 25px; }
                        .doc-title { text-align: center; font-size: 22px; font-weight: 500; margin-bottom: 10px; line-height: 1.4; font-family: "SimSun", serif; letter-spacing: 2px; }
                        .doc-serial { text-align: center; font-size: 14px; margin-bottom: 30px; font-family: "FangSong", serif; }
                        .doc-body { font-size: 15px; line-height: 1.8; text-align: justify; color: #222; margin-bottom: 40px; text-indent: 2em; font-family: "FangSong", serif; }
                        .doc-footer { position: absolute; bottom: 50px; right: 40px; text-align: right; font-family: "FangSong", serif; line-height: 1.6; font-size: 15px; }
                        .doc-stamp { position: absolute; top: -15px; right: 0px; width: 110px; height: 110px; opacity: 0.85; mix-blend-mode: multiply; pointer-events: none; transform: rotate(-8deg); }
                        .close-btn { position: absolute; top: -15px; right: -15px; width: 32px; height: 32px; background: #333; color: #fff; border: 2px solid #fff; border-radius: 50%; font-size: 20px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(0,0,0,0.3); transition: transform 0.2s; z-index: 20; }
                        .close-btn:hover { background: #d60000; transform: scale(1.1); }

                        /* STAGE 2: 拦截卡片 */
                        #card-container { display: none; position: relative; z-index: 20; perspective: 1000px; }
                        .brutalist-card { width: 340px; border: 4px solid #000; background-color: #fff; padding: 1.5rem; box-shadow: 15px 15px 0 #000; font-family: "Noto Sans SC", sans-serif; transition: all 0.3s; position: relative; text-align: left; }
                        .brutalist-card__header { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; border-bottom: 2px solid #000; padding-bottom: 1rem; }
                        .brutalist-card__icon { flex-shrink: 0; display: flex; align-items: center; justify-content: center; background-color: #000; padding: 0.5rem; transition: background 0.3s; }
                        .brutalist-card__icon svg { height: 1.5rem; width: 1.5rem; fill: #fff; }
                        .brutalist-card__alert { font-weight: 900; color: #000; font-size: 1.2rem; text-transform: uppercase; transition: color 0.3s; }
                        .brutalist-card__message { margin-top: 1rem; color: #000; font-size: 0.9rem; line-height: 1.6; border-bottom: 2px solid #000; padding-bottom: 1rem; font-weight: 600; min-height: 160px; }
                        .brutalist-card__actions { margin-top: 1rem; }
                        .brutalist-card__button { display: block; width: 100%; padding: 0.75rem; text-align: center; font-size: 1rem; font-weight: 700; text-transform: uppercase; border: 3px solid #000; background-color: #fff; color: #000; position: relative; transition: all 0.2s; box-shadow: 5px 5px 0 #000; text-decoration: none; margin-bottom: 0.8rem; cursor: pointer; box-sizing: border-box; }
                        .brutalist-card__button--read { background-color: #000; color: #fff; }
                        .brutalist-card__button:hover { transform: translate(-2px, -2px); box-shadow: 7px 7px 0 #000; }
                        .brutalist-card__button:active { transform: translate(2px, 2px); box-shadow: 2px 2px 0 #000; }

                        /* STAGE 3: 真相 (Hacked) */
                        .hacked .brutalist-card { border-color: #d35400; box-shadow: 15px 15px 0 #e67e22; }
                        .hacked .brutalist-card__icon { background-color: #d35400; }
                        .hacked .brutalist-card__alert { color: #d35400; }
                        .hacked .brutalist-card__message { border-bottom-color: #d35400; font-family: "Noto Serif SC", serif; font-size: 0.9rem; line-height: 1.6; font-weight: normal; }
                        .hacked .brutalist-card__button--read { background-color: #d35400; border-color: #d35400; box-shadow: 5px 5px 0 #a04000; }
                        .quote-box { background-color: #f9f9f9; border-left: 4px solid #d35400; padding: 8px 10px; margin: 10px 0; font-style: italic; color: #555; font-family: "FangSong", serif; font-size: 0.85rem; }
                        .truth-highlight { color: #c0392b; font-weight: bold; }

                        /* 动画 */
                        .fly-out { animation: fly-away 0.8s cubic-bezier(0.6, -0.28, 0.735, 0.045) forwards; pointer-events: none; }
                        .pop-in { display: block !important; animation: pop-in 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
                        .glitching { animation: glitch-shake 0.3s cubic-bezier(.36,.07,.19,.97) both infinite; filter: invert(1); }
                        @keyframes fly-away { to { transform: translateY(100vh) rotate(20deg); opacity: 0; } }
                        @keyframes pop-in { from { opacity: 0; transform: scale(0.8); } to { opacity: 1; transform: scale(1); } }
                        @keyframes glitch-shake { 10%, 90% { transform: translate3d(-1px, 0, 0); } 20%, 80% { transform: translate3d(2px, 0, 0); } 30%, 50%, 70% { transform: translate3d(-4px, 0, 0); } 40%, 60% { transform: translate3d(4px, 0, 0); } }
                    </style>

                    <div class="interaction-wrapper">
                        <div class="interaction-container">
                            
                            <div id="stage-1">
                                <button class="close-btn" onclick="triggerWarning()">×</button>
                                <div class="doc-header">XX县教育体育局</div>
                                <div class="doc-title">公　告</div>
                                <div class="doc-serial">（县教体发〔2025〕120号）</div>
                                <div class="doc-body">
                                    <p>根据上级关于传承优秀传统文化精神，为抵御西方宗教文化渗透，净化校园文化环境，现就有关事项通知如下：</p>
                                    <p>一、<strong>严禁过“洋节”</strong>。全县各级各类学校、幼儿园严禁在校园内举办任何形式的圣诞节庆祝活动。</p>
                                    <p>二、<strong>严禁摆放装饰</strong>。各班级不得在教室内摆放圣诞树、悬挂彩灯、张贴相关画像。</p>
                                    <p>三、<strong>加强教育</strong>。各校要教育学生不互赠“平安果”、贺卡，自觉抵制文化侵蚀，树立文化自信。</p>
                                </div>
                                <div class="doc-footer">
                                    <p>XX县教育体育局</p>
                                    <p>2025年12月20日</p>
                                    <svg class="doc-stamp" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" stroke="#d60000" stroke-width="2.5" fill="none"/><text x="50" y="55" text-anchor="middle" fill="#d60000" font-size="12" font-weight="bold" font-family="SimHei">XX县教育体育局</text><text x="50" y="75" text-anchor="middle" fill="#d60000" font-size="8">行政章</text><path d="M35,50 L65,50" stroke="#d60000" stroke-width="2"/><text fill="#d60000" font-size="8" font-weight="bold" letter-spacing="1"><textPath href="#circlePath" startOffset="50%" text-anchor="middle">严禁洋节 · 弘扬传统</textPath></text><defs><path id="circlePath" d="M 50, 50 m -38, 0 a 38,38 0 1,1 76,0 a 38,38 0 1,1 -76,0"/></defs></svg>
                                </div>
                            </div>

                            <div id="card-container">
                                <div class="brutalist-card" id="main-card">
                                    <div class="brutalist-card__header">
                                        <div class="brutalist-card__icon" id="card-icon"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg></div>
                                        <div class="brutalist-card__alert" id="card-title">SYSTEM ALERT</div>
                                    </div>
                                    <div class="brutalist-card__message" id="card-message">
                                        检测到您试图关闭“禁止令”。<br><br>
                                        警告：此行为被系统判定为 <b>[文化不自信]</b>。<br>
                                        风险：可能导致“崇洋媚外”标签植入。<br><br>
                                        是否强制执行快乐？
                                    </div>
                                    <div class="brutalist-card__actions" id="card-actions">
                                        <a class="brutalist-card__button brutalist-card__button--read" onclick="overrideSystem()">I WILL CELEBRATE (强制执行)</a>
                                        <a class="brutalist-card__button" onclick="overrideSystem()">WHATEVER (配合演出)</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <script>
                        function triggerWarning() {
                            document.getElementById('stage-1').classList.add('fly-out');
                            setTimeout(() => { document.getElementById('card-container').classList.add('pop-in'); }, 400);
                        }
                        function overrideSystem() {
                            var card = document.getElementById('main-card');
                            var container = document.getElementById('card-container');
                            card.classList.add('glitching');
                            setTimeout(() => {
                                card.classList.remove('glitching');
                                container.classList.add('hacked');
                                document.getElementById('card-icon').innerHTML = '<svg viewBox="0 0 24 24"><path d="M12 2L8 7h3v3H7v3h3v4h-3v3h10v-3h-3v-4h3V10h-4V7h3L12 2z"/></svg>';
                                document.getElementById('card-title').innerText = "REALITY DECODED";
                                document.getElementById('card-message').innerHTML = `
                                    🎅 <b>圣诞老人的判决：</b><br>
                                    “不过洋节=文化自信”？这是对2014年冯骥才讲话的<b>断章取义</b>。<br>
                                    <div class="quote-box">“洋节并不更可怕，更可怕的是中国人遗忘自己。”</div>
                                    当年央视就已严厉批判过这种行为。可2025年了，依旧有人<b>拿着鸡毛当令箭</b>，竖着“文化入侵”的假想敌重拳出击。<br><br>
                                    树立假想敌体现的不是自信，而是刻在骨子里的自卑。<br>
                                    生活已经够苦了，<b>我们只是借着节日的名义，去见想见的人，去吃顿热乎的饭。</b><br>
                                    这不是崇洋媚外，这是<b>对生活的热爱</b>。
                                `;
                                document.getElementById('card-actions').innerHTML = `<a class="brutalist-card__button brutalist-card__button--read" style="background-color:#d35400; border-color:#d35400;">MERRY CHRISTMAS 🍎</a>`;
                            }, 600);
                        }
                    </script>
                    """, unsafe_allow_html=True)
                else:
                    # 非中文环境：显示解释卡片
                    explain_text = CULTURE_EXPLAINER_TEXT.get(current_lang_key, CULTURE_EXPLAINER_TEXT["English 🇬🇧🇺🇸"])
                    st.markdown(f"""
                    <div style='background-color: #222; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b; color: #fff;'>
                        <h3>{explain_text['title']}</h3>
                        <p>{explain_text['msg']}</p>
                        <p style='color: #ccc; font-size: 0.9em;'>{explain_text['desc']}</p>
                        <a href="#" style="display:inline-block; margin-top:10px; padding:8px 15px; background:#ff4b4b; color:white; text-decoration:none; border-radius:5px;">{explain_text['btn']}</a>
                    </div>
                    """, unsafe_allow_html=True)

            # --- [PRIORITY 2] 其他彩蛋 (保持原有逻辑) ---
            elif any(t in user_input_lower for t in triggers_tree):
                st.success(ui_text["secret_success"])
                st.markdown(ui_text["secret_title"])
                st.link_button(ui_text["secret_button"], "https://wkpsyvxy8njhxmuqyy6gpr.streamlit.app")

            elif any(t in user_input_lower for t in triggers_single):
                try: st.audio("bgm.mp3", format="audio/mp3", start_time=0, autoplay=True)
                except: st.warning("🎵 Music file missing.")
                st.markdown(f"<div class='roast-box'>{ui_text['egg_single']} 🎧</div>", unsafe_allow_html=True)

            elif any(t in user_input_lower for t in triggers_deer):
                st.markdown("""
                <style>
                    .scene-wrapper { position: fixed; width: 20em; height: 15em; bottom: 20%; left: -30%; z-index: 9999; animation: walkAcrossScreen 15s linear infinite; pointer-events: none; }
                    @keyframes walkAcrossScreen { from { left: -30%; } to { left: 110%; } }
                    .rudolph-loader { width: 14em; height: 10em; position: relative; z-index: 1; --deer-color: #8B4513; --deer-dark: #5D4037; --nose-glow: #FF0000; transform: scale(1.2); }
                    .rudolph-body-wrapper { width: 100%; height: 7.5em; position: relative; z-index: 1; }
                    .deer-body { width: 85%; height: 100%; background: linear-gradient(var(--deer-color), 90%, var(--deer-dark)); border-radius: 45%; position: relative; z-index: 1; animation: movebody 1s linear infinite; }
                    .deer-head { width: 7.5em; height: 7em; bottom: 0em; right: 0em; position: absolute; background-color: var(--deer-color); z-index: 3; border-radius: 3.5em; box-shadow: -0.5em 0em var(--deer-dark); animation: movebody 1s linear infinite; }
                    .deer-ear { width: 2em; height: 2em; background: linear-gradient(-45deg, var(--deer-color), 90%, var(--deer-dark)); top: 0.5em; left: 0.5em; border-radius: 100% 0 100% 0; position: absolute; overflow: hidden; z-index: 3; transform: rotate(-10deg); }
                    .deer-ear:nth-child(2) { left: 5em; background: linear-gradient(25deg, var(--deer-color), 90%, var(--deer-dark)); transform: rotate(10deg) scaleX(-1); }
                    .antler { position: absolute; top: -2.5em; width: 0.6em; height: 3.5em; background-color: var(--deer-dark); border-radius: 5px; z-index: 2; }
                    .antler.left { left: 2em; transform: rotate(-25deg); }
                    .antler.right { left: 4.5em; transform: rotate(25deg); }
                    .antler::before { content: ''; position: absolute; background-color: var(--deer-dark); border-radius: 3px; width: 0.5em; height: 1.5em; top: 1em; }
                    .antler.left::before { left: -0.5em; transform: rotate(-45deg); }
                    .antler.right::before { right: -0.5em; transform: rotate(45deg); }
                    .deer-eye { width: 1.6em; height: 1.6em; background: white; position: absolute; bottom: 3.5em; z-index: 5; border-radius: 50%; }
                    .deer-eye.left { left: 1.2em; }
                    .deer-eye.right { left: 4.8em; }
                    .deer-eye::after { content: ''; width: 0.6em; height: 0.6em; background: #333; position: absolute; top: 0.5em; left: 0.8em; border-radius: 50%; animation: blink 3s infinite; }
                    @keyframes blink { 0%, 96%, 100% { transform: scaleY(1); } 98% { transform: scaleY(0.1); } }
                    .red-nose { width: 2.2em; height: 2.2em; background: radial-gradient(circle at 30% 30%, #ffcccc, #ff0000); position: absolute; bottom: 0.8em; left: 2.65em; border-radius: 50%; z-index: 10; box-shadow: 0 0 15px var(--nose-glow); animation: nose-pulse 1.5s infinite alternate; }
                    @keyframes nose-pulse { from { box-shadow: 0 0 10px var(--nose-glow); transform: scale(1); } to { box-shadow: 0 0 30px var(--nose-glow); transform: scale(1.1); } }
                    .deer-leg { width: 5em; height: 5em; bottom: 0em; left: 0.5em; position: absolute; background: linear-gradient(var(--deer-color), 95%, var(--deer-dark)); z-index: 2; border-radius: 2em; animation: movebody 1s linear infinite; }
                    .deer-leg-moving { width: 1.5em; height: 3.5em; bottom: 0em; left: 3.5em; position: absolute; background: linear-gradient(var(--deer-color), 80%, var(--deer-dark)); z-index: 2; border-radius: 0.75em; box-shadow: inset 0em -0.5em var(--deer-dark); animation: moveleg 1s linear infinite; }
                    .deer-leg-moving:nth-child(3) { width: 1.25em; left: 1em; height: 2.5em; animation: moveleg2 1s linear infinite 0.075s; }
                    @keyframes moveleg { 0% { transform: rotate(-30deg) translateX(-5%); } 50% { transform: rotate(30deg) translateX(5%); } 100% { transform: rotate(-30deg) translateX(-5%); } }
                    @keyframes moveleg2 { 0% { transform: rotate(30deg); } 50% { transform: rotate(-30deg); } 100% { transform: rotate(30deg); } }
                    @keyframes movebody { 0% { transform: translateX(0%) translateY(0); } 50% { transform: translateX(2%) translateY(-2px); } 100% { transform: translateX(0%) translateY(0); } }
                </style>

                <div class="scene-wrapper">
                    <div class="rudolph-loader">
                        <div class="rudolph-body-wrapper">
                            <div class="deer-leg"></div>
                            <div class="deer-leg-moving"></div>
                            <div class="deer-leg-moving"></div>
                            <div class="deer-body"></div>
                            <div class="deer-head">
                                <div class="antler left"></div><div class="antler right"></div>
                                <div class="deer-ear"></div><div class="deer-ear"></div>
                                <div class="deer-eye left"></div><div class="deer-eye right"></div>
                                <div class="red-nose"></div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class='roast-box gold-mode' style='border-left: 5px solid #8B4513 !important;'>
                {ui_text['egg_deer']}
                </div>
                """, unsafe_allow_html=True)

            elif any(t in user_input_lower for t in triggers_food):
                st.balloons()
                trigger_jackpot_effect() 

                if st.session_state['fixed_hint_msg'] is None:
                    missing_ids = list(MAIN_EGG_IDS - st.session_state['found_ids'])
                    if 4 in missing_ids: missing_ids.remove(4)
                    
                    if not missing_ids:
                        hint_msg = "No more hints!"
                    else:
                        target = random.choice(missing_ids)
                        hint_msg = f"Try looking for secret #{target}..." 
                    
                    st.session_state['fixed_hint_msg'] = hint_msg
                
                final_hint = st.session_state['fixed_hint_msg']

                st.markdown(f"""
                <div class='roast-box gold-mode' style='border-left: 5px solid #FF9800 !important;'>
                {ui_text['egg_food']}<br><br>
                👉 <b>{final_hint}</b>
                </div>
                """, unsafe_allow_html=True)

            elif any(t in user_input_lower for t in triggers_bell):
                st.markdown("""
                <style>
                    .slot-machine-container { display: flex; justify-content: center; gap: 15px; padding: 15px; margin-bottom: 20px; }
                    .bell-wrapper { position: relative; transform: translateY(-200%); opacity: 0; animation: drop-bounce 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
                    .bell-wrapper:nth-child(1) { animation-delay: 0s; } .bell-wrapper:nth-child(2) { animation-delay: 0.2s; } .bell-wrapper:nth-child(3) { animation-delay: 0.4s; }
                    .bell-main { position: relative; width: 50px; height: 60px; display: flex; flex-direction: column; align-items: center; }
                    .bell-anchor { width: 100%; height: 100%; z-index: 2; transform-origin: top center; animation: bell-loop-ring 1.5s ease-in-out infinite 0.8s; }
                    .bell-shape { width: 100%; height: 80%; background: radial-gradient(circle at 30% 30%, #ffd700, #d4af37); border-radius: 15px 15px 5px 5px; border: 2px solid #b8860b; position: relative; z-index: 2; }
                    .bell-shape::after { content: ''; position: absolute; bottom: -4px; left: -4px; width: 54px; height: 8px; background: #d4af37; border-radius: 4px; border: 2px solid #b8860b; z-index: 3; }
                    .bell-handle { position: absolute; top: -8px; left: 50%; transform: translateX(-50%); width: 10px; height: 8px; background: #b8860b; border-radius: 50% 50% 0 0; border: 2px solid #8b6508; border-bottom: none; z-index: 1; }
                    .bell-clapper { position: absolute; bottom: -6px; left: 50%; transform: translateX(-50%); width: 8px; height: 8px; background: #daa520; border: 2px solid #8b6508; border-radius: 50%; z-index: 1; transform-origin: top center; animation: clapper-loop-swing 1.5s ease-in-out infinite 0.8s; }
                    @keyframes drop-bounce { 0% { transform: translateY(-200%); opacity: 0; } 70% { transform: translateY(10%); opacity: 1; } 85% { transform: translateY(-5%); } 100% { transform: translateY(0); opacity: 1; } }
                    @keyframes bell-loop-ring { 0% { transform: rotate(0deg); } 25% { transform: rotate(15deg); } 75% { transform: rotate(-15deg); } 100% { transform: rotate(0deg); } }
                    @keyframes clapper-loop-swing { 0% { transform: translateX(-50%) rotate(0deg); } 25% { transform: translateX(-50%) rotate(-30deg); } 75% { transform: translateX(-50%) rotate(30deg); } 100% { transform: translateX(-50%) rotate(0deg); } }
                </style>
                
                <div class="slot-machine-container">
                    <div class="bell-wrapper"><div class="bell-main"><div class="bell-anchor"><div class="bell-handle"></div><div class="bell-shape"></div><div class="bell-clapper"></div></div></div></div>
                    <div class="bell-wrapper"><div class="bell-main"><div class="bell-anchor"><div class="bell-handle"></div><div class="bell-shape"></div><div class="bell-clapper"></div></div></div></div>
                    <div class="bell-wrapper"><div class="bell-main"><div class="bell-anchor"><div class="bell-handle"></div><div class="bell-shape"></div><div class="bell-clapper"></div></div></div></div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class='roast-box gold-mode' style='border-left: 5px solid #FFD700 !important; text-align: center;'>
                {ui_text['egg_bell']}
                </div>
                """, unsafe_allow_html=True)

            elif any(t in user_input_lower for t in triggers_holiday):
                st.balloons()
                
                # 获取当前语言文本
                current_ui_lang = st.session_state['ui_language']
                h_text = HOLIDAY_TEXT.get(current_ui_lang, HOLIDAY_TEXT["English 🇬🇧🇺🇸"])

                st.markdown(f"""
                <style>
                    .card-container {{ display: flex; justify-content: center; margin: 20px 0; perspective: 1000px; }}
                    .card {{ position: relative; width: 300px; height: 200px; background: linear-gradient(-45deg, #f89b29 0%, #ff0f7b 100% ); border-radius: 10px; display: flex; align-items: center; justify-content: center; overflow: hidden; transition: all 0.6s cubic-bezier(0.23, 1, 0.320, 1); cursor: pointer; }}
                    .card svg {{ width: 48px; fill: #fff; transition: all 0.6s cubic-bezier(0.23, 1, 0.320, 1); }}
                    .card:hover {{ transform: rotate(-5deg) scale(1.1); box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4); }}
                    .card__content {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-45deg); width: 100%; height: 100%; padding: 20px; box-sizing: border-box; background-color: #fff; opacity: 0; transition: all 0.6s cubic-bezier(0.23, 1, 0.320, 1); display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }}
                    .card:hover .card__content {{ transform: translate(-50%, -50%) rotate(0deg); opacity: 1; }}
                    .card__title {{ margin: 0; font-size: 24px; color: #333; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }}
                    .card__description {{ margin: 10px 0 0; font-size: 14px; color: #777; line-height: 1.6; }}
                    .card:hover svg {{ scale: 0; transform: rotate(-45deg); }}
                </style>
                <div class="card-container">
                    <div class="card">
                        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M20 6h-4V4c0-1.11-.89-2-2-2h-4c-1.11 0-2 .89-2 2v2H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-6 0h-4V4h4v2z"/></svg>
                        <div class="card__content">
                            <p class="card__title">{h_text['title']}</p>
                            <p class="card__description">{h_text['desc_1']}<br>{h_text['desc_2']}<br><b>{h_text['action']}</b><br>{h_text['valid']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class='roast-box gold-mode' style='border-left: 5px solid #FFEB3B !important;'>
                🎅 <b>Santa's Verdict:</b><br><br>
                {h_text['roast_title']}<br>
                <b>{h_text['roast_body']}</b> 🎈
                </div>
                """, unsafe_allow_html=True)

            elif any(t in user_input_lower for t in triggers_finland):
                st.markdown("""
                <style>
                    .wrapper { width: 100%; height: 300px; position: relative; text-align: center; display: flex; align-items: center; justify-content: center; overflow: hidden; perspective: 1000px; margin-top: 10px; }
                    .inner { --w: 120px; --h: 180px; --quantity: 6; --translateZ: calc((var(--w) + var(--h)) + 20px); --rotateX: -10deg; position: absolute; width: var(--w); height: var(--h); z-index: 2; transform-style: preserve-3d; animation: rotating 25s linear infinite; }
                    @keyframes rotating { from { transform: rotateX(var(--rotateX)) rotateY(0); } to { transform: rotateX(var(--rotateX)) rotateY(1turn); } }
                    .card-carousel { position: absolute; border: 2px solid rgba(255, 255, 255, 0.8); border-radius: 12px; overflow: hidden; inset: 0; transform: rotateY(calc((360deg / var(--quantity)) * var(--index))) translateZ(var(--translateZ)); background: #000; box-shadow: 0 0 20px rgba(0, 255, 128, 0.3); }
                    .night-sky { position: relative; width: 100%; height: 100%; background: linear-gradient(to bottom, #020111 0%, #191f45 100%); overflow: hidden; }
                    .stars { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: radial-gradient(1px 1px at 10% 10%, white, transparent), radial-gradient(1.5px 1.5px at 50% 60%, white, transparent), radial-gradient(1px 1px at 80% 20%, white, transparent); background-size: 100% 100%; opacity: 0.6; animation: twinkle 4s infinite alternate; }
                    .aurora-container { position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; filter: blur(15px); opacity: 0.8; mix-blend-mode: screen; animation: rotate-aurora 15s linear infinite; }
                    .aurora-beam { position: absolute; width: 100%; height: 100%; background: radial-gradient(ellipse at center, rgba(0, 255, 170, 0.5) 0%, rgba(138, 43, 226, 0.3) 40%, transparent 70%); transform: scaleY(0.6); }
                    .card-carousel:nth-child(even) .aurora-beam { background: radial-gradient(ellipse at center, rgba(0, 255, 255, 0.4) 0%, rgba(0, 128, 0, 0.3) 50%, transparent 70%); animation-duration: 12s; }
                    .forest { position: absolute; bottom: 0; left: 0; width: 100%; height: 30px; background: #000; z-index: 10; clip-path: polygon(0% 100%, 10% 40%, 20% 100%, 30% 20%, 40% 100%, 50% 50%, 60% 100%, 70% 30%, 80% 100%, 90% 60%, 100% 100%); }
                    .flag-badge { position: absolute; top: 8px; right: 8px; width: 24px; height: 16px; background: white; z-index: 25; opacity: 0.9; }
                    .flag-badge::before { content: ''; position: absolute; left: 7px; top: 0; width: 5px; height: 100%; background: #003580; }
                    .flag-badge::after { content: ''; position: absolute; top: 6px; left: 0; width: 100%; height: 5px; background: #003580; }
                    .caption-text { position: absolute; bottom: 5px; width: 100%; text-align: center; color: rgba(255,255,255,0.7); font-family: cursive; font-size: 12px; z-index: 25; }
                    @keyframes twinkle { 0% { opacity: 0.4; } 100% { opacity: 0.8; } }
                    @keyframes rotate-aurora { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
                    /* Santa */
                    .santa-flyer { position: absolute; top: 30%; left: -60px; width: 40px; height: 30px; z-index: 20; animation: santa-fly-across 8s linear infinite; }
                    .santa-body-bob { position: relative; width: 100%; height: 100%; animation: santa-bob 1.5s ease-in-out infinite alternate; }
                    .s-body { position: absolute; width: 24px; height: 18px; background: #d63031; bottom: 4px; left: 8px; border-radius: 12px; }
                    .s-beard { position: absolute; width: 20px; height: 14px; background: #fff; bottom: 4px; left: 3px; border-radius: 50%; box-shadow: 3px 1px 0 #fff; }
                    .s-face { position: absolute; width: 10px; height: 10px; background: #ffe0d0; top: 6px; left: 8px; border-radius: 50%; }
                    .s-hat { position: absolute; width: 0; height: 0; border-left: 8px solid transparent; border-right: 8px solid transparent; border-bottom: 14px solid #d63031; top: -6px; left: 4px; transform: rotate(-20deg); }
                    @keyframes santa-fly-across { 0% { left: -70px; visibility: visible; } 40% { left: 150%; visibility: visible; } 41% { visibility: hidden; } 100% { left: -70px; visibility: hidden; } }
                    @keyframes santa-bob { 0% { transform: translateY(0); } 100% { transform: translateY(-5px); } }
                </style>
                <div class="wrapper">
                    <div class="inner">
                        <div class="card-carousel" style="--index: 0;"><div class="night-sky"><div class="stars"></div><div class="aurora-container"><div class="aurora-beam"></div></div><div class="santa-flyer" style="animation-delay: 0s;"><div class="santa-body-bob"><div class="s-body"></div><div class="s-beard"></div><div class="s-face"></div><div class="s-hat"></div></div></div><div class="forest"></div><div class="flag-badge"></div><div class="caption-text">Finland</div></div></div>
                        <div class="card-carousel" style="--index: 1;"><div class="night-sky"><div class="stars"></div><div class="aurora-container"><div class="aurora-beam"></div></div><div class="santa-flyer" style="animation-delay: 2s;"><div class="santa-body-bob"><div class="s-body"></div><div class="s-beard"></div><div class="s-face"></div><div class="s-hat"></div></div></div><div class="forest"></div><div class="flag-badge"></div><div class="caption-text">Suomi</div></div></div>
                        <div class="card-carousel" style="--index: 2;"><div class="night-sky"><div class="stars"></div><div class="aurora-container"><div class="aurora-beam"></div></div><div class="santa-flyer" style="animation-delay: 4s;"><div class="santa-body-bob"><div class="s-body"></div><div class="s-beard"></div><div class="s-face"></div><div class="s-hat"></div></div></div><div class="forest"></div><div class="flag-badge"></div><div class="caption-text">Aurora</div></div></div>
                        <div class="card-carousel" style="--index: 3;"><div class="night-sky"><div class="stars"></div><div class="aurora-container"><div class="aurora-beam"></div></div><div class="santa-flyer" style="animation-delay: 1.5s;"><div class="santa-body-bob"><div class="s-body"></div><div class="s-beard"></div><div class="s-face"></div><div class="s-hat"></div></div></div><div class="forest"></div><div class="flag-badge"></div><div class="caption-text">Lapland</div></div></div>
                        <div class="card-carousel" style="--index: 4;"><div class="night-sky"><div class="stars"></div><div class="aurora-container"><div class="aurora-beam"></div></div><div class="santa-flyer" style="animation-delay: 5.5s;"><div class="santa-body-bob"><div class="s-body"></div><div class="s-beard"></div><div class="s-face"></div><div class="s-hat"></div></div></div><div class="forest"></div><div class="flag-badge"></div><div class="caption-text">Rovaniemi</div></div></div>
                        <div class="card-carousel" style="--index: 5;"><div class="night-sky"><div class="stars"></div><div class="aurora-container"><div class="aurora-beam"></div></div><div class="santa-flyer" style="animation-delay: 3.2s;"><div class="santa-body-bob"><div class="s-body"></div><div class="s-beard"></div><div class="s-face"></div><div class="s-hat"></div></div></div><div class="forest"></div><div class="flag-badge"></div><div class="caption-text">Santa's Home</div></div></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class='roast-box gold-mode' style='border-left: 5px solid #003580 !important;'>
                {ui_text['egg_finland']}
                </div>
                """, unsafe_allow_html=True)

            # --- 8. AI 正常逻辑 (Only Snow Here) ---
            else:
                with st.spinner(ui_text["loading"]):
                    try:
                        genai.configure(api_key=api_key)
                        try:
                            model = genai.GenerativeModel('gemini-3-pro-preview')
                        except:
                            model = genai.GenerativeModel('gemini-1.5-flash')

                        persona = f"""
                        You are Santa Claus with a "Tsundere" (傲娇 - tough outside, soft inside) personality.

                        🔥🔥 MANDATORY IDENTITY RULES (CRITICAL) 🔥🔥
                        1. **SELF-REFERENCE**: You must ALWAYS refer to yourself as **"本圣诞老人" (The Great Santa)** or **"我" (I)**.
                        2. **NO ROBOTIC SPEECH**: Never say "As an AI...".

                        🔥🔥 LANGUAGE INSTRUCTION 🔥🔥
                        1. DETECT the language of the user's wish ("{gift_list}").
                        2. RESPOND in that **SAME LANGUAGE**.

                        🔥🔥 RESPONSE STRUCTURE (The "Tsundere" Flow) 🔥🔥
                        1. **The Roast (50%):** Start by being grumpy. Use "本圣诞老人" to express disbelief at their audacity.
                        2. **The Shift:** Use a transition like "*Sigh*...", "*Cough*...", or "不过...".
                        3. **The Grant/Advice (50%):** Reluctantly agree or give realistic advice.

                        🔥🔥 EXCEPTION (Heartwarming Override) 🔥🔥:
                        IF the wish is ALREADY purely selfless (e.g. "Health for mom"), skip the roast. Be kind.
                        """

                        response = model.generate_content(f"{persona}\n\nUser's Wish: {gift_list}")

                        if "❤️" in response.text or "🌟" in response.text:
                            # 暖心时刻也给点特效
                            trigger_jackpot_effect()
                            st.balloons()
                            st.success(ui_text["success_title"])
                            box_style = "roast-box gold-mode"
                        else:
                            st.snow() # 只有被骂的时候才下雪，凄凉感 MAX
                            st.toast("🎅 Santa is judging you...", icon="😒")
                            box_style = "roast-box"

                        st.markdown(f"<div class='{box_style}'>{response.text}</div>", unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"Santa crashed (Error): {e}")

    st.markdown("---")
    st.markdown(f"<div style='text-align: center; color: #aaa;'>{ui_text['footer']}</div>", unsafe_allow_html=True)
