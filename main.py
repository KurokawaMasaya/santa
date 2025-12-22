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
        "game_rule": "💡 **How to play:**\nEnter your wishlist. Unlock 12 festive secrets!",
        "input_placeholder": "Your wishlist (e.g., iPhone 17 pro max...)",
        "button": "🎁 Roast My List",
        "loading": "🎅 Santa is assessing your worth...",
        "error_no_key": "Please enter your API Key first!",
        "error_no_text": "Write something!",
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
        "egg_finland": "Tervetuloa! You found my home — Finland! 🇫🇮",
        "egg_surprise": "🎁 SURPRISE! You summoned me directly!",
        "egg_padoru": "🎵 HASHIRE SORI YO... PADORU PADORU! 🧣",
        "egg_snow": "❄️ Let it snow! The world is quiet and beautiful now...",
        "egg_market": "🍷 Welcome to the Christmas Market! Hot Glühwein! 🥨",
        "egg_author": "👨‍💻 Creator found! Respect."
    },
    "Traditional Chinese (繁體中文) 🇹🇼🇭🇰🇲🇴": {
        "title": "🎅 聖誕老人吐槽大會",
        "subtitle": "讓本聖誕老人... 用邏輯粉碎你的夢想... 😏",
        "sidebar_title": "🎅 設定",
        "api_help": "Key 僅用於本次連線。",
        "game_rule": "💡 **玩法說明：**\n輸入願望清單。試著解鎖 12 個節日彩蛋！",
        "input_placeholder": "許願吧 (例如：iPhone 17 pro max...)",
        "button": "🎁 吐槽我的願望",
        "loading": "🎅 本聖誕老人正在審視你的人生...",
        "error_no_key": "請先輸入 Gemini API Key！",
        "error_no_text": "寫點東西啊！",
        "success_title": "🔔 判決已下！",
        "footer": "由 Google Gemini 3.0 Pro 強力驅動",
        "secret_success": "🎅 吼吼吼！你找到了聖誕樹！",
        "secret_title": "### 聖誕快樂！！！這是通往秘密基地的傳送門 🎄",
        "secret_button": "👉 點擊進入聖誕樹空間",
        "hunt_title": "🏆 彩蛋收集進度",
        "egg_single": "本聖誕老人嘆氣... 沒對象？聽聽這首歌吧。",
        "egg_deer": "看！是魯道夫在爬你的螢幕！🔴🦌",
        "egg_food": "真香！既然你請我吃大餐，本聖誕老人賞你一個線索：",
        "egg_bell": "叮叮噹！🔔 這是幸運的聲音！",
        "egg_finland": "Tervetuloa! 你竟然找到了我的老家——芬蘭！🇫🇮",
        "egg_surprise": "🎁 驚喜！你竟然直接召喚了本尊！",
        "egg_padoru": "🎵 走れ逸れよ... PADORU PADORU !!! 🧣",
        "egg_snow": "❄️ 讓雪落下吧！整個世界都安靜了...",
        "egg_market": "🍷 歡迎來到聖誕集市！來杯熱紅酒吧！🥨",
        "egg_author": "👨‍💻 作者出現！致敬時刻..."
    },
    "Simplified Chinese (简体中文) 🇨🇳": {
        "title": "🎅 圣诞老人吐槽大会",
        "subtitle": "让本圣诞老人... 用逻辑粉碎你的梦想... 😏",
        "sidebar_title": "🎅 设置",
        "api_help": "Key 仅用于本次会话。",
        "game_rule": "💡 **玩法说明：**\n输入愿望清单。试着解锁 12 个节日彩蛋！",
        "input_placeholder": "许愿吧 (例如：iPhone 17 pro max...)",
        "button": "🎁 吐槽我的愿望",
        "loading": "🎅 本圣诞老人正在审视你的人生...",
        "error_no_key": "请先输入 Gemini API Key！",
        "error_no_text": "写点东西啊！",
        "success_title": "🔔 判决已下！",
        "footer": "由 Google Gemini 3.0 Pro 强力驱动",
        "secret_success": "🎅 吼吼吼！你找到了圣诞树！",
        "secret_title": "### 圣诞快乐！！！这是通往秘密基地的传送门 🎄",
        "secret_button": "👉 点击进入圣诞树空间",
        "hunt_title": "🏆 圣诞彩蛋收集进度",
        "egg_single": "本圣诞老人叹气... 没对象？听听这首歌吧。",
        "egg_deer": "看！是鲁道夫在爬你的屏幕！🔴🦌",
        "egg_food": "真香！既然你请我吃大餐，本圣诞老人赏你一个线索：",
        "egg_bell": "叮叮当！🔔 这是幸运的声音！",
        "egg_finland": "Tervetuloa! 你竟然找到了我的老家——芬兰！🇫🇮",
        "egg_surprise": "🎁 惊喜！你竟然直接召唤了本尊！",
        "egg_padoru": "🎵 走れ逸れよ... PADORU PADORU !!! 🧣",
        "egg_snow": "❄️ 让雪落下吧！整个世界都安静了...",
        "egg_market": "🍷 欢迎来到圣诞集市！来杯热红酒吧！🥨",
        "egg_author": "👨‍💻 作者出现！致敬时刻..."
    }
}

HOLIDAY_TEXT = {
    "English 🇬🇧🇺🇸": {"roast_title": "Want a holiday?", "roast_body": "Granted! Take this ticket and tell your boss Santa said so."},
    "Simplified Chinese (简体中文) 🇨🇳": {"roast_title": "不想上班？想放假？", "roast_body": "准奏！拿好这张【摸鱼券】，告诉老板是我批准的！"},
    "Traditional Chinese (繁體中文) 🇹🇼🇭🇰🇲🇴": {"roast_title": "不想上班？想放假？", "roast_body": "准奏！拿好這張【摸魚券】，告訴老闆是我批准的！"}
}

MAIN_EGG_IDS = {1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13}

if 'found_ids' not in st.session_state: st.session_state['found_ids'] = set()
if 'hint_msg_v2' not in st.session_state: st.session_state['hint_msg_v2'] = None

def set_language(lang_key):
    st.session_state['ui_language'] = lang_key
    st.session_state['language_selected'] = True

def reset_language():
    st.session_state['language_selected'] = False

def get_base64_image(file_path):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return None

def add_christmas_magic():
    st.markdown("""
    <style>
        header[data-testid="stHeader"] { background-color: transparent !important; }
        .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label, .stMarkdown { color: #ffffff !important; text-shadow: 0 1px 3px rgba(0,0,0,0.8) !important; }
        .snowflake { position: fixed; top: -10px; z-index: 9999; color: #FFF; animation: fall linear infinite; pointer-events: none; }
        @keyframes fall { 0% { transform: translateY(0); opacity: 0.8; } 100% { transform: translateY(100vh); opacity: 0.2; } }
        .bulb { width: 20px; height: 30px; border-radius: 50%; margin: 0 10px; animation: flash 1.5s infinite; }
        @keyframes flash { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
        .stApp { background-image: linear-gradient(to bottom, #0f2027, #203a43, #2c5364); }
        .roast-box { background-color: #262730; padding: 20px; border-radius: 10px; border-left: 5px solid #FF4B4B; }
        .gold-mode { border-left: 5px solid #fff !important; box-shadow: 0 0 30px rgba(255, 255, 255, 0.4); }
        .hunt-panel { background-color: rgba(0, 0, 0, 0.3); padding: 15px; border-radius: 10px; margin-bottom: 20px; border: 1px solid rgba(255, 255, 255, 0.2); }
    </style>
    """, unsafe_allow_html=True)
    snow_html = "".join([f'<div class="snowflake" style="left: {random.randint(0, 100)}vw; animation-duration: {random.uniform(5, 15)}s;">❄</div>' for _ in range(30)])
    st.markdown(snow_html, unsafe_allow_html=True)

def trigger_jackpot_effect():
    st.markdown("""<style>@keyframes steam-rise { 0% { opacity: 0; } 50% { opacity: 0.8; } 100% { transform: translateY(-600px); opacity: 0; } }</style>""", unsafe_allow_html=True)

def update_hunt_progress(placeholder_obj, ui_text):
    found_main = [x for x in st.session_state['found_ids'] if x in MAIN_EGG_IDS]
    total = 12
    with placeholder_obj.container():
        st.markdown('<div class="hunt-panel">', unsafe_allow_html=True)
        st.markdown(f"#### {ui_text['hunt_title']} {len(found_main)} / {total}")
        st.progress(min(len(found_main) / total, 1.0))
        medals = "".join(["🎄 " if 1 in st.session_state['found_ids'] else "⚪ ", "👫 " if 2 in st.session_state['found_ids'] else "⚪ ", "🦌 " if 3 in st.session_state['found_ids'] else "⚪ ", "🍗 " if 4 in st.session_state['found_ids'] else "⚪ ", "🔔 " if 5 in st.session_state['found_ids'] else "⚪ ", "📅 " if 6 in st.session_state['found_ids'] else "⚪ ", "🇫🇮 " if 7 in st.session_state['found_ids'] else "⚪ ", "🎁 " if 9 in st.session_state['found_ids'] else "⚪ ", "🧣 " if 10 in st.session_state['found_ids'] else "⚪ ", "❄️ " if 11 in st.session_state['found_ids'] else "⚪ ", "🍷 " if 12 in st.session_state['found_ids'] else "⚪ ", "👨‍💻 " if 13 in st.session_state['found_ids'] else "⚪ "])
        st.caption(f"成就: {medals}")
        st.markdown('</div>', unsafe_allow_html=True)

def get_hint(lang):
    missing = list(MAIN_EGG_IDS - st.session_state['found_ids'])
    if 4 in missing: missing.remove(4)
    if not missing: return "You found all secrets!"
    target = random.choice(missing)
    hints = {
        1: ["客廳裡的綠色屍體...", "禮物放哪裡下面？"], 2: ["錢買不到的關係。", "單身狗的願望。"], 3: ["紅鼻子的司機。", "雪橇的動力。"],
        5: ["搖晃會尖叫的金屬。", "Jingle ____?"], 6: ["老闆不批準的假。", "不用上班的日子。"], 7: ["千湖之國老家。", "芬蘭的冷。"],
        9: ["呼喚我的名字。", "盒子裡的驚喜。"], 10: ["旋轉的紅斗篷。", "Hashire sori yo..."], 11: ["白色的頭皮屑。", "白色聖誕節。"],
        12: ["熱紅酒聚集地。", "聖誕購物的好去處。"], 13: ["幕後代碼者。", "誰創造了這裏？"]
    }
    return random.choice(hints.get(target, ["Keep searching..."]))

add_christmas_magic()

if not st.session_state.get('language_selected'):
    c1, c2, c3 = st.columns(3)
    c1.button("English 🇬🇧🇺🇸", on_click=set_language, args=("English 🇬🇧🇺🇸",))
    c2.button("简体中文 🇨🇳", on_click=set_language, args=("Simplified Chinese (简体中文) 🇨🇳",))
    c3.button("繁體中文 🇭🇰", on_click=set_language, args=("Traditional Chinese (繁體中文) 🇹🇼🇭🇰🇲🇴",))
else:
    current_lang = st.session_state['ui_language']
    ui_text = LANG_DICT[current_lang]
    st.title(ui_text["title"])
    hunt_placeholder = st.empty()
    update_hunt_progress(hunt_placeholder, ui_text)
    gift_list = st.text_area(ui_text["input_placeholder"], height=150)

    if st.button(ui_text["button"]):
        inp = gift_list.lower()
        if any(t in inp for t in ["foreign festival", "洋节", "禁止", "洋節"]):
            if 8 not in st.session_state['found_ids']: st.session_state['found_ids'].add(8)
            components.html("""<!DOCTYPE html><html><body style="background:white;color:black;padding:20px;font-family:serif;"><h1>公告</h1><p>根據上級精神，嚴禁慶祝洋節。</p><button onclick="parent.window.alert('聖誕老人：這不是崇洋媚外，這是對生活的熱愛。')">關閉</button></body></html>""", height=300)
            st.stop()

        egg_map = {
            1: ["tree", "圣诞树", "聖誕樹", "sapin"], 2: ["boyfriend", "girlfriend", "脱单", "戀愛"], 3: ["deer", "reindeer", "麋鹿", "驯鹿"],
            5: ["bell", "铃铛", "鈴鐺", "ベル"], 6: ["holiday", "vacation", "放假", "休み"], 7: ["finland", "芬兰", "芬蘭", "suomi"],
            9: ["santa", "gift", "present", "圣诞老人", "禮物"], 10: ["padoru", "nero", "帕多鲁", "hat"], 11: ["snow", "雪", "下雪"],
            12: ["market", "glühwein", "集市", "市集"], 13: ["joe", "qyc", "乔钰城", "作者"]
        }

        for eid, keywords in egg_map.items():
            if any(k in inp for k in keywords):
                if eid not in st.session_state['found_ids']:
                    st.session_state['found_ids'].add(eid)
                    st.toast(get_hint(current_lang), icon="💡")
                if eid == 1: st.success(ui_text["secret_success"]); st.link_button("CLICK", "https://wkpsyvxy8njhxmuqyy6gpr.streamlit.app")
                elif eid == 2: st.audio("bgm.mp3", autoplay=True); st.markdown(ui_text['egg_single'])
                elif eid == 4: st.balloons(); st.markdown(f"線索: {get_hint(current_lang)}")
                elif eid == 10: st.audio("MerryChristmas.mp3", autoplay=True); img_b64 = get_base64_image("padoru.gif"); components.html(f'<img src="data:image/gif;base64,{img_b64}" width="150">')
                elif eid == 11: st.snow(); st.info(ui_text['egg_snow'])
                elif eid == 13:
                    img_b64 = get_base64_image("pic.png")
                    if img_b64: st.markdown(f'<div style="display:flex;justify-content:center;"><img src="data:image/png;base64,{img_b64}" width="500"></div>', unsafe_allow_html=True)
                    st.info(f"請給作者私信一句 nb 吧")
                st.stop()

        if any(t in inp for t in ["cookie", "turkey", "eat", "大餐", "吃"]):
            if 4 not in st.session_state['found_ids']: st.session_state['found_ids'].add(4)
            st.balloons(); trigger_jackpot_effect()
            st.session_state['hint_msg_v2'] = get_hint(current_lang)
            st.markdown(f"<div class='roast-box gold-mode'>{ui_text['egg_food']}<br>👉 <b>{st.session_state['hint_msg_v2']}</b></div>", unsafe_allow_html=True)
            st.stop()

        with st.spinner(ui_text["loading"]):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                res = model.generate_content(f"You are Santa Claus with a Tsundere personality. Roast this wish in its original language: {gift_list}")
                st.toast("🎅 Santa is judging you...", icon="😒")
                st.markdown(f"<div class='roast-box'>{res.text}</div>", unsafe_allow_html=True)
            except Exception as e: st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown(f"<div style='text-align: center; color: #aaa;'>{ui_text['footer']}</div>", unsafe_allow_html=True)
