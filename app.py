import html
from pathlib import Path
from urllib.parse import quote

import streamlit as st


st.set_page_config(
    page_title="ПСИ-БЛОК",
    page_icon="favicon.jpg",
    layout="wide",
)

# Положи свой логотип рядом с app.py как logo.png
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
        "keywords": "выбор решение последствия вероятность варианты",
        "category": "Мышление",
    },
    "dbt_chain": {
        "title": "Цепочный анализ поведения (ДБТ)",
        "short": "Исследовать последовательность событий, реакций и последствий.",
        "description": "Карта контекста, звеньев цепочки и возможных точек вмешательства.",
        "keywords": "эмоции поведение дбт реакция событие цепочка",
        "category": "Эмоции",
    },
    "exposure": {
        "title": "Иерархия экспозиции",
        "short": "Составить лестницу ситуаций для постепенной практики.",
        "description": "Ситуации, прогнозы, посильные шаги и наблюдения.",
        "keywords": "тревога тревожность страх экспозиция ситуации практика",
        "category": "Тревожность",
    },
    "act_matrix": {
        "title": "ACT-матрица",
        "short": "Исследовать действия от дискомфорта и шаги к ценностям.",
        "description": "Визуальная карта внутреннего опыта, поведения и выбранных действий.",
        "keywords": "ценности дискомфорт действия мысли осознанность act",
        "category": "Самоосознание",
    },
}


# ---------------------------------------------------------------------
# Состояние приложения
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


def clear_searches():
    st.session_state.home_search = ""
    st.session_state.library_search = ""


def navigate(page, technique_id=None):
    current = {
        "page": st.session_state.page,
        "technique": st.session_state.selected_technique,
    }
    target = {"page": page, "technique": technique_id}

    if current != target:
        st.session_state.page_history.append(current)
        st.session_state.page_history = st.session_state.page_history[-30:]

    st.session_state.page = page
    st.session_state.selected_technique = technique_id


def go_home():
    clear_searches()
    navigate("home")


def go_library():
    clear_searches()
    navigate("library")


def go_about():
    clear_searches()
    navigate("about")


def go_back():
    clear_searches()
    if st.session_state.page_history:
        previous = st.session_state.page_history.pop()
        st.session_state.page = previous["page"]
        st.session_state.selected_technique = previous["technique"]
    else:
        st.session_state.page = "home"
        st.session_state.selected_technique = None


def open_technique(technique_id):
    navigate("technique", technique_id)


def search_techniques(query):
    query = " ".join((query or "").casefold().split())
    if not query:
        return list(TECHNIQUES.items())

    words = query.split()
    results = []

    for technique_id, technique in TECHNIQUES.items():
        searchable = " ".join(
            [
                technique["title"],
                technique["short"],
                technique["description"],
                technique["keywords"],
                technique["category"],
            ]
        ).casefold()

        if all(word in searchable for word in words):
            results.append((technique_id, technique))

    return results


# ---------------------------------------------------------------------
# Стили
# ---------------------------------------------------------------------

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700;800&display=swap');

    :root {{
        color-scheme: light !important;
    }}

    html, body, [data-testid="stAppViewContainer"] {{
        color-scheme: light !important;
        background-color: #F3F9FD !important;
        color: #294A65 !important;
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background-image:
            radial-gradient(ellipse at 10% 5%, rgba(196,228,248,.58), transparent 34%),
            radial-gradient(ellipse at 92% 18%, rgba(219,239,251,.68), transparent 36%);
    }}

    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        opacity: .56;
        background-image: url("data:image/svg+xml,{neuron_background}");
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
        max-width: 1160px;
        padding-top: 1rem;
        padding-bottom: 4rem;
    }}

    h1, h2, h3, h4, p, label, button, input, textarea, select {{
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }}

    h1, h2, h3, h4 {{
        color: #294A65 !important;
        letter-spacing: -0.025em;
    }}

    h1 {{ font-size: 2.5rem !important; font-weight: 800 !important; }}
    h2 {{ font-size: 1.8rem !important; font-weight: 800 !important; }}
    h3 {{ font-size: 1.25rem !important; font-weight: 800 !important; }}

    p, label, [data-testid="stCaptionContainer"], [data-testid="stMarkdownContainer"] {{
        color: #476B85 !important;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        border: 1px solid #C9DFEF !important;
        border-radius: 18px !important;
        background: rgba(248,252,255,.94) !important;
        box-shadow: 0 8px 22px rgba(62,112,148,.06);
    }}

    [data-testid="stTextInput"] [data-baseweb="input"],
    [data-testid="stTextArea"] [data-baseweb="textarea"],
    [data-testid="stNumberInput"] [data-baseweb="input"],
    [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    [data-baseweb="input"],
    [data-baseweb="textarea"] {{
        color-scheme: light !important;
        background: #FFFFFF !important;
        border: 1px solid #C9DDEB !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }}

    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] input,
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
        -webkit-text-fill-color: #7893A8 !important;
        opacity: 1 !important;
    }}

    .stButton > button {{
        min-height: 44px;
        border: 1px solid #AFCFE2 !important;
        border-radius: 13px !important;
        background: #F1F8FD !important;
        color: #315773 !important;
        font-size: .98rem;
        font-weight: 700;
        transition: .18s ease;
    }}

    .stButton > button:hover:not(:disabled) {{
        border-color: #6EA7CB !important;
        background: #E0F0FA !important;
        color: #234D6B !important;
        transform: translateY(-1px);
    }}

    .stButton > button:disabled {{
        opacity: .45;
    }}

    .stButton > button[kind="primary"] {{
        min-height: 50px;
        border: 1px solid #6EA7CB !important;
        border-radius: 14px !important;
        background: linear-gradient(135deg, #D9EEFA, #E5F3FC) !important;
        color: #234D6B !important;
        font-weight: 800;
    }}

    [data-testid="stAlert"] {{
        border: 1px solid #BCD9EB !important;
        border-radius: 14px !important;
        background: #EAF5FC !important;
    }}

    [data-testid="stMetric"] {{
        border: 1px solid #C9DFEF;
        border-radius: 16px;
        background: rgba(248,252,255,.96);
        padding: 14px;
    }}

    hr {{
        border-color: #D7E6F0 !important;
    }}

    .site-header {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 7px 0 16px;
        margin-bottom: 10px;
        border-bottom: 1px solid #D7E6F0;
    }}

    .brand-name {{
        color: #234D6B;
        font-size: clamp(1.7rem, 3vw, 2.25rem);
        font-weight: 800;
        line-height: 1.05;
        letter-spacing: -.045em;
        white-space: nowrap;
    }}

    .brand-fallback {{
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #BBD9EB;
        border-radius: 12px;
        background: rgba(255,255,255,.65);
    }}

    .hero {{
        position: relative;
        display: flex;
        align-items: center;
        min-height: 340px;
        overflow: hidden;
        padding: 38px 44px;
        margin: 20px 0 22px;
        border: 1px solid #D3E5F2;
        border-radius: 28px;
        background:
            radial-gradient(circle at 79% 42%, rgba(174,222,241,.66) 0 18%, transparent 18.5%),
            linear-gradient(110deg, #F8FCFF 0%, #EAF5FC 100%);
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
        letter-spacing: -.05em;
    }}

    .hero-subtitle {{
        max-width: 490px;
        margin: 12px 0 18px;
        color: #294A65;
        font-size: clamp(1.25rem, 2.5vw, 1.85rem);
        font-weight: 700;
        line-height: 1.3;
    }}

    .hero-description {{
        max-width: 460px;
        color: #476B85;
        font-size: 1.05rem;
        line-height: 1.6;
    }}

    .hero-art {{
        position: absolute;
        top: 50%;
        right: 3%;
        width: min(42%, 430px);
        transform: translateY(-50%);
        opacity: .78;
    }}

    .section-title {{
        margin: 28px 0 12px;
        color: #294A65;
        font-size: 1.7rem;
        font-weight: 800;
    }}

    .category-card {{
        min-height: 125px;
        padding: 17px;
        border: 1px solid #D3E3EF;
        border-radius: 18px;
        background: rgba(248,252,255,.94);
    }}

    .category-title {{
        color: #294A65;
        font-size: 1.04rem;
        font-weight: 800;
    }}

    .category-description {{
        margin-top: 7px;
        color: #648198;
        font-size: .9rem;
        line-height: 1.45;
    }}

    @media (max-width: 700px) {{
        .hero {{
            min-height: 290px;
            padding: 25px 22px;
        }}

        .hero-art {{
            right: -10%;
            width: 58%;
            opacity: .2;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# Шапка
# ---------------------------------------------------------------------

def render_header():
    brand_col, home_col, library_col, about_col, back_col = st.columns(
        [2.3, 1, 1.25, 1.1, 1]
    )

    with brand_col:
        logo_col, name_col = st.columns([0.6, 3.4])

        with logo_col:
            if LOGO_PATH.is_file():
                st.image(str(LOGO_PATH), width=42)
            else:
                st.markdown(
                    """
                    <div class="brand-fallback">
                      <svg width="30" height="30" viewBox="0 0 30 30"
                           xmlns="http://www.w3.org/2000/svg">
                        <g fill="none" stroke="#315773" stroke-width="1.5"
                           stroke-linecap="round">
                          <path d="M14.8 5.2c-4-3-8 0-7.5 4-3.8 1.3-3.4 6.1-.3 7.4-2.2 3.2.3 6.5 3.7 5.1 1.3 3 4.5 2.6 5.3.2"/>
                          <path d="M15.2 5.2c4-3 8 0 7.5 4 3.8 1.3 3.4 6.1.3 7.4 2.2 3.2-.3 6.5-3.7 5.1-1.3 3-4.5 2.6-5.3.2"/>
                          <path d="M15 5v17M9 10c2 0 3 1 3 3m-5 3c2-.5 4 .5 4 2m10-8c-2 0-3 1-3 3m5 3c-2-.5-4 .5-4 2"/>
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
            "Назад",
            key="header_back",
            on_click=go_back,
            disabled=not st.session_state.page_history,
            use_container_width=True,
        )


# ---------------------------------------------------------------------
# Карточки техник
# ---------------------------------------------------------------------

def render_technique_cards(items, key_prefix):
    if not items:
        st.info("Ничего не найдено. Попробуйте изменить поисковый запрос.")
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
                    st.write(technique["short"])
                    st.caption(
                        f"{technique['category']} · {technique['description']}"
                    )
                    st.button(
                        "Открыть",
                        key=f"{key_prefix}_{technique_id}",
                        on_click=open_technique,
                        args=(technique_id,),
                        use_container_width=True,
                    )


# ---------------------------------------------------------------------
# Главная страница
# ---------------------------------------------------------------------

def render_home():
    st.markdown(
        """
        <section class="hero">
          <div class="hero-copy">
            <h1 class="hero-title">ПСИ-БЛОК</h1>
            <div class="hero-subtitle">
              Инструменты для глубокой психологической работы
            </div>
            <div class="hero-description">
              Библиотека психологических техник для специалистов и клиентов.
              Выбирайте инструмент и исследуйте важные вопросы в удобном темпе.
            </div>
          </div>

          <div class="hero-art" aria-hidden="true">
            <svg viewBox="0 0 440 300" xmlns="http://www.w3.org/2000/svg">
              <path d="M225 18 C155 8 100 48 89 108 C81 151 99 180 72 204
                       C61 214 48 225 51 234 C55 244 73 246 82 250
                       C89 254 85 265 94 269 C105 275 119 269 126 282
                       C132 294 154 296 176 289 L225 278"
                    fill="none" stroke="#5B87A2" stroke-width="3"
                    stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M222 22 C292 17 347 55 356 113 C362 154 343 185 373 212
                       C390 228 412 233 411 244 C410 254 390 260 382 270
                       C374 280 362 291 341 289 L226 278"
                    fill="none" stroke="#5B87A2" stroke-width="3"
                    stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M223 54 C194 33 163 47 162 72 C133 75 132 108 154 119
                       C139 141 159 162 181 156 C188 179 215 178 226 160
                       C240 180 267 173 271 151 C297 151 305 124 287 108
                       C300 84 281 60 258 64 C251 47 236 46 223 54Z"
                    fill="none" stroke="#5B87A2" stroke-width="2.5"
                    stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M222 55 L222 159
                       M162 73 C183 83 187 101 181 117
                       M258 64 C242 79 242 96 254 109
                       M154 119 C174 117 187 127 181 156
                       M287 108 C264 111 253 127 271 151
                       M188 78 C204 88 206 105 196 119
                       M239 78 C222 90 223 108 239 118
                       M201 140 C212 130 225 131 234 143"
                    fill="none" stroke="#5B87A2" stroke-width="2"
                    stroke-linecap="round"/>
              <ellipse cx="224" cy="150" rx="190" ry="76"
                       transform="rotate(-12 224 150)"
                       fill="none" stroke="#76A6C0" stroke-width="2"/>
            </svg>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    action_col, about_col, _ = st.columns([1.7, 1.2, 3.5])
    with action_col:
        st.button(
            "Перейти в библиотеку",
            key="home_library_button",
            type="primary",
            on_click=go_library,
            use_container_width=True,
        )

    with about_col:
        st.button(
            "Узнать больше",
            key="home_about_button",
            on_click=go_about,
            use_container_width=True,
        )

    st.markdown(
        '<div class="section-title">Найти технику</div>',
        unsafe_allow_html=True,
    )

    query = st.text_input(
        "Поиск по техникам",
        key="home_search",
        placeholder="Например: тревожность, самооценка, выбор...",
        label_visibility="collapsed",
    )

    if query.strip():
        st.markdown("#### Результаты поиска")
        render_technique_cards(
            search_techniques(query),
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
    render_technique_cards(list(TECHNIQUES.items())[:2], "home_featured")

    st.markdown(
        '<div class="section-title">ПСИ-БЛОК — ваш помощник</div>',
        unsafe_allow_html=True,
    )
    st.info(
        "Инструменты помогают структурировать совместную работу и обсуждение. "
        "Они не заменяют профессиональную психологическую помощь."
    )


# ---------------------------------------------------------------------
# Библиотека
# ---------------------------------------------------------------------

def render_library():
    st.title("Библиотека техник")
    st.write("Ищите по названию, теме или описанию техники.")

    query = st.text_input(
        "Поиск по библиотеке",
        key="library_search",
        placeholder="Например: тревожность, поведение, выбор...",
        label_visibility="collapsed",
    )

    render_technique_cards(
        search_techniques(query),
        "library_result",
    )


# ---------------------------------------------------------------------
# Раздел О проекте
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
                if photo_path.is_file():
                    st.image(str(photo_path), use_container_width=True)
                else:
                    st.markdown(
                        """
                        <div style="
                            height:220px;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            border-radius:14px;
                            background:linear-gradient(135deg,#DDEFFA,#F2F8FC);
                            color:#5F86A0;">
                            Фото разработчика
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown(f"**{html.escape(person['name'])}**")
                st.caption(person["role"])


# ---------------------------------------------------------------------
# Техника: дерево решений
# ---------------------------------------------------------------------

def render_decision_tree():
    st.title("Дерево решений")
    st.write("Сравните варианты решения и возможные последствия.")

    question = st.text_input(
        "Какое решение нужно принять?",
        key="decision_question",
        placeholder="Например: Стоит ли менять работу?",
    )

    option_count = st.number_input(
        "Количество вариантов",
        min_value=2,
        max_value=5,
        value=2,
        step=1,
        key="decision_option_count",
    )

    results = []
    for index in range(int(option_count)):
        with st.container(border=True):
            st.markdown(f"### Вариант {index + 1}")
            name = st.text_input(
                "Название варианта",
                key=f"decision_name_{index}",
                placeholder=f"Вариант {index + 1}",
            )
            outcome = st.text_area(
                "Последствия",
                key=f"decision_outcome_{index}",
                placeholder="Что может произойти?",
            )
            probability = st.slider(
                "Вероятность, %",
                min_value=0,
                max_value=100,
                value=50,
                key=f"decision_probability_{index}",
            )
            score = st.slider(
                "Оценка исхода",
                min_value=-5.0,
                max_value=5.0,
                value=0.0,
                step=0.5,
                key=f"decision_score_{index}",
            )

        results.append(
            {
                "name": name,
                "outcome": outcome,
                "probability": probability,
                "score": score,
            }
        )

    if st.button(
        "Рассчитать и сравнить",
        key="decision_calculate",
        type="primary",
        use_container_width=True,
    ):
        if not question.strip():
            st.warning("Сначала сформулируйте решение.")
            return

        if any(not option["name"].strip() for option in results):
            st.warning("Введите название каждого варианта.")
            return

        evaluated = [
            option["score"] * option["probability"] / 100
            for option in results
        ]

        st.subheader("Сравнение вариантов")
        columns = st.columns(len(results))
        best_index = max(range(len(evaluated)), key=evaluated.__getitem__)

        for idx, (column, option, value) in enumerate(
            zip(columns, results, evaluated)
        ):
            with column:
                label = option["name"]
                if idx == best_index:
                    label = "Лидер: " + label
                st.metric(label, f"{value:.2f} / 5")
                st.caption(option["outcome"] or "Последствия не указаны.")

        st.info(
            "Расчёт — ориентир для обсуждения, а не автоматическое решение."
        )


# ---------------------------------------------------------------------
# Техника: цепочный анализ поведения
# ---------------------------------------------------------------------

def render_chain():
    st.title("Цепочный анализ поведения (ДБТ)")
    st.write("Исследуйте контекст, реакции, поведение и последствия.")
    st.info("Можно пропустить любое поле или остановиться в любой момент.")

    vulnerability = st.text_area(
        "Факторы уязвимости",
        key="chain_vulnerability",
        placeholder="Что могло сделать ситуацию сложнее заранее?",
    )
    trigger = st.text_area(
        "Запускающее событие",
        key="chain_trigger",
        placeholder="Что произошло непосредственно перед реакцией?",
    )
    links = st.text_area(
        "Звенья цепочки",
        key="chain_links",
        placeholder="Опишите по порядку мысли, эмоции, ощущения и действия.",
        height=160,
    )
    target = st.text_area("Целевое поведение", key="chain_target")

    left_col, right_col = st.columns(2)
    with left_col:
        immediate = st.text_area("Последствия сразу после", key="chain_immediate")
    with right_col:
        later = st.text_area("Последствия позднее", key="chain_later")

    alternative = st.text_area(
        "Возможная точка вмешательства или поддержка",
        key="chain_alternative",
    )

    with st.expander("Показать сводку", expanded=True):
        for title, value in [
            ("Факторы уязвимости", vulnerability),
            ("Запускающее событие", trigger),
            ("Звенья цепочки", links),
            ("Целевое поведение", target),
            ("Последствия сразу после", immediate),
            ("Последствия позднее", later),
            ("Возможная поддержка", alternative),
        ]:
            st.markdown(f"**{title}**")
            st.write(value or "—")


# ---------------------------------------------------------------------
# Техника: иерархия экспозиции
# ---------------------------------------------------------------------

def render_exposure():
    st.title("Иерархия экспозиции")
    st.write("Составьте лестницу ситуаций для обсуждения и планирования практики.")
    st.info(
        "Практика должна быть добровольной и согласованной со специалистом. "
        "Не используйте упражнение для ситуаций с реальной опасностью."
    )

    goal = st.text_area("Цель работы", key="exposure_goal")
    count = st.number_input(
        "Количество ступеней",
        min_value=1,
        max_value=10,
        value=3,
        step=1,
        key="exposure_count",
    )

    steps = []
    for index in range(int(count)):
        with st.container(border=True):
            st.markdown(f"### Ступень {index + 1}")
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
            prediction = st.text_area(
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

    completed = [step for step in steps if step["situation"].strip()]
    completed.sort(key=lambda step: step["distress"])

    st.subheader("Лестница по ожидаемой тревоге")
    if not completed:
        st.caption("Заполните описание хотя бы одной ситуации.")
        return

    for index, step in enumerate(completed, start=1):
        with st.container(border=True):
            st.markdown(
                f"**{index}. {step['situation']}** — "
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

    left_col, right_col = st.columns(2)
    with left_col:
        with st.container(border=True):
            st.markdown("### Действия от дискомфорта")
            away = st.text_area(
                "Что вы делаете, чтобы избежать дискомфорта?",
                key="act_away",
            )
        with st.container(border=True):
            st.markdown("### Внутренний опыт")
            inner = st.text_area(
                "Мысли, эмоции, телесные ощущения",
                key="act_inner",
            )

    with right_col:
        with st.container(border=True):
            st.markdown("### Действия к важному")
            toward = st.text_area(
                "Какое действие приближает к важному?",
                key="act_toward",
            )
        with st.container(border=True):
            st.markdown("### Внутренний опыт при этом шаге")
            toward_inner = st.text_area(
                "Что может возникать внутри?",
                key="act_toward_inner",
            )

    step = st.text_area("Небольшой выбранный шаг", key="act_step")

    st.subheader("Сводка")
    st.write(f"**Ситуация:** {situation or '—'}")
    st.write(f"**Что важно:** {values or '—'}")

    summary_left, summary_right = st.columns(2)
    with summary_left:
        st.markdown("**Действия от дискомфорта**")
        st.write(away or "—")
        st.markdown("**Внутренний опыт**")
        st.write(inner or "—")

    with summary_right:
        st.markdown("**Действия к важному**")
        st.write(toward or "—")
        st.markdown("**Внутренний опыт при этом шаге**")
        st.write(toward_inner or "—")

    st.markdown("**Небольшой выбранный шаг**")
    st.write(step or "—")


# ---------------------------------------------------------------------
# Открытая техника
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
# Запуск приложения
# ---------------------------------------------------------------------

render_header()

if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "library":
    render_library()
elif st.session_state.page == "about":
    render_about()
elif st.session_state.page == "technique":
    render_selected_technique()
else:
    st.session_state.page = "home"
    render_home()
