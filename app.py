import html
import uuid
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="ПСИ-БЛОК",
    page_icon="favicon.jpg",
    layout="wide",
)


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
        "short": "Исследовать действия «от дискомфорта» и шаги «к ценностям».",
        "description": "Карта внутреннего опыта, поведения и выбранных действий.",
        "keywords": "ценности дискомфорт действия мысли осознанность act",
        "category": "Самоосознание",
    },
}


# ---------------------------------------------------------------------
# Состояние и навигация
# ---------------------------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_technique" not in st.session_state:
    st.session_state.selected_technique = None

if "page_history" not in st.session_state:
    st.session_state.page_history = []

if "home_search_result" not in st.session_state:
    st.session_state.home_search_result = None

if "library_search_result" not in st.session_state:
    st.session_state.library_search_result = None


def navigate(page, technique_id=None):
    current_page = st.session_state.page
    current_technique = st.session_state.selected_technique

    if current_page != page or current_technique != technique_id:
        st.session_state.page_history.append(
            {
                "page": current_page,
                "selected_technique": current_technique,
            }
        )
        st.session_state.page_history = st.session_state.page_history[-30:]

    st.session_state.page = page
    st.session_state.selected_technique = technique_id


def go_back():
    if st.session_state.page_history:
        previous = st.session_state.page_history.pop()
        st.session_state.page = previous["page"]
        st.session_state.selected_technique = previous["selected_technique"]
    else:
        st.session_state.page = "home"
        st.session_state.selected_technique = None


def go_home():
    navigate("home")


def go_library():
    navigate("library")


def go_about():
    navigate("about")


def open_technique(technique_id):
    navigate("technique", technique_id)


# ---------------------------------------------------------------------
# Поиск
# ---------------------------------------------------------------------

def search_techniques(query):
    """Ищет по названию, описаниям, категории и ключевым словам."""
    query = " ".join((query or "").casefold().split())

    if not query:
        return list(TECHNIQUES.items())

    words = query.split()
    matches = []

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

        # Все слова запроса должны присутствовать в карточке.
        if all(word in searchable for word in words):
            matches.append((technique_id, technique))

    return matches


def submit_home_search():
    st.session_state.home_search_result = st.session_state.home_search_input.strip()


def submit_library_search():
    st.session_state.library_search_result = (
        st.session_state.library_search_input.strip()
    )


# ---------------------------------------------------------------------
# Общие стили
# ---------------------------------------------------------------------

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700;800&display=swap'
    );

    :root {
        color-scheme: light;
    }

    html, body, [data-testid="stAppViewContainer"] {
        color-scheme: light !important;
        background-color: #F3F9FD !important;
        color: #294A65 !important;
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }

    [data-testid="stAppViewContainer"] {
        background-image:
            radial-gradient(
                ellipse at 10% 5%,
                rgba(196, 228, 248, .58),
                transparent 34%
            ),
            radial-gradient(
                ellipse at 92% 18%,
                rgba(219, 239, 251, .68),
                transparent 36%
            );
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    .block-container {
        max-width: 1160px;
        padding-top: 1rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3, h4, p, label, button, input, textarea, select {
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }

    h1, h2, h3, h4 {
        color: #294A65 !important;
        letter-spacing: -0.025em;
    }

    h1 {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
    }

    h2 {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
    }

    h3 {
        font-size: 1.25rem !important;
        font-weight: 800 !important;
    }

    p, label, [data-testid="stCaptionContainer"],
    [data-testid="stMarkdownContainer"] {
        color: #476B85 !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #C9DFEF !important;
        border-radius: 18px !important;
        background: rgba(248, 252, 255, .96) !important;
        box-shadow: 0 8px 22px rgba(62, 112, 148, .06);
    }

    [data-testid="stTextInput"] [data-baseweb="input"],
    [data-testid="stTextArea"] [data-baseweb="textarea"],
    [data-testid="stNumberInput"] [data-baseweb="input"],
    [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    [data-baseweb="input"],
    [data-baseweb="textarea"] {
        color-scheme: light !important;
        background: #FFFFFF !important;
        border: 1px solid #C9DDEB !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }

    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] input,
    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea {
        color: #294A65 !important;
        background: #FFFFFF !important;
        -webkit-text-fill-color: #294A65 !important;
        border: 0 !important;
        box-shadow: none !important;
        outline: none !important;
        caret-color: #315773 !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #7893A8 !important;
        -webkit-text-fill-color: #7893A8 !important;
        opacity: 1 !important;
    }

    [data-baseweb="select"] span,
    [data-baseweb="menu"] li {
        color: #294A65 !important;
    }

    [data-baseweb="popover"],
    [data-baseweb="menu"] {
        color-scheme: light !important;
        background: #FFFFFF !important;
    }

    .stButton > button {
        min-height: 44px;
        border: 1px solid #AFCFE2 !important;
        border-radius: 13px !important;
        background: #F1F8FD !important;
        color: #315773 !important;
        font-size: .98rem;
        font-weight: 700;
        transition: .18s ease;
    }

    .stButton > button:hover:not(:disabled) {
        border-color: #6EA7CB !important;
        background: #E0F0FA !important;
        color: #234D6B !important;
        transform: translateY(-1px);
    }

    .stButton > button:disabled {
        opacity: .48;
    }

    .stButton > button[kind="primary"] {
        border-color: #6EA7CB !important;
        background: linear-gradient(135deg, #D9EEFA, #E5F3FC) !important;
        color: #234D6B !important;
        font-weight: 800;
    }

    [data-testid="stAlert"] {
        border: 1px solid #BCD9EB !important;
        border-radius: 14px !important;
        background: #EAF5FC !important;
        color: #315773 !important;
    }

    [data-testid="stAlert"] * {
        color: #315773 !important;
    }

    [data-testid="stMetric"] {
        border: 1px solid #C9DFEF;
        border-radius: 16px;
        background: rgba(248, 252, 255, .96);
        padding: 14px;
    }

    hr {
        border-color: #D7E6F0 !important;
    }

    .site-header {
        display: flex;
        align-items: center;
        gap: 24px;
        padding: 8px 0 14px;
        margin-bottom: 20px;
        border-bottom: 1px solid #D7E6F0;
    }

    .site-brand {
        color: #234D6B;
        font-size: 1.55rem;
        line-height: 1;
        font-weight: 800;
        white-space: nowrap;
    }

    .site-brand-mark {
        display: inline-flex;
        width: 34px;
        height: 34px;
        align-items: center;
        justify-content: center;
        margin-right: 8px;
        border: 1px solid #BBD9EB;
        border-radius: 50%;
        color: #315773;
        font-size: .9rem;
        vertical-align: middle;
    }

    .hero {
        position: relative;
        display: flex;
        align-items: center;
        min-height: 340px;
        overflow: hidden;
        padding: 38px 44px;
        margin: 12px 0 22px;
        border: 1px solid #D3E5F2;
        border-radius: 28px;
        background:
            radial-gradient(
                circle at 78% 42%,
                rgba(178, 222, 241, .7) 0 18%,
                transparent 18.5%
            ),
            linear-gradient(110deg, #F8FCFF 0%, #EAF5FC 100%);
    }

    .hero-copy {
        position: relative;
        z-index: 1;
        max-width: 540px;
    }

    .hero-title {
        margin: 0;
        color: #214D6C;
        font-size: clamp(2.8rem, 6vw, 4.5rem);
        font-weight: 800;
        line-height: 1.04;
        letter-spacing: -.045em;
    }

    .hero-subtitle {
        max-width: 490px;
        margin: 14px 0;
        color: #294A65;
        font-size: clamp(1.25rem, 2.6vw, 1.8rem);
        font-weight: 700;
        line-height: 1.3;
    }

    .hero-description {
        max-width: 470px;
        color: #476B85;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    .hero-art {
        position: absolute;
        top: 50%;
        right: 3%;
        width: min(42%, 430px);
        transform: translateY(-50%);
        opacity: .82;
    }

    .section-title {
        margin: 28px 0 12px;
        color: #294A65;
        font-size: 1.7rem;
        font-weight: 800;
    }

    .category-card {
        min-height: 130px;
        padding: 17px;
        border: 1px solid #D3E3EF;
        border-radius: 18px;
        background: rgba(248, 252, 255, .94);
    }

    .category-title {
        color: #294A65;
        font-size: 1.05rem;
        font-weight: 800;
    }

    .category-description {
        margin-top: 7px;
        color: #648198;
        font-size: .9rem;
        line-height: 1.45;
    }

    @media (max-width: 700px) {
        .site-header {
            flex-wrap: wrap;
            gap: 10px;
        }

        .hero {
            min-height: 290px;
            padding: 26px 22px;
        }

        .hero-art {
            right: -9%;
            width: 55%;
            opacity: .2;
        }
    }

    .developer-name {
        margin-top: 12px;
        color: #294A65;
        font-size: 1.1rem;
        font-weight: 800;
        text-align: center;
    }

    .developer-role {
        color: #648198;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# Шапка и карточки
# ---------------------------------------------------------------------

def render_header():
    brand_col, home_col, library_col, about_col, back_col = st.columns(
        [2.4, 1, 1.2, 1.2, 1]
    )

    with brand_col:
        st.markdown(
            '<div class="site-brand">'
            '<span class="site-brand-mark">П</span>ПСИ-БЛОК'
            '</div>',
            unsafe_allow_html=True,
        )

    with home_col:
        st.button(
            "Главная",
            key="nav_home",
            on_click=go_home,
            use_container_width=True,
        )

    with library_col:
        st.button(
            "Библиотека",
            key="nav_library",
            on_click=go_library,
            use_container_width=True,
        )

    with about_col:
        st.button(
            "О проекте",
            key="nav_about",
            on_click=go_about,
            use_container_width=True,
        )

    with back_col:
        st.button(
            "← Назад",
            key="nav_back",
            on_click=go_back,
            disabled=not st.session_state.page_history,
            use_container_width=True,
        )


def render_technique_cards(items, key_prefix):
    if not items:
        st.info("Ничего не найдено. Попробуйте изменить запрос.")
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
                        "Открыть технику →",
                        key=f"{key_prefix}_{technique_id}",
                        on_click=open_technique,
                        args=(technique_id,),
                        use_container_width=True,
                    )


# ---------------------------------------------------------------------
# Главная и библиотека
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
                    <path d="M225 18
                        C155 8 100 48 89 108
                        C81 151 99 180 72 204
                        C61 214 48 225 51 234
                        C55 244 73 246 82 250
                        C89 254 85 265 94 269
                        C105 275 119 269 126 282
                        C132 294 154 296 176 289
                        L225 278"
                        fill="none" stroke="#5B87A2" stroke-width="3"
                        stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M222 22
                        C292 17 347 55 356 113
                        C362 154 343 185 373 212
                        C390 228 412 233 411 244
                        C410 254 390 260 382 270
                        C374 280 362 291 341 289
                        L226 278"
                        fill="none" stroke="#5B87A2" stroke-width="3"
                        stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M223 54
                        C194 33 163 47 162 72
                        C133 75 132 108 154 119
                        C139 141 159 162 181 156
                        C188 179 215 178 226 160
                        C240 180 267 173 271 151
                        C297 151 305 124 287 108
                        C300 84 281 60 258 64
                        C251 47 236 46 223 54Z"
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
            on_click=go_about,
            use_container_width=True,
        )

    st.markdown(
        '<div class="section-title">Найти технику</div>',
        unsafe_allow_html=True,
    )

    # Форма отправляет введённый текст в Streamlit по кнопке.
    with st.form("home_search_form"):
        search_col, button_col = st.columns([6, 1.2])

        with search_col:
            st.text_input(
                "Поиск по техникам",
                key="home_search_input",
                placeholder=(
                    "Например: тревожность, самооценка, выбор..."
                ),
                label_visibility="collapsed",
            )

        with button_col:
            st.form_submit_button(
                "Найти",
                on_click=submit_home_search,
                use_container_width=True,
            )

    if st.session_state.home_search_result is not None:
        query = st.session_state.home_search_result

        if query:
            st.markdown("#### Результаты поиска")
            render_technique_cards(
                search_techniques(query),
                "home_search_result",
            )
        else:
            st.caption("Введите слово или фразу для поиска.")
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
        '<div class="section-title">ПСИ-БЛОК — ваш помощник</div>',
        unsafe_allow_html=True,
    )
    st.info(
        "Инструменты помогают структурировать совместную работу и обсуждение. "
        "Они не заменяют профессиональную психологическую помощь."
    )


def render_library():
    st.title("Библиотека техник")
    st.write("Ищите по названию, теме или описанию техники.")

    with st.form("library_search_form"):
        search_col, button_col = st.columns([6, 1.2])

        with search_col:
            st.text_input(
                "Поиск по библиотеке",
                key="library_search_input",
                placeholder=(
                    "Например: тревожность, поведение, выбор..."
                ),
                label_visibility="collapsed",
            )

        with button_col:
            st.form_submit_button(
                "Найти",
                on_click=submit_library_search,
                use_container_width=True,
            )

    query = st.session_state.library_search_result or ""
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
        key="decision_question",
        placeholder="Например: «Стоит ли менять работу?»",
    )

    st.caption(
        "Добавьте варианты, исходы, их вероятности и личную оценку."
    )

    options = []
    option_count = st.number_input(
        "Количество вариантов",
        min_value=2,
        max_value=5,
        value=2,
        step=1,
        key="decision_option_count",
    )

    for option_index in range(int(option_count)):
        with st.container(border=True):
            st.markdown(f"### Вариант {option_index + 1}")
            name = st.text_input(
                "Название варианта",
                key=f"decision_option_name_{option_index}",
                placeholder=f"Вариант {option_index + 1}",
            )

            scenario_count = st.number_input(
                "Количество возможных исходов",
                min_value=1,
                max_value=5,
                value=2,
                step=1,
                key=f"decision_scenario_count_{option_index}",
            )

            scenarios = []
            for scenario_index in range(int(scenario_count)):
                st.markdown(f"**Исход {scenario_index + 1}**")
                scenario_name = st.text_input(
                    "Описание исхода",
                    key=f"decision_scenario_name_{option_index}_{scenario_index}",
                    placeholder="Что может произойти?",
                )

                probability_col, score_col = st.columns(2)
                with probability_col:
                    probability = st.slider(
                        "Вероятность, %",
                        min_value=0,
                        max_value=100,
                        value=50,
                        key=f"decision_probability_{option_index}_{scenario_index}",
                    )
                with score_col:
                    score = st.slider(
                        "Оценка исхода",
                        min_value=-5.0,
                        max_value=5.0,
                        value=0.0,
                        step=0.5,
                        key=f"decision_score_{option_index}_{scenario_index}",
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
        key="calculate_decision",
        type="primary",
        use_container_width=True,
    ):
        if not question.strip():
            st.warning("Сначала сформулируйте решение.")
            return

        results = []
        validation_error = None

        for option_index, option in enumerate(options, start=1):
            if not option["name"].strip():
                validation_error = f"Введите название варианта {option_index}."
                break

            if any(not item["name"].strip() for item in option["scenarios"]):
                validation_error = (
                    f"Заполните все исходы варианта {option_index}."
                )
                break

            probability_total = sum(
                item["probability"] for item in option["scenarios"]
            )
            if probability_total == 0:
                validation_error = (
                    f"Задайте ненулевую вероятность для варианта {option_index}."
                )
                break

            score = sum(
                item["probability"] / probability_total * item["score"]
                for item in option["scenarios"]
            )

            results.append(
                {
                    "name": option["name"],
                    "score": score,
                    "scenarios": option["scenarios"],
                }
            )

        if validation_error:
            st.warning(validation_error)
            return

        best = max(results, key=lambda item: item["score"])
        st.subheader("Сравнение")
        result_columns = st.columns(len(results))

        for column, result in zip(result_columns, results):
            with column:
                st.metric(
                    result["name"],
                    f"{result['score']:.2f} / 5",
                    "Наивысшая оценка" if result is best else None,
                )

        st.info(
            "Расчёт — только опора для обсуждения, а не автоматическое "
            "решение. Вероятности каждого варианта нормализуются отдельно."
        )


# ---------------------------------------------------------------------
# Цепочный анализ поведения
# ---------------------------------------------------------------------

def render_chain():
    st.title("Цепочный анализ поведения (ДБТ)")
    st.write("Исследуйте контекст, реакции, поведение и последствия.")
    st.info(
        "Можно пропустить любое поле или остановиться в любой момент."
    )

    vulnerability = st.text_area(
        "Факторы уязвимости",
        key="chain_vulnerability",
        placeholder="Что могло сделать ситуацию сложнее заранее?",
    )
    prompting = st.text_area(
        "Запускающее событие",
        key="chain_prompt",
        placeholder="Что произошло непосредственно перед реакцией?",
    )

    link_count = st.number_input(
        "Количество звеньев цепочки",
        min_value=1,
        max_value=10,
        value=3,
        step=1,
        key="chain_link_count",
    )

    links = []
    for index in range(int(link_count)):
        with st.container(border=True):
            st.markdown(f"### Звено {index + 1}")
            left, right = st.columns(2)

            with left:
                thought = st.text_area(
                    "Мысли или образы",
                    key=f"chain_thought_{index}",
                )
                emotion = st.text_area(
                    "Эмоции",
                    key=f"chain_emotion_{index}",
                )

            with right:
                body = st.text_area(
                    "Ощущения в теле",
                    key=f"chain_body_{index}",
                )
                action = st.text_area(
                    "Импульсы или действия",
                    key=f"chain_action_{index}",
                )

            intensity = st.slider(
                "Интенсивность",
                min_value=0,
                max_value=10,
                value=0,
                key=f"chain_intensity_{index}",
            )

        links.append(
            {
                "thought": thought,
                "emotion": emotion,
                "body": body,
                "action": action,
                "intensity": intensity,
            }
        )

    target = st.text_area(
        "Целевое поведение",
        key="chain_target",
    )

    immediate_col, later_col = st.columns(2)
    with immediate_col:
        immediate = st.text_area(
            "Последствия сразу после",
            key="chain_immediate",
        )
    with later_col:
        later = st.text_area(
            "Последствия позднее",
            key="chain_later",
        )

    support = st.text_area(
        "Поддержка или альтернативный шаг",
        key="chain_support",
    )

    with st.expander("Показать сводку"):
        st.markdown("**Факторы уязвимости**")
        st.write(vulnerability or "—")
        st.markdown("**Запускающее событие**")
        st.write(prompting or "—")

        for index, link in enumerate(links, start=1):
            st.markdown(f"**Звено {index}**")
            st.write(
                f"Мысли: {link['thought'] or '—'} · "
                f"Эмоции: {link['emotion'] or '—'} · "
                f"Ощущения: {link['body'] or '—'} · "
                f"Действия: {link['action'] or '—'} · "
                f"Интенсивность: {link['intensity']}/10"
            )

        st.markdown("**Целевое поведение**")
        st.write(target or "—")
        st.markdown("**Последствия сразу после**")
        st.write(immediate or "—")
        st.markdown("**Последствия позднее**")
        st.write(later or "—")
        st.markdown("**Поддержка или альтернативный шаг**")
        st.write(support or "—")


# ---------------------------------------------------------------------
# Иерархия экспозиции
# ---------------------------------------------------------------------

def render_exposure():
    st.title("Иерархия экспозиции")
    st.write(
        "Составьте лестницу ситуаций для обсуждения и планирования практики."
    )
    st.info(
        "Практика должна быть добровольной и согласованной со специалистом. "
        "Не используйте упражнение для ситуаций с реальной опасностью."
    )

    goal = st.text_area(
        "Цель работы",
        key="exposure_goal",
    )

    step_count = st.number_input(
        "Количество ступеней",
        min_value=1,
        max_value=12,
        value=3,
        step=1,
        key="exposure_step_count",
    )

    steps = []
    for index in range(int(step_count)):
        with st.container(border=True):
            st.markdown(f"### Ступень {index + 1}")
            situation = st.text_area(
                "Ситуация",
                key=f"exposure_situation_{index}",
                placeholder="Опишите ситуацию.",
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
            status = st.selectbox(
                "Статус",
                ["Не обсуждали", "Обсудили", "Запланировали", "Попробовали"],
                key=f"exposure_status_{index}",
            )

        steps.append(
            {
                "situation": situation,
                "distress": distress,
                "prediction": prediction,
                "plan": plan,
                "status": status,
            }
        )

    st.subheader("Лестница по ожидаемой тревоге")
    st.write(f"**Цель:** {goal or '—'}")

    ordered_steps = sorted(
        enumerate(steps, start=1),
        key=lambda pair: (pair[1]["distress"], pair[0]),
    )

    visible_steps = [
        (position, step)
        for position, step in ordered_steps
        if step["situation"].strip()
    ]

    if not visible_steps:
        st.caption("Заполните описание хотя бы одной ситуации.")
        return

    for position, (_, step) in enumerate(visible_steps, start=1):
        with st.container(border=True):
            st.markdown(
                f"**{position}. {step['situation']}** — "
                f"тревога {step['distress']}/10"
            )
            st.caption(f"Статус: {step['status']}")
            if step["prediction"]:
                st.write(f"**Прогноз:** {step['prediction']}")
            if step["plan"]:
                st.write(f"**Посильный шаг:** {step['plan']}")


# ---------------------------------------------------------------------
# ACT-матрица
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
            st.markdown("### Действия «от дискомфорта»")
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
            st.markdown("### Действия «к важному»")
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

    step = st.text_area(
        "Небольшой выбранный шаг",
        key="act_step",
    )

    st.subheader("Сводка")
    st.write(f"**Ситуация:** {situation or '—'}")
    st.write(f"**Что важно:** {values or '—'}")

    summary_left, summary_right = st.columns(2)
    with summary_left:
        st.markdown("**От дискомфорта**")
        st.write(away or "—")
        st.markdown("**Внутренний опыт**")
        st.write(inner or "—")

    with summary_right:
        st.markdown("**К важному**")
        st.write(toward or "—")
        st.markdown("**Внутренний опыт при шаге**")
        st.write(toward_inner or "—")

    st.markdown("**Небольшой выбранный шаг**")
    st.write(step or "—")


# ---------------------------------------------------------------------
# О проекте
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
                            color:#5F86A0;
                        ">
                            Фото разработчика
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"<div class='developer-name'>"
                    f"{html.escape(person['name'])}</div>"
                    f"<div class='developer-role'>"
                    f"{html.escape(person['role'])}</div>",
                    unsafe_allow_html=True,
                )


# ---------------------------------------------------------------------
# Открытая техника
# ---------------------------------------------------------------------

def render_selected_technique():
    technique_id = st.session_state.selected_technique

    if technique_id not in TECHNIQUES:
        st.warning("Техника не найдена.")
        st.button("Вернуться в библиотеку", on_click=go_library)
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
