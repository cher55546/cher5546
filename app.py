import html
from pathlib import Path
from urllib.parse import quote

import streamlit as st


st.set_page_config(
    page_title="ПСИ-БЛОК",
    page_icon="favicon.jpg",
    layout="wide",
)

# Положи свой логотип в папку с app.py и назови logo.png.
# Можно заменить имя файла, например на "my-logo.jpg".
LOGO_PATH = Path(__file__).resolve().parent / "logo.png"


# ---------------------------------------------------------------------
# Декоративный фон с нейронными связями
# ---------------------------------------------------------------------

NEURON_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="800" viewBox="0 0 1000 800">
  <g fill="none" stroke="#4389B5" stroke-opacity="0.13" stroke-width="2">
    <path d="M25 92 L130 145 L225 80 L340 150 L455 70 L565 145 L690 86 L815 155 L955 82"/>
    <path d="M130 145 L175 290 L300 340 L420 250 L565 145"/>
    <path d="M225 80 L245 20"/>
    <path d="M340 150 L325 235 L420 250 L500 360 L635 325 L760 390"/>
    <path d="M455 70 L485 20"/>
    <path d="M565 145 L635 210 L760 170 L815 155"/>
    <path d="M690 86 L710 25"/>
    <path d="M815 155 L860 275 L955 310"/>
    <path d="M175 290 L100 430 L215 510 L300 430 L300 340"/>
    <path d="M420 250 L380 430 L500 520 L635 450 L635 325"/>
    <path d="M760 390 L840 500 L950 455"/>
    <path d="M100 430 L55 600 L180 700 L310 635 L300 520 L215 510"/>
    <path d="M500 520 L455 660 L570 760 L710 675 L635 560 L635 450"/>
    <path d="M840 500 L815 650 L930 735"/>
    <path d="M310 635 L390 760"/>
  </g>
  <g fill="#4389B5" fill-opacity="0.17" stroke="#FFFFFF" stroke-opacity="0.8" stroke-width="3">
    <circle cx="25" cy="92" r="8"/><circle cx="130" cy="145" r="12"/>
    <circle cx="225" cy="80" r="9"/><circle cx="340" cy="150" r="12"/>
    <circle cx="455" cy="70" r="8"/><circle cx="565" cy="145" r="11"/>
    <circle cx="690" cy="86" r="9"/><circle cx="815" cy="155" r="12"/>
    <circle cx="955" cy="82" r="8"/><circle cx="175" cy="290" r="10"/>
    <circle cx="300" cy="340" r="8"/><circle cx="420" cy="250" r="12"/>
    <circle cx="500" cy="360" r="9"/><circle cx="635" cy="325" r="12"/>
    <circle cx="760" cy="390" r="10"/><circle cx="100" cy="430" r="8"/>
    <circle cx="215" cy="510" r="12"/><circle cx="380" cy="430" r="9"/>
    <circle cx="500" cy="520" r="12"/><circle cx="635" cy="450" r="9"/>
    <circle cx="840" cy="500" r="11"/><circle cx="180" cy="700" r="9"/>
    <circle cx="310" cy="635" r="11"/><circle cx="570" cy="760" r="8"/>
    <circle cx="710" cy="675" r="12"/><circle cx="930" cy="735" r="9"/>
  </g>
</svg>
"""

neuron_background = quote(NEURON_SVG, safe="")


# ---------------------------------------------------------------------
# Каталог техник
# ---------------------------------------------------------------------

TECHNIQUES = {
    "decision_tree": {
        "title": "Дерево решений",
        "short": "Разложить сложный выбор на варианты и возможные последствия.",
        "description": "Сравнение вариантов, исходов, вероятностей и оценок.",
        "keywords": "выбор решение последствия вероятность варианты мышление",
        "category": "Мышление",
    },
    "dbt_chain": {
        "title": "Цепочный анализ поведения (ДБТ)",
        "short": "Исследовать последовательность событий, реакций и последствий.",
        "description": "КПонял: логотип нужно добавлять **варта контекста, звеньев цепочки и возможных точек вмешательства.",
        " проект как файл**, без загрузчика на сайтеkeywords": "эмоции поведение дбт реакция событие цепочка",
        "category": "Эмоции",
    },
    "exposure": {
        "title": ". Ниже — полный `app.py` с этим вариантом, фоном в стиле нейронных связей, поиском, который обновляется при вводе и сбрасывается при очистИерархия экспозиции",
        "short": "Составить лестницу ситуаций для постепенной практики.",
        "description": "Ситуации, прогнозы, посильные шаги и наблюке поля, и рабочей кнопкой «Назад» в шапке.

Чтобы поставить свой логотип, положи изображение рядом с `app.py`дения.",
        "keywords": "тревога тревожность страх экспозиция ситуации практика",
        "category": под именем `logo.png`. Если у тебя другое имя или расширение, поменяй "Тревожность",
    },
    "act_matrix": {
        "title": "ACT-матрица",
        "short": "Исследовать действия значение `LOGO_PATH` в начале файла. Эмодзи и декоративные кнопки, которые ничего не делают, «от дискомфорта» и шаги «к ценностям».",
        "description": "Карта внутреннего опыта, поведения и выбранных действий.",
        "keywords": " не используются.

```python name=app.py
import html
ценности дискомфорт действия мысли осознанность act",
        "category": "Самоосознание",
    },
}


# ---------------------------------------------------------------------
# Состояние приложения и навигация
# ---------------------------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_technique" not in st.session_state:
    st.session_state.selected_technique = None

if "page_history" not in st.session_state:
    st.session_state.page_historyimport uuid
from pathlib import Path

import streamlit as st


# ---------------------------------------------------------------------
# Настройки страницы и локальные изображения
# ---------------------------------------------------------------------

APP_DIR = Path(__file__).resolve().parent

# Положи файл логотипа рядом с app.py.
# Если файл называется иначе, измени путь, например:
# LOGO_PATH = APP_DIR / "my = []


def clear_searches():
    """Сбрасы-logo.svg"
LOGO_PATH = APP_DIR / "logo.png"

st.set_pageвает текущие поисковые запросы и их результаты."""
    for key in ("home_search", "_config(
    page_title="ПСИ-БЛОК",
    page_icon="favicon.jpg",
    layout="wide",
)


# ---------------------------------------------------------------------
# Фон: нейронные связи
# ----------------------------------------------------------------library_search"):
        if key in st.session_state:
            st.session_state[key] = ""


def navigate(page, technique_id=None):
    current = {
        "page": st.session_state.page,
        "-----

NEURON_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="800" viewBox="0 0 technique": st.session_state.selected_technique,
    }
    target = {"1000 800">
  <g fill="none" strokepage": page, "technique": technique_id}

    if current != target:
        st.session_state.page_history.append(current)
       ="#4389B5" stroke-opacity="0.13" stroke-width st.session_state.page_history = st.session_state.page_history[-30:]

    st.session_state.page =="2">
    <path d="M25 92 L130 145 L225 80 L340 150 L455 70 L565 145 L690 page
    st.session_state.selected_technique = technique_id


def go_home():
    clear_searches()
    navigate("home 86 L815 155 L955 82"/>
    <path")


def go_library():
    clear_searches()
    navigate("library d="M130 145 L175 290 L300 340")


def go_about():
    clear_searches()
    navigate("about")


def L420 250 L565 145"/>
    <path d="M225 80 L go_back():
    clear_searches()

    if st245 20"/>
    <path d="M340.session_state.page_history:
        previous = 150 L325 235 L420 250 L500 360 L635 325 L760 390"/>
    <path d="M455 70 st.session_state.page_history.pop()
        st.session_state.page = previous["page"]
        st.session_state.selected_technique = previous["technique"]
    else:
        st L485 20"/>
    <path d="M565 .session_state.page = "home"
        st.session_state.selected_145 L635 210 L760 170 L815technique = None


def open_technique(technique_id 155"/>
    <path d="M690 86 L710 25"/>
    <):
    navigate("technique", technique_id)


def search_techniques(query):
    """path d="M815 155 L860 275 L955 310"/>
    <path d="M175 290 L100 430Ищет технику по словам в названии, L215 510 L300 430 L300 340"/>
    <path d="M420 250 L380 430 L500 520 L635 450 L635 325"/>
    <path d="M760 390 L840 500 L950 455"/>
    <path d="M100 430 L55 описании, теме и ключевых словах."""
    words = " ".join((query or "").casefold().split()).split()

    if not words:
        return list(TECHNIQUES.items())

    results = []

    for technique_id, technique in TECHNIQUES.items():
        searchable_text = " ".join(
            (
                technique["title"],
                technique["short"],
                600 L180 700 L310 635 L300 520 L215 510"/>
    < techniquepath d="["description"],
M500 520                technique["keywords L455"],
                technique 660 L570 760 L710 675 L635 560 L635 450"/>
    <path d="M840 500 L815 650 L930 735"/>
    <path d="M310 635 L390 760"/>
  </g>
  <g fill="#4389B5" fill-opacity["category"],
            )
        ).casefold()

        if all(word in searchable_text for word in words):
            results.append((technique_id, technique))

    return results


# ---------------------------------------------------------------------
# Стили
# ---------------------------------------------------------------------

st.markdown(
    f"""
    <style>
    @import url('https://fonts="0.17" stroke="#FFFFFF" stroke-opacity="0.8" stroke-width=".googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;7003">
    <circle cx;800&display=="25" cy="92" r="8"/><circle cx="130" cy="145" r="12"/>
    <circle cx="225swap');

    :root {{
        color-scheme: light !important;
    }}

    html, body, [data-testid="stAppViewContainer"] {{
        color-scheme" cy="80" r="9"/><circle cx="340" cy="150" r="12"/>
    <circle cx="455" cy="70" r="8"/><circle cx="565" cy="145" r="11"/>
: light !important;
        background-color: #F3F9FD !important;
        color: #294A65 !important;
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }}

    <circle cx="690" cy="86" r="9"/><circle cx="815" cy="    [data-testid="stAppViewContainer"] {{
        background-image:
            radial-gradient(155" r="12"/>
    <circle cx="955" cy="82" r="8"/><circle cx="ellipse at 10% 5%, rgba(196,228,248,.58), transparent 34%),
            radial-gradient(ellipse at 92% 18%, rgba(219,239,251,.68175" cy="290" r="10"/>
    <circle cx="300"), transparent 36%);
    }}

    [data-testid="stAppViewContainer"]::before {{
 cy="340" r="8"/><circle cx="420" cy="250" r="12        content: "";
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer"/>
    <circle cx="500" cy="360" r="9"/><circle cx="635" cy="325" r="12"/>
    <circle cx="760" cy-events: none;
        opacity: .56;
        background-image: url("data:image/svg+xml,{neuron_background}");
        background-repeat: repeat;
        background-size: ="390" r="10"/><circle cx="100" cy="430" r="8"/>
    <circle cx="215" cy="510" r="12"/><circle cx="3801000px 800px;
        background-position: left top;
    }}

    [data-testid="stAppViewContainer"] > .main {{
        position: relative;
        z-index: 1;
    }}

    [data-testid="stHeader"] {{
        background: transparent !important;
    }}

    .block-container {{
        max-width: 1160px;
        padding-top: 1.1rem;
        padding-bottom: 4rem;
    }}

    h1, h" cy="430" r="9"/>
    <circle cx="500" cy="520" r="12"/><circle cx="635" cy="450" r="9"/>
    <circle cx="840" cy="500" r="11"/><circle cx="180" cy="700" r="9"/>
    <circle cx="310" cy="635" r="11"/2, h3, h4, p, label, button, input, textarea><circle cx="570" cy="760" r="8"/>
    <, select {{
        font-family: "Nunito Sans", "Segoe UI", sans-serif !circle cx="710" cy="675" r="12"/><circle cx="930" cy="important;
    }}

    h1, h2, h3, h4 {{
        color735" r="9"/>
  </g>
</svg>
"""


# ---------------------------------------------------------------------
#: #294A65 !important;
        letter-spacing: -0.025em;
    }}

    Каталог техник
# ---------------------------------------------------------------------

TECHNIQUES = {
    "decision_tree": {
        "title": " h1 {{ font-size: 2.5rem !important; font-weight: 800 !important;Дерево решений",
        "short": "Разложить сложный выбор на варианты и возмож }}
    h2 {{ font-size: 1.8rem !important; font-weight: 800 !important; }}
   ные последствия.",
        "description": "Сравнение вариантов, исходов, вероятностей и оценок h3 {{ font-size: 1.25rem !important; font-weight: .",
        "keywords": "выбор решение последствия вероятность варианты",
        "category": "Мышление",
    },
    "800 !important; }}

    p, label, [data-testid="stCaptionContainer"],
    [data-testid="stMarkdownContainer"] {{
        color: #476dbt_chain": {
        "title": "Цепочный анализ поведения (ДБТ)",
        "short": "Исследовать последовательностьB85 !important;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        border: 1px solid #C событий, реакций и последствий.",
        "description": "Карта контекста, звеньев цепочки и возможных точек вмешательства.",
        "keywords": "эмоции поведение дбт реакция событие цепочка",
        "9DFEF !important;
        border-radius: 18px !important;
        background: rgba(248,category": "Эмоции",
    },
    "exposure": {
        "title": "И252,255,.94) !important;
        box-shadow: 0 8px 22px rgba(62,112,148,.06);
    }}

    [data-testid="stTextInput"] [data-baseweb="input"],
    [dataерархия экспозиции",
        "short": "Составить лестницу ситуаций для постепенной практики.",
        "description": "Ситуации, прогнозы, пос-testid="stTextArea"] [data-baseweb="textareaильные шаги и наблюдения.",
        "keywords": "тревога тревожность страх экспозиция ситуации"],
    [data-testid="stNumberInput"] [data-baseweb="input"],
    [data-testid="stSelectИзвини — в предыдущbox"] [data-baseweb="select"] > div,
    [data-baseweb="input"],
    [ практика",
        "category": "Тревожность",
    },
    "act_matrix": {
        "title": "ей версии я добавил загрузчик изображения прямо на сайт, хотя тебе нужно вставлять логотип в проект самостоятельно, и спрятdata-baseweb="textarea"] {{
        color-schemeACT-матрица",
        "short": "Исал кнопку «Назад». Ниже полный `app.py` безследовать действия «от дискомфорта» и шаги «к ценностям».",
: light !important;
        background: #FFFFFF !important;
        border: 1px solid #C9DDEB !important;
        border-radius: 12px !important;
        box        "description": "Визуальная карта внутреннего опыта, поведения и выбранных действий.",
        "keywords": загрузчика: положи свой файл логотипа рядом с `app.py` и наз-shadow: none !important;
    }}

    [data-testid="stTextInput"] input,
    [dataови его `logo.png`. Если у файла другое имя, измени `LOGO_PATH` в "ценности дискомфорт действия мысли осознанность act",
        "category": "Самоосознание",
    },
}


# ---------------------------------------------------------------------
# Состояние приложения и начале кода. Кнопка «Назад» есть в-testid="stTextArea"] textarea,
    [data-testid="stNumberInput"] input,
    навигация
# ---------------------------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_technique" not in st.session_state:
    st.session_state.selected_technique = None

if "page_history" not in st.session_state:
    st.session_state.page_history = []

if "home_search" not in st.session_state:
    st.session_state.home_search = ""

if "library_search" not in st.session_state:
    st.session_state.library_search = ""


def clear_searches верхней навигации. Поиск обновляет результаты при вводе и возвращает главную страницу, когда поле очищено.

```python name=app.py
from pathlib import Path
import html
import uuid

import streamlit as st


# ---------------------------------------------------------------------
# Настройки страницы и логотип
# ---------------------------------------------------------------------

st.set_page_config(
    page_title="ПСИ-БЛОК",
    page_icon="favicon.jpg",
    layout="wide",
)

# Вставь свой [data-testid="stSelectbox"] input,
    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea {{
        color: #294A65 !important;
        background: #FFFFFF !important;
        -webkit-text-fill-color: #294A65 !important;
        border: 0 !important;
        box-shadow: none !important;
        outline: none !important;
        caret-color: #315773 !important;
    }}

    input::placeholder,
    textarea::placeholder {{
        color: #7893A8 !important;
        -webkit-text-fill-color: #7893A8 !important():
    """Сбрасывает запросы, например при переходе на другую страницу."""
 файл логотипа в репозиторий рядом с app.py.
# Например: logo.png, logo.jpg или logo.webp.
    st.session_state.home_search = ""
    st.session_state.library_search = ""


;
        opacity: 1 !important;
    }}

    .stButton > button {{
       # Если используешь другое имя, измени эту строку.
def navigate(page, technique_id=None):
    current = {
        " min-height: 44px;
        border: 1px solid #AFCFE2 !LOGO_PATH = Path(__file__).resolve().parent / "logo.png"


# ---------------------------------------------------------------------
# Декоративные иллюстрации
# SVG вimportant;
        border-radius: 13px !important;
        background: #page": st.session_state.page,
        "selected_technique": st.sessionF1F8FD !important;
        color: #315773 !important;
        font-size: .98rem главном блоке подключён как фоновое изображение,
# поэтому его_state.selected_technique,
    }
    target = {
        "page": page,
        "selected_technique": technique_id,
    }

    if current != target:
        st.session_state исходный код не отображается на странице.
# ---------------------------------------------------------------------

NE;
        font-weight: 700;
        transition: .18s ease;
URON_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width=".page_history.append(current)
        st.session_state.page_history = st.session_state.page_history[-30:]

    }}

    .stButton > button:hover:not(:disabled) {{
        border-color: #1000" height="800" viewBox="0 0 1000 800">
  <g fill="none"6EA7CB !important;
        background: #E0F0FA !important;
        color: #234    st.session_state.page = page
    st.session_state.selected_technique = technique_id


def goD6B !important;
        transform: translateY(-1_back():
    if st.session_state.page_history:
        previous = st stroke="#4389B5" stroke-opacity="0.13" stroke-widthpx);
    }}

    .stButton > button:disabled {{
        opacity: .45;
    }}

   ="2">
    <path d="M25 92 L130 145 L225 80 L340 150 L.session_state.page_history.pop()
        st.session_state.page = previous["page"]
        st.session_state.selected_technique = previous["selected_technique"]
    else:
        st.session_state.page = " .stButton > button[kind="primary"] {{
        min-height: 455 70 L565 145 L690 86 L815 155 L955 8250px;
        border: 1px solid #6EA7CB !important;
        border-radius: 14"/>
    <path d="M130 145 L175 290 L300 340 L420 250 L565 home"
        st.session_state.selected_technique = None

    clear_searches()


def go_home():
   px !important;
        background: linear-gradient(135deg, #D9 clear_searches()
    navigate("home")


def go_library():
   145"/>
    <path d="M225 80 L245 20"/>
    <pathEEFA, #E5F3FC) !important;
        color: #234D6B d="M340 150 L325 235 L420 250 L500 360 L635 325 L760 390"/>
    clear_searches()
    navigate("library")


def go_about():
    clear_searches()
    <path d="M455 70 L485 20"/>
    <path d=" !important;
        font-weight: 800;
    }}

    [ navigate("about")


def open_technique(technique_id):
    navigate("techniquedata-testid="stAlert"] {{
        border: 1px solid #BCD9EB !important;
        borderM565 145 L635 210 L760 170 L815 155"/>
    <path d="", technique_id)


# ---------------------------------------------------------------------
# Поиск
# ---------------------------------------------------------------------

def search_M690 86 L710 25"/>
    <path d="M815 155 L860 275 L955-radius: 14px !important;
        background: #EAF5FC !important;
techniques(query):
    """Поиск по названию, описанию, категории и 310"/>
    <path d="M175 290 L100 430 L215    }}

    [data-testid="stMetric"] {{
        border: 1px ключевым словам."""
    query = " ".join((query or "").casefold().split())

    if not query:
        return list(TECHNIQUES.items())

    words = query.split 510 L300 430 L300 340"/>
    <path d="M420 250 L380 430 L solid #C9DFEF;
        border-radius: 16px;
        background: rgba(248()
    results = []

    for technique_id, technique in TECHNIQUES.items():
,252,255,.96);
        padding: 14px500 520 L635 450 L635 325"/>
    <path d="M760;
    }}

    hr {{
        border-color: #D7E6F0 !important;
    }}

    . 390 L840 500 L950 455"/>
    <path d="M100 430 L55 600        searchable_text = " ".join(
            [
                technique["title"],
                technique[" L180 700 L310 635 L300 520 L215 510"/>
    <path d="M500 520 L455 660 L570 760 L710 675 L635 560 L635 450"/>
    <path d="M840 500 L815 650 L930 735"/>
    <path d="M310 635 L390 760"/>
  </g>
  <short"],
                technique["description"],
                technique["keywords"],
                technique["category"],
            ]
        ).casefold()

        if all(word in searchable_text for word in words):
            results.append((technique_id, technique))

    return results


# ---------------------------------------------------------------------
# Стили
# ---------------------------------------------------------------------

st.markdownsite-header {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 7px 0 16px;
        margin-bottom: 12px;
        border-bottom: 1px solid #D7E6F0;
    }}

    .brandg fill="#4389B5" fill-opacity="0.17" stroke="#FFFFFF" stroke-opacity="0.8" stroke-width="3">
   -name {{
        color: #234D6B;
        font-size: clamp(1.7rem, 3vw, 2.(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght25rem);
        font-weight: 800;
        line-height:  <circle cx="25" cy="92" r="8"/><circle cx@400;500;600;700;800&display=swap');

    :root="130" cy="145" r="12"/>
    <circle cx="225" cy="80" r="9"/><1.05;
        letter-spacing: -.045em;
        white {{
        color-scheme: light !important;
    }}

    html, body, [data-testid="stAppView-space: nowrap;
    }}

    .brand-fallback {{
       Container"] {{
        color-scheme: light !important;
       circle cx="340" cy="150" r="12"/>
    < background-color: #F3F9 width: 42px;
        heightcircle cx="455" cy="70" r="8"/><circle cx="565" cy="145" r="FD !important;
        color: #294A65 !important;
        font: 42px;
        display: flex;
        align-items: center;
-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background-image:
            radial-gradient(ellipse at 10% 5%, rgba(        justify-content: center;
        border: 1px solid #BBD9EB;
        border-radius: 12px;
        background: rgba(255,255,255,.65);
    }}

    .11"/>
    <circle cx="690" cy="86" r="9"/><circle cx="815" cy="155" r="12"/>
    <circle cx="955" cy="82" r="8"/><circle cx="175" cy="290" r="10"/>
    <circle cx="300" cy="340" r="8"/><196,228,248,.52), transparent 34%),
            radialhero {{
        position: relative;
        display: flex;
        align-items: center-gradient(ellipse at 92% 18%, rgba(219,239,251,.62), transparent 36%);
;
        min-height: 340px;
        overflow: hidden;
        padding: 38px 44pxcircle cx="420" cy="250" r="12"/>
    <circle cx="500" cy="360" r="9"/;
        margin: 20px 0 22px;
        border: 1    }}

    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed><circle cx="635" cy="325" r="12"/>
    <circle cx="760" cypx solid #D3E5F2;
        border-radius: 28;
        inset: 0;
        z-index: 0;
        pointer="390" r="10"/><circle cx="100" cy="430"-events: none;
        opacity: .58;
        background-image: url("data:image/svg+xml,{ r="8"/>
    <circle cx="215" cy="510" r="12"/><circle cx="380px;
        background:
            radial-gradient(circle at 79% 42%, rgba" cy="430" r="9"/>
    <circle cx="500" cy="520" r="12"/><(174,222,241,.66) 0 18%, transparent 18.5%),
            linear-gradientNEURON_SVG.replace('#', '%23').replace(' ', '%(110deg, #F8FCFF circle cx="635" cy="450" r="920').replace('\\n', '')"/>
    <circle cx="840" cy="500" r="11"/><circle cx="180" cy="700" r="9"/>
    <circle cx="310" cy="635" r="11"/><circle cx="570" cy="760" r="8"/>
    <circle cx="710" cy="675" r="12"/><circle cx="930" cy="735" r="9"/>
  </g>
</svg>
"""

HERO_SVG}");
        background-repeat: repeat;
        background-size: 1000px 800px;
        background-position: left top;
    }}

    [data-testid="stAppViewContainer"] > .main {{
        position: relative;
        z-index: 1;
    }}

    [data-testid="stHeader"] {{
        background: transparent !important;
    }}

    .block-container {{
        max-width: 1180px;
        padding-top: 1rem;
        padding-bottom: 4rem0%, #EAF5FC 100%);
    }}

    .hero-copy {{
        position: relative;
        z-index: 1;
        max-width: 530px;
    }}

    .hero-title {{
        margin: 0;
        color: #214D6C;
        font-size: clamp(2.8rem, 6vw, 4.3rem);
        font-weight: 800;
        line-height: 1.04;
        letter-spacing: = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0  -.05em;
    }}

    .hero-subtitle {{
        max-width: 490px;
       ;
    }}

    h1, h2, h3, h4, p, label, button, input, margin: 12px 0 18px;
        color: #294A65;
        font-size:440 330">
  <path d="M223 25
    C165 11  textarea, select {{
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }}

    h1, h2, h3, h4 {{
        color: #294A65 ! clamp(1.25rem, 2.5vw, 1.85rem);
        font-weight: 111 47 97 99
    C87 136 101 165 80 192
    C66 209 48 218 51 229
    C54700;
        line-height: 1.3;
    }}

    .hero-description {{
        max-width: important;
        letter-spacing: -0.025em;
    }}

    h1 {{ font-size: 2.5rem !important; font-weight: 800 !important; }}
    h2 {{ font-size: 1.8rem ! 239 72 242 82 247
    C90 251 84 460px;
        color: #476B85;
        font-size: 1.05rem;
       important; font-weight: 800 !important line-height: 1.6;
    }}

    .263 95 270
hero-art {{
        position: absolute;
        top: 50%;
        right:    C105 277 119 270 126 283
    C134; }}
    h3 {{ font-size: 1.25rem !important; 3%;
        font-weight:  296 155800 !important  width: min(42%, 430px);
        transform: translateY(-50%);
        opacity: .78;
    }}

    .section-title {{
        margin: 28; }}

    p, label, [data-testid="stCaptionContainer"],
    [data-testid="stMarkdownContainer"] {{
        color: #476B85 !important297 178 289
    L224 278"
    fill="none" stroke="#5B87A2" stroke-width="3"
    stroke-linecappx 0 12px;
        color: #294A65;
        font-size: 1.7;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        border: 1px solid #="round" stroke-linejoin="round"/>
  <path d="M224 27
    C284 19 338 52 351 103
    CC9DFEF !important;
        border-radius: 18pxrem;
        font-weight: 800;
    }}

    .category-card {{
362 143 345 172 371 201
    C387 219  !important;
        background: rgba(248,252,255,.94) !important;
               min-height: 125px;
        padding: 17px;
        border:  box-shadow: 0 81px solid #D3E408 224 408 3EF;
        border-radius: 18px;
        background: rgba(px 24px rgba(62,112,148,.07236
    C408 247 389 254 248,252,255,.94);
    }}

    .category-title {{
        color: #294A65;
        font-size: 1.380 265
    C370 278 358 290 339 289
    L225);
    }}

    [data-testid="stTextInput"] [data-baseweb="input"],
    [data-testid="stTextArea"] [data-baseweb="textarea"],
    [data-testid="stNumberInput"] [data-baseweb="input"],
    [data-testid 278"
    fill="none" stroke="#5B87A2" stroke-width="3"
    stroke-linecap="round04rem;
        font-weight: 800;
    }}

    .category-description {{
        margin-top: 7px;
        color: #648198;
        font-size: .9rem;
        line="stSelectbox"] [data-baseweb="select"] > div,
    [" stroke-linejoin="round"/>
  <path d="M222 63
    C201 45 172 54 166-height: 1.45;
    }}

    @media (max-width: 700data-baseweb="input"],
    [data-baseweb="textarea"] {{
        color-scheme: light !important;
        background: #FFFFFF !important;
        border: px) {{
        .hero {{
            min-height: 290px;
            padding 75
    C140 77 135 106 155 : 25px 22px;
        }}

        .hero-art {{
            right:1px solid #C9DDEB !important;
        border-radius: 12px120
    C142 141 159 158 181 154 -10%;
            width: 58%;
            opacity: .2;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# Шапка сайта
# ---------------------------------------------------------------------

def render_header():
    brand_col, home_col, library_col, about_col, back_col = st.columns(
        [2.4,
    C188 176 211 178 224 160
    C240 178 264 171 270 150
    C293 149 301 124 285 108
    C296 86 280 65 258 68
    C250 !important;
        box-shadow: none !important;
    }}

    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] input,
    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea {{
        color: 1, 1.25, 1.2, 1]
    )

    with brand_col:
        st 51 235 51 222 63Z"
    fill="none" stroke="#5B87A #294A65 !important;
        background: #FFFFFF !important;
        -webkit-text-fill-color: #294A2" stroke-width="2.5"
    stroke-linecap="round" stroke-linejoin="round"/>
 65 !important;
        border: 0 !important;
        box-shadow: none !important;
       .markdown('<div class="site-header">', unsafe_allow_html=True)

        if LOGO_PATH.is_file():
            st.image(str(LOGO_PATH), width=42)
        else:
            <path d="M223 63 L223 160
    M166 76 C outline: none !important;
        caret-color: #315773 !important;
    }}

    input::placeholder,
    textarea::placeholder {{
        color: #7893185 84 190 101 181 117
    M258  st.markdown(
                """
                <div class="brand-fallbackA8 !important;
        -webkit-text-fill-color: #7893A8 !68 C242 82 242 98 254 111
    M" aria-label="Логотип ПСИ-БЛОК">
                    <important;
        opacity: 1 !important;
    }}

    [data-baseweb="select"] span,
    [155 120 C174 117 187 130 181 154
    M285 108 C263svg width="30" height="30" viewBox="0 0  111 252 129 270 150
    M190 78 Cdata-baseweb="menu"] li {{
        color: #294A65 !30 30"
                         xmlns="http://www.w3.org/2000/svgimportant;
    }}

    [data-baseweb="popover"],
    [data-baseweb="menu"] {{
        color-s205 89 207 104 197 119
    M240 80 C225 91 ">
                      <g fill="none" stroke="#315773" stroke-width="1.5"
225 107 239 119
    M201 140 C212 131                          stroke-linecap="round">
                        <path d="cheme: light !important;
        background: #FFFFFF !important;
    }}

M14.8 5.    .stButton > button {{
        min-height: 44226 132 235 143"
    fill="none" stroke="#5px;
        border: 1px solid #AFCFE2 !important;
        border-radiusB87A2" stroke-width="2"
    stroke-linecap="round"/>
  <ellipse2c-4-3- cx="225" cy="157" rx="190" ry="76"
    transform="rotate(-12 8 0-7.5 4-3: 13px !important;
        background: rgba(245,250,254.8 1.3-3.4 6.1-.3225 157)"
    fill="none" stroke="#76A6C0" stroke-width="2"/>
</,.94) !important;
        color: #315773 !important;
        font-size: .96rem;
        font-weight: 700;
        transition: .18s 7.4-2.2 svg>
"""


# ---------------------------------------------------------------------
# Каталог техник
# ---------------------------------------------------------------------

TECHNIQUES = {
 ease;
    }}

    .stButton > button:hover:not(:disabled) {{
    "decision_tree": {
        "title": "Дерево решений",
        "3.2.3 6.5 3.7 short": "Разложить сложный выбор на варианты и возможные последствия.",
        "description": "Сравнение вариантов, исход5.1 1.3 3 4.5 2.6 5.        border-color: #6EA7CB !important;
        background: #E0F0FA !important;
        color: #234D6B !important;
        transform: translateYов, вероятностей и оценок.",
        "category": "Мышление",
        "3.2"/>
                        <(-1px);
    }}

    .stButton > button:keywords": "выбор решение последствия вероятность варианты",
    },
    "dbpath d="M15.2 5.2c4-3t_chain": {
        "title": "Цепочный анализ поведения (ДБТ)",
        "short": "Ис 8 0 7.5 4 3.8 1.3 3.4 6.disabled {{
        opacity: .45;
    }}

    .stButton > button[kind="primaryследовать последовательность событий, реакций и последствий.",
        "description": "Карта контекста,"] {{
        min-height: 48px;
        border: 1px solid #6EA7CB1.3 7.4 2.2 3.2-.3 6.5-3.7 5.1-1.3  !important;
        border-radius: 14px !important;
        background: # звеньев цепочки и возможных точек вмешательства.",
        "category": "ЭDCEFF9 !important;
        color: #234моции",
        "keywords": "эмоции поведение дбт реакция3-4.5 2.6-5.3.2"/>
                        <D6B !important;
        font-weight: 800;
    }}

    [data-testid="stForm"] {{
        border: 0 !important;
        padding: 0 !important;
        background: transparent !important;
    }}

    [data-testid="stAlert"] {{
        border: 1px solid #BCD9EB !important;
        событие цепочка",
    },
    "exposure": {
        "title": "Иерархия экспозиции",
        "short": "Составить лестницу ситуаций для постепенной практики.",
        "description": "Ситуации, прогнозы, посильные шаги и наблюдения.",
        "category": "Тревожность",
        "keywords": "тревpath d="M15 5v17M9 10c2 0 3 1 3 3m-5 3c2-.5 4 .5 4 2m10-8c-2 0-3 1-3 3m5 3c-2-.5-4 . border-radius: 14px !important;
        background: #EAF5FC !important;
        color: #315773 !important;
    }}

    [ога тревожность страх экспозиция ситуации практика",
    },
    "act_matrix": {
        "title": "ACT-матрица",
        "short": "Исслед5-4 2"/>
                      </g>
                    </svg>
                </овать действия «от дискомфорта» и шаги «к ценностям».",
data-testid="stAlert"] * {{
        color: #315773 !importantdiv>
                """,
                unsafe_allow_html=True,
            )

        st        "description": "Карта внутреннего опыта, поведения и выбранных действий.",
       ;
    }}

    [data-testid="stMetric"] {{
        border: 1px solid #C9DFEF;
        border-radius: 16px;
        background: rgba "category": "Самоосознание",
        "keywords": "ценности дискомфорт действия мысли.markdown(
            '<div class="brand-name">ПСИ-БЛОК</div></ осознанность act",
    },
}


# ---------------------------------------------------------------------
# Состояние приложения и(248,252,255,.96);
        padding: 14px;
    }}

    hr {{
        borderdiv>',
            unsafe_allow_html=True,
        )

    with home-color: #D7E6F0 !important;
    }}

    . переходы
# ---------------------------------------------------------------------

if "page" not in st.session_state:
    st.session_state_col:
        st.button(
            "Главная",
            key="nav_homeheader-brand {{
        display: flex;
        align-items: center;
        gap:",
            on_click=go_home,
            use_container_width=True,
        )

    with library_col.page = "home"

if "selected_technique" not in st.session_state:
    st 11px;
        min-height: 48px;
        color: #234D.session_state.selected_technique = None

if "page_history" not in st.session_state:
    st.session_state:
        st.button(
            "Библиотека",
            key="nav_library",
            on_click=go_library,
            use_container_width=True,
        )

    with about_col:
6B;
        font-size: clamp(1.5rem, 2.7vw.page_history = []


def reset_search_fields():
    """Очищает поис, 2.1rem);
        font-weight: 800;
        line-height: 1;
               st.button(
            "О проекте",
            key="nav_about",
            on_click=goковые поля при переходе между разделами."""
    for key in ("home_search", " letter-spacing: -.045em;
        white-space: nowrap;
   _about,
            use_container_width=True,
        )

    with back_col:
        st.buttonlibrary_search"):
        if key in st.session_state:
            st.session_state[key] = ""


(
            "← Назад",
            key="nav_back",
            on_click=go_back,
            disabled }}

    .header-logo-placeholder {{
        width: 38px;
        height: 38def navigate(page, technique_id=None):
    current = {
        "page": st.session_state.page,
        "selected_technique": st.session_state.selected_technique,
    }
    target = {
        "=not st.session_state.page_history,
            use_container_width=True,
        )


#px;
        display: flex;
        align-items: center;
        justify-content:page": page,
        "selected_technique": technique_id,
    }

    if current != center;
        flex: 0 0 38px;
        border ---------------------------------------------------------------------
# Карточки техник
# ---------------------------------------------------------------------

def render_technique_cards(items, key_prefix):
    if not items:
        st.info("Ничего не найдено. Попроб: 1px solid #BDD8E9;
        border-radius: 50%;
        color: # target:
        st.session_state.page_history.append(current)
        st.session_state.page_history = st.session_state.page_history[-30:]

    st.session_state.page = page
    st.session_state.selected_tech315773;
        background: rgba(255,255,255,.35);
уйте изменить поисковый запрос.")
        return

    for start in range(0,nique = technique_id


def go_home():
    reset_search_fields()
    navigate("home")


def go_library():
    reset_search len(items), 2):
        columns = st.columns(2)

        for column, (technique    }}

    .header-logo-placeholder svg {{
        width: 25px;
        height: _fields()
    navigate("library")


def go_about():
    reset_search_fields()
    navigate("about")


def open_25px;
    }}

    .hero {{
        position: relative;
        display: flex_id, technique) in zip(
            columns,
            items[start:start + 2],
        ):
            with column:
;
        align-items: center;
        min-height: 340px;
        overflow:technique(technique_id):
    navigate("technique", technique_id)


def                with st.container(border=True):
                    st.markdown(f"### {technique hidden;
        padding: 38px 44px;
        margin: 18px 0 ['title']}")
                    st.write(technique["short"])
                    st.caption(
                        f"{ go_back():
    if st.session_state.page_history:
        previous = st.session_state.page_history.pop()
        st.session_state.page = previous["page"]
        st.session_state.selected_technique = previous["selected_technique"]
    else:
        st.session_state.page = "home"
        st.session_state.selected_technique22px;
        border: 1px solid #D3E5F2;
        border-radius: 28px;
        background:
            radial-gradient(circle at 79% 43technique['category']} · {technique['description']}"
                    )
                    st.button(
                        "Открыть →",
                        key=f"{key_prefix}_{technique_id}",
                        on_click%, rgba(178,222,241,.76) 0 18%, transparent 18.5%),
            linear-gradient(110deg, #F8FCFF 0%, #EAF5FC 100%);
    }}

    .hero-copy {{
        position: relative;
        z-index: 1;
        max-width: 520px;
    }}

    .hero=open_technique,
                        args=(technique_id,),
                        use_container_width=True,
                    )


# ---------------------------------------------------------------------
# Главная
# ---------------------------------------------------------------------

def render_home():
    st.markdown(
        """
        <section class="hero">
          <div class="hero-copy">
            <h1 class="hero-title">ПСИ-БЛОК</h1>
            = None


def search_techniques(query):
    """Ищет по названию, описанию, категории и ключевым словам."""
    query = " ".join((query or "").casefold().split())
    if not query:
        return list(TECHNIQUES.items())

    words = query.split()
    matches = []

    for technique_id, technique in TECHNIQUES.items():
        searchable = " ".join(
            (
-title {{
        margin: 0;
        color: #214D6C;
        font-size: <div class="hero-subtitle">
              Инструменты для глубокой психологической работы
                technique["title"],
                technique["short"],
                technique["description"],
                technique["category"],
                           </div>
            <div class="hero-description">
              technique["keywords"],
            )
        ).casefold()

        if all(word in searchable for clamp(2.8rem, 6vw, 4.5rem Библиотека проверенных психологических техник
              для специалистов и клиентов.
            </div>
          </div>

 word in words):
            matches.append((technique_id, technique))

    return matches


# ---------------------------------------------------------------------
#);
        font-weight: 800;
        line-height: 1.05;
        letter-spacing: Стили
# ---------------------------------------------------------------------

st.markdown(
    f"""
    <style>
    @import url('https://fonts -.045em;
    }}

    .hero-subtitle {{
        max-width: 490px;
        margin          <div class="hero-art" aria-hidden="true">
            <svg viewBox="0 0 440 300" xmlns="http://www.w3.org/2000/svg">
              <path.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700: 12px 0 16px;
        color: #294A65;
;800&display=swap');

    :root {{
        color-scheme: light !important;
    }}

 d="M225 18 C155 8 100 48 89 108 C81 151 99        font-size: clamp(1.25rem, 2.5vw, 1.9rem);
           html, body, [data-testid="stAppViewContainer"] {{
        color-scheme: font-weight: 700;
        line-height: 1.3;
    }}

    . 180 72 204
                       C61 214 48 225 51 234 C55 244 73 246 82 250
                       C89 254 hero-description {{
        max-width: 470px;
        color: #476B85;
        font light !important;
        background-color: #F3F9FD !important;
        color: #294A65 !important;
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }}

    [data85 265 94 269 C105 275 119 269 126 282
                       C132 -size: 1.05rem;
        line-height: 1.6;
    }}

    .hero-art {{
        position: absolute;
        top: 50%;
        right: 3%;
        width: min294 154 296 176 289 L225 278"
                    fill="none"-testid="stAppViewContainer"] {{
        background-image:
            radial-gradient(ellipse at 10 stroke="#5B87A2" stroke-width="3"
                    stroke-linecap="round" stroke-linejoin="round(43%, 450px);
        transform: translateY(-50%);
        opacity: .83;
    }}

% 5%, rgba(196,228,248,.48), transparent 34%),
            radial-gradient(ellipse at 92% 18%, rgba(219,239,251,.58), transparent 36%);
    }}

    ["/>
              <path d="M222 22 C292 17 347 55 356    .section-heading {{
        margin: 27px 0 12px;
 113 C362 154 343 185 373 212
                       C390 228 412 data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        inset: 0;
               color: #294A65;
        font-size: 1.65rem;
        font-weight: 800;
    }}

    .category-card {{
        min-height: 130px;
        padding: 233 411 244 C410 254 390 260 382 270
                       C374 280 362 z-index: 0;
        pointer-events: none;
        opacity: .60;
        background-image: url("data:image/svg+xml,{NEURON_SVG.replace('#', '% 291 341 289 L226 278"
                    fill="none" stroke="#5B87A2"17px;
        border: 1px solid #D3E3EF;
        border-radius: 18px stroke-width="3"
                    stroke-linecap="round" stroke-linejoin="round"/>
              <path d="23').replace(' ', '%20').replace('\\n', '')}");
        background-repeat;
        background: rgba(248,252,255,.92);
    }}

    .category-titleM223 54 C194 33 163 47 162 72 C133  {{
        color: #294A65;
        font-size: 1.05rem;
       : repeat;
        background-size: 1000px 800px;
        background-position: left75 132 108 154 119
                       C139 141 159 162 181 top;
    }}

    [data-testid="stAppViewContainer"] > .main {{
        position: relative;
 font-weight: 800;
    }}

    .category-description {{
        margin-top: 7px 156 C188 179 215 178 226 160
                       C240 180;
        color: #648198;
        font-size: .9rem;
        line        z-index: 1;
    }}

    [data-testid="stHeader"] {{
        background: transparent !important;
    }}

    .block-container {{
        max-width: 1180px;
        padding-top: 1. 267 173 271 151 C297 151 305 124 287 108-height: 1.45;
    }}

    .card-category
                       C300 84 281 60 258 64 C251 47 236 {{
        color: #648198;
        font-size: .85rem;
       1rem;
        padding-bottom: 4rem;
    }}

    h1, 46 223 54Z"
                    fill="none" stroke="#5B87A2" stroke-width="2.5"
                    stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M222 55 L222 159
                       M162 73 C183 83 187 101 h2, h3, h4, p, label, button, input, textarea, select {{
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }}

    h1, h2, h3, h4 {{
        color: #294A65 !important;
        letter-spacing font-weight: 700;
    }}

    .developer-name {{
        margin-top: 12px;
        color: #294A65;
        font-size: 1.1rem;
        font-weight: 800;
        text-align: center;
    }}

    .developer-role {{
        color: #648198;
        text-align: center;
    }}

    @media (max-width: 760px) {{
        .hero {{
            min-height: 300px;
            padding: 26px 22px;
        }}

        .hero-art {{
            right: - 181 117
                       M258 64 C242 79 242 96 254 109
                       M154 119 C174 117 187 127 181 156
                       M287 108 C264 111 253 127 271 : -0.025em;
    }}

    h1 {{ font-size: 2.5rem !important; font-weight: 800 !important; }}
    h2 {{ font-size: 1.8rem !important; font-weight: 800 !important; }}
   151
                       M188 78 C204 88 206 105 196 119
                       h3 {{ font-size: 1.25rem !important; font-weight: 800 !important; }}

    p,12%;
            width: 56%;
            opacity: .24;
        }}
    }}
    </ M239 78 C222 90 223 108 239 118
                       M201 label, [datastyle>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# Ш 140 C212 130 225 131 234 143"
                    fill="none" stroke="#5апка сайта
# ---------------------------------------------------------------------

def render_header():
    brand_col, home_col, library-testid="stCaptionContainer"],
    [data-testid="stMarkdownContainer"] {{
        color: #476B85 !important;
    }}

    [data-testid="_col, about_col, back_col = st.columns(
        [2.4, 1, 1.B87A2" stroke-width="2"
                    stroke-linecap="round"/>
              <ellipse cx="224"stVerticalBlockBorderWrapper"] {{
        border: 1px solid #C9DFEF !important;
        border-radius:  cy="150" rx="190" ry="76"
                       transform="rotate(-12 224 150)"
                      25, 1.15, 1]
    )

    with brand_col:
        logo_col, name18px !important;
        background: rgba(248,252,255,.94) !important;
        box-shadow_col = st.columns([0.65, 3.35], fill="none" stroke="#76A6C0" stroke-width="2: 0 8px 22px rgba(62,112,148,.06);
    vertical_alignment="center")

        with logo_col:
            if LOGO_PATH.is_file():
                st.image(str(LOG }}

    [data-testid="stTextInput"] [data-baseweb="input"],
    [data-testid="stTextArea"] [data-base"/>
            </svg>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    action_col,O_PATH), width=38)
            else:
                st.markdown(
                    """
                    <divweb="textarea"],
    [data-testid="stNumberInput"] [data-baseweb="input"],
    [ about_col, _ = st.columns([1.7, 1.2, 3.5])

    with action_col:
        st.button(
            "Перейти в библиотеку →data-testid="stSelectbox"] [data-baseweb="select"] > div,
    [data-baseweb="input"],
    class="header-logo-placeholder" aria-hidden="true">
                        <svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg",
            key="home_library_button",
            type="primary",
            on_click=go_library [data-baseweb="textarea"] {{
        color-scheme: light !important;
        background: #FFFFFF !important;
        border: 1px solid #C9DDEB !important;
        border-radius:,
            use_container_width=True,
        )

    with about_col:
        st.button(
            "Узнать больше">
                            <path d="M15.8 5.",
            key="home_about_button",
            on_click=go_about,
            use2c-3.1-2-7.2.1- 12px !important;
        box-shadow: none !important;
    }}

    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid_container_width=True,
        )

    st.markdown(
        '<div7.1 3.8-3. class="section-title">Найти технику</div>',
        unsafe="stNumberInput"] input,
    [data-testid="stSelectbox"] input,
    [8.8-4.1 5.8-.9 7._allow_html=True,
    )

    query = st.text_input(
        "Поиск по техникамdata-baseweb="input"] input,
    [data-baseweb="textarea"] textarea {{
        color: #294A653-2.7 2.8-.5 7.",
        key="home_search",
        placeholder="Найти технику или запрос, !important;
        background: #FFFFFF !important;
        -webkit-text-fill-color: #2941 3.2 6.6.7 3.6 5.1 4.2 6.8 1. например: тревожность, самооценка...",
        label_visibility="collapsed",
   A65 !important;
        border: 0 !important;
        box-shadow: none ! )

    # Поиск обновляется при вводе; пустой запрос сразуimportant;
        outline: none !important;
        caret-color: #315773 !important;
    }}

    input::2V7.5c-.5-1-1.placeholder,
    textarea::placeholder {{
        color: #7893A8 !important;
       1-1.8-2-2.3 убирает результаты.
    if query.strip():
        st.mark -webkit-text-fill-color: #7893A8 !important;
        opacity: down("#### Результаты поиска")
        render_technique_cards(
            search_techZ"
                                  fill="none" stroke="#315773" stroke-width="1.5" stroke-linejoin="round"/>
                            <path d="M16.2 5.2c3.1-2 7.2.1 7.1 3.8 3.8.8 4.1 5.8.9 7.3 2.7 2.8.51 !important;
    }}

    .stButton > button {{
        min-height: 44px;
        border: 1px solid #AFCFE2 !important;
        border-radius: 13px !important;
        background: #F1F8FD !important;
        color: #315773 !important;
        font-size: .98rem;
        font-weight: 700;
niques(query),
            "home_search_result",
        )
        return

    st.markdown(
        '<div class="section-title">Исследуйте библиотеку</div>',
        unsafe_allow_html=True,
    )

    categories = [
        ("Эмоции", "Работа с эмоциональными состояниями"),
        ("Коммуникация", "В 7.1-3.2 6.6-.7 3.6-5.1 4.2-6.8 1.2V7заимодействие и отношения"),
        ("Самооценка", "Образ себя и личные границы"),
        ("Мышление", "Убеждения и автоматические мысли"),
        transition: .18s ease;
    }}

    .stButton > button:hover:not(:disabled) {{
        border-color: #6EA7CB !important;
        background: #E0F0FA !important;
        color.5c.5-1 1.1-1.8 2    ]

    category_columns = st.columns(4)
    for column, (-2.3Z"
                                  fill="none" stroke="#315773" stroke-width="title, description) in zip(category_columns, categories):
        with column:
            st.markdown(
: #234D6B !important;
        transform: translateY(-1px1.5" stroke-linejoin="round"/>
                            <path d="M11 );
    }}

    .stButton > button[kind="primary"] {{
        min                f"""
                <div class="category-card">
                  <div class="category-title">{10c2.4.2 3.1 -height: 50px;
        border: 1px solid #6EA7CB !important;
        border-radiustitle}</div>
                  <div class="category-description">{description}</div>
                </div>
                ""1.8 2.7 3.4M9",
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class=": 15px !important;
        background: linear-gradient(135deg, #D9EEFA, #E5F3FC) !important;
        color: #234D6.6 16c2-.8 3.section-title">Популярные инструменты</div>',
        unsafe_allow_html=True,
    )
    render_technique_cards(
        list(TECHNIQUES.items())[:2],
7.2 3.8 2.2m7.B !important;
        font-size: 1rem;
        font-weight: 800;
    }}

    [data-testid="6-8.2c-2.4.2-3.1 1.8-        "home_featured",
    )

    st.markdown(
        '<div class="sectionstAlert"] {{
        border: 1px solid #BCD9EB !important;
        border-title">ПСИ-БЛОК — ваш помощник</div>',
        unsafe_allow_html=True,
    )
    st.info(
        "Ин-radius: 14px !important;
        background: #EAF5FC !important;
    }}

    [data-testid="stAlert"] * {{
2.7 3.4m4.1 2.6c-2-.8-3.7.2-        color: #315773 !important;
    }}

    .brand-name {{
       струменты помогают структурировать совместную работу и обсуждение. "
        "Они не заменяют профессиональную психолог3.8 2.2"
                                  fill="none" stroke="#315773" stroke-width="1.2" stroke-linecap="round"/>
                        </svg>
                    </div>
                    """,
                   ическую помощь."
    )


# ---------------------------------------------------------------------
# Библиотека
# ---------------------------------------------------------------------

def render_library():
    st color: #234D6B;
        font-size: clamp(1.7rem, 3vw, .title("Библиотека техник")
    st.write("Ищите технику по2.25rem);
        font-weight: 800;
        letter-spacing: -.05em;
 unsafe_allow_html=True,
                )

        with name_col:
            st.markdown        white-space: nowrap;
        line-height: 1;
        padding-top: (
                '<div class="header-brand">ПСИ-БЛОК</div>',
 названию, теме или описанию.")

    query = st.text_input(
        "Поиск                unsafe_allow_html=True,
            )

    with home_col:
        st.button(
            "Главная",
            по библиотеке",
        key="library_search",
        placeholder="Например: тревожность, поведение, выбор...",
   7px;
    }}

    .brand-fallback {{
        width: 40px;
        height: 40px;
        display key="header_home",
            on_click=go_home,
           : flex;
        align-items: center;
        justify-content: center;
        border )

    render_technique_cards(
        search_techniques(query),
-radius: 12px;
        border: 1px solid #C9E1F0;
               "library_search_result",
    )


# ---------------------------------------------------------------------
# Техника: use_container_width=True,
        )

    with library_col:
        st.button(
            "Библиотека",
            key="header_library",
            on_click=go_library,
            use_container_width=True,
        )

    with about background: rgba(168,214,235,.30);
        color: #315773;
        font-size: дерево решений
# ---------------------------------------------------------------------

def render_decision_tree():
    st.title("Дерево решений")
    st.write("Сравните варианты решения и возможные последствия.")

    question = st.text_input(
 1.3rem;
        font-weight: 800;
    }}

    .hero {{
        position: relative;
        display:_col:
        st.button(
            "О проекте",
            key="header_about",
            on_click=        "Какое решение нужно принять?",
        key="decision_question",
        placeholder="Например flex;
        align-items: center;
        min-height: 350px;
        overflow: hidden;
go_about,
            use_container_width=True,
        )

    with back_col:
        st.button(
            "←: «Стоит ли менять работу?»",
    )

    count = st.number_input        padding: 38px 44px;
        margin: 22px 0  Назад",
            key="header_back",
            on_click=go_back(
        "Количество вариантов",
        min_value=2,
        max_value=5,
        value=2,
        step=1,
        key="decision_option_count",
    )

    options = []
    for index in range(int(count)):
        with st.container(border=True):
            st.markdown(f"### Вариант {index + 124px;
        border: 1px solid #D3E5F2;
        border-radius: 28px;
        background:
            radial-gradient(circle at 78% 39%, rgba(174,222,241,.68) 0 18%, transparent 18.5%),
            linear-gradient(110deg, #F8FCFF 0%, #EAF5,
            disabled=not st.session_state.page_history,
            use_container_width=True,
        )

    st.markdown(
        "<hr style='margin: 8px 0 20px; opacity: .65;'>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------
# Карточки}")
            name = st.text_input(
                "Название варианта",
                key=f"decision_name_{index}",
                placeholder=f"Вариант {index + 1}",
            )
           FC 100%);
    }}

    .hero-copy {{
        position: relative;
        z-index: 1;
        max-width: 540px;
    }}

    .hero-title {{
        margin: 0 техник
# ---------------------------------------------------------------------

def render_technique_cards(items, key_prefix):
    if not items:
        st.info("По этому outcome = st.text_area(
                "Возможные последствия",
                key=f"decision;
        color: #214D6C;
        font-size: clamp(2.8rem,  запросу ничего не найдено. Попробуйте другие слова.")
        return

    for_outcome_{index}",
                placeholder="Что может произойти?",
            )
            probability = st.slider(
                "О6vw, 4.35rem);
        font-weight: 800;
        line-height: 1.05;
        start in range(0, len(items), 2):
        columns = st.columns(2)

        for column, ( letter-spacing: -.05em;
    }}

    .hero-subtitle {{
        max-width: 470px;
        margintechnique_id, technique) in zip(
            columns,
            items[start:start + 2],
        ):
           ценка вероятности, %",
                min_value=0,
                max_value=100,
                value=50,
                key=f"decision_probability_{index}",
            )
            score = st.slider(
                " with column:
                with st.container(border=True):
                    st.markdown(f"### {technique['title: 12px 0 18px;
        color: #294A65;
        font-size: clamp(1.25rem, 2.5vw, 1.85rem);
        font-weight: 700;
       ']}")
                    st.write(technique["short"])
                    st.markdown(
                        f"<div class='Оценка исхода",
                min_value=-5.0,
                max_value=5.0,
                line-height: 1.3;
    }}

    .hero-description {{
        max-width: 460px;
        color: # value=0.0,
                step=0.5,
                key=f"decision_score_{index}",
               card-category'>"
                        f"{html.escape(technique['category'])}</div>",
                        unsafe476B85;
        font-size: 1.05rem;
        line-height: 1.6;
    }}

    .hero help="−5 — крайне нежелательный исход, +5 — очень желательный.",
            )
        options.append(
_allow_html=True,
                    )
                    st.caption(technique["description"])
                    st.button(
                        "-art {{
        position: absolute;
        top: 50%;
        right: 3%;
        width:Открыть →",
                        key=f"{key_prefix}_{technique_id}",
                        on_click=open_technique,
            {
                "name": name,
                "outcome": outcome,
                "probability min(43%, 440px);
        aspect-ratio: 440 / 330;
        transform": probability,
                "score": score,
            }
        )

    if st.button(
        "Р                        args=(technique_id,),
                        use_container_width=True,
                    )


# ---------------------------------------------------------------------
# Вспомог: translateY(-50%);
        background-image: url("data:image/svg+xml,{HEROассчитать и сравнить",
        key="decision_calculate",
        type="primary",
ательные функции для схем техник
# ---------------------------------------------------------------------

def svg_escape(value_SVG.replace('#', '%23').replace(' ', '%20').replace('\\n', '')}");
        background):
    return html.escape(str(value or ""), quote=True)


def svg_wrap(value, width=30, max_lines=5):
        use_container_width=True,
    ):
        if not question.strip():
            st.warning("Сначала сформулируйте решение.")
            return

        if any(not option["name"].strip() for option in options):
    value = str(value or "").strip()
    if not value:
        return ["—-size: contain;
        background-repeat: no-repeat;
        background-position"]

    lines = []
    for paragraph in value.splitlines():
        words = paragraph.split()
       : center;
    }}

    .section-title {{
        margin: 28px 0 12px;
        color: #294            st.warning("Введите название каждого варианта.")
            return

        results = [
            option[" current = ""

        for word in words:
            if notscore"] * option["probability"] / 100
            for option in options
        ]

A65;
        font-size: 1.65rem;
        font-weight:         st.subheader("Сравнение вариантов")
       800;
    }}

    .category-card {{
        min-height: 125px;
 current:
                current = word
            elif len(current) + len(word) + 1 <=        padding: 16px;
        border: 1px solid # width:
                current += " " + word
            else:
                lines.append(current)
                current = word

        if current:
            lines.append(current)

    result_columns = st.columns(len(options))
        best_indexD3E3EF;
        border-radius: 18px;
        background: rgba(248,252,255,.95 return lines[:max_lines] or ["—"]


def svg_text(value, x, y, width=30);
    }}

    .category-title {{
        color: #294A65;
        font-weight: 800 = max;
        font-size: 1.05rem;
    }}

    .category-description {{
        margin-top, font_size=16,
             fill="#294A65", max_lines=5,(range(len(results)), key=results.__getitem__)

        for index, (column, option, result) in enumerate(
            zip(result_columns, options, results)
        ):
            with column: 7px;
        color: #648198;
        font-size: .9rem;
        line-height:  line_height=None):
    lines = svg_wrap(value, width, max_lines)
    line_height = line_height1.45;
    }}

    .developer-name {{
        margin-top: 12px;
        color: #294A65;
        font-size: 1.1rem;
        font-weight: 800;
        text-align: center;
    }}

    .developer-role {{
        color: #648198;
        text-align: center;
    }}

    @media (max-width: 700px) {{
 or int(font_size * 1.35)
    spans = []

    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_height
        spans.append(
            f'<tspan x="{x}" dy="{dy}">{svg_escape(line)}</tspan>'
        )

    return (
        f'<text x="{x}" y="{:
                label = option["name"]
                if index == best_index:
                    label = f"Наивысшая оценка: {label}"
                st.metric(label, f"{result:.2f} / 5")
                st.caption(option["outcome"] or "Последствия не указаны.")

        st.info(
            "Расчёт — ориентир для обсуждения, а не автоматическое решение."
        )


# ---------------------------------------------------------------------
# Техника:y}" text-anchor="middle" '
        f'font-family="Arial, sans-serif" font-size="{font_size}" '
        f цепочный анализ поведения
# ---------------------------------------------------------------------

def render_chain():
    st.title("Цепочный анализ поведения (Д        .hero {{
            min-height: 300px;
            padding: 26px 22px;
        }}

        .hero-art {{
            right: -БТ)")
    st.write("Исследуйте контекст, реакции, поведение и последствия.")
    st.info(
        "Можно'fill="{fill}">{"".join(spans)}</text>'
    )


def9%;
            width: 55%;
            opacity: .24;
        }}
    }}
    </style>
    """,
 svg_card(x, y, width, height, title, body,
             fill="#F8FCFF пропустить любое поле или остановиться в любой момент."
    )

    vulnerability = st.text_area(
        "Факторы    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# Верхняя навигация
", stroke="#AFCFE2"):
    max_chars = max(15, int(width / 12))
    return# ---------------------------------------------------------------------

def render_header():
    logo_col, home_col, library_col, about_col, уязвимости",
        key="chain_vulnerability",
        placeholder="Что могло сделать ситуацию сложнее f"""
    <rect x="{x}" y="{y}" width="{width}" height="{height}"
          rx back_col = st.columns(
        [2.4, 1.1, 1.25, 1.2 заранее?",
    )
    trigger = st.text_area(
        "Запускающее событие",
        key=", 1.0]
    )

    with logo_col:
        image_col, title_col = st="20" fill="{fill}" stroke="{stroke}" stroke-width="3"/>
   chain_trigger",
        placeholder="Что произошло непосредственно перед реакцией?",
    )
    links {svg_text(title, x + width / 2, y + 32, max_chars, 17, "# = st.text_area(
        "Звенья цепочки",
        key="chain_links",
        placeholder=(
.columns([1, 5])

        with image_col:
            if LOGO_PATH.is_file():
                st.image(str(LOGO_PATH), width=40)
            else:
                st.markdown(
                    '<div class="brand-fallback">П</div>',
                               "Опишите по порядку мысли, эмоции,294A65", 2)}
    {svg_text(body, x + width / 2, y + 62, max_chars ощущения и действия. "
            "Каждое звено можно записать с новой строки."
        ),
        height=160,
 unsafe_allow_html=True,
                )

        with title_col:
            st.markdown(
, 14, "#476B85", 5)}
    """


def svg_document(title, content, width, height):
    return f"""
    <svg xmlns="http://www    )
    target = st.text_area(
        "Целевое поведение",
        key="chain_target",
                   '<div class="brand-name">ПСИ-БЛОК</div>',
                unsafe_allow_html=True,
            )

    with.w3.org/2000/svg"
         width="{width}" height="{height}"
         viewBox="0 0 { home_col:
        st.button(
            "Главная",
            key="nav_home",
            on_click=go_home,
 )

    left, right = st.columns(2)
    with left:
        immediate = st.text_area(
            "Последствия сразу после",
            key="chain_im            use_container_width=True,
        )

    with library_col:
        st.button(
            "Библиотека",
            key="width} {height}">
      <rect width="100%" height="100%" fill="#F5FAFE"/>
      <mediate",
        )
    with right:
        later = st.text_area(
            "Последствия позднее",
nav_library",
            on_click=go_library,
            use_container_width=True,
        )

    with about_col:
       text x="{width / 2}" y="45" text-anchor="middle"
            font-family="Arial, sans-serif" font-size="29"
            font            key="chain_later",
        )

    alternative = st.text_area st.button(
            "О проекте",
            key="nav_about",
            on_click=go(
        "Возможная точка вмешательства или поддержка",
        key="chain_about,
            use_container_width=True,
        )

    with back_col:
        st.button(
            "← Назад-weight="bold" fill="#294A65">
        {svg_escape(title)}
      </text",
            key="nav_back",
            on_click=go_back,
            disabled=not st.session_state.page_history,
           _alternative",
    )

    with st.expander("Показать сводку"):
        for title,>
      {content}
    </svg>
    """


def render_interactive_diagram(svg, key, height= use_container_width=True,
        )

    st.markdown(
        "<hr style='margin740):
    safe_key = "".join(ch for ch in key if ch.isalnum() or value in [
            ("Факторы уяз ch == "_")
    svg_id = f"diagram_{safe_key}"
    diagram_svg = svgвимости", vulnerability),
            ("Запускающее событие", trigger),
            ("Звенья: 8px 0 18px; border-color: #D7E6F0;'>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------
# По цепочки", links),
            ("Целевое поведение", target),
            ("Последствия сразу после", immediate.replace("<svg ", f'<svg id="{svg_id}" ', 1)

    template = r"""
    <!иск и карточки техник
# ---------------------------------------------------------------------

def render_technique_cards(items, key_prefix):
    if not),
            ("Последствия позднее", later),
            ("Возможная поддержка", alternativedoctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        html, body {
          margin: 0;
         ),
        ]:
            st.markdown(f"**{title}**")
            st.write(value or items:
        st.info("По вашему запросу ничего не найден padding: 0;
          width: 100%;
          height: 100%;
          overflow: hidden;
          background: transparent;
          font-family: Arial, sans-serif;
        }
        .toolbar {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          align-items: center;
          padding: 6px 2px 10о.")
        return

    for start in range(0, len(items), 2):
        columns = st.columns(2)

        for column, (technique_id, technique) in zip(
            columns,
            items[start:start + 2],
        ):
            with column:
                with st.container(border=True):
                    st.markdown(f"### {technique['title']}")
                    st.write(technique["short "—")


# ---------------------------------------------------------------------
# Техника: иерархия экспозиции
# ---------------------------------------------------------------------

def render_exposure():
    st.title("Иерархия экспозиции")
    st.write("Составьте лестницу ситуаций для обсуждения и планирования практики.")
    st.info(
        "Практика должна быть доброволь"])
                    st.caption(
                        f"{technique['category']} · {technique['description']}"
                    )
                    st.button(
                        "Открыть →",
                        key=f"{key_prefix}_{px;
        }
        .toolbar button {
          border: 1px solid #9FC5DE;
          border-radius: 10px;
          background: #EAFной и согласованной со специалистом. "
        "Не используйте упражнение для ситуаций с реальной опасностью."
    )

    st.text_area("Цель работы",5FC;
          color: #294A65;
          padding: 8px 13px;
          font-weight key="exposure_goal")

    count = st.numbertechnique_id}",
                        on_click=open_technique,
                        args=(technique_id,),
                        use_container_width: 700;
          cursor: pointer;
        }
        .toolbar button:hover {
          background: #D9EDF9;
       _input(
        "Количество ступеней",
        min_value=1,
        max_value=10,
        value=True,
                    )


# ---------------------------------------------------------------------
# Главная
# ---------------------------------------------------------------------

def render_home():
    st.markdown(
        """
        <section }
        .hint {
          color: #54718A;
          font-size: 13px;
          margin-left: 5px;
        }
        .=3,
        step=1,
        key="exposure_count",
    )

    steps = []
    for index in range(int(count)):
        with st.container(border=True):
            st.markdown(f"### Ступень { class="hero">
          <div class="hero-copy">
            <h1 class="hero-title">ПСИ-БЛОК</h1>
index + 1}")
            situation = st.text_input(
                "Ситуация",
                key=f"exposure_situation_{index}",
            )
            distress = st.slider(
                "Ожидаемая тревога",
                min_value=0,
                max_value=10,
                value=3,
                key=f"exposure_distress_{index}",
            )
           viewport {
          width: 100%;
          height: calc(100% - 58px);
          overflow: hidden;
          border: 1px solid #BBD7E8;
          border-radius: 16px;
          background: #F5FAFE;
          cursor: grab;
          touch-action: none;
        }
        .viewport.dragging {
          cursor            <div class="hero-subtitle">
              Инструменты для глубокой психологической работы
            </div>
            <div class="hero-description">
              Библи: grabbing;
        }
        #DIAGRAM_ID {
          display: block;
          width: 100%;
          height: 100%;
          user-select: none;
        }
      </style>
    </head>
    <body>
      <div class="toolbar">
        <button id="zoomIn">Увеличить</button>
        <button id="zoomOut">Уменьшить</button>
        <button id="reset prediction = st.text_area(
                "Прогноз или опасение",
                key=f"exposure_prediction_{index}",
            )
            plan = st.text_area(
                "Посильный шаг",
                key=f"exposure_plan_{index}",
            )
        steps.append(
            {
                "situation": situation,
                "distress": distress,
                "prediction": prediction,
                "plan": plan,
            }
        )

   отека проверенных психологических техник
              для специалистов и клиентов.
            </div>
          </div>
          <div class="hero-art" aria-hidden="true"></div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    library_col, about_col, _ = st.columns([1.7, 1.3, 3.5])

    with library_col:
        st.button(
            "Перейти в библиотеку →",
            key="home_library_button",
            type="primary",
            on_click=go_library,
            use_container_width=True,
        )

    with about_col:
        st.button(
            "Узнать больше",
            key="home_about_button",
            on_click=go_about">Сбросить вид</button>
        <button id="downloadPng">Скачать PNG</button>
        <span class="hint">Колесо мыши — масштаб; перетаскивание — перем,
            use_container_width=True,
        )

    st.markdown(
        '<div class="section-title">Найти технику</div>',
        unsafe_allow_html=True,
    )

    query = st.text_input(
        "По completed = [
        step for step in steps
        if step["situation"].strip()
    ]
    completed.sort(key=lambda step: step["distress"])

    st.subheader("ещение</span>
      </div>
      <div class="viewport" id="viewport">DIAGRAM_SVG</div>

      <script>
        (() => {
          const svg = document.getElementById("DIAGRAM_ID");
          constЛестница по ожидаемой тревоге")
    if not completed:
        st.caption("Заполните описание хотя бы одной ситуации.")
        return

    for index, step in enumerate(completed, start=1):
иск по техникам",
        key="home_search",
        placeholder="Найти технику или запрос, например: тревожность, самооценка...",
        label_visibility="collapsed",
    )

    if query viewport = document.getElementById("viewport");
          const vb = svg.viewBox.baseVal;
          const base = {x: vb.strip():
        st.markdown("#### Результаты поиска")
        render_technique_cards(
            search_techniques        with st.container(border=True):
            st.markdown(
                f"**{index}. {step['situation']}** —(query),
            "home_search_result",
        )
        return

    st.markdown(
        '<div class="section-title">Исследуйте библиотеку</div>',
        unsafe_allow_html=True,
    )

    categories = [
        ("Эмоции", "Работа с эмоциональными состояниями"),
        ("Коммуникация", "Взаимодействие и отношения"),
        ("Самооценка", "Образ себя и личные границы"),
        ("Мышление", "Убеждения и автоматические мысли"),
    ]

    category_columns = st.columns(4)
    for column, (title, description) in zip(category_columns, categories):
        with column:
            st.markdown(
                f"""
                <div class="category-card">
                    <div class="category-title">{title}</div>
                    <div class="category-description">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-title">Популярные инструменты</div>',
        unsafe_allow_html=True,
    )
    render_technique_cards(
        list(TECHNIQUES.items())[:2],
        "home_featured",
    )

    st.markdown(
        '<div class="section-title">ПСИ-БЛОК — ваш помощник</div.x, y: vb.y, width: vb.width, height: vb.height};
          const view = {...base};

          function applyView() {
            svg.setAttribute(
              "viewBox",
              `${view.x} ${view.y} ${view.width} ${view.height}`
            );
          }

          function zoom(factor, clientX, clientY) {
            const rect = svg.getBoundingClientRect();
            const px = clientX === undefined ? rect.left + rect.width / 2 : clientX;
            const py = clientY === undefined ? rect.top + rect.height / 2 : clientY;
            const rx = (px - rect.left) / rect.width;
            const ry = (py - rect.top) / rect.height;
            const oldWidth = view.width;
            const oldHeight = view.height;

            view.width *= factor;
            view.height *= factor;
            view.x += (oldWidth - view.width) * rx;
            view.y += (oldHeight - view.height) * ry;
            applyView();
          }

          document.getElementById("zoomIn").onclick = () => zoom(0.8);
          document.getElementById("zoomOut").onclick = () => zoom(1.25);
          document.getElementById("reset").onclick = () => {
            Object.assign(view, base);
            applyView();
          };

          viewport.addEventListener("wheel", event => {
            event.preventDefault();
            zoom(event.deltaY < 0 ? 0.9 : 1.1, event.clientX, event.clientY);
          }, { "
                f"ожидаемая тревога {step['distress']}/10"
            )
            if step["prediction"]:
                st.write(f"**Прогноз:** {step['prediction']}")
            if step["plan"]:
                st.write(f"**Посильный шаг:** {step['plan']}")


# ---------------------------------------------------------------------
# Техника: ACT-матрица
# ---------------------------------------------------------------------

def render_act_matrix():
    st.title("ACT-матрица")
    st.write(
        "Исследуйте, что уводит от дискомфорта и какие действия "
        "приближают к важному."
    )
    st.info(
        "Матрица — материал для совместного исследования. "
        "Она не оценивает поведение как правильное или неправильное."
    )

    situation = st.text_area(
        "Ситуация, которую хотите исследовать",
        key="act_situation",
    )
    values = st.text_area(
        "Что важно для вас?",
        key="act_values",
        placeholder="Например: близость, забота, любознательность.",
    )

    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown("### Действия «от дискомфорта»")
            away = st.text_area(
                "Что вы делаете, чтобы избежать дискомфорта?",
                key="act_away",
            )
        with st.container(border=True):
            st.markdown("### Внутренний опыт")
            inner = stpassive: false});

          let dragging = false;
          let lastX = 0;
          let lastY = 0;

          viewport.addEventListener("pointerdown", event => {
            dragging = true;
            lastX = event.text_area(
                "Мысли, эмоции, телесные ощущения",
                key="act_inner",
            )

    with right:
        with st.container(border=True):
            st.markdown("### Действия «к важному>',
        unsafe_allow_html=True,
    )
    st.info(
        "Инструменты помогают структур»")
            toward = st.text_area(
                "Какое действие приближает к важному?",
                key="act_toward.clientX;
            lastY = event.clientY;
            viewport.classList.add("dragging");
            viewport.setPointerCapture(event.pointer",
            )
        with st.container(border=True):
            st.markdown("### Внутренний опыт при этом шаге")
            toward_inner = st.text_area(
                "Что может возникать внутри?",
                key="Id);
          });

          viewport.addEventListener("pointermove", event => {
            if (!dragging) return;
            const rect = svg.getBoundingClientRect();
            view.x -= (event.clientX -act_toward_inner",
            )

    step = st.text_area(
        "Небольшой выбранный шаг",
        key="act_step",
    )

    st.subheader("Сводка")
    st.write(f"**Ситуация:** {situation or '—'}")
    st.write(f"**Что важно:** {values or '—'}")

    summary_left, summary_right = st.columns(2)
    with summary_left:
        st.markdown("**Действия «от дискомфорта»**")
        st.write(away or "—")
        st.markdown("**Внутренний опыт**")
        st.write(inner or "—")

    with summary_right:
        st.markdown("**Действия «к важному»**")
        st.write lastX) * view.width / rect.width;
            view.y -= (event.clientY - lastY) * view.height / rect.height;
            lastX = event.clientX;
            lastY = event.clientY;
            applyView();
          });

          function stopDragging() {
            dragging = false;
            viewport.classList.remove("dragging");
          }

          viewport.addEventListener("pointerup", stopDragging);
          viewport.addEventListener("pointercancel", stopDragging);

          document.getElementById("downloadPng").onclick = () => {
            const clone = svg.cloneNode(true);
            clone.removeAttribute("id");
            clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
            clone.setAttribute("width", base.width);
           ировать совместную работу и обсуждение. "
        "Они не заменяют профессиональную психологическую помощь."
    )


# ---------------------------------------------------------------------
# Библиотека
# ---------------------------------------------------------------------

def render_library():
    st.title("Библиотека техник")
    st.write("Поиск работает по названию, теме и описанию.")

    query = st.text_input(
        "Поиск в библиотеке",
        key="library_search",
        placeholder="Например: тревожность, поведение, выбор...",
        label_visibility="collapsed",
    )

    render_technique_cards(
        search_techniques(query),
        "library_search_result",
    )


# ---------------------------------------------------------------------
# Дерево решений
# ---------------------------------------------------------------------

def render_decision_tree():
    st.title("Дерево решений")
    st.write("Сравните варианты решения и возможные последствия.")

    question = st.text_input(
        "Какое решение нужно принять?",
        key="dt_question",
        placeholder="Например: «Стоит ли менять работу(toward or "—")
        st.markdown("**Внутренний опыт при этом шаге**")
        st.write(toward_inner or "—")

    st.markdown("**Небольшой выбранный шаг**")
    st.write(step or " clone.setAttribute("height", base.height);
            clone.setAttribute(
              "viewBox",
              `${base.x} ${base.y} ${base.width} ${base.height}`
            );

            const source = new XMLSerializer().serializeToString(clone);
            const blob = new?»",
    )

    option_count = st.number_input(
        "Количество вариантов",
        min_value=2,
        max_value=5,
        value=2,
        step=1 Blob(
              [source],
              {type: "image/svg+xml;charset=utf-8"}
            );
            const url = URL.createObjectURL(blob—")


# ---------------------------------------------------------------------
# Раздел «О проекте»
# ---------------------------------------------------------------------

def render_about():
    st.title("О проекте")
    st.markdown(
        """
        **ПСИ-БЛОК** — библиотека интерактивных инструментов
        для психологических консультаций. Она помогает специалисту
        и клиенту совместно структурировать обсуждение и фиксировать идеи.
        """
    )

   );
            const image = new Image();

            image.onload = () => {
              const canvas = document.createElement("canvas");
              canvas.width = Math.round(base.width * 2);
              canvas.height = Math.round(base.height * 2);
              const ctx = canvas.getContext("2d");
             ,
        key="dt_option_count",
    )

    options = []
    for option_index in range(int(option_count)):
        with st.container(border=True):
            st.markdown(f"### Вариант {option_index + 1}")
            name = st.text_input(
                "Название варианта",
                key=f"dt_option_name_{option_index}",
                placeholder=f"Вариант {option_index + 1}",
            )

            scenario_count = st.number_input(
                "Количество возможных исходов",
                min_value=1,
                max_value=5,
                value=2,
                step=1,
                key=f"dt_scenario_count_{option_index}",
            )

            scenarios = []
 ctx.fillStyle = "#F5FAFE";
              ctx.fillRect(0, 0, canvas.width, canvas.height);
              ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
              URL.revokeObjectURL(url);

              canvas.toBlob(png => {
                if (!png) {
                  alert("Не удалось создать PNG. Попробуйте ещё раз.");
                  return;
                }
                const link = document.createElement("a");
                link.href = URL.createObjectURL(png);
                link.download = "DIAGRAM_FILENAME.png";
                document.body.appendChild(link);
                link.click();
                link.remove();
                setTimeout(() => URL.revokeObjectURL(link.href), 1500);
              }, "image/png");
            };

            image.onerror = () => {
              URL.revokeObjectURL(url);
              alert("Не удалось подготовить изображение для скачивания.");
            };

            image.src = url;
          };
        })();
 st.divider()
    st.subheader("Команда разработчиков")

    developers = [
        {
            "name": "Артём Черемкин",
            "role": "Разработчик сайта, практикующий психолог",
            "photo": "developer1.jpg",
        },
        {
            "name": "Анна Пыжьянова",
            "role": "Практикующий психолог",
            "photo": "developer2.jpg",
        },
        {
            "name": "Ферузахон Сайдазимова",
            "role": "Практикующий психолог",
            "photo": "developer3.jpg",
        },
    ]

    columns = st.columns(3)
    app_dir = Path(__file__).resolve().parent

    for column, person in zip(columns, developers):
        with column:
            with st.container(border=True):
                photo_path = app_dir / person["photo"]

                if photo            for scenario_index in range(int(scenario_count)):
                st.markdown(f"**Исход {scenario_index + 1}**")
                scenario_name = st.text_input(
                    "Описание исхода",
                    key=f"dt_scenario_name_{option_index}_{scenario_index}",
                    placeholder="Что может произойти?",
                )

                probability_col, score_col = st.columns(2)
                with probability_col:
                    probability = st.slider(
                        "Вероятность, %",
                        min_value=0,
                        max_value=100,
                        value=50,
                        key=f"dt_probability_{option_index}_{scenario_index}",
                    )
                with score_col:
                    score = st.slider(
                        "Оценка исхода",
                        min_value=-5.0,
                        max_value=5.0,
                        value=0.0,
                        step=0.5,
                        key=f"dt_score_{option_index}_{scenario_index}",
                        help="−5 — очень нежелательный, +5 — очень желательный.",
                    )

                scenarios.append(
                    {
                        "name": scenario_name,
                        "probability": probability,
                        "score": score,
                    }
                )

            options.append({"name": name, "scenarios": scenarios})

    if st.button(
        "Рассчитать и сравнить варианты",
        key="dt_calculate",
        type="primary",
        use_container_width=True,
    ):
        if not question.strip():
            st.warning("Сначала сформулируйте решение.")
            return

        results = []
        error = None

             </script>
    </body>
    </html>
    """

    html_blob = (
        template
        .replace("DIAGRAM_ID", svg_id)
        .replace("DIAGRAM_SVG", diagram_svg_path.is_file():
                    st.image(str(photo_path), use_container_width=True)
                else:
                    st.markdown(
                        """
                        <div style="
                            height:220px;
                            display:flex;
                            align-items:center;
                            justify-content:center for option_index, option in enumerate(options, start=1):
            if not option["name"].strip():
                error = f"Введите название варианта {option_index};
                            border-radius:14px;
                            background:linear-gradient(135deg,#DDEFFA,#F2F8FC);
                            color:#5F86A0;">
                            Фото разработчика
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"**{html.escape(person['name'])}**"
                )
                st.caption(person["role"])


# ---------------------------------------------------------------------
# Открытие выбранной техники
# ---------------------------------------------------------------------

def render_selected_technique():
    technique_id = st.session_state.selected_technique

    if technique_id not in TECHNIQUES:
        st.warning("Техника не найдена.")
        return

    if technique_id == "decision_tree":
        render_decision_tree()
    elif technique_id == "dbt_chain":
        render_chain()
    elif technique_id == "exposure":
        render_exposure()
    elif technique_id == "act_matrix":
        render_act_matrix()


# ---------------------------------------------------------------------
# Запуск)
        .replace("DIAGRAM_FILENAME", safe_key)
    )
    st.components.v1.html(html_blob, height=height, scrolling=False)


def make_vertical_diagram(title, sections, note):
    width = 1100
    card_height = 120
    gap = 40
    top = 90
    height = max(540, top + len(sections) * (card_height + gap) + 70)
    content = []

    for index, (heading, body) in enumerate(sections):
        y = top + index * (card_height + gap)
        fill = "#E8F4FB" if index % 2 == 0 else "#F3F8FC"
        content.append(
            svg_card(115, y, 870, card_height, heading, body, fill, "#AFCFE2")
        )

        if index < len(sections) - 1:
            content.append(
                f'<line x1="550" y1="{y + card."
                break

            if any(not scenario["name"].strip() for scenario in option["scenarios"]):
                error = f"Заполните все исходы варианта {option_index}."
                break

            total_probability = sum(
                scenario["probability"] for scenario in option["scenarios"]
            )
            if total_probability == 0:
                error = (
                    f"Задайте ненулевую вероятность для варианта {option_index}."
                )
                break

            score = sum(
                scenario["probability"] / total_probability * scenario["score"]
                for scenario in option["scenarios"]
            )
            results.append({"name": option["name"], "score": score})

        if error:
            st.warning(error)
            return

        best = max(results, key=lambda result: result["score"])
        st.subheader("Сравнение вариантов")
        result_columns = st.columns(len(results))

        for column, result in zip(result_columns, results):
            with column:
                st.metric(
                    result["name"],
                   
# ---------------------------------------------------------------------

def render_header():
    brand_col, home_col, library_col, about_col, back_col = st.columns(
        [2.3, 1, 1.25 f"{result['score']:.2f} / 5",
                    "Наивысшая оценка" if result is best else None,
                )

        st.info(
            "Результат — опора для обсуж_height}" '
                f'x2="550" y2="{y + card_height + gap - 6}" '
                'stroke="#6EA7CB" stroke-width="4"/>'
            )
            content.append(
                f'<path d="M540 {y + card_height + gap - 15} '
                f'L550 {y + card_height + gap - 6} '
                f'L560 {y + card_height +дения, а не автоматическое решение. "
            "Вероятности нормализуются отдельно внутри каждого варианта."
        )


# ---------------------------------------------------------------------
# Цепочный анализ поведения
# ---------------------------------------------------------------------

def initialize_chain():
    if "chain_links" not in st.session_state:
        st, 1.1, 1]
    )

    with brand_col:
        logo_col, name_col = st.columns([0.6, 3.4])
        with logo_col:
            if gap - 15}" '
                'fill="none" stroke="#6EA7CB" stroke-width LOGO_PATH.is_file():
                st.image(str(LOGO_PATH), width=42)
            else:
                st.session_state.chain_links = [
            {"id": uuid.uuid4().hex},
            {"id": uuid.uuid4().hex},
        ]


def add_chain_link():
    st.session_state.chain_links.append({"id": uuid.uuid4().hex})


def remove_chain_link(link_id):
    if len(st.session_state.chain_links) > 1:
        st.session_state.chain_links = [
            item for item in st.session_state.chain_links
            if item["id"] != link_id
        ]


def render_chain():
    initialize_chain()

    st.title("Цепочный анализ поведения (ДБТ)")
    st.write("Исследуйте контекст, реакции, поведение и последствия.")
    st.info("Можно пропустить поле или остановиться в любой момент.")

    vulnerability = st.text_area(
        "Ф.markdown(
                    """
                    <div class="brand-fallback">
                      <svg width="30" height="30" viewBox="0 0 30 30"
                           xmlns="http://www.w3.org/2000/svg">
                        <g fill="none" stroke="#315773" stroke-width="1.5"
                           stroke-linecap="round">
                          <path d="M14.8 5.2c-4-3-8 0-7.5 4-3.8 1.3-3.4 6.1-.3 7.4-2.2 3.="4"/>'
            )

    content.append(
        f'<text x="550" y="{height - 20}" text-anchor="middle" '
        'font-family="Arial, sans-serif" font-size="13" fill="#54718A">'
        f'{svg_escape(note)}</text>'
    )
    return svg_document(title, "".join(content), width, height)


def make_decision_diagram(question, options):
    card_w = 290
    card_h = 150
    option_w = 300
    option_h = 120
    leaf_spacing = 330
    left_margin = 170
    top_y = 105
   акторы уязвимости",
        key="chain_vulnerability",
        placeholder="Что могло сделать ситуацию сложнее заранее?",
    )
    prompting = st.text_area(
        "Запускающее событие",
        key="chain_prompt",
        placeholder="Что произошло непосредственно перед реакцией?",
    )

    st.sub option_y = 410
    root_y = 680
    root_w = 440
    root_h = 110

    total_leaf_count = max(
        sum(len(option["scenarios"]) for option in options),
        2.3 6.5 3.7 5.1 1.3 3 4.5 2.6 5.3.2"/>
                          <path d="M15.2 5.2c4-1,
    )
    width = left_margin * 2 + (total_leaf_count - 1) * leaf_spacing + card_w
    root_x = width / 2
    height = 850
    colors = ["#6AAED0", "#65Bheader("Звенья цепочки")
    links_summary = []

    for index, link in enumerate(list(st.session_state.chain_links), start=1):
        link_id = link["id"]

        with st.container(border=True):
            title_col, remove_col = st3 8 0 7.5 4 3.8 1.3 3.4 6.1.3 7.4 2.2 3.2-.3 6.5-3.7 5.1-1.99C", "#76A5D2", "#8BB7D8", "#5F9FC4"]
    content = []

    layout = []
    next_leaf.columns([5, 1.4])
            with title_col:
                st.markdown(f"**Звено {3 3-4.5 2.6-5.3.2"/>
                          <path d="M15 5v17M9 10c2_index = 0

    for option_index, option in enumerate(options):
        centers = [
            left_margin + card_w / 2 + (index}**")
            with remove_col:
                st.button(
                    "Удалить",
                    key=f"remove_chain_{link_id}",
                    0 3 1 3 3m-5 3c2-.5 4 .5 4 2m10-8c-2 0next_leaf_index + i) * leaf_spacing
            for i in range(len(option["scenarios"]))
        ]
        next_leaf_index += len(option["scenarios"])
        layout.append(
            {
                "option": option,
                "color": colors[option_index % len(colors)],
 on_click=remove_chain_link,
                    args=(link_id,),
                    disabled=len(st.session_state.chain_links) <= 1,
                    use_container_width=True,
                )

            left, right = st.columns(2)
            with left:
                thought = st.text_area(
                    "Мысли или об-3 1-3 3m5 3c-2-.5-4 .5-4 2"/>
                        </g>
                      </svg>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        with name_col:
            st.markdown(
                '<div class="brand-name">ПСИ-БЛОК</div>',
                unsafe_allow_html=True,
            )

    with home_col:
        st.button(
            "Главная",
            key="header_home",
            on_click=go_home,
            use_container_width=True,
        )

    with library_col:
        st.button(
            "Библиотека",
            key="header_library",
            on_click=go_library,
            use_container_width=True,
        )

    with about_col:
        st.button(
            "О проекте",
            key="header_about",
            on_click=go_about,
            use_container_width=True,
        )

    with back_col:
        st.button(
            "← Назад",
            key="header_back",
            on_click=go_back,
            disabled=not st.session_state.page_history,
            use_container_width=True,
        )


render_header()

if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "library":
    render_library()
elif st                "scenario_centers": centers,
                "center_x": sum(centers) / len(centers),
            }
        )

    for entry in layout:
        for center in entry["scenario_centers"]:
            content.append(
                f'<path d="M {center} {top_y + card_h} '
                f'C {center} 325, {entry["center_x"]} 330, '
                f'{entry["center_x"]} {option_y}" '
                f'fill="none" stroke="{entry["color"]}" stroke-width="4"/>'
            )

    for entry in layout:
        content.append(
            f'<path d="M {entry["center_x"]} {option_y + option_h} '
            f'C {entry["center_x"]} 560, {root_x} 570, {root_x} {root_y}" '
            f'fill="none" stroke="{entry["color"]}" stroke-width="6"/>'
        )

    leaf_index = 0
    forразы",
                    key=f"chain_thought_{link_id}",
                )
                body = st.text_area(
                    "Ощущения в теле",
                    key=f"chain_body_{link_id}",
                )
            with right:
                emotion = st.text_area(
                    "Эмоции",
                    key=f"chain_emotion_{link_id}",
                )
                action = st.text_area(
                    "Импульсы или действия",
                    key=f"chain_action_{link_id}",
                )

            intensity = st.slider(
                "Интенсивность",
                min_value=0,
                max_value=10,
                value=0,
                key=f"chain_intensity_{link_id}",
            )
            support = st.text_area(
                "Возможная поддержка или другой шаг",
                key=f"chain_support_{link_id}",
            )

        links_summary.append(
            (
                f"Звено {index}",
                "\n".join(
                    [
                        f"Мы entry in layout:
        option = entry["option"]
        for scenario_index, scenario in enumerate(option["scenarios"]):
            center = left_margin + card_w /.session_state.page == "about":
    render_about()
elif st.session_state.page == "technique":
    render_selected_technique()
else:
    st.sessionсли: {thought or '—'}",
                        f"Эмоции: {emotion or '—'}",
                        f"Ощущения: {body or ' 2 + leaf_index * leaf_spacing
            leaf_index += 1
            body = (
                f"{scenario['name']}\\n"
                f"{option['_state.page = "home"
    render_home()
```—'}",
                        f"Действия: {action or '—'}",
                        f"Интенсивность: {intensity}/10",
                        f"Поддержка: {normalized'][scenario_index]:.1f}% · "
                f"оценка {scenariosupport or '—'}",
                    ]
                ),
            )
        )

    st.button("Добавить['score']:g}"
            )
            content.append(
                svg_card(
                    center - card_w / 2,
                    top_y,
                    card_w,
                    звено", on_click=add_chain_link)

    st.subheader("Поведение и последствия")
    target = st.text_area("Ц card_h,
                    f"Исход {scenario_index + 1}",
                    body,
                    "#FFFFFF",
                    entry["color"],
                )
            )

    for entry in layout:
       елевое поведение", key="chain_target")
    immediate_col, later_col = st.columns(2)

    with immediate_col:
        immediate = st.text_area(
            "Последствия сразу после",
