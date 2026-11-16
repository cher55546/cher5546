import html
import textwrap
import uuid
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="ПСИ-БЛОК",
    page_icon="🌿",
    layout="wide",
)


# -------------------------------------------------------------------
# Оформление
# -------------------------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700;800&display=swap');

    .stApp {
        background:
            radial-gradient(ellipse at 10% 5%, rgba(196, 228, 248, .58), transparent 34%),
            radial-gradient(ellipse at 92% 18%, rgba(219, 239, 251, .72), transparent 36%),
            linear-gradient(145deg, #F5FAFE 0%, #EDF6FC 52%, #F8FBFE 100%);
        color: #294A65;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1120px;
        padding-top: 1.8rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3, h4, p, label, button, input, textarea {
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }

    h1, h2, h3, h4 {
        color: #294A65 !important;
        letter-spacing: -0.025em;
    }

    h1 {
        font-size: 2.8rem !important;
        font-weight: 800 !important;
    }

    h2 {
        font-size: 1.9rem !important;
        font-weight: 800 !important;
    }

    h3 {
        font-size: 1.35rem !important;
        font-weight: 800 !important;
    }

    p, label, [data-testid="stCaptionContainer"] {
        color: #54718A;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #D4E5F1 !important;
        border-radius: 20px !important;
        background: rgba(255,255,255,0.88) !important;
        box-shadow: 0 10px 26px rgba(62, 112, 148, 0.08);
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {
        border: 1px solid #C9DDEB;
        border-radius: 13px;
        background: #FFFFFF;
        color: #294A65;
    }

    .stButton > button {
        min-height: 48px;
        border: 1px solid #C1D8E9;
        border-radius: 14px;
        background: #F4F9FD;
        color: #315773;
        font-size: 1rem;
        font-weight: 700;
        transition: 0.18s ease;
    }

    .stButton > button:hover:not(:disabled) {
        border-color: #8FB9D5;
        background: #E8F4FC;
        color: #234D6B;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(61, 119, 158, 0.12);
    }

    .stButton > button[kind="primary"] {
        min-height: 58px;
        border: 1px solid #79AFCF;
        border-radius: 16px;
        background: linear-gradient(135deg, #D9EEFA, #E5F3FC);
        color: #234D6B;
        font-size: 1.12rem;
        font-weight: 800;
        box-shadow: 0 7px 18px rgba(61, 119, 158, 0.10);
    }

    [data-testid="stMetric"] {
        border: 1px solid #D4E5F1;
        border-radius: 17px;
        background: rgba(255,255,255,0.9);
        padding: 14px;
    }

    [data-testid="stAlert"] {
        border-radius: 15px;
    }

    hr {
        border-color: #D4E5F1;
    }

    .hero {
        position: relative;
        overflow: hidden;
        min-height: 355px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 55px 28px;
        margin: 20px 0 28px 0;
        border: 1px solid #C9E0EF;
        border-radius: 30px;
        background: linear-gradient(135deg, #E5F3FC 0%, #F4FAFE 52%, #DCEFFA 100%);
        box-shadow: 0 18px 42px rgba(48, 105, 145, 0.12);
        text-align: center;
    }

    .neuron-pattern {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        opacity: .48;
        pointer-events: none;
    }

    .hero-content {
        position: relative;
        z-index: 1;
        max-width: 800px;
    }

    .hero-title {
        color: #214D6C;
        font-size: clamp(3.8rem, 9vw, 6.5rem);
        font-weight: 800;
        line-height: 1;
        letter-spacing: .035em;
        margin-bottom: 22px;
        text-shadow: 0 3px 14px rgba(255,255,255,.75);
    }

    .hero-subtitle {
        max-width: 720px;
        margin: 0 auto;
        color: #476B85;
        font-size: 1.25rem;
        line-height: 1.7;
    }

    .developer-name {
        margin-top: 12px;
        color: #294A65;
        font-size: 1.15rem;
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


# -------------------------------------------------------------------
# Навигация
# -------------------------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_technique" not in st.session_state:
    st.session_state.selected_technique = None


def go_home():
    st.session_state.page = "home"


def go_library():
    st.session_state.page = "library"


def go_about():
    st.session_state.page = "about"


def open_technique(technique_id):
    st.session_state.selected_technique = technique_id
    st.session_state.page = "technique"


techniques = {
    "decision_tree": {
        "title": "Дерево решений",
        "short": "Разложить сложный выбор на варианты и возможные последствия.",
        "description": "Сравнение вариантов решения через возможные исходы, вероятности и личную оценку.",
        "icon": "🌿",
    },
    "dbt_chain": {
        "title": "Цепочный анализ поведения (ДБТ)",
        "short": "Исследовать последовательность событий, реакций и последствий.",
        "description": "Карта факторов уязвимости, запускающего события, звеньев цепочки и возможных точек вмешательства.",
        "icon": "🔗",
    },
    "exposure": {
        "title": "Иерархия экспозиции",
        "short": "Составить и обсудить лестницу ситуаций для постепенной практики.",
        "description": "Совместное планирование ситуаций, прогнозов, посильных шагов и наблюдений.",
        "icon": "🪜",
    },
    "act_matrix": {
        "title": "ACT-матрица",
        "short": "Исследовать действия «от дискомфорта» и шаги «к ценностям».",
        "description": "Визуальная карта внутреннего опыта, поведения, ценностей и выбранных действий.",
        "icon": "🧭",
    },
}


def render_navigation():
    left, middle, right = st.columns([1, 1, 5])

    with left:
        st.button("⌂ Главная", on_click=go_home, use_container_width=True)

    with middle:
        st.button("Библиотека", on_click=go_library, use_container_width=True)

    with right:
        if st.session_state.page == "technique":
            technique = techniques.get(st.session_state.selected_technique)
            if technique:
                st.caption(f"{technique['icon']} {technique['title']}")


# -------------------------------------------------------------------
# Общие вспомогательные функции
# -------------------------------------------------------------------

def esc(value):
    return html.escape(str(value)).replace("\n", "<br>")


def initialize_decision_tree():
    if "dt_options" not in st.session_state:
        st.session_state.dt_options = [new_option(), new_option()]

    if "decision_calculation" not in st.session_state:
        st.session_state.decision_calculation = None

    if "decision_question" not in st.session_state:
        st.session_state.decision_question = ""


def clear_decision_result():
    st.session_state.decision_calculation = None


def new_scenario(first=False):
    return {
        "id": uuid.uuid4().hex,
        "default_probability": 100 if first else 0,
    }


def new_option():
    return {
        "id": uuid.uuid4().hex,
        "scenarios": [new_scenario(first=True)],
    }


def option_name_key(option_id):
    return f"dt_option_name_{option_id}"


def scenario_name_key(scenario_id):
    return f"dt_scenario_name_{scenario_id}"


def probability_key(scenario_id):
    return f"dt_probability_{scenario_id}"


def score_key(scenario_id):
    return f"dt_score_{scenario_id}"


def add_decision_option():
    st.session_state.dt_options.append(new_option())
    clear_decision_result()


def delete_decision_option(option_id):
    if len(st.session_state.dt_options) <= 2:
        return

    st.session_state.dt_options = [
        option for option in st.session_state.dt_options
        if option["id"] != option_id
    ]
    clear_decision_result()


def add_decision_scenario(option_id):
    for option in st.session_state.dt_options:
        if option["id"] == option_id:
            option["scenarios"].append(new_scenario())
            clear_decision_result()
            return


def delete_decision_scenario(option_id, scenario_id):
    for option in st.session_state.dt_options:
        if option["id"] == option_id and len(option["scenarios"]) > 1:
            option["scenarios"] = [
                scenario for scenario in option["scenarios"]
                if scenario["id"] != scenario_id
            ]
            clear_decision_result()
            return


# -------------------------------------------------------------------
# Дерево решений: SVG
# -------------------------------------------------------------------

def wrap_svg_label(value, width=22, max_lines=2):
    lines = textwrap.wrap(str(value), width=width) or [""]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: max(1, width - 1)] + "…"
    return lines


def build_tree_svg(options, best_name, question):
    leaf_w = 205
    leaf_gap = 30
    group_gap = 58

    leaf_y = 140
    option_y = 400
    trunk_fork_y = 525
    root_card_y = 652
    svg_height = 755

    group_widths = [
        max(
            leaf_w,
            len(option["scenarios"]) * leaf_w
            + (len(option["scenarios"]) - 1) * leaf_gap,
        )
        for option in options
    ]

    svg_width = 100 + sum(group_widths) + group_gap * max(0, len(options) - 1)

    groups = []
    cursor_x = 50

    for index, option in enumerate(options):
        group_width = group_widths[index]
        scenario_count = len(option["scenarios"])
        content_width = scenario_count * leaf_w + (scenario_count - 1) * leaf_gap
        first_leaf_x = cursor_x + (group_width - content_width) / 2

        leaf_centers = [
            first_leaf_x + i * (leaf_w + leaf_gap) + leaf_w / 2
            for i in range(scenario_count)
        ]

        groups.append({
            "option": option,
            "center_x": cursor_x + group_width / 2,
            "leaf_centers": leaf_centers,
        })

        cursor_x += group_width + group_gap

    root_x = (groups[0]["center_x"] + groups[-1]["center_x"]) / 2
    colors = ["#80BFE0", "#71BFA9", "#E1AE83", "#A99BD0", "#D99BB2"]

    parts = [f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         width="{svg_width}" height="{svg_height}"
         viewBox="0 0 {svg_width} {svg_height}"
         role="img" aria-label="Дерево решений">
      <defs>
        <linearGradient id="wood" x1="0" x2="1" y1="0" y2="0">
          <stop offset="0%" stop-color="#A97F60"/>
          <stop offset="50%" stop-color="#C99A73"/>
          <stop offset="100%" stop-color="#A97F60"/>
        </linearGradient>
        <filter id="tree-shadow" x="-30%" y="-30%" width="160%" height="170%">
          <feDropShadow dx="0" dy="4" stdDeviation="5"
                        flood-color="#54738A" flood-opacity="0.14"/>
        </filter>
      </defs>
      <rect width="100%" height="100%" rx="24" fill="#F8FBFD"/>
    """]

    for index, group in enumerate(groups):
        option = group["option"]
        color = "#65AD91" if option["name"] == best_name else colors[index % len(colors)]
        option_x = group["center_x"]

        parts.append(f"""
          <path d="M {root_x} {trunk_fork_y}
                   C {root_x} {trunk_fork_y - 65},
                     {option_x} {option_y + 125},
                     {option_x} {option_y + 20}"
                fill="none" stroke="{color}" stroke-width="9"
                stroke-linecap="round"/>
        """)

        for leaf_x in group["leaf_centers"]:
            parts.append(f"""
              <path d="M {option_x} {option_y - 18}
                       C {option_x} {option_y - 95},
                         {leaf_x} {leaf_y + 100},
                         {leaf_x} {leaf_y + 24}"
                    fill="none" stroke="{color}" stroke-width="5"
                    stroke-linecap="round"/>
            """)

    parts.append(f"""
      <path d="M {root_x} {root_card_y}
               C {root_x - 8} {root_card_y - 35},
                 {root_x + 10} {trunk_fork_y + 55},
                 {root_x} {trunk_fork_y}"
            fill="none" stroke="url(#wood)" stroke-width="22"
            stroke-linecap="round"/>
    """)

    for index, group in enumerate(groups):
        option = group["option"]
        color = "#65AD91" if option["name"] == best_name else colors[index % len(colors)]
        option_x = group["center_x"]
        option_label = html.escape(option["name"])
        if len(option_label) > 30:
            option_label = option_label[:29] + "…"

        parts.append(f"""
          <circle cx="{option_x}" cy="{option_y}" r="18"
                  fill="{color}" stroke="#FFFFFF" stroke-width="5"
                  filter="url(#tree-shadow)"/>
          <rect x="{option_x - 116}" y="{option_y + 28}"
                width="232" height="68" rx="18"
                fill="#FFFFFF" stroke="{color}" stroke-width="2"
                filter="url(#tree-shadow)"/>
          <text x="{option_x}" y="{option_y + 54}" text-anchor="middle"
                font-family="Nunito Sans, Arial, sans-serif"
                font-size="14" font-weight="800" fill="#36546C">
            {option_label}
          </text>
          <text x="{option_x}" y="{option_y + 78}" text-anchor="middle"
                font-family="Nunito Sans, Arial, sans-serif"
                font-size="12" fill="#58748A">
            Итоговая оценка: {option["score"]:.2f}
          </text>
        """)

        for scenario_index, scenario in enumerate(option["scenarios"]):
            leaf_x = group["leaf_centers"][scenario_index]
            probability = option["normalized"][scenario_index]
            lines = wrap_svg_label(scenario["name"])

            parts.append(f"""
              <circle cx="{leaf_x}" cy="{leaf_y}" r="22"
                      fill="{color}" fill-opacity="0.78"
                      stroke="{color}" stroke-width="3"
                      filter="url(#tree-shadow)"/>
              <circle cx="{leaf_x}" cy="{leaf_y}" r="14"
                      fill="none" stroke="#FFFFFF" stroke-opacity="0.78"
                      stroke-width="2"/>
            """)

            card_y = leaf_y + 38
            parts.append(f"""
              <rect x="{leaf_x - 96}" y="{card_y}" width="192" height="76"
                    rx="16" fill="#FFFFFF" fill-opacity="0.97"
                    stroke="{color}" stroke-opacity="0.72" stroke-width="1.5"/>
            """)

            for line_index, line in enumerate(lines):
                parts.append(f"""
                  <text x="{leaf_x}" y="{card_y + 23 + line_index * 17}"
                        text-anchor="middle"
                        font-family="Nunito Sans, Arial, sans-serif"
                        font-size="12" font-weight="700" fill="#36546C">
                    {html.escape(line)}
                  </text>
                """)

            parts.append(f"""
              <text x="{leaf_x}" y="{card_y + 63}" text-anchor="middle"
                    font-family="Nunito Sans, Arial, sans-serif"
                    font-size="11" fill="#58748A">
                {probability:.1f}% · оценка {scenario["score"]:g}
              </text>
            """)

    question_lines = wrap_svg_label(question, width=42, max_lines=2)
    root_box_width = 390
    root_box_height = 66

    parts.append(f"""
      <rect x="{root_x - root_box_width / 2}" y="{root_card_y}"
            width="{root_box_width}" height="{root_box_height}" rx="23"
            fill="#F4D6B8" stroke="#D8A77E" stroke-width="2"
            filter="url(#tree-shadow)"/>
    """)

    first_text_y = root_card_y + (27 if len(question_lines) == 1 else 23)

    for line_index, line in enumerate(question_lines):
        parts.append(f"""
          <text x="{root_x}" y="{first_text_y + line_index * 19}"
                text-anchor="middle"
                font-family="Nunito Sans, Arial, sans-serif"
                font-size="15" font-weight="800" fill="#604B3D">
            {html.escape(line)}
          </text>
        """)

    parts.append("</svg>")

    return f"""
    <div style="width:100%; overflow-x:auto; border:1px solid #DCE8F0;
                border-radius:24px; background:#F8FBFD; padding:12px;
                box-sizing:border-box;">
        {''.join(parts)}
    </div>
    """


# -------------------------------------------------------------------
# Дерево решений: интерфейс
# -------------------------------------------------------------------

def render_decision_tree():
    initialize_decision_tree()

    st.title("🌿 Дерево решений")
    st.write("Разложите сложный выбор на варианты и возможные последствия.")

    st.text_input(
        "Какое решение нужно принять?",
        key="decision_question",
        placeholder="Например: «Стоит ли менять работу?»",
        on_change=clear_decision_result,
    )

    st.subheader("Добавьте варианты")
    st.caption("Для каждого варианта укажите возможные исходы, вероятность и оценку для вас.")

    for option_index, option in enumerate(list(st.session_state.dt_options)):
        option_id = option["id"]
        name_key = option_name_key(option_id)

        if name_key not in st.session_state:
            st.session_state[name_key] = ""

        with st.container(border=True):
            title_col, delete_col = st.columns([5, 1.7])

            with title_col:
                st.markdown(f"### Вариант {option_index + 1}")

            with delete_col:
                st.button(
                    "Удалить вариант",
                    key=f"delete_option_{option_id}",
                    disabled=len(st.session_state.dt_options) <= 2,
                    on_click=delete_decision_option,
                    args=(option_id,),
                    use_container_width=True,
                )

            st.text_input(
                "Название варианта",
                key=name_key,
                placeholder=f"Например: «Вариант {option_index + 1}»",
                on_change=clear_decision_result,
            )

            for scenario_index, scenario in enumerate(list(option["scenarios"])):
                scenario_id = scenario["id"]
                scenario_name_state = scenario_name_key(scenario_id)
                probability_state = probability_key(scenario_id)
                score_state = score_key(scenario_id)

                if scenario_name_state not in st.session_state:
                    st.session_state[scenario_name_state] = ""
                if probability_state not in st.session_state:
                    st.session_state[probability_state] = scenario["default_probability"]
                if score_state not in st.session_state:
                    st.session_state[score_state] = 0.0

                with st.container(border=True):
                    scenario_title, scenario_delete = st.columns([5, 1.7])

                    with scenario_title:
                        st.markdown(f"**Сценарий {scenario_index + 1}**")

                    with scenario_delete:
                        st.button(
                            "Удалить сценарий",
                            key=f"delete_scenario_{scenario_id}",
                            disabled=len(option["scenarios"]) <= 1,
                            on_click=delete_decision_scenario,
                            args=(option_id, scenario_id),
                            use_container_width=True,
                        )

                    st.text_input(
                        "Описание возможного исхода",
                        key=scenario_name_state,
                        placeholder="Например: «Найду более интересную работу»",
                        on_change=clear_decision_result,
                    )

                    probability_col, score_col = st.columns(2)

                    with probability_col:
                        st.slider(
                            "Вероятность, %",
                            min_value=0,
                            max_value=100,
                            step=1,
                            key=probability_state,
                            on_change=clear_decision_result,
                        )

                    with score_col:
                        st.slider(
                            "Оценка исхода",
                            min_value=-5.0,
                            max_value=5.0,
                            step=0.5,
                            key=score_state,
                            help="−5 — очень нежелательный исход, +5 — очень желательный.",
                            on_change=clear_decision_result,
                        )

            st.button(
                "＋ Добавить сценарий",
                key=f"add_scenario_{option_id}",
                on_click=add_decision_scenario,
                args=(option_id,),
            )

    add_col, remove_col, _ = st.columns([1.7, 1.8, 4])

    with add_col:
        st.button(
            "＋ Добавить вариант",
            key="add_decision_option",
            on_click=add_decision_option,
            use_container_width=True,
        )

    with remove_col:
        st.button(
            "− Удалить последний",
            key="remove_last_decision_option",
            disabled=len(st.session_state.dt_options) <= 2,
            on_click=delete_decision_option,
            args=(st.session_state.dt_options[-1]["id"],),
            use_container_width=True,
        )

    st.divider()

    if st.button("Рассчитать и построить дерево", type="primary", use_container_width=True):
        question = st.session_state.decision_question.strip()
        error = None
        prepared_options = []
        used_names = set()

        if not question:
            error = "Сначала сформулируйте решение."

        for option_index, option in enumerate(st.session_state.dt_options):
            if error:
                break

            option_name = st.session_state[option_name_key(option["id"])].strip()

            if not option_name:
                error = f"Введите название варианта {option_index + 1}."
                break

            if option_name in used_names:
                error = f"Названия вариантов должны отличаться: «{option_name}»."
                break

            used_names.add(option_name)
            scenarios = []

            for scenario_index, scenario in enumerate(option["scenarios"]):
                scenario_name = st.session_state[scenario_name_key(scenario["id"])].strip()

                if not scenario_name:
                    error = (
                        f"Заполните описание сценария {scenario_index + 1} "
                        f"в варианте «{option_name}»."
                    )
                    break

                scenarios.append({
                    "name": scenario_name,
                    "probability": int(st.session_state[probability_key(scenario["id"])]),
                    "score": float(st.session_state[score_key(scenario["id"])]),
                })

            if error:
                break

            total_probability = sum(item["probability"] for item in scenarios)

            if total_probability == 0:
                error = (
                    f"В варианте «{option_name}» задайте ненулевую вероятность "
                    "хотя бы одному сценарию."
                )
                break

            normalized = [
                item["probability"] / total_probability * 100
                for item in scenarios
            ]

            expected_score = sum(
                normalized[index] / 100 * item["score"]
                for index, item in enumerate(scenarios)
            )

            prepared_options.append({
                "name": option_name,
                "scenarios": scenarios,
                "normalized": normalized,
                "score": expected_score,
            })

        if error:
            st.session_state.decision_calculation = None
            st.warning(error)
        else:
            best_name = max(prepared_options, key=lambda item: item["score"])["name"]
            st.session_state.decision_calculation = {
                "question": question,
                "options": prepared_options,
                "best_name": best_name,
            }

    result = st.session_state.decision_calculation

    if result:
        st.subheader("Результат")
        st.write(f"**Решение:** {result['question']}")

        metric_columns = st.columns(len(result["options"]))
        for column, option in zip(metric_columns, result["options"]):
            with column:
                label = f"🌿 {option['name']}" if option["name"] == result["best_name"] else option["name"]
                st.metric(label=label, value=f"{option['score']:.2f} / 5")

        st.success(f"По указанным оценкам лидирует вариант: **{result['best_name']}**.")
        st.caption(
            "Это ориентир для размышления, а не автоматическое решение. "
            "Вероятности сценариев нормализуются отдельно внутри каждого варианта."
        )

        st.subheader("Дерево возможных исходов")
        components.html(
            build_tree_svg(result["options"], result["best_name"], result["question"]),
            height=780,
            scrolling=True,
        )


# -------------------------------------------------------------------
# Цепочный анализ поведения
# -------------------------------------------------------------------

def initialize_chain():
    if "chain_links" not in st.session_state:
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


def render_chain_analysis():
    initialize_chain()

    st.title("🔗 Цепочный анализ поведения (ДБТ)")
    st.write("Совместно исследуйте контекст, последовательность реакций, целевое поведение и его последствия.")

    st.info(
        "Если обсуждение становится слишком интенсивным, можно сделать паузу, "
        "пропустить поле или остановиться."
    )

    vulnerability = st.text_area(
        "Факторы уязвимости",
        key="chain_vulnerability",
        placeholder="Что могло сделать ситуацию сложнее заранее? Например, недосып, голод, напряжение.",
    )

    prompting_event = st.text_area(
        "Запускающее событие",
        key="chain_prompt",
        placeholder="Что произошло непосредственно перед поведением? Опишите наблюдаемые факты.",
    )

    st.subheader("Звенья цепочки")
    st.caption(
        "Добавляйте звенья по порядку: мысли, эмоции, ощущения в теле, "
        "импульсы или действия."
    )

    for index, link in enumerate(list(st.session_state.chain_links), start=1):
        link_id = link["id"]

        with st.container(border=True):
            header, delete_col = st.columns([5, 1.5])
            with header:
                st.markdown(f"**Звено {index}**")
            with delete_col:
                st.button(
                    "Удалить",
                    key=f"chain_delete_{link_id}",
                    disabled=len(st.session_state.chain_links) <= 1,
                    on_click=remove_chain_link,
                    args=(link_id,),
                    use_container_width=True,
                )

            col1, col2 = st.columns(2)
            with col1:
                st.text_area(
                    "Мысли или образы",
                    key=f"chain_thought_{link_id}",
                    placeholder="Что промелькнуло в голове?",
                )
                st.text_area(
                    "Ощущения в теле",
                    key=f"chain_body_{link_id}",
                    placeholder="Что происходило в теле?",
                )
            with col2:
                st.text_area(
                    "Эмоции",
                    key=f"chain_emotion_{link_id}",
                    placeholder="Что вы чувствовали?",
                )
                st.text_area(
                    "Импульсы или действия",
                    key=f"chain_action_{link_id}",
                    placeholder="Что захотелось сделать или что вы сделали?",
                )

            st.slider(
                "Насколько интенсивным было это звено? (необязательно)",
                min_value=0,
                max_value=10,
                value=0,
                key=f"chain_intensity_{link_id}",
            )

            st.checkbox(
                "Обсудить это звено как возможную точку вмешательства",
                key=f"chain_intervention_{link_id}",
            )

            st.text_area(
                "Какой другой шаг, навык или поддержка могли бы здесь помочь?",
                key=f"chain_skill_{link_id}",
                placeholder="Заполняйте по желанию вместе со специалистом.",
            )

    st.button(
        "＋ Добавить звено",
        on_click=add_chain_link,
        use_container_width=False,
    )

    st.subheader("Целевое поведение и последствия")
    target = st.text_area(
        "Какое конкретное поведение разбираете?",
        key="chain_target",
        placeholder="Опишите поведение нейтрально и конкретно.",
    )

    immediate, later = st.columns(2)
    with immediate:
        st.text_area(
            "Последствия сразу после",
            key="chain_immediate",
            placeholder="Что изменилось сразу после поведения?",
        )
    with later:
        st.text_area(
            "Последствия позднее",
            key="chain_later",
            placeholder="Какие последствия проявились позже?",
        )

    st.text_area(
        "Восстановление ситуации или снижение последствий",
        key="chain_repair",
        placeholder="Есть ли что-то, что хотелось бы сделать для восстановления или поддержки?",
    )

    if st.checkbox("Показать сводную карту цепочки", value=True, key="chain_show_summary"):
        st.markdown("### Сводная карта")

        with st.container(border=True):
            st.markdown("**Факторы уязвимости**")
            st.write(vulnerability or "Пока не заполнено")

            st.markdown("↓ **Запускающее событие**")
            st.write(prompting_event or "Пока не заполнено")

            for index, link in enumerate(st.session_state.chain_links, start=1):
                link_id = link["id"]
                st.markdown(f"↓ **Звено {index}**")

                values = [
                    ("Мысли", st.session_state.get(f"chain_thought_{link_id}", "")),
                    ("Эмоции", st.session_state.get(f"chain_emotion_{link_id}", "")),
                    ("Ощущения в теле", st.session_state.get(f"chain_body_{link_id}", "")),
                    ("Импульсы / действия", st.session_state.get(f"chain_action_{link_id}", "")),
                ]

                for label, value in values:
                    if value:
                        st.write(f"**{label}:** {value}")

                if st.session_state.get(f"chain_intervention_{link_id}", False):
                    st.success("Отмечено как возможная точка вмешательства.")
                    skill = st.session_state.get(f"chain_skill_{link_id}", "")
                    if skill:
                        st.write(f"**Возможная поддержка:** {skill}")

            st.markdown("↓ **Целевое поведение**")
            st.write(target or "Пока не заполнено")

            st.markdown("**Последствия сразу:**")
            st.write(st.session_state.get("chain_immediate", "") or "Пока не заполнено")

            st.markdown("**Последствия позднее:**")
            st.write(st.session_state.get("chain_later", "") or "Пока не заполнено")


# -------------------------------------------------------------------
# Иерархия экспозиции
# -------------------------------------------------------------------

def initialize_exposure():
    if "exposure_steps" not in st.session_state:
        st.session_state.exposure_steps = [
            {"id": uuid.uuid4().hex},
            {"id": uuid.uuid4().hex},
            {"id": uuid.uuid4().hex},
        ]


def add_exposure_step():
    st.session_state.exposure_steps.append({"id": uuid.uuid4().hex})


def remove_exposure_step(step_id):
    if len(st.session_state.exposure_steps) > 1:
        st.session_state.exposure_steps = [
            step for step in st.session_state.exposure_steps
            if step["id"] != step_id
        ]


def render_exposure():
    initialize_exposure()

    st.title("🪜 Иерархия экспозиции")
    st.write("Составьте с клиентом лестницу ситуаций для обсуждения и планирования постепенной практики.")

    st.info(
        "Практика должна быть добровольной и согласованной со специалистом. "
        "Не используйте упражнение для ситуаций с реальной опасностью."
    )

    st.text_area(
        "Цель работы",
        key="exposure_goal",
        placeholder="Например: «Увереннее участвовать в рабочих обсуждениях».",
    )

    st.subheader("Ступени")
    st.caption(
        "Оценка тревоги помогает организовать обсуждение, но не назначает "
        "автоматически порядок или обязательный первый шаг."
    )

    items = []

    for index, step in enumerate(list(st.session_state.exposure_steps), start=1):
        step_id = step["id"]

        if f"exposure_distress_{step_id}" not in st.session_state:
            st.session_state[f"exposure_distress_{step_id}"] = 3

        with st.container(border=True):
            header, delete_col = st.columns([5, 1.5])

            with header:
                st.markdown(f"**Ступень {index}**")

            with delete_col:
                st.button(
                    "Удалить",
                    key=f"exposure_delete_{step_id}",
                    disabled=len(st.session_state.exposure_steps) <= 1,
                    on_click=remove_exposure_step,
                    args=(step_id,),
                    use_container_width=True,
                )

            st.text_area(
                "Ситуация",
                key=f"exposure_situation_{step_id}",
                placeholder="Опишите конкретную ситуацию.",
            )

            st.slider(
                "Ожидаемая тревога (0–10)",
                min_value=0,
                max_value=10,
                key=f"exposure_distress_{step_id}",
            )

            st.text_area(
                "Прогноз или опасение",
                key=f"exposure_prediction_{step_id}",
                placeholder="Чего вы ожидаете или опасаетесь?",
            )

            st.text_area(
                "Обсуждаемый посильный шаг",
                key=f"exposure_plan_{step_id}",
                placeholder="Какой конкретный шаг вы планируете вместе со специалистом?",
            )

            st.selectbox(
                "Статус",
                ["Не обсуждали", "Обсудили", "Запланировали", "Попробовали"],
                key=f"exposure_status_{step_id}",
            )

            st.text_area(
                "Наблюдения после практики — необязательно",
                key=f"exposure_reflection_{step_id}",
                placeholder="Что произошло и что вы заметили? Можно заполнить позже.",
            )

        items.append({
            "id": step_id,
            "situation": st.session_state.get(f"exposure_situation_{step_id}", ""),
            "distress": st.session_state.get(f"exposure_distress_{step_id}", 3),
            "prediction": st.session_state.get(f"exposure_prediction_{step_id}", ""),
            "plan": st.session_state.get(f"exposure_plan_{step_id}", ""),
            "status": st.session_state.get(f"exposure_status_{step_id}", "Не обсуждали"),
            "index": index,
        })

    st.button("＋ Добавить ступень", on_click=add_exposure_step)

    st.subheader("Лестница по оценке тревоги")
    ordered = sorted(items, key=lambda item: (item["distress"], item["index"]))

    if not any(item["situation"].strip() for item in ordered):
        st.caption("Заполните ситуации, чтобы увидеть их в сводке.")
    else:
        for position, item in enumerate(ordered, start=1):
            if not item["situation"].strip():
                continue

            with st.container(border=True):
                st.markdown(
                    f"**{position}. {item['situation']}** "
                    f"— ожидаемая тревога: **{item['distress']}/10**"
                )
                st.caption(f"Статус: {item['status']}")

                if item["prediction"].strip():
                    st.write(f"**Прогноз:** {item['prediction']}")
                if item["plan"].strip():
                    st.write(f"**Обсуждаемый шаг:** {item['plan']}")


# -------------------------------------------------------------------
# ACT-матрица
# -------------------------------------------------------------------

def render_act_matrix():
    st.title("🧭 ACT-матрица")
    st.write("Визуальная карта внутреннего опыта и поведения: что уводит от дискомфорта и какие действия приближают к важному.")

    st.info(
        "Квадранты — материал для совместного исследования, а не оценка "
        "правильности поведения. Ценности и выбранные шаги определяет сам клиент."
    )

    st.text_area(
        "Ситуация, которую хотите исследовать",
        key="act_situation",
        placeholder="Кратко опишите контекст или трудность.",
    )

    st.text_area(
        "Кто или что важно для вас? Какие качества жизни вы хотите воплощать?",
        key="act_values",
        placeholder="Например: близость, забота, любознательность, независимость.",
    )

    st.caption(
        "Внутренний опыт — мысли, чувства, телесные ощущения и воспоминания. "
        "Поведение — наблюдаемые действия."
    )

    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            st.markdown("### Действия «от дискомфорта»")
            st.caption("Что вы делаете, чтобы избежать или уменьшить неприятный опыт?")
            st.text_area(
                "Поведение / действия",
                key="act_away_actions",
                placeholder="Например: отменяю встречу, откладываю разговор, отвлекаюсь.",
                label_visibility="collapsed",
            )

        with st.container(border=True):
            st.markdown("### Внутренний опыт")
            st.caption("Какие мысли, чувства или ощущения связаны с этой ситуацией?")
            st.text_area(
                "Мысли, эмоции, ощущения",
                key="act_inner_experience",
                placeholder="Например: тревога, мысль «я не справлюсь», напряжение в теле.",
                label_visibility="collapsed",
            )

    with right:
        with st.container(border=True):
            st.markdown("### Шаги «к важному»")
            st.caption("Какое небольшое наблюдаемое действие приблизило бы вас к ценности?")
            st.text_area(
                "Действия в направлении ценностей",
                key="act_toward_actions",
                placeholder="Например: написать близкому человеку, задать вопрос, сделать первый шаг.",
                label_visibility="collapsed",
            )

        with st.container(border=True):
            st.markdown("### Внутренний опыт при движении к важному")
            st.caption("Что может возникать внутри, когда вы делаете этот шаг?")
            st.text_area(
                "Мысли, эмоции, ощущения",
                key="act_toward_inner",
                placeholder="Например: волнение, сомнение, надежда, ощущение интереса.",
                label_visibility="collapsed",
            )

    st.subheader("Небольшой выбранный шаг")
    st.text_area(
        "Что вы сами хотели бы попробовать сделать в направлении важного?",
        key="act_next_step",
        placeholder="Шаг должен быть выбран клиентом и согласован в рамках консультации.",
    )

    if st.checkbox("Показать сводную матрицу", value=True, key="act_show_summary"):
        st.markdown("### Сводка")

        values = [
            ("Ситуация", st.session_state.get("act_situation", "")),
            ("Что важно", st.session_state.get("act_values", "")),
            ("Действия «от дискомфорта»", st.session_state.get("act_away_actions", "")),
            ("Внутренний опыт", st.session_state.get("act_inner_experience", "")),
            ("Действия «к важному»", st.session_state.get("act_toward_actions", "")),
            ("Внутренний опыт при движении к важному", st.session_state.get("act_toward_inner", "")),
            ("Выбранный небольшой шаг", st.session_state.get("act_next_step", "")),
        ]

        for label, value in values:
            if value.strip():
                with st.container(border=True):
                    st.markdown(f"**{label}**")
                    st.write(value)


# -------------------------------------------------------------------
# Home / About / Library
# -------------------------------------------------------------------

def render_home():
    st.markdown(
        """
        <div class="hero">
            <svg class="neuron-pattern" viewBox="0 0 1200 480"
                 preserveAspectRatio="xMidYMid slice"
                 xmlns="http://www.w3.org/2000/svg">
                <g fill="none" stroke="#5794BB" stroke-width="2">
                    <path d="M40 95 L170 155 L285 80 L420 145 L545 65"/>
                    <path d="M170 155 L250 285 L390 250 L420 145"/>
                    <path d="M285 80 L315 25"/>
                    <path d="M390 250 L520 330 L650 260 L770 325"/>
                    <path d="M545 65 L680 120 L810 65 L930 145"/>
                    <path d="M680 120 L650 260"/>
                    <path d="M810 65 L865 25"/>
                    <path d="M930 145 L1080 90 L1170 170"/>
                    <path d="M930 145 L980 285 L1130 330"/>
                    <path d="M770 325 L850 415 L980 285"/>
                    <path d="M40 95 L25 210"/>
                    <path d="M520 330 L485 430"/>
                </g>
                <g fill="#4D8FB8" stroke="#F5FAFE" stroke-width="5">
                    <circle cx="40" cy="95" r="10"/>
                    <circle cx="170" cy="155" r="13"/>
                    <circle cx="285" cy="80" r="10"/>
                    <circle cx="420" cy="145" r="12"/>
                    <circle cx="545" cy="65" r="9"/>
                    <circle cx="250" cy="285" r="10"/>
                    <circle cx="390" cy="250" r="13"/>
                    <circle cx="520" cy="330" r="10"/>
                    <circle cx="650" cy="260" r="12"/>
                    <circle cx="680" cy="120" r="9"/>
                    <circle cx="810" cy="65" r="12"/>
                    <circle cx="930" cy="145" r="13"/>
                    <circle cx="1080" cy="90" r="10"/>
                    <circle cx="980" cy="285" r="11"/>
                    <circle cx="1130" cy="330" r="9"/>
                    <circle cx="850" cy="415" r="10"/>
                    <circle cx="1170" cy="170" r="8"/>
                </g>
            </svg>

            <div class="hero-content">
                <div class="hero-title">ПСИ-БЛОК</div>
                <div class="hero-subtitle">
                    Пространство с наглядными инструментами для совместной
                    работы психолога и клиента. Мы создаём его, чтобы
                    структурировать обсуждение и делать психологические техники
                    удобно заметными и применимыми в реальной практике.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)

    with left:
        if st.button("📚  Библиотека техник", type="primary", use_container_width=True):
            go_library()

    with right:
        if st.button("ℹ️  О нас", type="primary", use_container_width=True):
            go_about()

    st.divider()
    st.markdown(
        """
        #### Инструменты для совместной работы
        Выберите технику, чтобы открыть её интерактивный черновик. Материалы
        предназначены для поддержки обсуждения и не заменяют профессиональную
        оценку или терапевтическую работу.
        """
    )


def render_library():
    st.title("📚 Библиотека техник")
    st.write("Выберите инструмент, который хотите открыть.")

    cards = list(techniques.items())

    for start in range(0, len(cards), 2):
        columns = st.columns(2)

        for column, (technique_id, technique) in zip(columns, cards[start:start + 2]):
            with column:
                with st.container(border=True):
                    st.markdown(f"### {technique['icon']} {technique['title']}")
                    st.write(technique["short"])
                    st.caption(technique["description"])
                    st.button(
                        "Открыть технику →",
                        key=f"open_{technique_id}",
                        on_click=open_technique,
                        args=(technique_id,),
                        use_container_width=True,
                    )


def render_about():
    st.title("ℹ️ О нас")

    st.markdown(
        """
        **ПСИ-БЛОК** — проект библиотеки интерактивных инструментов
        для психологических консультаций.

        Мы хотим помочь психологу и клиенту совместно структурировать
        обсуждение, визуализировать связи и возвращаться к важным идеям
        в ходе работы. Инструменты не заменяют специалиста и не принимают
        решения за клиента.
        """
    )

    st.divider()
    st.subheader("Команда разработчиков")

    developers = [
        {
            "name": "Имя Фамилия",
            "role": "Роль в проекте",
            "photo": "assets/developer1.jpg",
        },
        {
            "name": "Имя Фамилия",
            "role": "Роль в проекте",
            "photo": "assets/developer2.jpg",
        },
    ]

    columns = st.columns(len(developers))

    for column, person in zip(columns, developers):
        with column:
            with st.container(border=True):
                photo_path = Path(person["photo"])

                if photo_path.exists():
                    st.image(str(photo_path), use_container_width=True)
                else:
                    st.info(f"Фотография не найдена: `{person['photo']}`")

                st.markdown(
                    f"<div class='developer-name'>{html.escape(person['name'])}</div>"
                    f"<div class='developer-role'>{html.escape(person['role'])}</div>",
                    unsafe_allow_html=True,
                )

    st.divider()
    st.warning(
        "Это прототип. Не вводите в него идентифицирующие или особенно "
        "чувствительные сведения: защищённое хранение клиентских данных "
        "пока не реализовано."
    )


def render_selected_technique():
    technique_id = st.session_state.selected_technique
    technique = techniques.get(technique_id)

    if not technique:
        st.warning("Техника не найдена.")
        st.button("Вернуться в библиотеку", on_click=go_library)
        return

    if st.button("← К библиотеке", on_click=go_library):
        return

    st.divider()

    if technique_id == "decision_tree":
        render_decision_tree()
    elif technique_id == "dbt_chain":
        render_chain_analysis()
    elif technique_id == "exposure":
        render_exposure()
    elif technique_id == "act_matrix":
        render_act_matrix()


# -------------------------------------------------------------------
# Основной роутинг
# -------------------------------------------------------------------

render_navigation()
st.divider()

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
