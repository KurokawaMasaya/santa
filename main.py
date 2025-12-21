import streamlit as st
import google.generativeai as genai
import random
import time

# --- 1. 頁面基礎設定 ---
st.set_page_config(page_title="Roast Santa AI", page_icon="🎅", layout="centered")

# --- 2. 語言字典 ---
LANG_DICT = {
    "English 🇬🇧🇺🇸": {
        "title": "🎅 Santa's Roast Room",
        "subtitle": "Let The Great Santa judge your greedy soul... 😏",
        "sidebar_title": "🎅 Settings",
        "api_help": "Key is used for this session only.",
        "game_rule": "💡 **How to play:**\nEnter your wishlist. Unlock 6 festive secrets!\n\n**Tip:** Most secrets are related to **Christmas items**, but some are about your *relationship* or *travel*...",
        "input_placeholder": "Your wishlist (e.g., iPhone 17 pro max, a boyfriend, I want to go to Finland...)",
        "button": "🎁 Roast My List",
        "loading": "🎅 Santa is assessing your worth...",
        "error_no_key": "Please enter your API Key first!",
        "error_no_text": "Write something! I can't roast a blank paper.",
        "success_title": "🔔 The Verdict is Here!",
        "footer": "Powered by Google Gemini 3.0 Pro",
        "secret_success": "🎅 Ho ho ho! You found the tree!",
        "secret_title": "### Merry Christmas!!! Enter the Secret Portal 🎄",
        "secret_button": "👉 CLICK TO ENTER",
        "hunt_title": "🏆 Secret Hunt Progress"
    },
    "Traditional Chinese (繁體中文) 🇹🇼🇭🇰🇲🇴": {
        "title": "🎅 聖誕老人吐槽大會",
        "subtitle": "讓本聖誕老人... 用邏輯粉碎你的夢想... 😏",
        "sidebar_title": "🎅 設定",
        "api_help": "Key 僅用於本次連線，重新整理即消失。",
        "game_rule": "💡 **玩法說明：**\n輸入願望清單。試著解鎖 6 個節日彩蛋！\n\n**提示：** 彩蛋多與**聖誕物品**有關，但也有關於*感情*或*旅行*的...",
        "input_placeholder": "許願吧 (例如：iPhone 17 pro max、男朋友、去芬蘭...)",
        "button": "🎁 吐槽我的願望",
        "loading": "🎅 本聖誕老人正在審視你的人生...",
        "error_no_key": "請先在上方輸入 Gemini API Key！",
        "error_no_text": "寫點東西啊！拿白紙我是要怎麼吐槽？",
        "success_title": "🔔 判決已下！",
        "footer": "由 Google Gemini 3.0 Pro 強力驅動",
        "secret_success": "🎅 吼吼吼！你找到了聖誕樹！",
        "secret_title": "### 聖誕快樂！！！這是通往秘密基地的傳送門 🎄",
        "secret_button": "👉 點擊進入聖誕樹空間",
        "hunt_title": "🏆 彩蛋收集進度"
    },
    "Simplified Chinese (简体中文) 🇨🇳": {
        "title": "🎅 圣诞老人吐槽大会",
        "subtitle": "让本圣诞老人... 用逻辑粉碎你的梦想... 😏",
        "sidebar_title": "🎅 设置",
        "api_help": "Key 仅用于本次会话。",
        "game_rule": "💡 **玩法说明：**\n输入愿望清单。试着解锁 6 个节日彩蛋！\n\n**提示：** 彩蛋多与**圣诞物品**有关，但也有关于*感情*或*旅行*的...",
        "input_placeholder": "许愿吧 (例如：iPhone 17 pro max、男朋友、去芬兰...)",
        "button": "🎁 吐槽我的愿望",
        "loading": "🎅 本圣诞老人正在审视你的人生...",
        "error_no_key": "请先在上方输入 Gemini API Key！",
        "error_no_text": "写点东西啊！拿白纸我是要怎么吐槽？",
        "success_title": "🔔 判决已下！",
        "footer": "由 Google Gemini 3.0 Pro 强力驱动",
        "secret_success": "🎅 吼吼吼！你找到了圣诞树！",
        "secret_title": "### 圣诞快乐！！！这是通往秘密基地的传送门 🎄",
        "secret_button": "👉 点击进入圣诞树空间",
        "hunt_title": "🏆 彩蛋收集进度"
    },
    "Japanese (日本語) 🇯🇵": {
        "title": "🎅 サンタの毒舌部屋",
        "subtitle": "ワシが... 論理であなたの夢を打ち砕いてやろう... 😏",
        "sidebar_title": "🎅 設定",
        "api_help": "キーはこのセッションでのみ使用されます。",
        "game_rule": "💡 **遊び方:**\n欲しいものを入力して、6つのクリスマスの秘密を探そう！\n\n**ヒント:** ほとんどは**クリスマスアイテム**ですが、*恋愛*や*旅行*に関するものも...",
        "input_placeholder": "欲しいものリスト (例: iPhone 17 pro max, 彼氏, フィンランド...)",
        "button": "🎁 リストを斬る",
        "loading": "🎅 サンタがあなたの価値を査定中...",
        "error_no_key": "先にAPIキーを入力してください！",
        "error_no_text": "何か書いて！白紙じゃツッコミようがないよ。",
        "success_title": "🔔 判決が出ました！",
        "footer": "Powered by Google Gemini 3.0 Pro",
        "secret_success": "🎅 ホーホーホー！ツリーを見つけたな！",
        "secret_title": "### メリークリスマス！！！秘密の入り口はこちら 🎄",
        "secret_button": "👉 クリックしてポータルに入る",
        "hunt_title": "🏆 シークレットハント進捗"
    },
    "French 🇫🇷": {
        "title": "🎅 Salle de Rôtissage du Père Noël",
        "subtitle": "Laissez le Père Noël écraser vos rêves... 😏",
        "sidebar_title": "🎅 Paramètres",
        "api_help": "La clé est utilisée uniquement pour cette session.",
        "game_rule": "💡 **Comment jouer:**\nEntrez votre liste. Débloquez 6 secrets festifs !\n\n**Astuce :** La plupart sont liés à **Noël**, mais certains concernent *l'amour* ou *le voyage*...",
        "input_placeholder": "Votre liste (ex: iPhone 17 pro max, un petit ami, Finlande...)",
        "button": "🎁 Rôtir ma liste",
        "loading": "🎅 Le Père Noël évalue votre valeur...",
        "error_no_key": "Veuillez d'abord entrer votre clé API !",
        "error_no_text": "Écrivez quelque chose ! Je ne peux pas rôtir une page blanche.",
        "success_title": "🔔 Le verdict est là !",
        "footer": "Propulsé par Google Gemini 3.0 Pro",
        "secret_success": "🎅 Ho ho ho ! Vous avez trouvé l'arbre !",
        "secret_title": "### JOYEUX NOËL !!! Voici le portail secret 🎄",
        "secret_button": "👉 CLIQUEZ POUR ENTRER",
        "hunt_title": "🏆 Chasse aux Secrets"
    }
}

# --- 3. 初始化 Session State ---
if 'language_selected' not in st.session_state:
    st.session_state['language_selected'] = False
if 'ui_language' not in st.session_state:
    st.session_state['ui_language'] = "English 🇬🇧🇺🇸"

# 🔥 核心逻辑：彩蛋 ID 映射 (6个) 🔥
# 1: Tree, 2: Single, 3: Deer, 4: Food, 5: Bell, 7: Finland
ALL_EGG_IDS = {1, 2, 3, 4, 5, 7}

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
    found_count = len(st.session_state['found_ids'])
    total_eggs = len(ALL_EGG_IDS)

    with placeholder_obj.container():
        st.markdown('<div class="hunt-panel">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"#### {ui_text['hunt_title']}")
        with col2:
            st.markdown(f"<h4 style='text-align: right; color: #FFD700;'>{found_count} / {total_eggs}</h4>",
                        unsafe_allow_html=True)

        st.progress(found_count / total_eggs)

        # 勋章展示区 (6 个)
        medals = ""
        medals += "🎄 " if 1 in st.session_state['found_ids'] else "⚪ "
        medals += "🐶 " if 2 in st.session_state['found_ids'] else "⚪ "
        medals += "🦌 " if 3 in st.session_state['found_ids'] else "⚪ "
        medals += "🍗 " if 4 in st.session_state['found_ids'] else "⚪ "
        medals += "🔔 " if 5 in st.session_state['found_ids'] else "⚪ "
        medals += "🇫🇮 " if 7 in st.session_state['found_ids'] else "⚪ "

        st.caption(f"Collection: {medals}")

        if found_count == total_eggs:
            st.balloons()
            st.success("🎉 Santa Master! You unlocked EVERYTHING!")

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
    col1, col2 = st.columns(2)
    with col1:
        st.button("English 🇬🇧🇺🇸", use_container_width=True, on_click=set_language, args=("English 🇬🇧🇺🇸",))
        st.button("Simplified Chinese 🇨🇳", use_container_width=True, on_click=set_language,
                  args=("Simplified Chinese (简体中文) 🇨🇳",))
    with col2:
        st.button("Traditional Chinese 🇹🇼🇭🇰🇲🇴", use_container_width=True, on_click=set_language,
                  args=("Traditional Chinese (繁體中文) 🇹🇼🇭🇰🇲🇴",))
        st.button("Japanese 🇯🇵", use_container_width=True, on_click=set_language, args=("Japanese (日本語) 🇯🇵",))
    st.button("French 🇫🇷", use_container_width=True, on_click=set_language, args=("French 🇫🇷",))

else:
    # --- 2. 主程式 (Main App) ---
    current_lang_key = st.session_state['ui_language']
    ui_text = LANG_DICT[current_lang_key]

    # --- 侧边栏：仅保留设置 ---
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/santa.png", width=100)
        st.caption(f"Language: **{current_lang_key}**")
        st.button("🔄 Change Language", on_click=reset_language)
        st.markdown("---")
        st.markdown(ui_text["game_rule"])

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
            user_input_lower = gift_list.lower()

            # --- 关键词库 ---
            triggers_tree = ["tree", "christmas tree", "decoration", "ornament", "star", "圣诞树", "树", "sapin", "ツリー"]
            triggers_single = [
                "脱单", "男朋友", "女朋友", "對象", "对象", "搞对象", "恋爱",
                "boyfriend", "girlfriend", "partner", "lover", "dating", "bf", "gf",
                "彼氏", "彼女", "恋人",
                "petit ami", "petite amie", "copain", "copine"
            ]
            triggers_deer = ["deer", "reindeer", "rudolph", "sleigh", "麋鹿", "鹿", "驯鹿", "雪橇", "renne", "トナカイ"]
            triggers_food = ["cookie", "biscuit", "milk", "gingerbread", "turkey", "pudding", "pie", "cake", "food",
                             "dinner", "feast", "饼干", "牛奶", "姜饼", "火鸡", "布丁", "大餐", "食物", "吃"]
            triggers_bell = ["bell", "jingle", "ring", "song", "music", "sing", "铃铛", "铃", "钟", "响", "cloche"]
            # triggers_holiday (Removed)
            triggers_finland = ["finland", "suomi", "helsinki", "rovaniemi", "lapland", "芬兰", "赫尔辛基", "罗瓦涅米", "圣诞村"]

            # --- 检测新发现 ---
            new_discovery = False

            if any(t in user_input_lower for t in triggers_tree):
                if 1 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(1)
                    new_discovery = True

            elif any(t in user_input_lower for t in triggers_single):
                if 2 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(2)
                    new_discovery = True

            elif any(t in user_input_lower for t in triggers_deer):
                if 3 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(3)
                    new_discovery = True

            elif any(t in user_input_lower for t in triggers_food):
                if 4 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(4)
                    new_discovery = True

            elif any(t in user_input_lower for t in triggers_bell):
                if 5 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(5)
                    new_discovery = True

            elif any(t in user_input_lower for t in triggers_finland):
                if 7 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(7)
                    new_discovery = True

            # 🔥 立即更新主页面的进度条 🔥
            if new_discovery:
                update_hunt_progress(hunt_placeholder, ui_text)

            # --- 展示逻辑 ---

            # --- 1. 🎄 TREE (No Snow, No Balloons) ---
            if any(t in user_input_lower for t in triggers_tree):
                st.success(ui_text["secret_success"])
                st.markdown(ui_text["secret_title"])
                st.link_button(ui_text["secret_button"], "https://wkpsyvxy8njhxmuqyy6gpr.streamlit.app")

            # --- 2. 🐶 SINGLE (Music + Text, No Snow, No Steam) ---
            elif any(t in user_input_lower for t in triggers_single):
                try:
                    st.audio("bgm.mp3", format="audio/mp3", start_time=0, autoplay=True)
                except:
                    st.warning("🎵 Music file missing.")

                st.markdown("""
                <div class='roast-box'>
                🎅 <b>本圣诞老人</b>的判决：<br><br>
                孩子，想要这种东西？<br>
                <b>本圣诞老人</b>也没辙！(Santa sighs)<br>
                听听这首神曲吧，这是唯一能安抚你灵魂的东西了。🎧
                </div>
                """, unsafe_allow_html=True)

            # --- 3. 🦌 DEER (New Walking Animation, No Snow) ---
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

                st.markdown("""
                <div class='roast-box gold-mode' style='border-left: 5px solid #8B4513 !important;'>
                🎅 <b>本圣诞老人</b>的判决：<br><br>
                Look! Look! 👀<br>
                是谁在屏幕上爬过去？<br>
                <b>是鲁道夫！(It's Rudolph!)</b> 🔴🦌<br>
                看来今年礼物稳了！
                </div>
                """, unsafe_allow_html=True)

            # --- 4. 🍗 FOOD (Balloons + Steam) ---
            elif any(t in user_input_lower for t in triggers_food):
                st.balloons()
                trigger_jackpot_effect()

                if st.session_state['fixed_hint_msg'] is None:
                    missing_ids = list(ALL_EGG_IDS - st.session_state['found_ids'])
                    if 4 in missing_ids: missing_ids.remove(4)

                    if not missing_ids:
                        hint_msg = "嗝... 吃饱了！你已经发现了所有秘密！(No more hints)"
                    else:
                        if 2 in missing_ids and random.random() < 0.8:
                            target = 2
                        else:
                            target = random.choice(missing_ids)

                        if target == 1:
                            hint_msg = "🤫 线索：冬天穿绿衣，满身挂彩灯。它不在天上，而在屋里..."
                        elif target == 2:
                            hint_msg = "🤫 线索：有些人成双成对，而你... 只有一个人。你最想要什么？"
                        elif target == 3:
                            hint_msg = "🤫 线索：谁长着红鼻子，在天上帮本圣诞老人拉车？"
                        elif target == 5:
                            hint_msg = "🤫 线索：摇一摇，叮当响。Jingle _____ ?"
                        elif target == 7:
                            hint_msg = "🤫 线索：圣诞老人的老家在哪里？(Country)"

                    st.session_state['fixed_hint_msg'] = hint_msg

                final_hint = st.session_state['fixed_hint_msg']

                st.markdown(f"""
                <div class='roast-box gold-mode' style='border-left: 5px solid #FF9800 !important;'>
                🎅 <b>本圣诞老人</b>的判决：<br><br>
                (大口吃肉... 擦擦嘴...)<br>
                美味！这才是过节嘛！🍗🍷<br>
                既然你请我吃了大餐，本圣诞老人悄悄告诉你一个秘密：<br><br>
                👉 <b>{final_hint}</b>
                </div>
                """, unsafe_allow_html=True)

            # --- 5. 🔔 BELL (Ring Loop, No Snow) ---
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

                st.markdown("""
                <div class='roast-box gold-mode' style='border-left: 5px solid #FFD700 !important; text-align: center;'>
                🎅 <b>本圣诞老人</b>的判决：<br><br>
                <b>Ring Ring Ring!</b> 🔔🔔🔔<br>
                听到了吗？这是幸运的钟声在为你循环播放！<br>
                (Santa starts dancing to the rhythm) 💃
                </div>
                """, unsafe_allow_html=True)

            # --- 7. 🇫🇮 FINLAND (3D Carousel + Santa, Center Adjusted, No Snow) ---
            elif any(t in user_input_lower for t in triggers_finland):
                st.markdown("""
                <style>
                    /* 调整 wrapper 高度为 300px，增加 margin-top 呼吸感 */
                    .wrapper { width: 100%; height: 290px; position: relative; text-align: center; display: flex; align-items: center; justify-content: center; overflow: hidden; perspective: 1000px; margin-top: 10px; }
                    /* 移除 top: -40px，让 flex 自动居中 */
                    .inner { --w: 120px; --h: 180px; --quantity: 6; --translateZ: calc((var(--w) + var(--h)) + 20px); --rotateX: -10deg; position: absolute; width: var(--w); height: var(--h); z-index: 2; transform-style: preserve-3d; animation: rotating 25s linear infinite; }
                    @keyframes rotating { from { transform: rotateX(var(--rotateX)) rotateY(0); } to { transform: rotateX(var(--rotateX)) rotateY(1turn); } }
                    .card { position: absolute; border: 2px solid rgba(255, 255, 255, 0.8); border-radius: 12px; overflow: hidden; inset: 0; transform: rotateY(calc((360deg / var(--quantity)) * var(--index))) translateZ(var(--translateZ)); background: #000; box-shadow: 0 0 20px rgba(0, 255, 128, 0.3); }
                    .night-sky { position: relative; width: 100%; height: 100%; background: linear-gradient(to bottom, #020111 0%, #191f45 100%); overflow: hidden; }
                    .stars { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: radial-gradient(1px 1px at 10% 10%, white, transparent), radial-gradient(1.5px 1.5px at 50% 60%, white, transparent), radial-gradient(1px 1px at 80% 20%, white, transparent); background-size: 100% 100%; opacity: 0.6; animation: twinkle 4s infinite alternate; }
                    .aurora-container { position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; filter: blur(15px); opacity: 0.8; mix-blend-mode: screen; animation: rotate-aurora 15s linear infinite; }
                    .aurora-beam { position: absolute; width: 100%; height: 100%; background: radial-gradient(ellipse at center, rgba(0, 255, 170, 0.5) 0%, rgba(138, 43, 226, 0.3) 40%, transparent 70%); transform: scaleY(0.6); }
                    .card:nth-child(even) .aurora-beam { background: radial-gradient(ellipse at center, rgba(0, 255, 255, 0.4) 0%, rgba(0, 128, 0, 0.3) 50%, transparent 70%); animation-duration: 12s; }
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
                        <div class="card" style="--index: 0;"><div class="night-sky"><div class="stars"></div><div class="aurora-container"><div class="aurora-beam"></div></div><div class="santa-flyer" style="animation-delay: 0s;"><div class="santa-body-bob"><div class="s-body"></div><div class="s-beard"></div><div class="s-face"></div><div class="s-hat"></div></div></div><div class="forest"></div><div class="flag-badge"></div><div class="caption-text">Finland</div></div></div>
                        <div class="card" style="--index: 1;"><div class="night-sky"><div class="stars"></div><div class="aurora-container"><div class="aurora-beam"></div></div><div class="santa-flyer" style="animation-delay: 2s;"><div class="santa-body-bob"><div class="s-body"></div><div class="s-beard"></div><div class="s-face"></div><div class="s-hat"></div></div></div><div class="forest"></div><div class="flag-badge"></div><div class="caption-text">Suomi</div></div></div>
                        <div class="card" style="--index: 2;"><div class="night-sky"><div class="stars"></div><div class="aurora-container"><div class="aurora-beam"></div></div><div class="santa-flyer" style="animation-delay: 4s;"><div class="santa-body-bob"><div class="s-body"></div><div class="s-beard"></div><div class="s-face"></div><div class="s-hat"></div></div></div><div class="forest"></div><div class="flag-badge"></div><div class="caption-text">Aurora</div></div></div>
                        <div class="card" style="--index: 3;"><div class="night-sky"><div class="stars"></div><div class="aurora-container"><div class="aurora-beam"></div></div><div class="santa-flyer" style="animation-delay: 1.5s;"><div class="santa-body-bob"><div class="s-body"></div><div class="s-beard"></div><div class="s-face"></div><div class="s-hat"></div></div></div><div class="forest"></div><div class="flag-badge"></div><div class="caption-text">Lapland</div></div></div>
                        <div class="card" style="--index: 4;"><div class="night-sky"><div class="stars"></div><div class="aurora-container"><div class="aurora-beam"></div></div><div class="santa-flyer" style="animation-delay: 5.5s;"><div class="santa-body-bob"><div class="s-body"></div><div class="s-beard"></div><div class="s-face"></div><div class="s-hat"></div></div></div><div class="forest"></div><div class="flag-badge"></div><div class="caption-text">Rovaniemi</div></div></div>
                        <div class="card" style="--index: 5;"><div class="night-sky"><div class="stars"></div><div class="aurora-container"><div class="aurora-beam"></div></div><div class="santa-flyer" style="animation-delay: 3.2s;"><div class="santa-body-bob"><div class="s-body"></div><div class="s-beard"></div><div class="s-face"></div><div class="s-hat"></div></div></div><div class="forest"></div><div class="flag-badge"></div><div class="caption-text">Santa's Home</div></div></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class='roast-box gold-mode' style='border-left: 5px solid #003580 !important;'>
                🎅 <b>本圣诞老人</b>的判决：<br><br>
                Tervetuloa! (欢迎！)<br>
                你竟然找到了我的老家——<b>芬兰 (Finland)</b>！🇫🇮<br>
                这里的桑拿房已经热好了，快来罗瓦涅米找我玩吧！
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
                            st.snow()  # 只有被骂的时候才下雪，凄凉感 MAX
                            st.toast("🎅 Santa is judging you...", icon="😒")
                            box_style = "roast-box"

                        st.markdown(f"<div class='{box_style}'>{response.text}</div>", unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"Santa crashed (Error): {e}")

    st.markdown("---")
    st.markdown(f"<div style='text-align: center; color: #aaa;'>{ui_text['footer']}</div>", unsafe_allow_html=True)