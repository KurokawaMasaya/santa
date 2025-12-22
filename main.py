import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import random
import time
import base64

st.set_page_config(page_title="Roast Santa AI", page_icon="🎅", layout="centered")

LANG_DICT = {
    "English 🇬🇧🇺🇸": {
        "title": "🎅 Santa's Roast Room",
        "subtitle": "Let The Great Santa judge your greedy soul... 😏",
        "sidebar_title": "🎅 Settings",
        "api_help": "Key is used for this session only.",
        "game_rule": "💡 **How to play:**\nEnter your wishlist. Unlock 12 festive secrets!\n\n**Tip:** Most secrets are related to **Christmas items**, but some are about your *relationship*, *work* or *travel*...",
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
        "egg_finland": "Tervetuloa! You found my home — Finland (Suomi)! 🇫🇮\nThe sauna is ready, come visit Rovaniemi!",
        "egg_surprise": "🎁 SURPRISE! You summoned me directly!",
        "egg_padoru": "🎵 HASHIRE SORI YO... KAZE NO YOU NI... PADORU PADORU! 🧣",
        "egg_snow": "❄️ Let it snow! The world is quiet and beautiful now...",
        "egg_market": "🍷 Welcome to the Christmas Market! Hot Glühwein & Pretzels! 🥨",
        "egg_author": "👨‍💻 Creator found! Respect."
    },
    "Traditional Chinese (繁體中文) 🇹🇼🇭🇰🇲🇴": {
        "title": "🎅 聖誕老人吐槽大會",
        "subtitle": "讓本聖誕老人... 用邏輯粉碎你的夢想... 😏",
        "sidebar_title": "🎅 設定",
        "api_help": "Key 僅用於本次連線，重新整理即消失。",
        "game_rule": "💡 **玩法說明：**\n輸入願望清單。試著解鎖 12 個節日彩蛋！\n\n**提示：** 彩蛋多與**聖誕物品**有關，但也有關於*感情*、*打工*或*旅行*的...",
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
        "egg_finland": "Tervetuloa! (歡迎！) 你竟然找到了我的老家——芬蘭 (Finland)！🇫🇮\n這裡的桑拿房已經熱好了，快來羅瓦涅米找我玩吧！",
        "egg_surprise": "🎁 驚喜！你竟然直接召喚了本尊！",
        "egg_padoru": "🎵 走れ逸れよ... 風のように... PADORU PADORU !!! 🧣",
        "egg_snow": "❄️ 讓雪落下吧！整個世界都安靜了...",
        "egg_market": "🍷 歡迎來到聖誕集市！來杯熱紅酒配扭結餅吧！🥨",
        "egg_author": "👨‍💻 作者出現！致敬時刻..."
    },
    "Simplified Chinese (简体中文) 🇨🇳": {
        "title": "🎅 圣诞老人吐槽大会",
        "subtitle": "让本圣诞老人... 用逻辑粉碎你的梦想... 😏",
        "sidebar_title": "🎅 设置",
        "api_help": "Key 仅用于本次会话。",
        "game_rule": "💡 **玩法说明：**\n输入愿望清单。试着解锁 12 个节日彩蛋！\n\n**提示：** 彩蛋多与**圣诞物品**有关，但也有关于*感情*、*打工*或*旅行*的...",
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
        "hunt_title": "🏆 圣诞彩蛋收集进度",
        "egg_single": "本圣诞老人叹气... 没对象？听听这首歌吧。",
        "egg_deer": "看！是鲁道夫在爬你的屏幕！🔴🦌",
        "egg_food": "真香！既然你请我吃大餐，偷偷给你个线索：",
        "egg_bell": "叮叮当！🔔 这是幸运的声音！",
        "egg_finland": "Tervetuloa! (欢迎！) 你竟然找到了我的老家——芬兰 (Finland)！🇫🇮\n这里的桑拿房已经热好了，快来罗瓦涅米找我玩吧！",
        "egg_surprise": "🎁 惊喜！你竟然直接召唤了本尊！",
        "egg_padoru": "🎵 走れ逸れよ... 風のように... PADORU PADORU !!! 🧣",
        "egg_snow": "❄️ 让雪落下吧！整个世界都安静了...",
        "egg_market": "🍷 欢迎来到圣诞集市！来杯热红酒配扭结饼吧！🥨",
        "egg_author": "👨‍💻 作者出现！致敬时刻..."
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

if 'language_selected' not in st.session_state:
    st.session_state['language_selected'] = False
if 'ui_language' not in st.session_state:
    st.session_state['ui_language'] = "English 🇬🇧🇺🇸"

MAIN_EGG_IDS = {1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13}

if 'found_ids' not in st.session_state:
    st.session_state['found_ids'] = set() 

if 'hint_msg_v2' not in st.session_state:
    st.session_state['hint_msg_v2'] = None

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
    except:
        return None

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

add_christmas_magic()

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
            st.markdown(f"<h4 style='text-align: right; color: #FFD700;'>{found_main_count} / {total_eggs}</h4>", unsafe_allow_html=True)
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
        if 8 in st.session_state['found_ids']: medals += "👁️ " 
        st.caption(f"Collection: {medals}")
        if found_main_count == total_eggs:
            if 8 in st.session_state['found_ids']: st.success("🎉 GODLIKE! You found ALL secrets!")
            else: st.balloons(); st.success("🎉 Santa Master! You unlocked all secrets!")
        st.markdown('</div>', unsafe_allow_html=True)

def get_next_hint_msg(current_lang_key):
    missing_ids = list(MAIN_EGG_IDS - st.session_state['found_ids'])
    if 4 in missing_ids: missing_ids.remove(4)
    if not missing_ids: return None
    target = random.choice(missing_ids)
    hints_tw = {
        1: ["提示：客廳裡的綠色屍體...", "提示：禮物通常放在哪裡下面？"],
        2: ["提示：錢買不到，你也遇不到的關係。", "提示：雙人床的另一邊是空的..."],
        3: ["提示：紅鼻子的司機。", "提示：雪橇的動力來源。"],
        5: ["提示：搖晃會尖叫的金屬。", "提示：Jingle ____?"],
        6: ["提示：你最想從老闆那裡得到的批准。", "提示：不用去公司的日子。"],
        7: ["提示：千湖之國，我的老家。", "提示：以 F 開頭，以 d 結尾的寒冷國家。"],
        9: ["提示：直接呼喚我的尊名。", "提示：我不只送禮物，我就是..."],
        10: ["提示：一個紅色的、會旋轉的二次元生物...", "提示：Hashire sori yo..."],
        11: ["提示：白色的、冰涼的頭皮屑。", "提示：讓世界變安靜的天氣。"],
        12: ["提示：熱紅酒和扭結餅的聚集地。", "提示：聖誕節燒錢的好去處。"],
        13: ["提示：幕後的代碼編寫者。", "提示：誰創造了這個宇宙？"]
    }
    hints_cn = {
        1: ["提示：客厅里的绿色尸体...", "提示：礼物通常放在哪里下面？"],
        2: ["提示：钱买不到，你也遇不到的关系。", "提示：双人床的另一边是空的..."],
        3: ["提示：红鼻子的司机。", "提示：雪橇的动力来源。"],
        5: ["提示：摇晃会尖叫的金属。", "提示：叮叮当...？"],
        6: ["提示：你最想从老板那里得到的批准。", "提示：不用去公司的日子。"],
        7: ["提示：千湖之国，我的老家。", "提示：以 F 开头，以 d 结尾的寒冷国家。"],
        9: ["提示：直接呼唤我的尊名。", "提示：我不只送礼物，我就是..."],
        10: ["提示：一个红色的、会旋转的二次元生物...", "提示：Hashire sori yo..."],
        11: ["提示：白色的、冰凉的头皮屑。", "提示：让世界变安静的天气。"],
        12: ["提示：热红酒和扭结饼的聚集地。", "提示：圣诞节烧钱的好去处。"],
        13: ["提示：幕后的代码编写者。", "提示：谁创造了这个宇宙？"]
    }
    hints_en = {
        1: ["Hint: Green thing in living room.", "Hint: Presents go under...?"],
        2: ["Hint: No lover?", "Hint: Lonely in Christmas?"],
        3: ["Hint: Red-nosed driver.", "Hint: Sleigh power."],
        5: ["Hint: Jingle ____?", "Hint: Metal tongue."],
        6: ["Hint: Escape work.", "Hint: Not going to office."],
        7: ["Hint: Santa's home.", "Hint: Cold Nordic country."],
        9: ["Hint: Call my name.", "Hint: I'm not just a gift giver."],
        10: ["Hint: Spinning anime meme.", "Hint: Hashire sori yo..."],
        11: ["Hint: Cold sky dandruff.", "Hint: White Christmas weather."],
        12: ["Hint: Hot wine stalls.", "Hint: Outdoor shopping."],
        13: ["Hint: The coder.", "Hint: Creator of this App."]
    }
    if "Traditional" in current_lang_key: return random.choice(hints_tw.get(target, ["繼續許願..."]))
    elif "Simplified" in current_lang_key: return random.choice(hints_cn.get(target, ["继续许愿..."]))
    else: return random.choice(hints_en.get(target, ["Keep wishing..."]))

if not st.session_state['language_selected']:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2: st.image("https://img.icons8.com/color/144/santa.png", width=120)
    st.title("Welcome to Santa's Roast Room")
    st.subheader("Please select your language:")
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1: st.button("English 🇬🇧🇺🇸", use_container_width=True, on_click=set_language, args=("English 🇬🇧🇺🇸",))
    with c2: st.button("简体中文 🇨🇳", use_container_width=True, on_click=set_language, args=("Simplified Chinese (简体中文) 🇨🇳",))
    with c3: st.button("繁體中文 🇭🇰", use_container_width=True, on_click=set_language, args=("Traditional Chinese (繁體中文) 🇹🇼🇭🇰🇲🇴",))

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
            if "GEMINI_API_KEY" in st.secrets: api_key = st.secrets["GEMINI_API_KEY"]
        except: pass
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
        if not api_key: st.error(ui_text["error_no_key"])
        elif not gift_list: st.warning(ui_text["error_no_text"])
        else:
            user_input_lower = gift_list.lower()
            is_egg = False
            
            triggers_culture = ["foreign festival", "ban", "invasion", "western festival", "洋节", "抵制", "公文", "文化入侵", "不过洋节", "禁止", "洋節", "忘本"]
            if any(t in user_input_lower for t in triggers_culture):
                if 8 not in st.session_state['found_ids']: 
                    st.session_state['found_ids'].add(8)
                    update_hunt_progress(hunt_placeholder, ui_text)
                if "Chinese" in current_lang_key or "中文" in current_lang_key:
                    components.html("""
<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"><style>@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700;900&family=Noto+Sans+SC:wght@400;700&display=swap');*{box-sizing:border-box}body{margin:0;height:100vh;background-color:transparent;display:flex;justify-content:center;align-items:center;font-family:"Noto Sans SC",sans-serif;overflow:hidden}.interaction-container{position:relative;width:100%;height:100%;display:flex;justify-content:center;align-items:center}#stage-1{position:absolute;width:85%;max-width:340px;background:#fff;padding:40px 25px 60px;box-shadow:0 15px 40px rgba(0,0,0,.5);transform:rotate(-.5deg);z-index:10;transition:all .6s cubic-bezier(.68,-.55,.265,1.55);color:#000;font-family:"FangSong","SimSun",serif;border-radius:2px}.doc-header{text-align:center;color:#d60000;font-family:"SimSun","SimHei",serif;font-size:24px;font-weight:500;letter-spacing:1px;margin-bottom:20px}.doc-title{text-align:center;font-size:20px;font-weight:500;margin-bottom:10px;line-height:1.4;font-family:"SimSun",serif;letter-spacing:2px}.doc-serial{text-align:center;font-size:12px;margin-bottom:25px;font-family:"FangSong",serif}.doc-body{font-size:14px;line-height:1.6;text-align:justify;color:#222;margin-bottom:30px;text-indent:2em;font-family:"FangSong",serif}.close-btn{position:absolute;top:10px;right:10px;width:32px;height:32px;background:#f0f0f0;color:#333;border:1px solid #ccc;border-radius:50%;font-size:20px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 5px rgba(0,0,0,.1);transition:transform .2s;z-index:20}.close-btn:hover{background:#d60000;color:#fff;transform:scale(1.1);border-color:#d60000}#card-container{display:none;position:relative;z-index:20;perspective:1000px;width:100%;justify-content:center}.brutalist-card{width:85%;max-width:340px;border:4px solid #000;background-color:#fff;padding:1.2rem;box-shadow:10px 10px 0 #000;font-family:"Noto Sans SC",sans-serif;transition:all .3s;position:relative}.brutalist-card__header{display:flex;align-items:center;gap:1rem;margin-bottom:1rem;border-bottom:2px solid #000;padding-bottom:1rem}.brutalist-card__icon{flex-shrink:0;display:flex;align-items:center;justify-content:center;background-color:#000;padding:.5rem;transition:background .3s}.brutalist-card__icon svg{height:1.5rem;width:1.5rem;fill:#fff}.brutalist-card__alert{font-weight:900;color:#000;font-size:1.1rem;text-transform:uppercase}.brutalist-card__message{margin-top:1rem;color:#000;font-size:.9rem;line-height:1.6;border-bottom:2px solid #000;padding-bottom:1rem;font-weight:600;min-height:140px}.brutalist-card__actions{margin-top:1rem;display:flex;flex-direction:column;gap:10px}.brutalist-card__button{display:block;width:100%;padding:.75rem;text-align:center;font-size:.95rem;font-weight:700;text-transform:uppercase;border:3px solid #000;background-color:#fff;color:#000;position:relative;transition:all .2s;box-shadow:4px 4px 0 #000;text-decoration:none;cursor:pointer}.brutalist-card__button--read{background-color:#000;color:#fff}.hacked .brutalist-card{border-color:#d35400;box-shadow:10px 10px 0 #e67e22}.hacked .brutalist-card__icon{background-color:#d35400}.hacked .brutalist-card__alert{color:#d35400}.hacked .brutalist-card__message{border-bottom-color:#d35400;font-family:"Noto Serif SC",serif;font-size:.85rem;font-weight:400}.pop-in{display:flex!important;animation:pop-in .4s cubic-bezier(.175,.885,.32,1.275) forwards}.fly-out{animation:fly-away .8s cubic-bezier(.6,-.28,.735,.045) forwards;pointer-events:none}.glitching{animation:glitch-shake .3s cubic-bezier(.36,.07,.19,.97) both infinite;filter:invert(1)}@keyframes fly-away{to{transform:translateY(120vh) rotate(20deg);opacity:0}}@keyframes pop-in{from{opacity:0;transform:scale(.8)}to{opacity:1;transform:scale(1)}}@keyframes glitch-shake{10%,90%{transform:translate3d(-1px,0,0)}20%,80%{transform:translate3d(2px,0,0)}30%,50%,70%{transform:translate3d(-4px,0,0)}40%,60%{transform:translate3d(4px,0,0)}}</style></head><body><div class="interaction-container"><div id="stage-1"><button class="close-btn" onclick="triggerWarning()">×</button><div class="doc-header">XX县教育体育局</div><div class="doc-title">公　告</div><div class="doc-serial">（XX教体字 2025 第 120 号）</div><div class="doc-body"><p>根据上级精神，为抵御西方文化渗透，严禁过“洋节”。全县学校严禁摆放圣诞树、彩灯等装饰。</p></div></div><div id="card-container" style="display:none"><div class="brutalist-card" id="main-card"><div class="brutalist-card__header"><div class="brutalist-card__icon" id="card-icon"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg></div><div class="brutalist-card__alert" id="card-title">SYSTEM ALERT</div></div><div class="brutalist-card__message" id="card-message">检测到您试图关闭“禁止令”。警告：此行为被判定为 [文化不自信]。风险：可能导致“崇洋媚外”标签。</div><div class="brutalist-card__actions"><a class="brutalist-card__button brutalist-card__button--read" onclick="overrideSystem()">I WILL CELEBRATE</a><a class="brutalist-card__button" onclick="overrideSystem()">WHATEVER</a></div></div></div></div><script>function triggerWarning(){document.getElementById('stage-1').classList.add('fly-out');setTimeout(()=>{document.getElementById('card-container').classList.add('pop-in')},400)}function overrideSystem(){var c=document.getElementById('main-card');c.classList.add('glitching');setTimeout(()=>{c.classList.remove('glitching');document.getElementById('card-container').classList.add('hacked');document.getElementById('card-title').innerText="REALITY DECODED";document.getElementById('card-message').innerHTML="🎅 <b>圣诞老人的判决：</b><br>生活已经够苦了，我们只是借着节日去见想见的人，吃顿热乎饭。这不是崇洋媚外，这是对生活的热爱。";},600)}</script></body></html>
                    """, height=650)
                else:
                    st.markdown(f"<div class='roast-box'>{CULTURE_EXPLAINER_TEXT['English 🇬🇧🇺🇸']['msg']}<br>{CULTURE_EXPLAINER_TEXT['English 🇬🇧🇺🇸']['desc']}</div>", unsafe_allow_html=True)
                st.stop()

            triggers_tree = ["tree", "christmas tree", "decoration", "圣诞树", "装饰", "聖誕樹", " decoración", "sapin"]
            if any(t in user_input_lower for t in triggers_tree):
                if 1 not in st.session_state['found_ids']: 
                    st.session_state['found_ids'].add(1)
                    st.toast(get_next_hint_msg(current_lang_key), icon="💡")
                    update_hunt_progress(hunt_placeholder, ui_text)
                st.success(ui_text["secret_success"])
                st.link_button(ui_text["secret_button"], "https://wkpsyvxy8njhxmuqyy6gpr.streamlit.app")
                st.stop()

            triggers_single = ["boyfriend", "girlfriend", "partner", "lover", "脱单", "男朋友", "女朋友", "恋爱", "脫單", "談戀愛", "彼氏", "彼女", "petit ami"]
            if any(t in user_input_lower for t in triggers_single):
                if 2 not in st.session_state['found_ids']: 
                    st.session_state['found_ids'].add(2)
                    st.toast(get_next_hint_msg(current_lang_key), icon="💡")
                    update_hunt_progress(hunt_placeholder, ui_text)
                try: st.audio("bgm.mp3", format="audio/mp3", start_time=0, autoplay=True)
                except: pass
                st.markdown(f"<div class='roast-box'>{ui_text['egg_single']} 🎧</div>", unsafe_allow_html=True)
                st.stop()

            triggers_deer = ["deer", "reindeer", "rudolph", "麋鹿", "驯鹿", "鲁道夫", "トナカイ", "renne"]
            if any(t in user_input_lower for t in triggers_deer):
                if 3 not in st.session_state['found_ids']: 
                    st.session_state['found_ids'].add(3)
                    st.toast(get_next_hint_msg(current_lang_key), icon="💡")
                    update_hunt_progress(hunt_placeholder, ui_text)
                st.markdown("""<style>.scene-wrapper{position:fixed;width:20em;height:15em;bottom:20%;left:-30%;z-index:9999;animation:walkAcrossScreen 15s linear infinite;pointer-events:none}@keyframes walkAcrossScreen{from{left:-30%}to{left:110%}}.rudolph-loader{width:14em;height:10em;position:relative;--deer-color:#8B4513;--deer-dark:#5D4037;--nose-glow:#FF0000;transform:scale(1.2)}.deer-body{width:85%;height:100%;background:linear-gradient(var(--deer-color),90%,var(--deer-dark));border-radius:45%;position:relative;animation:movebody 1s linear infinite}.deer-head{width:7.5em;height:7em;bottom:0;right:0;position:absolute;background-color:var(--deer-color);border-radius:3.5em;box-shadow:-.5em 0 var(--deer-dark);animation:movebody 1s linear infinite}.antler{position:absolute;top:-2.5em;width:.6em;height:3.5em;background-color:var(--deer-dark);border-radius:5px}.antler.left{left:2em;transform:rotate(-25deg)}.antler.right{left:4.5em;transform:rotate(25deg)}.red-nose{width:2.2em;height:2.2em;background:radial-gradient(circle at 30% 30%,#ffcccc,#f00);position:absolute;bottom:.8em;left:2.65em;border-radius:50%;z-index:10;box-shadow:0 0 15px var(--nose-glow);animation:nose-pulse 1.5s infinite alternate}@keyframes nose-pulse{from{transform:scale(1)}to{transform:scale(1.1)}}@keyframes movebody{0%,100%{transform:translateY(0)}50%{transform:translateY(-2px)}}</style><div class="scene-wrapper"><div class="rudolph-loader"><div class="deer-body"></div><div class="deer-head"><div class="antler left"></div><div class="antler right"></div><div class="red-nose"></div></div></div></div>""", unsafe_allow_html=True)
                st.markdown(f"<div class='roast-box gold-mode' style='border-left: 5px solid #8B4513 !important;'>{ui_text['egg_deer']}</div>", unsafe_allow_html=True)
                st.stop()

            triggers_food = ["cookie", "biscuit", "milk", "gingerbread", "turkey", "pie", "cake", "food", "dinner", "feast", "eat", "饼干", "牛奶", "姜饼", "火鸡", "大餐", "食物", "吃", "饿", "蛋糕", "晚餐"]
            if any(t in user_input_lower for t in triggers_food):
                if 4 not in st.session_state['found_ids']: 
                    st.session_state['found_ids'].add(4)
                    new_discovery = True
                    update_hunt_progress(hunt_placeholder, ui_text)
                st.balloons(); trigger_jackpot_effect()
                if st.session_state['hint_msg_v2'] is None: st.session_state['hint_msg_v2'] = get_next_hint_msg(current_lang_key)
                st.markdown(f"<div class='roast-box gold-mode' style='border-left: 5px solid #FF9800 !important;'>{ui_text['egg_food']}<br><br>👉 <b>{st.session_state['hint_msg_v2']}</b></div>", unsafe_allow_html=True)
                st.stop()

            triggers_bell = ["bell", "jingle", "ring", "song", "music", "sing", "铃铛", "铃", "响", "歌", "音乐", "叮当", "鈴鐺", "鈴聲", "音樂", "ベル"]
            if any(t in user_input_lower for t in triggers_bell):
                if 5 not in st.session_state['found_ids']: 
                    st.session_state['found_ids'].add(5)
                    st.toast(get_next_hint_msg(current_lang_key), icon="💡")
                    update_hunt_progress(hunt_placeholder, ui_text)
                st.markdown("""<style>.slot-machine-container{display:flex;justify-content:center;gap:15px;padding:15px}.bell-wrapper{position:relative;animation:drop-bounce .8s forwards}.bell-main{width:50px;height:60px;transform-origin:top center;animation:bell-loop-ring 1.5s infinite alternate}.bell-shape{width:100%;height:80%;background:gold;border-radius:15px 15px 5px 5px;border:2px solid #b8860b}@keyframes bell-loop-ring{from{transform:rotate(15deg)}to{transform:rotate(-15deg)}}</style><div class="slot-machine-container"><div class="bell-wrapper"><div class="bell-main"><div class="bell-shape"></div></div></div><div class="bell-wrapper"><div class="bell-main"><div class="bell-shape"></div></div></div><div class="bell-wrapper"><div class="bell-main"><div class="bell-shape"></div></div></div></div>""", unsafe_allow_html=True)
                st.markdown(f"<div class='roast-box gold-mode' style='border-left: 5px solid #FFD700 !important; text-align: center;'>{ui_text['egg_bell']}</div>", unsafe_allow_html=True)
                st.stop()

            triggers_finland = ["finland", "suomi", "rovaniemi", "芬兰", "芬蘭", "フィンランド", "finlande"]
            if any(t in user_input_lower for t in triggers_finland):
                if 7 not in st.session_state['found_ids']: 
                    st.session_state['found_ids'].add(7)
                    st.toast(get_next_hint_msg(current_lang_key), icon="💡")
                    update_hunt_progress(hunt_placeholder, ui_text)
                st.markdown(f"<div class='roast-box gold-mode' style='border-left: 5px solid #003580 !important;'>{ui_text['egg_finland']}</div>", unsafe_allow_html=True)
                st.stop()

            triggers_holiday = ["holiday", "vacation", "work", "job", "break", "放假", "假期", "上班", "工作", "打工", "加班", "老闆", "休み", "休暇", "vacances"]
            if any(t in user_input_lower for t in triggers_holiday):
                if 6 not in st.session_state['found_ids']: 
                    st.session_state['found_ids'].add(6)
                    st.toast(get_next_hint_msg(current_lang_key), icon="💡")
                    update_hunt_progress(hunt_placeholder, ui_text)
                h_text = HOLIDAY_TEXT.get(current_lang_key, HOLIDAY_TEXT["English 🇬🇧🇺🇸"])
                st.markdown(f"<div class='roast-box gold-mode'>{h_text['roast_title']}<br><b>{h_text['roast_body']}</b></div>", unsafe_allow_html=True)
                st.stop()

            triggers_surprise = ["santa", "gift", "present", "box", "圣诞老人", "礼物", "礼盒", "サンタ", "cadeau"]
            if any(t in user_input_lower for t in triggers_surprise):
                if 9 not in st.session_state['found_ids']: 
                    st.session_state['found_ids'].add(9)
                    st.toast(get_next_hint_msg(current_lang_key), icon="💡")
                    update_hunt_progress(hunt_placeholder, ui_text)
                st.balloons()
                components.html("""<!DOCTYPE html><html><body style="margin:0;display:flex;justify-content:center;align-items:center;height:100vh;background:transparent;overflow:hidden"><div style="font-size:100px;animation:pop 1s cubic-bezier(.17,.67,.83,.67) infinite">🎅🎁</div><style>@keyframes pop{0%,100%{transform:scale(1)}50%{transform:scale(1.5)}}</style></body></html>""", height=300)
                st.markdown(f"<div class='roast-box gold-mode' style='text-align:center;'>{ui_text['egg_surprise']}</div>", unsafe_allow_html=True)
                st.stop()

            triggers_padoru = ["padoru", "nero", "帕多鲁", "帕多露", "帽子", "christmas hat", "hat"]
            if any(t in user_input_lower for t in triggers_padoru):
                if 10 not in st.session_state['found_ids']: 
                    st.session_state['found_ids'].add(10)
                    st.toast(get_next_hint_msg(current_lang_key), icon="💡")
                    update_hunt_progress(hunt_placeholder, ui_text)
                st.balloons()
                try: st.audio("MerryChristmas.mp3", format="audio/mp3", start_time=0, autoplay=True)
                except: pass
                gif_b64 = get_base64_image("padoru.gif")
                img_tag = f'<img src="data:image/gif;base64,{gif_b64}" width="150">' if gif_b64 else '🧣'
                components.html(f"""<!DOCTYPE html><html><style>body{{margin:0;overflow:hidden;background:transparent}}.p{{position:fixed;top:50%;left:-200px;animation:r 6s linear infinite}}@keyframes r{{0%{{left:-200px}}100%{{left:100vw}}}}</style><body><div class="p">{img_tag}</div></body></html>""", height=200)
                st.markdown(f"<div class='roast-box gold-mode' style='text-align:center;'>{ui_text['egg_padoru']}</div>", unsafe_allow_html=True)
                st.stop()

            triggers_snow = ["snow", "let it snow", "雪", "下雪", "冬天", "neige"]
            if any(t in user_input_lower for t in triggers_snow):
                if 11 not in st.session_state['found_ids']: 
                    st.session_state['found_ids'].add(11)
                    st.toast(get_next_hint_msg(current_lang_key), icon="💡")
                    update_hunt_progress(hunt_placeholder, ui_text)
                st.snow()
                st.markdown(f"<div class='roast-box gold-mode'>{ui_text['egg_snow']}</div>", unsafe_allow_html=True)
                st.stop()

            triggers_market = ["market", "glühwein", "集市", "市集", "熱紅酒", "marché"]
            if any(t in user_input_lower for t in triggers_market):
                if 12 not in st.session_state['found_ids']: 
                    st.session_state['found_ids'].add(12)
                    st.toast(get_next_hint_msg(current_lang_key), icon="💡")
                    update_hunt_progress(hunt_placeholder, ui_text)
                st.balloons()
                st.markdown(f"<div class='roast-box gold-mode' style='border-left: 5px solid #FF5722 !important;'>{ui_text['egg_market']}</div>", unsafe_allow_html=True)
                st.stop()

            triggers_author = ["joe qiao", "joe", "qyc", "乔钰城", "乔老师", "18岁老师", "乔哥", "作者", "开发者"]
            if any(t in user_input_lower for t in triggers_author):
                if 13 not in st.session_state['found_ids']: 
                    st.session_state['found_ids'].add(13)
                    st.toast(get_next_hint_msg(current_lang_key), icon="💡")
                    update_hunt_progress(hunt_placeholder, ui_text)
                st.balloons()
                matched = next((t for t in triggers_author if t in user_input_lower), "Joe")
                img_b64 = get_base64_image("pic.png")
                if img_b64: st.markdown(f'<div style="display:flex;justify-content:center;"><img src="data:image/png;base64,{img_b64}" style="width:600px;border-radius:10px;"></div>', unsafe_allow_html=True)
                st.markdown(f"<div class='roast-box gold-mode'>👨‍💻 请给 <b>{matched}</b> 私信一句 <b>{matched}nb</b> 吧～</div>", unsafe_allow_html=True)
                st.stop()

            with st.spinner(ui_text["loading"]):
                try:
                    genai.configure(api_key=api_key)
                    try: model = genai.GenerativeModel('gemini-3-pro-preview')
                    except: model = genai.GenerativeModel('gemini-1.5-flash')
                    persona = f"""You are Santa Claus with a 'Tsundere' personality. Refer to yourself as '本圣诞老人' or '我'. Language: RESPOND in the SAME LANGUAGE as '{gift_list}'. Roast the user first, then reluctantly give advice."""
                    response = model.generate_content(f"{persona}\n\nWish: {gift_list}")
                    if "❤️" in response.text or "🌟" in response.text:
                        trigger_jackpot_effect(); st.balloons(); st.success(ui_text["success_title"])
                        box_style = "roast-box gold-mode"
                    else: st.toast("🎅 Santa is judging you...", icon="😒"); box_style = "roast-box"
                    st.markdown(f"<div class='{box_style}'>{response.text}</div>", unsafe_allow_html=True)
                except Exception as e: st.error(f"Santa crashed: {e}")

    st.markdown("---")
    st.markdown(f"<div style='text-align: center; color: #aaa;'>{ui_text['footer']}</div>", unsafe_allow_html=True)
