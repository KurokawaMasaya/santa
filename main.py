import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import random
import time
import base64

st.set_page_config(page_title="Roast Santa AI", page_icon="🎅", layout="centered")

# --- 语言字典 (仅保留 中/英) ---
LANG_DICT = {
    "English 🇬🇧🇺🇸": {
        "title": "🎅 Santa's Roast Room",
        "subtitle": "Let The Great Santa judge your greedy soul... 😏",
        "sidebar_title": "🎅 Settings",
        "api_help": "Key is used for this session only.",
        "game_rule": "💡 **How to play:**\nEnter your wishlist. Unlock 12 festive secrets!\n\n**Tip:** Finding a secret will grant you a hint for the next one!",
        "input_placeholder": "Your wishlist (e.g., iPhone 17 pro max, a boyfriend, money)",
        "button": "🎁 Roast My List",
        "loading": "🎅 Santa is assessing your worth...",
        "error_no_key": "Please enter your API Key first!",
        "error_no_text": "Write something! I can't roast a blank paper.",
        "success_title": "🔔 The Verdict is Here!",
        "footer": "Powered by Google Gemini",
        "secret_success": "🎅 Ho ho ho! You found the tree!",
        "secret_title": "### Merry Christmas!!! Enter the Secret Portal 🎄",
        "secret_button": "👉 CLICK TO ENTER",
        "hunt_title": "🏆 Secret Hunt Progress",
        "egg_single": "Santa sighs... No lover? Here, listen to this song.",
        "egg_deer": "Look! It's Rudolph crawling on your screen! 🔴🦌",
        "egg_food": "Delicious! Thanks for the treat!",
        "egg_bell": "Ring Ring! 🔔 That's the sound of luck!",
        "egg_finland": "Tervetuloa! You found my home — Finland! 🇫🇮",
        "egg_surprise": "🎁 SURPRISE! You summoned me directly!",
        "egg_padoru": "🎵 PADORU PADORU! 🧣",
        "egg_snow": "❄️ Let it snow! The world is quiet and beautiful now...",
        "egg_market": "🍷 Welcome to the Christmas Market! Hot Glühwein! 🥨",
        "egg_author": "👨‍💻 Creator found! Respect.",
        "new_hint_prefix": "📍 New Hint Unlocked:"
    },
    "简体中文 🇨🇳": {
        "title": "🎅 圣诞老人吐槽大会",
        "subtitle": "让本圣诞老人... 用逻辑粉碎你的梦想... 😏",
        "sidebar_title": "🎅 设置",
        "api_help": "Key 仅用于本次会话。",
        "game_rule": "💡 **玩法说明：**\n输入愿望清单。解锁 12 个节日彩蛋！\n\n**提示：** 每找到一个彩蛋，都会获得下一个彩蛋的精准线索！",
        "input_placeholder": "许愿吧 (例如：iPhone 17 pro max、男朋友、很多钱...)",
        "button": "🎁 吐槽我的愿望",
        "loading": "🎅 本圣诞老人正在审视你的人生...",
        "error_no_key": "请先在左侧输入 Gemini API Key！",
        "error_no_text": "写点东西啊！拿白纸我是要怎么吐槽？",
        "success_title": "🔔 判决已下！",
        "footer": "由 Google Gemini 强力驱动",
        "secret_success": "🎅 吼吼吼！你找到了圣诞树！",
        "secret_title": "### 圣诞快乐！！！这是通往秘密基地的传送门 🎄",
        "secret_button": "👉 点击进入圣诞树空间",
        "hunt_title": "🏆 彩蛋收集进度",
        "egg_single": "本圣诞老人叹气... 没对象？听听这首歌吧。",
        "egg_deer": "看！是鲁道夫在爬你的屏幕！🔴🦌",
        "egg_food": "真香！既然你请我吃大餐，给你个线索：",
        "egg_bell": "叮叮当！🔔 这是幸运的声音！",
        "egg_finland": "Tervetuloa! (欢迎！) 你找到了我的老家——芬兰！🇫🇮",
        "egg_surprise": "🎁 惊喜！你竟然直接召唤了本尊！",
        "egg_padoru": "🎵 PADORU PADORU !!! 🧣",
        "egg_snow": "❄️ 让雪落下吧！整个世界都安静了...",
        "egg_market": "🍷 欢迎来到圣诞集市！来杯热红酒！🥨",
        "egg_author": "👨‍💻 作者出现！致敬时刻...",
        "new_hint_prefix": "📍 获得新线索："
    },
    "繁體中文 🇹🇼🇭🇰": {
        "title": "🎅 聖誕老人吐槽大會",
        "subtitle": "讓本聖誕老人... 用邏輯粉碎你的夢想... 😏",
        "sidebar_title": "🎅 設定",
        "api_help": "Key 僅用於本次連線。",
        "game_rule": "💡 **玩法說明：**\n輸入願望清單。解鎖 12 個節日彩蛋！\n\n**提示：** 每找到一個彩蛋，都會獲得下一個彩蛋的精準線索！",
        "input_placeholder": "許願吧 (例如：iPhone 17 pro max、男朋友、很多錢...)",
        "button": "🎁 吐槽我的願望",
        "loading": "🎅 本聖誕老人正在審視你的人生...",
        "error_no_key": "請先在左側輸入 Gemini API Key！",
        "error_no_text": "寫點東西啊！拿白紙我是要怎麼吐槽？",
        "success_title": "🔔 判決已下！",
        "footer": "由 Google Gemini 強力驅動",
        "secret_success": "🎅 吼吼吼！你找到了聖誕樹！",
        "secret_title": "### 聖誕快樂！！！這是通往秘密基地的傳送門 🎄",
        "secret_button": "👉 點擊進入聖誕樹空間",
        "hunt_title": "🏆 彩蛋收集進度",
        "egg_single": "本聖誕老人嘆氣... 沒對象？聽聽這首歌吧。",
        "egg_deer": "看！是魯道夫在爬你的螢幕！🔴🦌",
        "egg_food": "真香！既然你請我吃大餐，給你個線索：",
        "egg_bell": "叮叮噹！🔔 這是幸運的聲音！",
        "egg_finland": "Tervetuloa! (歡迎！) 你找到了我的老家——芬蘭！🇫🇮",
        "egg_surprise": "🎁 驚喜！你竟然直接召喚了本尊！",
        "egg_padoru": "🎵 PADORU PADORU !!! 🧣",
        "egg_snow": "❄️ 讓雪落下吧！整個世界都安靜了...",
        "egg_market": "🍷 歡迎來到聖誕集市！來杯熱紅酒！🥨",
        "egg_author": "👨‍💻 作者出現！致敬時刻...",
        "new_hint_prefix": "📍 獲得新線索："
    }
}

# --- 彩蛋线索字典 ---
HINTS = {
    "English 🇬🇧🇺🇸": {
        1: "A corpse dressed in jewelry, dying slowly in your living room. 💎🥀",
        2: "Something money can't buy, and your personality can't attract. 💔",
        3: "My enslaved aerial taxi drivers. One has a glowing nose. 🔴🚕",
        4: "I'm hungry. Maybe some milk and cookies? 🍪",
        5: "Golden skin, metal tongue, screams when you shake it. 🔔😱",
        6: "A piece of paper that grants freedom from work. 📄😈",
        7: "A place colder than your ex's heart. My frozen wasteland. ❄️🏠",
        9: "Try calling my name directly, or asking for 'it'. 🎁",
        10: "A red, spinning meme creature... Try Christmas hat? 🧣",
        11: "I fall from the sky, white and cold... ❄️",
        12: "Hot wine, pretzels, and crowded stalls... 🍷",
        13: "Who created me? (About the developer) 👨‍💻"
    },
    "Chinese": {
        1: "提示：一种在客厅里慢慢死去的植物，身上还挂着珠宝。💎🥀",
        2: "提示：你的存款买不到，你的性格也吸引不到的那种关系。💔",
        3: "提示：一群被我奴役的空中出租车司机，其中有个红鼻子的。🔴🚕",
        4: "提示：我饿了，不打算请我吃点饼干和牛奶吗？🍪",
        5: "提示：有金属舌头，脑袋空空，一摇晃就会尖叫的东西。🔔😱",
        6: "提示：一张赋予你摸鱼自由，但你不敢拿给老板看的纸。📄😈",
        7: "提示：比你的心还要冰冷的地方，也是我的老巢。❄️🏠",
        9: "提示：试着直接呼唤我的名字，或者跟我要「那个」礼物？🎁",
        10: "提示：一个红色的、会旋转的迷因生物... 试试圣诞帽？ 🧣",
        11: "提示：我从天上掉下来，又白又冷... ❄️",
        12: "提示：热红酒、扭结饼、人挤人... 🍷",
        13: "提示：是谁创造了我？(关于作者) 👨‍💻"
    }
}

# --- 核心逻辑变量 ---
if 'found_ids' not in st.session_state: st.session_state['found_ids'] = set()
if 'ui_language' not in st.session_state: st.session_state['ui_language'] = "English 🇬🇧🇺🇸"
if 'language_selected' not in st.session_state: st.session_state['language_selected'] = False

MAIN_EGG_IDS = {1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13}

def set_language(lang_key):
    st.session_state['ui_language'] = lang_key
    st.session_state['language_selected'] = True

# --- 视觉装饰函数 ---
def add_bg():
    st.markdown("""
    <style>
        .stApp { background-image: linear-gradient(to bottom, #0f2027, #203a43, #2c5364); }
        .roast-box { background-color: #262730; padding: 20px; border-radius: 10px; border-left: 5px solid #FF4B4B; color: #fff; }
        .gold-mode { border-left: 5px solid #FFD700 !important; box-shadow: 0 0 20px rgba(255,215,0,0.3); }
    </style>
    """, unsafe_allow_html=True)

# --- 游戏逻辑 ---
if not st.session_state['language_selected']:
    st.title("🎅 Santa's Roast Room")
    col1, col2, col3 = st.columns(3)
    with col1: st.button("English 🇬🇧🇺🇸", on_click=set_language, args=("English 🇬🇧🇺🇸",))
    with col2: st.button("简体中文 🇨🇳", on_click=set_language, args=("简体中文 🇨🇳",))
    with col3: st.button("繁體中文 🇹🇼🇭🇰", on_click=set_language, args=("繁體中文 🇹🇼🇭🇰",))
else:
    add_bg()
    ui = LANG_DICT[st.session_state['ui_language']]
    
    # 侧边栏
    with st.sidebar:
        st.title(ui["sidebar_title"])
        api_key = st.text_input("Gemini API Key", type="password")
        st.markdown(ui["game_rule"])
        if st.button("🔄 Change Language"): st.session_state['language_selected'] = False; st.rerun()

    st.title(ui["title"])
    
    # 彩蛋进度条
    found_count = len([x for x in st.session_state['found_ids'] if x in MAIN_EGG_IDS])
    st.write(f"**{ui['hunt_title']}: {found_count} / 12**")
    st.progress(found_count / 12)

    gift_list = st.text_area(ui["input_placeholder"], height=150)
    
    if st.button(ui["button"], type="primary"):
        if not api_key: st.error(ui["error_no_key"])
        elif not gift_list: st.warning(ui["error_no_text"])
        else:
            txt = gift_list.lower()
            new_id = None
            
            # --- 简易匹配逻辑 ---
            if any(w in txt for w in ["tree", "圣诞树", "聖誕樹"]): new_id = 1
            elif any(w in txt for w in ["boyfriend", "girlfriend", "对象", "脫單", "男朋友"]): new_id = 2
            elif any(w in txt for w in ["deer", "麋鹿", "鲁道夫"]): new_id = 3
            elif any(w in txt for w in ["cookie", "food", "饼干", "吃"]): new_id = 4
            elif any(w in txt for w in ["bell", "铃铛", "鈴鐺"]): new_id = 5
            elif any(w in txt for w in ["holiday", "work", "下班", "请假", "放假"]): new_id = 6
            elif any(w in txt for w in ["finland", "芬兰", "芬蘭"]): new_id = 7
            elif any(w in txt for w in ["santa", "圣诞老人", "禮物"]): new_id = 9
            elif any(w in txt for w in ["padoru", "圣诞帽", "帽"]): new_id = 10
            elif any(w in txt for w in ["snow", "下雪", "雪"]): new_id = 11
            elif any(w in txt for w in ["market", "集市", "市集"]): new_id = 12
            elif any(w in txt for w in ["author", "creator", "作者", "开发者"]): new_id = 13
            elif any(w in txt for w in ["洋节", "文化入侵"]): new_id = 8

            # 如果触发了新彩蛋
            if new_id and new_id not in st.session_state['found_ids']:
                st.session_state['found_ids'].add(new_id)
                
                # 提示逻辑 (洋节 8 除外)
                if new_id != 8:
                    remaining = list(MAIN_EGG_IDS - st.session_state['found_ids'])
                    if remaining:
                        next_hint_id = random.choice(remaining)
                        h_lang = "Chinese" if "中文" in st.session_state['ui_language'] else "English 🇬🇧🇺🇸"
                        hint_txt = HINTS[h_lang][next_hint_id]
                        st.info(f"{ui['new_hint_prefix']} {hint_txt}")
                st.balloons()
            
            # 展示对应内容 (此处简化，仅展示文字提示，结构参考原代码)
            if new_id == 1: st.success(ui["secret_success"])
            elif new_id == 2: st.markdown(f"<div class='roast-box gold-mode'>{ui['egg_single']}</div>", unsafe_allow_html=True)
            elif new_id == 6: st.warning("🎫 SLACK OFF PERMIT UNLOCKED!")
            # ... 其他彩蛋展示逻辑同理 ...

            # AI 吐槽
            with st.spinner(ui["loading"]):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"You are a tsundere Santa. Roast this wish list but be secretly kind: {gift_list}. Respond in {st.session_state['ui_language']}."
                    response = model.generate_content(prompt)
                    st.markdown(f"<div class='roast-box'>{response.text}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error("Santa is busy...")

    st.markdown(f"<center style='color:gray; font-size:10px;'>{ui['footer']}</center>", unsafe_allow_html=True)
