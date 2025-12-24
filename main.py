import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import os
import random
import time
import base64

# --- 1. 初始化頁面設定 ---
st.set_page_config(page_title="Roast Santa AI", page_icon="🎅", layout="centered")

# --- 2. 定義常數與字典 (保持不變) ---
LANG_DICT = {
    "English 🇬🇧🇺🇸": {
        "title": "🎅 Santa's Roast Room",
        "subtitle": "Let The Great Santa judge your greedy soul... 😏",
        "sidebar_title": "🎅 Settings",
        "api_help": "Key is used for this session only.",
        "game_rule": "💡 **How to play:**\nEnter your wishlist. Unlock 12 festive secrets!\n\n**Tip:** Most secrets are related to **Christmas items**, but some are about your *relationship*, *work* or *travel*...",
        "input_placeholder": "Tell Santa whatever you want or whatever comes to mind... (e.g. Tree, Bell, Boyfriend...)",
        "button": "🔥 Roast Me!",
        "loading": "🎅 Santa is assessing your worth...",
        "error_no_key": "Please enter your API Key first!",
        "error_no_text": "Write something! I can't roast a blank paper.",
        "success_title": "🔔 The Verdict is Here!",
        "footer": "Powered by Google Gemini 3.0 Pro",
        "secret_success": "🎅 Ho ho ho! You found the tree!",
        "secret_title": "### Merry Christmas!!! Enter the Secret Portal 🎄",
        "secret_button": "👉 ENTER THE CHRISTMAS TREE", 
        "return_button": "🔙 Back to Santa", 
        "hunt_title": "🏆 Secret Hunt Progress",
        "egg_single": "Santa sighs... No lover? Here, listen to this song.",
        "egg_deer": "Look! It's Rudolph crawling on your screen! 🔴🦌",
        "egg_food": "Delicious! Thanks for the food!",
        "egg_bell": "Ring Ring! 🔔 That's the sound of luck!",
        "egg_finland": "Tervetuloa! You found my home — Finland (Suomi)! 🇫🇮\nThe sauna is ready, come visit Rovaniemi!",
        "egg_surprise": "🎁 SURPRISE! You summoned me directly!",
        "egg_padoru": "🎵 HASHIRE SORI YO... KAZE NO YOU NI... PADORU PADORU! 🧣",
        "egg_snow": "❄️ Let it snow! The world is quiet and beautiful now...",
        "egg_market": "🍷 Welcome to the Christmas Market! Hot Glühwein & Pretzels! 🥨",
        "egg_author": "👨‍💻 Creator found! Respect.",
        "hint_prefix": "💡 **New Riddle Unlocked:** ",
        "final_hint_title": "🔒 FINAL SEAL UNLOCKED",
        "final_hint_msg": "🎅 **Ho ho ho! I found a 'treasure' from China. How ironic.**\n\nWant to see it? Type **Merry Christmas** to unlock the truth."
    },
    "Traditional Chinese (繁體中文) 🇹🇼🇭🇰🇲🇴": {
        "title": "🎅 聖誕老人吐槽大會",
        "subtitle": "讓本聖誕老人... 用邏輯粉碎你的夢想... 😏",
        "sidebar_title": "🎅 設定",
        "api_help": "Key 僅用於本次連線，重新整理即消失。",
        "game_rule": "💡 **玩法說明：**\n輸入願望清單。試著解鎖 12 個節日彩蛋！\n\n**提示：** 彩蛋多與**聖誕物品**有關，但也有關於*感情*、*打工*或*旅行*的...",
        "input_placeholder": "聖誕節你想要什麼或者想到什麼，都和本聖誕老人說說吧... (例如：聖誕樹、男朋友...)",
        "button": "🔥 吐槽我！",
        "loading": "🎅 本聖誕老人正在審視你的人生...",
        "error_no_key": "請先在上方輸入 Gemini API Key！",
        "error_no_text": "寫點東西啊！拿白紙我是要怎麼吐槽？",
        "success_title": "🔔 判決已下！",
        "footer": "由 Google Gemini 3.0 Pro 強力驅動",
        "secret_success": "🎅 吼吼吼！你找到了聖誕樹！",
        "secret_title": "### 聖誕快樂！！！這是通往秘密基地的傳送門 🎄",
        "secret_button": "👉 進入聖誕樹空間",
        "return_button": "🔙 返回吐槽大會",
        "hunt_title": "🏆 彩蛋收集進度",
        "egg_single": "本聖誕老人嘆氣... 沒對象？聽聽這首歌吧。",
        "egg_deer": "看！是魯道夫在爬你的螢幕！🔴🦌",
        "egg_food": "真香！既然你請我吃大餐，這就當回禮吧！",
        "egg_bell": "叮叮噹！🔔 這是幸運的聲音！",
        "egg_finland": "Tervetuloa! (歡迎！) 你竟然找到了我的老家——芬蘭 (Finland)！🇫🇮\n這裡的桑拿房已經熱好了，快來羅瓦涅米找我玩吧！",
        "egg_surprise": "🎁 驚喜！你竟然直接召喚了本尊！",
        "egg_padoru": "🎵 走れ逸れよ... 風のように... PADORU PADORU !!! 🧣",
        "egg_snow": "❄️ 讓雪落下吧！整個世界都安靜了...",
        "egg_market": "🍷 歡迎來到聖誕集市！來杯熱紅酒配扭結餅吧！🥨",
        "egg_author": "👨‍💻 作者出現！致敬時刻...",
        "hint_prefix": "💡 **解鎖新謎題：** ",
        "final_hint_title": "🔒 最終封印已解除",
        "final_hint_msg": "🎅 **吼吼吼，本聖誕老人找到了一份來自中國的寶貝，真是諷刺啊。**\n\n想看嗎？想看請輸入 **聖誕快樂**。"
    },
    "Simplified Chinese (简体中文) 🇨🇳": {
        "title": "🎅 圣诞老人吐槽大会",
        "subtitle": "让本圣诞老人... 用逻辑粉碎你的梦想... 😏",
        "sidebar_title": "🎅 设置",
        "api_help": "Key 仅用于本次会话。",
        "game_rule": "💡 **玩法说明：**\n输入愿望清单。试着解锁 12 个节日彩蛋！\n\n**提示：** 彩蛋多与**圣诞物品**有关，但也有关于*感情*、*打工*或*旅行*的...",
        "input_placeholder": "圣诞节你想要什么或者想到什么，都和本圣诞老人说说吧... (例如：圣诞树、男朋友...)",
        "button": "🔥 吐槽我！",
        "loading": "🎅 本圣诞老人正在审视你的人生...",
        "error_no_key": "请先在上方输入 Gemini API Key！",
        "error_no_text": "写点东西啊！拿白纸我是要怎么吐槽？",
        "success_title": "🔔 判决已下！",
        "footer": "由 Google Gemini 3.0 Pro 强力驱动",
        "secret_success": "🎅 吼吼吼！你找到了圣诞树！",
        "secret_title": "### 圣诞快乐！！！这是通往秘密基地的传送门 🎄",
        "secret_button": "👉 点击进入圣诞树空间",
        "return_button": "🔙 返回吐槽大会",
        "hunt_title": "🏆 彩蛋收集进度",
        "egg_single": "本圣诞老人叹气... 没对象？听听这首歌吧。",
        "egg_deer": "看！是鲁道夫在爬你的屏幕！🔴🦌",
        "egg_food": "真香！既然你请我吃大餐，这就当回礼吧！",
        "egg_bell": "叮叮当！🔔 这是幸运的声音！",
        "egg_finland": "Tervetuloa! (欢迎！) 你竟然找到了我的老家——芬兰 (Finland)！🇫🇮\n这里的桑拿房已经热好了，快来罗瓦涅米找我玩吧！",
        "egg_surprise": "🎁 惊喜！你竟然直接召唤了本尊！",
        "egg_padoru": "🎵 走れ逸れよ... 風のように... PADORU PADORU !!! 🧣",
        "egg_snow": "❄️ 让雪落下吧！整个世界都安静了...",
        "egg_market": "🍷 欢迎来到圣诞集市！来杯热红酒配扭结饼吧！🥨",
        "egg_author": "👨‍💻 作者出现！致敬时刻...",
        "hint_prefix": "💡 **解锁新谜题：** ",
        "final_hint_title": "🔒 最终封印已解除",
        "final_hint_msg": "🎅 **吼吼吼，本圣诞老人找到了一份来自中国大陆的宝贝。**\n\n请输入 **圣诞快乐**查看。"
    }
}

HINT_CLUES = {
    "English 🇬🇧🇺🇸": {
        1: "A corpse dressed in jewelry, dying slowly in your living room for your amusement. 🌲💎",
        2: "Something money can't buy, and your personality certainly can't attract. 💔",
        3: "My enslaved aerial taxi driver. He guides my sleigh with a glowing red nose. 🔴🦌",
        4: "I am hungry. Bribe me with calcium (milk) and baked goods, and I might forgive you. 🍪",
        5: "I have a metal tongue but no mouth. Shake me and I scream for joy. 🔔",
        6: "The forbidden paper that grants freedom. Your boss fears it, you crave it. 📄",
        7: "My frozen homeland. The land of a thousand lakes and infinite darkness. 🇫🇮",
        9: "Stop asking for things. Try summoning the Boss directly by his name. 🎅",
        10: "A red, spinning calamity... She appears when you ask for a **Christmas Hat**. 🧣",
        11: "I fall silently to bury the world in white. I am cold, just like your ex's heart. ❄️",
        12: "Hot wine, crowds, and overpriced crafts. The gathering place of festive capitalism. 🍷",
        13: "Look behind the curtain. Who is the puppet master controlling this AI? 👨‍💻"
    },
    "Simplified Chinese (简体中文) 🇨🇳": {
        1: "一具披着发光珠宝的尸体，在你的客厅里慢慢枯萎供你观赏。",
        2: "你的存款买不到，你的性格也吸引不到的那种人际关系。",
        3: "我的空中出租车苦力，长着角，还有个发光的红鼻子。",
        4: "想贿赂我？准备好钙质（牛奶）和烘焙食品，我可能会原谅你。",
        5: "我有金属舌头但没有嘴，摇晃我，我就会尖叫。",
        6: "一张赋予你自由的纸，老板最怕见到它，而你最渴望它。",
        7: "我那冰封的故乡，千湖之国，永夜之地。",
        9: "别光顾着要东西，试试直接呼唤本大爷（老板）的名字？",
        10: "一个红色的、会旋转的鬼畜灾难... 想要召唤她？试试提到【圣诞帽】。",
        11: "我无声地落下，将世界掩埋在白色之下。我很冷，像你前任的心一样。",
        12: "热红酒、拥挤的人群、昂贵的小商品... 充满节日气息的消费主义集会。",
        13: "这一行行代码背后，是谁在操控我？（关于作者）"
    },
    "Traditional Chinese (繁體中文) 🇹🇼🇭🇰🇲🇴": {
        1: "一具披著發光珠寶的屍體，在你的客廳裡慢慢枯萎供你觀賞。",
        2: "你的存款買不到，你的性格也吸引不到的那種人際關係。",
        3: "我的空中計程車苦力，長著角，還有個發光的紅鼻子。",
        4: "想賄賂我？準備好鈣質（牛奶）和烘焙食品，我可能會原諒你。",
        5: "我有金屬舌頭但沒有嘴，搖晃我，我就會尖叫。",
        6: "一張賦予你自由的紙，老闆最怕見到它，而你最渴望它。",
        7: "我那冰封的故鄉，千湖之國，永夜之地。",
        9: "別光顧著要東西，試試直接呼喚本大爺（老闆）的名字？",
        10: "一個紅色的、會旋轉的迷因災難... 想要召喚她？試試提到【聖誕帽】。",
        11: "我無聲地落下，將世界掩埋在白色之下。我很冷，像你前任的心一樣。",
        12: "熱紅酒、擁擠的人群、昂貴的小商品... 充滿節日氣息的消費主義集會。",
        13: "這一行行程式碼背後，是誰在操控我？（關於作者）"
    }
}

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

# --- 3. 初始化 Session State ---
if 'language_selected' not in st.session_state:
    st.session_state['language_selected'] = False
if 'ui_language' not in st.session_state:
    st.session_state['ui_language'] = "English 🇬🇧🇺🇸"
if 'found_ids' not in st.session_state:
    st.session_state['found_ids'] = set()
if 'show_tree' not in st.session_state: # 新增：控制是否顯示聖誕樹
    st.session_state['show_tree'] = False

MAIN_EGG_IDS = {1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13}

# --- 4. 輔助函數 ---
def set_language(lang_key):
    st.session_state['ui_language'] = lang_key
    st.session_state['language_selected'] = True

def reset_language():
    st.session_state['language_selected'] = False

def get_base64_image(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception as e:
        return None

# --- 新增：聖誕樹顯示模式函數 ---
def show_tree_mode(ui_text):
    # 讀取原本 tree.py 的 index.html
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_code = f.read()
    except FileNotFoundError:
        st.error("Error: index.html not found.")
        return

    # 注入全螢幕 CSS (來自 tree.py)，並隱藏 header/sidebar
    st.markdown(f"""
        <style>
            /* 移除 Streamlit 預設的 Padding 和 Margin */
            .block-container {{
                padding: 0 !important;
                margin: 0 !important;
                max-width: 100% !important;
            }}
            /* 隱藏 header, footer, sidebar */
            header, footer, [data-testid="stSidebar"] {{
                display: none !important;
            }}
            /* 強制 iframe 全螢幕 */
            iframe {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                border: none;
                z-index: 10;
            }}
            /* 返回按鈕樣式 */
            .stButton > button {{
                position: fixed !important;
                top: 20px !important;
                left: 20px !important;
                z-index: 99999 !important;
                background-color: rgba(0,0,0,0.5) !important;
                color: white !important;
                border: 1px solid rgba(255,255,255,0.3) !important;
            }}
            .stButton > button:hover {{
                background-color: rgba(255,255,255,0.2) !important;
                border-color: white !important;
            }}
        </style>
        """, unsafe_allow_html=True)
    
    # 渲染 HTML
    components.html(html_code, height=1000, scrolling=False)
    
    # 返回按鈕
    if st.button(ui_text.get("return_button", "🔙 Back"), key="back_from_tree"):
        st.session_state['show_tree'] = False
        st.rerun()

# --- 5. 裝飾與特效函數 (保持不變) ---
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

def update_hunt_progress(placeholder_obj, ui_text):
    main_targets = {1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13}
    found_main_count = len([x for x in st.session_state['found_ids'] if x in main_targets])
    total_eggs = 12

    with placeholder_obj.container():
        st.markdown('<div class="hunt-panel">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"#### {ui_text['hunt_title']}")
        with col2:
            st.markdown(f"<h4 style='text-align: right; color: #FFD700;'>{found_main_count} / {total_eggs}</h4>",
                        unsafe_allow_html=True)

        st.progress(min(found_main_count / total_eggs, 1.0))

        medals = ""
        medals += "🎄 " if 1 in st.session_state['found_ids'] else "⚪ "
        medals += "🐶 " if 2 in st.session_state['found_ids'] else "⚪ "
        medals += "🦌 " if 3 in st.session_state['found_ids'] else "⚪ "
        medals += "🍗 " if 4 in st.session_state['found_ids'] else "⚪ "
        medals += "🔔 " if 5 in st.session_state['found_ids'] else "⚪ "
        medals += "📅 " if 6 in st.session_state['found_ids'] else "⚪ "
        medals += "🇫🇮 " if 7 in st.session_state['found_ids'] else "⚪ "
        medals += "🎁 " if 9 in st.session_state['found_ids'] else "⚪ "
        medals += "🧣 " if 10 in st.session_state['found_ids'] else "⚪ "
        medals += "❄️ " if 11 in st.session_state['found_ids'] else "⚪ "
        medals += "🍷 " if 12 in st.session_state['found_ids'] else "⚪ "
        medals += "👨‍💻 " if 13 in st.session_state['found_ids'] else "⚪ "

        if 8 in st.session_state['found_ids']:
            medals += "👁️ "

        st.caption(f"Collection: {medals}")

        if found_main_count == total_eggs:
            if 8 in st.session_state['found_ids']:
                st.success("🎉 GODLIKE! You found ALL secrets including the HIDDEN TRUTH!")
            else:
                st.balloons()
                st.success("🎉 You have found all fragments! Check the message below.")

        st.markdown('</div>', unsafe_allow_html=True)

def render_culture_egg(current_lang_key):
    is_chinese = "Chinese" in current_lang_key or "中文" in current_lang_key
    if is_chinese:
        # 使用你之前的 HTML 內容
        components.html("""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700;900&family=Noto+Sans+SC:wght@400;700&display=swap');
    * { box-sizing: border-box; }
    body { margin: 0; height: 100vh; background-color: transparent; display: flex; justify-content: center; align-items: center; font-family: "Noto Sans SC", sans-serif; overflow: hidden; }
    .interaction-container { position: relative; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; }
    #stage-1 { position: absolute; width: 85%; max-width: 340px; background: #fff; padding: 40px 25px 60px 25px; box-shadow: 0 15px 40px rgba(0,0,0,0.5); transform: rotate(-0.5deg); z-index: 10; transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55); color: #000; font-family: "FangSong", "SimSun", serif; border-radius: 2px; }
    .doc-header { text-align: center; color: #d60000; font-family: "SimSun", "SimHei", serif; font-size: 24px; font-weight: 500; letter-spacing: 1px; margin-bottom: 20px; }
    .doc-title { text-align: center; font-size: 20px; font-weight: 500; margin-bottom: 10px; line-height: 1.4; font-family: "SimSun", serif; letter-spacing: 2px; }
    .doc-serial { text-align: center; font-size: 12px; margin-bottom: 25px; font-family: "FangSong", serif; }
    .doc-body { font-size: 14px; line-height: 1.6; text-align: justify; color: #222; margin-bottom: 30px; text-indent: 2em; font-family: "FangSong", serif; }
    .doc-body p { margin: 0 0 8px 0; }
    .doc-footer { position: absolute; bottom: 40px; right: 30px; text-align: right; font-family: "FangSong", serif; line-height: 1.6; font-size: 14px; }
    .doc-stamp { position: absolute; top: -10px; right: -10px; width: 100px; height: 100px; opacity: 0.85; mix-blend-mode: multiply; pointer-events: none; transform: rotate(-8deg); }
    .close-btn { position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; background: #f0f0f0; color: #333; border: 1px solid #ccc; border-radius: 50%; font-size: 20px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: transform 0.2s; z-index: 20; }
    .close-btn:hover { background: #d60000; color: #fff; transform: scale(1.1); border-color: #d60000; }
    #card-container { display: none; position: relative; z-index: 20; perspective: 1000px; width: 100%; display: flex; justify-content: center; }
    .brutalist-card { width: 85%; max-width: 340px; border: 4px solid #000; background-color: #fff; padding: 1.2rem; box-shadow: 10px 10px 0 #000; font-family: "Noto Sans SC", sans-serif; transition: all 0.3s; position: relative; }
    .brutalist-card__header { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; border-bottom: 2px solid #000; padding-bottom: 1rem; }
    .brutalist-card__icon { flex-shrink: 0; display: flex; align-items: center; justify-content: center; background-color: #000; padding: 0.5rem; transition: background 0.3s; }
    .brutalist-card__icon svg { height: 1.5rem; width: 1.5rem; fill: #fff; }
    .brutalist-card__alert { font-weight: 900; color: #000; font-size: 1.1rem; text-transform: uppercase; transition: color 0.3s; }
    .brutalist-card__message { margin-top: 1rem; color: #000; font-size: 0.85rem; line-height: 1.5; border-bottom: 2px solid #000; padding-bottom: 1rem; font-weight: 600; min-height: 140px; }
    .brutalist-card__actions { margin-top: 1rem; display: flex; flex-direction: column; gap: 10px; }
    .brutalist-card__button { display: block; width: 100%; padding: 0.75rem; text-align: center; font-size: 0.95rem; font-weight: 700; text-transform: uppercase; border: 3px solid #000; background-color: #fff; color: #000; position: relative; transition: all 0.2s; box-shadow: 4px 4px 0 #000; text-decoration: none; cursor: pointer; box-sizing: border-box; }
    .brutalist-card__button--read { background-color: #000; color: #fff; }
    .brutalist-card__button:active { transform: translate(2px, 2px); box-shadow: 2px 2px 0 #000; }
    .hacked .brutalist-card { border-color: #d35400; box-shadow: 10px 10px 0 #e67e22; }
    .hacked .brutalist-card__icon { background-color: #d35400; }
    .hacked .brutalist-card__alert { color: #d35400; }
    .hacked .brutalist-card__message { border-bottom-color: #d35400; font-family: "Noto Serif SC", serif; font-size: 0.85rem; line-height: 1.6; font-weight: normal; }
    .hacked .brutalist-card__button--read { background-color: #d35400; border-color: #d35400; box-shadow: 4px 4px 0 #a04000; }
    .quote-box { background-color: #f9f9f9; border-left: 4px solid #d35400; padding: 6px 10px; margin: 8px 0; font-style: italic; color: #555; font-family: "FangSong", serif; font-size: 0.85rem; }
    .pop-in { display: flex !important; animation: pop-in 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
    .fly-out { animation: fly-away 0.8s cubic-bezier(0.6, -0.28, 0.735, 0.045) forwards; pointer-events: none; }
    .glitching { animation: glitch-shake 0.3s cubic-bezier(.36,.07,.19,.97) both infinite; filter: invert(1); }
    @keyframes fly-away { to { transform: translateY(120vh) rotate(20deg); opacity: 0; } }
    @keyframes pop-in { from { opacity: 0; transform: scale(0.8); } to { opacity: 1; transform: scale(1); } }
    @keyframes glitch-shake { 10%, 90% { transform: translate3d(-1px, 0, 0); } 20%, 80% { transform: translate3d(2px, 0, 0); } 30%, 50%, 70% { transform: translate3d(-4px, 0, 0); } 40%, 60% { transform: translate3d(4px, 0, 0); } }
</style>
</head>
<body>
    <div class="interaction-container">
        <div id="stage-1">
            <button class="close-btn" onclick="triggerWarning()">×</button>
            <div class="doc-header">XX县教育体育局</div>
            <div class="doc-title">公　告</div>
            <div class="doc-serial">（XX教体字 2025 第 120 号）</div>
            <div class="doc-body">
                <p>根据上级关于传承优秀传统文化精神，为抵御西方宗教文化渗透，净化校园文化环境，现就有关事项通知如下：</p>
                <p>一、<strong>严禁过“洋节”</strong>。全县各级各类学校、幼儿园严禁在校园内举办任何形式的圣诞节庆祝活动。</p>
                <p>二、<strong>严禁摆放装饰</strong>。各班级不得在教室内摆放圣诞树、悬挂彩灯、张贴相关画像。</p>
            </div>
            <div class="doc-footer">
                <p>XX县教育体育局</p>
                <p>2025年12月20日</p>
                <svg class="doc-stamp" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="50" cy="50" r="45" stroke="#d60000" stroke-width="2.5" fill="none" />
                    <text x="50" y="55" text-anchor="middle" fill="#d60000" font-size="12" font-weight="bold" font-family="SimHei">XX县教育体育局</text>
                    <text x="50" y="75" text-anchor="middle" fill="#d60000" font-size="8">行政章</text>
                    <path d="M35,50 L65,50" stroke="#d60000" stroke-width="2" />
                    <text fill="#d60000" font-size="8" font-weight="bold" letter-spacing="1">
                        <textPath href="#circlePath" startOffset="50%" text-anchor="middle">严禁洋节 · 弘扬传统</textPath>
                    </text>
                    <defs><path id="circlePath" d="M 50, 50 m -38, 0 a 38,38 0 1,1 76,0 a 38,38 0 1,1 -76,0" /></defs>
                </svg>
            </div>
        </div>
        <div id="card-container" style="display: none;">
            <div class="brutalist-card" id="main-card">
                <div class="brutalist-card__header">
                    <div class="brutalist-card__icon" id="card-icon">
                        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
                    </div>
                    <div class="brutalist-card__alert" id="card-title">SYSTEM ALERT</div>
                </div>
                <div class="brutalist-card__message" id="card-message">
                    检测到您试图关闭“禁止令”。<br><br>
                    警告：此行为被系统判定为 <b>[文化不自信]</b>。<br>
                    风险：可能导致“崇洋媚外”标签植入。<br>
                </div>
                <div class="brutalist-card__actions" id="card-actions">
                    <a class="brutalist-card__button brutalist-card__button--read" onclick="overrideSystem()">I WILL CELEBRATE (强制执行)</a>
                    <a class="brutalist-card__button" onclick="overrideSystem()">WHATEVER (配合演出)</a>
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

                // === 文案逻辑 ===
                document.getElementById('card-title').innerText = "REALITY DECODED";
                document.getElementById('card-message').innerHTML = `
                    <div class="quote-box">“洋节并不更可怕，更可怕的是中国人遗忘自己。” —— 冯骥才</div>
                    官方从未禁止过民间庆祝圣诞。所谓的“禁令”，往往是部分地方拿着鸡毛当令箭，是对这段讲话的断章取义，是一场将“不过洋节=文化自信”划等号的形式主义闹剧。<br><br>
                    节日无非是给了普通人一个放纵和娱乐的契机。<b>吃想吃的饭，见想见的人，做想做的事情。</b>给自己在这个紧绷的社会中多一点热爱生活的理由。<br>
                    我们永远不要忘记，<b>真正的自信不是排他的，而是海纳百川的。</b><br>

                    <div class="quote-box" style="border-left: 4px solid #27ae60; margin-top: 10px;">
                    最后祝大家：“在追求高素质生活的同时，也要有<b>乐天、惜福</b>的人生态度。”
                    </div>
                    生活不易，再次祝大家<b>圣诞快乐</b>！🍎
                `;
                

                document.getElementById('card-actions').innerHTML = `<a class="brutalist-card__button brutalist-card__button--read" style="background-color:#d35400; border-color:#d35400;">MERRY CHRISTMAS 🍎</a>`;
            }, 600);
        }
    </script>
</body>
</html>
        """, height=650, scrolling=False)
    else:
        st.markdown(f"""
        <div style='background-color: #222; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b; color: #fff;'>
            <h3>⚠️ HIDDEN TRUTH UNLOCKED</h3>
            <p>You have found the final secret.</p>
            <p style='color: #ccc; font-size: 0.9em;'>Switch to Simplified Chinese to experience the full interactive story about "Cultural Confidence".</p>
        </div>
        """, unsafe_allow_html=True)

# --- 6. 主程式邏輯 ---

# [關鍵修改] 優先檢查是否在樹模式 (如果是，直接渲染樹並停止後續執行)
if st.session_state['show_tree']:
    current_lang = st.session_state['ui_language']
    ui_text_tree = LANG_DICT[current_lang]
    show_tree_mode(ui_text_tree)
    st.stop() # 停止執行下方的正常頁面邏輯

add_christmas_magic()

if not st.session_state['language_selected']:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://img.icons8.com/color/144/santa.png", width=120)
    st.title("Welcome to Santa's Roast Room")
    st.subheader("Please select your language:")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("English 🇬🇧🇺🇸", use_container_width=True, on_click=set_language, args=("English 🇬🇧🇺🇸",))
    with col2:
        st.button("Simplified Chinese 🇨🇳", use_container_width=True, on_click=set_language,
                  args=("Simplified Chinese (简体中文) 🇨🇳",))
    with col3:
        st.button("Traditional Chinese 🇹🇼🇭🇰🇲🇴", use_container_width=True, on_click=set_language,
                  args=("Traditional Chinese (繁體中文) 🇹🇼🇭🇰🇲🇴",))

else:
    current_lang_key = st.session_state['ui_language']
    ui_text = LANG_DICT[current_lang_key]

    with st.sidebar:
        st.image("https://img.icons8.com/color/96/santa.png", width=100)
        st.caption(f"Language: **{current_lang_key}**")
        st.button("🔄 Change Language", on_click=reset_language)
        st.markdown("---")
        st.markdown(ui_text["game_rule"])

        api_key = None
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            st.warning("Enter Key to activate AI features")
            api_key = st.text_input("Gemini API Key", type="password")

        st.sidebar.caption(ui_text["api_help"])

    st.title(ui_text["title"])
    st.subheader(ui_text["subtitle"])

    hunt_placeholder = st.empty()
    update_hunt_progress(hunt_placeholder, ui_text)

    gift_list = st.text_area(ui_text["input_placeholder"], height=150)

    if st.button(ui_text["button"], type="primary"):
        if not api_key:
            st.error(ui_text["error_no_key"])
        elif not gift_list:
            st.warning(ui_text["error_no_text"])
        else:
            user_input_lower = gift_list.lower()

            triggers_tree = ["tree", "christmas tree", "decoration", "ornament", "star", "pine", "圣诞树", "树", "装饰", "挂件", "星星", "聖誕樹", "樹", "裝飾"]
            triggers_single = ["boyfriend", "girlfriend", "partner", "lover", "dating", "bf", "gf", "husband", "wife", "脱单", "男朋友", "女朋友", "对象", "搞对象", "恋爱", "处对象", "老公", "老婆", "脫單", "對象", "談戀愛", "男友", "女友"]
            triggers_deer = ["deer", "reindeer", "rudolph", "sleigh", "ride", "麋鹿", "鹿", "驯鹿", "雪橇", "鲁道夫", "馴鹿", "魯道夫"]
            triggers_food = ["cookie", "biscuit", "milk", "gingerbread", "turkey", "pudding", "pie", "cake", "food", "dinner", "feast", "eat", "hungry", "饼干", "牛奶", "姜饼", "火鸡", "布丁", "大餐", "食物", "吃", "饿", "蛋糕", "餅乾", "薑餅", "火雞", "晚餐", "餓"]
            triggers_bell = ["bell", "jingle", "ring", "song", "music", "sing", "carol", "sound", "铃铛", "铃", "钟", "响", "歌", "音乐", "叮当", "鈴鐺", "鈴聲", "音樂"]
            triggers_holiday = ["holiday", "vacation", "work", "job", "leave", "break", "office", "boss", "tired", "放假", "假期", "上班", "工作", "打工", "加班", "累", "请假", "老板", "休假", "請假", "老闆"]
            triggers_finland = ["finland", "suomi", "helsinki", "rovaniemi", "lapland", "travel", "trip", "north pole", "芬兰", "赫尔辛基", "罗瓦涅米", "圣诞村", "旅行", "出去玩", "北极", "芬蘭", "赫爾辛基", "聖誕老人村", "旅遊", "北極"]
            triggers_surprise = ["santa", "gift", "present", "box", "claus", "圣诞老人", "礼物", "礼盒", "圣诞老爷爷", "聖誕老人", "禮物", "禮盒", "聖誕老公公"]
            triggers_padoru = ["padoru", "hashire sori yo", "nero", "fate", "tsukimihara", "帕多鲁", "帕多露", "聖誕帽", "圣诞帽", "帽子", "christmas hat", "hat"]
            triggers_snow = ["snow", "let it snow", "white christmas", "winter", "cold", "雪", "下雪", "雪花", "冬天", "冷", "白"]
            triggers_market = ["market", "bazaar", "glühwein", "shopping", "stall", "集市", "市集", "逛街", "热红酒", "赶集", "聖誕市集", "熱紅酒"]
            triggers_author = ["joe qiao", "joe", "qyc", "乔钰城", "乔老师", "18岁老师", "乔哥", "小乔", "author", "creator", "developer", "who made this", "dev", "code", "作者", "开发者", "是谁做的", "开发", "程序员", "代码", "開發者", "是誰做的", "程式"]
            triggers_final = ["merry christmas", "merry xmas", "圣诞快乐", "圣旦快乐", "生蛋快乐", "聖誕快樂"]

            new_discovery = False
            trigger_hint = False

            # --- 彩蛋檢測邏輯 ---
            if any(t in user_input_lower for t in triggers_tree):
                if 1 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(1)
                    new_discovery = True
                    trigger_hint = True
            elif any(t in user_input_lower for t in triggers_single):
                if 2 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(2)
                    new_discovery = True
                    trigger_hint = True
            elif any(t in user_input_lower for t in triggers_deer):
                if 3 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(3)
                    new_discovery = True
                    trigger_hint = True
            elif any(t in user_input_lower for t in triggers_food):
                if 4 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(4)
                    new_discovery = True
                    trigger_hint = True
            elif any(t in user_input_lower for t in triggers_bell):
                if 5 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(5)
                    new_discovery = True
                    trigger_hint = True
            elif any(t in user_input_lower for t in triggers_holiday):
                if 6 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(6)
                    new_discovery = True
                    trigger_hint = True
            elif any(t in user_input_lower for t in triggers_finland):
                if 7 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(7)
                    new_discovery = True
                    trigger_hint = True
            elif any(t in user_input_lower for t in triggers_surprise):
                if 9 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(9)
                    new_discovery = True
                    trigger_hint = True
            elif any(t in user_input_lower for t in triggers_padoru):
                if 10 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(10)
                    new_discovery = True
                    trigger_hint = True
            elif any(t in user_input_lower for t in triggers_snow):
                if 11 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(11)
                    new_discovery = True
                    trigger_hint = True
            elif any(t in user_input_lower for t in triggers_market):
                if 12 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(12)
                    new_discovery = True
                    trigger_hint = True
            elif any(t in user_input_lower for t in triggers_author):
                if 13 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(13)
                    new_discovery = True
                    trigger_hint = True

            if new_discovery:
                update_hunt_progress(hunt_placeholder, ui_text)

            standard_eggs = {1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13}
            found_standard_count_now = len([x for x in st.session_state['found_ids'] if x in standard_eggs])

            if found_standard_count_now >= 12 and any(t in user_input_lower for t in triggers_final):
                if 8 not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(8)
                    update_hunt_progress(hunt_placeholder, ui_text)
                    st.balloons()
                    st.success("🎉 TRUTH REVEALED!")
                render_culture_egg(current_lang_key)

            # --- [關鍵修改] 聖誕樹：按鈕點擊後切換狀態 ---
            elif any(t in user_input_lower for t in triggers_tree):
                st.success(ui_text["secret_success"])
                st.markdown(ui_text["secret_title"])
                # 這裡不再跳轉，而是切換 session_state
                if st.button(ui_text["secret_button"], type="primary"):
                    st.session_state['show_tree'] = True
                    st.rerun()
            # ---------------------------------------------

            elif any(t in user_input_lower for t in triggers_single):
                try:
                    st.audio("bgm.mp3", format="audio/mp3", start_time=0, autoplay=True)
                except:
                    pass
                st.markdown(f"<div class='roast-box'>{ui_text['egg_single']} 🎧</div>", unsafe_allow_html=True)

            elif any(t in user_input_lower for t in triggers_deer):
                st.markdown("""<style>.scene-wrapper { position: fixed; width: 20em; height: 15em; bottom: 20%; left: -30%; z-index: 9999; animation: walkAcrossScreen 15s linear infinite; pointer-events: none; } @keyframes walkAcrossScreen { from { left: -30%; } to { left: 110%; } } .rudolph-loader { transform: scale(1.2); } .deer-body { background: #8B4513; } .red-nose { background: red; box-shadow: 0 0 15px red; animation: nose-pulse 1.5s infinite; } @keyframes nose-pulse { from { box-shadow: 0 0 10px red; } to { box-shadow: 0 0 30px red; } }</style>
                <div class="scene-wrapper"><div style="font-size:100px;">🦌</div></div>""", unsafe_allow_html=True) 
                st.markdown(f"<div class='roast-box gold-mode' style='border-left: 5px solid #8B4513 !important;'>{ui_text['egg_deer']}</div>", unsafe_allow_html=True)

            elif any(t in user_input_lower for t in triggers_food):
                st.balloons()
                trigger_jackpot_effect()
                st.markdown(f"<div class='roast-box gold-mode' style='border-left: 5px solid #FF9800 !important;'>{ui_text['egg_food']}</div>", unsafe_allow_html=True)

            elif any(t in user_input_lower for t in triggers_bell):
                try:
                    st.audio("bell.mp3", format="audio/mp3", start_time=0, autoplay=True)
                except:
                    pass
                st.markdown(f"<div class='roast-box gold-mode' style='border-left: 5px solid #FFD700 !important;'>{ui_text['egg_bell']}</div>", unsafe_allow_html=True)

            elif any(t in user_input_lower for t in triggers_holiday):
                st.balloons()
                h_text = HOLIDAY_TEXT.get(current_lang_key, HOLIDAY_TEXT["English 🇬🇧🇺🇸"])
                st.markdown(f"<div class='roast-box gold-mode' style='border-left: 5px solid #FFEB3B !important;'>🎅 <b>Santa's Verdict:</b><br>{h_text['roast_body']}</div>", unsafe_allow_html=True)

            elif any(t in user_input_lower for t in triggers_finland):
                st.markdown(f"<div class='roast-box gold-mode' style='border-left: 5px solid #003580 !important;'>{ui_text['egg_finland']}</div>", unsafe_allow_html=True)

            elif any(t in user_input_lower for t in triggers_surprise):
                st.balloons()
                st.markdown(f"<div class='roast-box gold-mode' style='border-left: 5px solid #FF3D00 !important;'>{ui_text['egg_surprise']}</div>", unsafe_allow_html=True)

            elif any(t in user_input_lower for t in triggers_padoru):
                st.balloons()
                gif_b64 = get_base64_image("padoru.gif")
                img_tag = f'<img src="data:image/gif;base64,{gif_b64}" style="width:150px;">' if gif_b64 else '🧣'
                st.markdown(f"<div style='position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);z-index:9999;'>{img_tag}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='roast-box gold-mode' style='border-left: 5px solid #D32F2F !important;'>{ui_text['egg_padoru']}</div>", unsafe_allow_html=True)

            elif any(t in user_input_lower for t in triggers_snow):
                st.snow()
                st.markdown(f"<div class='roast-box gold-mode' style='border-left: 5px solid #E0F7FA !important;'>{ui_text['egg_snow']}</div>", unsafe_allow_html=True)

            elif any(t in user_input_lower for t in triggers_market):
                st.balloons()
                st.markdown(f"<div class='roast-box gold-mode' style='border-left: 5px solid #FF5722 !important;'>{ui_text['egg_market']}</div>", unsafe_allow_html=True)

            elif any(t in user_input_lower for t in triggers_author):
                st.balloons()
                st.image("pic.png", caption="The Creator", width=300)
                st.markdown(f"<div class='roast-box gold-mode' style='border-left: 5px solid #4CAF50 !important;'>{ui_text['egg_author']}</div>", unsafe_allow_html=True)

            else:
                with st.spinner(ui_text["loading"]):
                    try:
                        genai.configure(api_key=api_key)
                        # [保持原樣] 您的模型選擇邏輯
                        try:
                            model = genai.GenerativeModel('gemini-3-pro-preview')
                        except:
                            model = genai.GenerativeModel('gemini-1.5-flash')

                        persona = f"You are Santa Claus. User Language: {current_lang_key}. Roast them but be funny."
                        response = model.generate_content(f"{persona}\n\nUser's Wish: {gift_list}")
                        st.markdown(f"<div class='roast-box'>{response.text}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Santa crashed: {e}")

            if trigger_hint:
                missing_ids = list(MAIN_EGG_IDS - st.session_state['found_ids'])
                if missing_ids:
                    target_id = random.choice(missing_ids)
                    clue = HINT_CLUES.get(current_lang_key, {}).get(target_id, "")
                    if clue:
                        st.info(f"{ui_text['hint_prefix']}{clue}")

            if len([x for x in st.session_state['found_ids'] if x in standard_eggs]) == 12 and 8 not in st.session_state['found_ids']:
                time.sleep(1)
                st.markdown("---")
                st.warning(ui_text['final_hint_msg'], icon="🔐")

    st.markdown("---")
    st.markdown(f"<div style='text-align: center; color: #aaa;'>{ui_text['footer']}</div>", unsafe_allow_html=True)
