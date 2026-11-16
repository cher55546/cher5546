pip install streamlit matplotlib
streamlit run app.py
from io import BytesIO
from pathlib import Path
import html
import textwrap
import uuid

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="ПСИ-БЛОК",
    page_icon="🌿",
    layout="wide",
)


# -------------------------------------------------------------------
# Декоративный фон: полупрозрачная нейронная сеть по всему экрану
# -------------------------------------------------------------------

NEURON_BACKGROUND = """
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="800" viewBox="0 0 1000 800">
  <g fill="none" stroke="#4389B5" stroke-opacity="0.11" stroke-width="2">
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
  <g fill="#4389B5" fill-opacity="0.16" stroke="#FFFFFF" stroke-opacity="0.65" stroke-width="3">
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

import base64

NEURON_BACKGROUND_B64 = base64.b64encode(
    NEURON_BACKGROUND.encode("utf-8")
).decode("ascii")


# -------------------------------------------------------------------
# Стили
# -------------------------------------------------------------------

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700;800&display=swap');

    .stApp {{
        background:
            radial-gradient(ellipse at 10% 5%, rgba(196, 228, 248, .62), transparent 34%),
            radial-gradient(ellipse at 92% 18%, rgba(219, 239, 251, .70), transparent 36%),
            linear-gradient(145deg, #F5FAFE 0%, #EDF6FC 52%, #F8FBFE 100%);
        color: #294A65;
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        opacity: 0.72;
        background-image: url("data:image/svg+xml;base64,{NEURON_BACKGROUND_B64}");
        background-size: 1000px 800px;
        background-repeat: repeat;
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stAppViewContainer"] > .main {{
        position: relative;
        z-index: 1;
    }}

    .block-container {{
        max-width: 1120px;
        padding-top: 1.4rem;
        padding-bottom: 4rem;
    }}

    h1, h2, h3, h4, p, label, button, input, textarea {{
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }}

    h1, h2, h3, h4 {{
        color: #294A65 !important;
        letter-spacing: -0.025em;
    }}

    h1 {{ font-size: 2.65rem !important; font-weight: 800 !important; }}
    h2 {{ font-size: 1.85rem !important; font-weight: 800 !important; }}
    h3 {{ font-size: 1.3rem !important; font-weight: 800 !important; }}

    p, label, [data-testid="stCaptionContainer"] {{
        color: #54718A;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        border: 1px solid #D4E5F1 !important;
        border-radius: 20px !important;
        background: rgba(255,255,255,0.92) !important;
        box-shadow: 0 10px 26px rgba(62, 112, 148, 0.08);
    }}

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {{
        border: 1px solid #C9DDEB;
        border-radius: 13px;
        background: #FFFFFF;
        color: #294A65;
    }}

    .stButton > button {{
        min-height: 46px;
        border: 1px solid #C1D8E9;
        border-radius: 14px;
        background: #F4F9FD;
        color: #315773;
        font-size: 1rem;
        font-weight: 700;
        transition: 0.18s ease;
    }}

    .stButton > button:hover:not(:disabled) {{
        border-color: #8FB9D5;
        background: #E8F4FC;
        color: #234D6B;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(61, 119, 158, 0.12);
    }}

    .stButton > button[kind="primary"] {{
        min-height: 60px;
        border: 1px solid #79AFCF;
        border-radius: 16px;
        background: linear-gradient(135deg, #D9EEFA, #E5F3FC);
        color: #234D6B;
        font-size: 1.12rem;
        font-weight: 800;
        box-shadow: 0 7px 18px rgba(61, 119, 158, 0.10);
    }}

    [data-testid="stDownloadButton"] > button {{
        min-height: 46px;
        border-radius: 14px;
        border: 1px solid #8FB9D5;
        background: #E8F4FC;
        color: #234D6B;
        font-weight: 800;
    }}

    [data-testid="stMetric"] {{
        border: 1px solid #D4E5F1;
        border-radius: 17px;
        background: rgba(255,255,255,0.94);
        padding: 14px;
    }}

    [data-testid="stAlert"] {{
        border-radius: 15px;
    }}

    hr {{
        border-color: #D4E5F1;
    }}

    .hero-title {{
        color: #214D6C;
        font-family: "Nunito Sans", "Segoe UI", sans-serif;
        font-size: clamp(3.8rem, 9vw, 6.7rem);
        font-weight: 800;
        line-height: 1;
        letter-spacing: .035em;
        text-shadow: 0 3px 14px rgba(255,255,255,.75);
    }}

    .hero-subtitle {{
        max-width: 760px;
        margin: 20px auto 0 auto;
        color: #476B85;
        font-family: "Nunito Sans", "Segoe UI", sans-serif;
        font-size: 1.2rem;
        line-height: 1.7;
    }}

    .developer-name {{
        margin-top: 12px;
        color: #294A65;
        font-size: 1.15rem;
        font-weight: 800;
        text-align: center;
    }}

    .developer-role {{
        color: #648198;
        text-align: center;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------------------------------------------------------
# Навигация и каталог
# -------------------------------------------------------------------

TECHNIQUES = {
    "decision_tree": {
        "title": "Дерево решений",
        "short": "Разложить сложный выбор на варианты и возможные последствия.",
        "description": "Сравнение вариантов решения через возможные исходы, вероятности и личную оценку.",
        "icon": "🌿",
    },
    "dbt_chain": {
        "title": "Цепочный анализ поведения (ДБТ)",
        "short": "Исследовать последовательность событий, реакций и последствий.",
        "description": "Карта контекста, звеньев цепочки и возможных точек вмешательства.",
        "icon": "🔗",
    },
    "exposure": {
        "title": "Иерархия экспозиции",
        "short": "Составить и обсудить лестницу ситуаций для постепенной практики.",
        "description": "Планирование ситуаций, прогнозов, посильных шагов и наблюдений.",
        "icon": "🪜",
    },
    "act_matrix": {
        "title": "ACT-матрица",
        "short": "Исследовать действия «от дискомфорта» и шаги «к ценностям».",
        "description": "Визуальная карта внутреннего опыта, поведения, ценностей и выбранных действий.",
        "icon": "🧭",
    },
}

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


def render_navigation():
    home_col, library_col, spacer = st.columns([1.2, 1.2, 5])

    with home_col:
        st.button("⌂ Главная", on_click=go_home, use_container_width=True)

    with library_col:
        st.button("Библиотека", on_click=go_library, use_container_width=True)


def safe_text(value):
    return html.escape(str(value))


# -------------------------------------------------------------------
# Графики для PNG-экспорта
# -------------------------------------------------------------------

def fig_to_png(fig):
    output = BytesIO()
    fig.savefig(
        output,
        format="png",
        dpi=180,
        bbox_inches="tight",
        facecolor="#F7FBFE",
    )
    plt.close(fig)
    output.seek(0)
    return output.getvalue()


def wrap_for_plot(text, width=28):
    text = str(text or "").strip()
    if not text:
        return "—"
    return "\n".join(textwrap.wrap(text, width=width))


def draw_box(ax, x, y, width, height, title, body, color="#EAF5FB"):
    box = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        linewidth=1.5,
        edgecolor="#8BB9D5",
        facecolor=color,
    )
    ax.add_patch(box)
    ax.text(
        x + width / 2,
        y + height * 0.70,
        title,
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
        color="#294A65",
        wrap=True,
    )
    ax.text(
        x + width / 2,
        y + height * 0.34,
        wrap_for_plot(body, 25),
        ha="center",
        va="center",
        fontsize=9,
        color="#476B85",
        wrap=True,
    )


def make_decision_png(question, options):
    count = max(1, sum(len(option["scenarios"]) for option in options))
    width = max(9, min(18, 3.2 * count))
    fig, ax = plt.subplots(figsize=(width, 7))
    ax.set_facecolor("#F7FBFE")
    ax.axis("off")

    ax.text(
        0.5, 0.97, "Дерево решений",
        transform=ax.transAxes,
        ha="center", va="top",
        fontsize=20, fontweight="bold", color="#294A65",
    )
    ax.text(
        0.5, 0.90, wrap_for_plot(question, 75),
        transform=ax.transAxes,
        ha="center", va="top",
        fontsize=12, color="#476B85",
    )

    option_xs = [(i + 1) / (len(options) + 1) for i in range(len(options))]
    root_x = 0.5
    root_y = 0.74

    ax.scatter([root_x], [root_y], s=250, color="#C99A73", zorder=3)
    ax.text(
        root_x, root_y - 0.06, "Решение",
        ha="center", va="top", fontsize=9, color="#604B3D",
    )

    palette = ["#80BFE0", "#71BFA9", "#E1AE83", "#A99BD0", "#D99BB2"]
    leaf_positions = []

    for option_index, option in enumerate(options):
        ox = option_xs[option_index]
        color = palette[option_index % len(palette)]
        ax.plot([root_x, ox], [root_y, 0.52], color=color, linewidth=3, zorder=1)
        ax.scatter([ox], [0.52], s=180, color=color, zorder=3)
        ax.text(
            ox, 0.47,
            wrap_for_plot(option["name"], 20),
            ha="center", va="top", fontsize=10,
            fontweight="bold", color="#294A65",
        )
        ax.text(
            ox, 0.40,
            f"Оценка: {option['score']:.2f}",
            ha="center", va="top", fontsize=8, color="#54718A",
        )

        scenarios = option["scenarios"]
        n = len(scenarios)
        xs = [ox + (j - (n - 1) / 2) * min(0.13, 0.55 / max(n, 1)) for j in range(n)]

        for j, scenario in enumerate(scenarios):
            lx = xs[j]
            leaf_positions.append((ox, lx, scenario, option, color, j))
            ax.plot([ox, lx], [0.50, 0.29], color=color, linewidth=1.8)
            ax.scatter([lx], [0.29], s=100, color=color, alpha=0.85, zorder=3)

    for ox, lx, scenario, option, color, j in leaf_positions:
        norm_probability = option["normalized"][j]
        ax.text(
            lx, 0.24,
            wrap_for_plot(scenario["name"], 18),
            ha="center", va="top", fontsize=8, color="#294A65",
        )
        ax.text(
            lx, 0.13,
            f"{norm_probability:.1f}% · оценка {scenario['score']:g}",
            ha="center", va="top", fontsize=7, color="#54718A",
        )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return fig_to_png(fig)


def make_vertical_map_png(title, sections, note=None):
    rows = max(1, len(sections))
    fig, ax = plt.subplots(figsize=(10, max(5, rows * 1.55 + 1.5)))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, rows + 1)
    ax.axis("off")
    ax.set_facecolor("#F7FBFE")

    ax.text(
        0.5, rows + 0.78, title,
        ha="center", va="center",
        fontsize=19, fontweight="bold", color="#294A65",
    )

    colors = ["#EAF5FB", "#EFF8F6", "#F2F1FA", "#FFF6EC", "#FCEFF2"]

    for i, (heading, body) in enumerate(sections):
        y = rows - i - 0.15
        draw_box(
            ax, 0.08, y - 0.65, 0.84, 0.58,
            heading, body, colors[i % len(colors)]
        )
        if i < rows - 1:
            ax.annotate(
                "",
                xy=(0.5, y - 0.92),
                xytext=(0.5, y - 0.68),
                arrowprops=dict(arrowstyle="->", color="#7CA9C5", lw=1.6),
            )

    if note:
        ax.text(
            0.5, 0.02, wrap_for_plot(note, 110),
            ha="center", va="bottom", fontsize=8, color="#648198",
        )

    return fig_to_png(fig)


def make_act_png(situation, values, away_actions, inner_experience,
                 toward_actions, toward_inner, next_step):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_facecolor("#F7FBFE")

    ax.text(
        0.5, 0.97, "ACT-матрица",
        ha="center", va="top", fontsize=21,
        fontweight="bold", color="#294A65",
    )
    ax.text(
        0.5, 0.91, f"Ситуация: {wrap_for_plot(situation, 90)}",
        ha="center", va="top", fontsize=10, color="#54718A",
    )
    ax.text(
        0.5, 0.85, f"Что важно: {wrap_for_plot(values, 90)}",
        ha="center", va="top", fontsize=10, color="#54718A",
    )

    # Сетка квадрантов
    ax.plot([0.5, 0.5], [0.12, 0.78], color="#9DBBD0", linewidth=2)
    ax.plot([0.08, 0.92], [0.45, 0.45], color="#9DBBD0", linewidth=2)

    quadrants = [
        (0.08, 0.48, "Действия «от дискомфорта»", away_actions, "#FFF1F1"),
        (0.52, 0.48, "Действия «к важному»", toward_actions, "#EAF7F1"),
        (0.08, 0.14, "Внутренний опыт", inner_experience, "#F2F5FC"),
        (0.52, 0.14, "Внутренний опыт при движении к важному", toward_inner, "#EFF8FC"),
    ]

    for x, y, heading, body, color in quadrants:
        draw_box(ax, x, y, 0.40, 0.28, heading, body, color)

    ax.text(
        0.5, 0.075, f"Выбранный небольшой шаг: {wrap_for_plot(next_step, 100)}",
        ha="center", va="center", fontsize=10,
        fontweight="bold", color="#315773",
    )

    return fig_to_png(fig)


def download_png(label, data, filename, key):
    st.download_button(
        label=label,
        data=data,
        file_name=filename,
        mime="image/png",
        key=key,
        use_container_width=True,
    )


# -------------------------------------------------------------------
# Дерево решений
# -------------------------------------------------------------------

def new_scenario(first=False):
    return {"id": uuid.uuid4().hex, "default_probability": 100 if first else 0}


def new_option():
    return {"id": uuid.uuid4().hex, "scenarios": [new_scenario(first=True)]}


def decision_clear_result():
    st.session_state.decision_result = None


def initialize_decision_tree():
    if "dt_options" not in st.session_state:
        st.session_state.dt_options = [new_option(), new_option()]
    if "decision_result" not in st.session_state:
        st.session_state.decision_result = None
    if "decision_question" not in st.session_state:
        st.session_state.decision_question = ""


def add_decision_option():
    st.session_state.dt_options.append(new_option())
    decision_clear_result()


def delete_decision_option(option_id):
    if len(st.session_state.dt_options) <= 2:
        return
    st.session_state.dt_options = [
        item for item in st.session_state.dt_options if item["id"] != option_id
    ]
    decision_clear_result()


def add_decision_scenario(option_id):
    for option in st.session_state.dt_options:
        if option["id"] == option_id:
            option["scenarios"].append(new_scenario())
            decision_clear_result()
            break


def delete_decision_scenario(option_id, scenario_id):
    for option in st.session_state.dt_options:
        if option["id"] == option_id and len(option["scenarios"]) > 1:
            option["scenarios"] = [
                item for item in option["scenarios"] if item["id"] != scenario_id
            ]
            decision_clear_result()
            break


def option_name_key(option_id):
    return f"dt_name_{option_id}"


def scenario_name_key(scenario_id):
    return f"dt_scenario_name_{scenario_id}"


def probability_key(scenario_id):
    return f"dt_probability_{scenario_id}"


def score_key(scenario_id):
    return f"dt_score_{scenario_id}"


def render_decision_tree():
    initialize_decision_tree()

    st.title("🌿 Дерево решений")
    st.write("Разложите сложный выбор на варианты и возможные последствия.")

    st.text_input(
        "Какое решение нужно принять?",
        key="decision_question",
        placeholder="Например: «Стоит ли менять работу?»",
        on_change=decision_clear_result,
    )

    st.caption("Для каждого варианта добавьте возможные исходы, вероятности и личную оценку.")

    for option_index, option in enumerate(list(st.session_state.dt_options), start=1):
        option_id = option["id"]
        name_key = option_name_key(option_id)

        if name_key not in st.session_state:
            st.session_state[name_key] = ""

        with st.container(border=True):
            title_col, delete_col = st.columns([5, 1.5])
            with title_col:
                st.markdown(f"### Вариант {option_index}")
            with delete_col:
                st.button(
                    "Удалить вариант",
                    key=f"dt_delete_option_{option_id}",
                    disabled=len(st.session_state.dt_options) <= 2,
                    on_click=delete_decision_option,
                    args=(option_id,),
                    use_container_width=True,
                )

            st.text_input(
                "Название варианта",
                key=name_key,
                placeholder=f"Вариант {option_index}",
                on_change=decision_clear_result,
            )

            for scenario_index, scenario in enumerate(list(option["scenarios"]), start=1):
                sid = scenario["id"]
                nkey, pkey, skey = (
                    scenario_name_key(sid),
                    probability_key(sid),
                    score_key(sid),
                )

                if nkey not in st.session_state:
                    st.session_state[nkey] = ""
                if pkey not in st.session_state:
                    st.session_state[pkey] = scenario["default_probability"]
                if skey not in st.session_state:
                    st.session_state[skey] = 0.0

                with st.container(border=True):
                    head, delete = st.columns([5, 1.5])
                    with head:
                        st.markdown(f"**Сценарий {scenario_index}**")
                    with delete:
                        st.button(
                            "Удалить",
                            key=f"dt_delete_scenario_{sid}",
                            disabled=len(option["scenarios"]) <= 1,
                            on_click=delete_decision_scenario,
                            args=(option_id, sid),
                            use_container_width=True,
                        )

                    st.text_input(
                        "Описание возможного исхода",
                        key=nkey,
                        placeholder="Например: «Найду более интересную работу»",
                        on_change=decision_clear_result,
                    )

                    c1, c2 = st.columns(2)
                    with c1:
                        st.slider(
                            "Вероятность, %",
                            0, 100, step=1,
                            key=pkey,
                            on_change=decision_clear_result,
                        )
                    with c2:
                        st.slider(
                            "Оценка исхода",
                            -5.0, 5.0, step=0.5,
                            key=skey,
                            help="−5 — очень нежелательный, +5 — очень желательный.",
                            on_change=decision_clear_result,
                        )

            st.button(
                "＋ Добавить сценарий",
                key=f"dt_add_scenario_{option_id}",
                on_click=add_decision_scenario,
                args=(option_id,),
            )

    c1, c2, _ = st.columns([1.6, 1.8, 4])
    with c1:
        st.button(
            "＋ Добавить вариант",
            key="dt_add_option",
            on_click=add_decision_option,
            use_container_width=True,
        )
    with c2:
        st.button(
            "− Удалить последний",
            key="dt_remove_last",
            disabled=len(st.session_state.dt_options) <= 2,
            on_click=delete_decision_option,
            args=(st.session_state.dt_options[-1]["id"],),
            use_container_width=True,
        )

    if st.button("Рассчитать и построить дерево", type="primary", use_container_width=True):
        question = st.session_state.decision_question.strip()
        prepared = []
        error = None
        used_names = set()

        if not question:
            error = "Сначала сформулируйте решение."

        for oi, option in enumerate(st.session_state.dt_options, start=1):
            if error:
                break

            name = st.session_state.get(option_name_key(option["id"]), "").strip()
            if not name:
                error = f"Введите название варианта {oi}."
                break
            if name in used_names:
                error = f"Названия вариантов должны отличаться: «{name}»."
                break
            used_names.add(name)

            scenarios = []
            for si, scenario in enumerate(option["scenarios"], start=1):
                sid = scenario["id"]
                sname = st.session_state.get(scenario_name_key(sid), "").strip()
                if not sname:
                    error = f"Заполните сценарий {si} варианта «{name}»."
                    break
                scenarios.append({
                    "name": sname,
                    "probability": int(st.session_state[probability_key(sid)]),
                    "score": float(st.session_state[score_key(sid)]),
                })

            if error:
                break

            total = sum(s["probability"] for s in scenarios)
            if total <= 0:
                error = f"Для варианта «{name}» задайте ненулевую вероятность."
                break

            normalized = [s["probability"] / total * 100 for s in scenarios]
            expected = sum(
                normalized[i] / 100 * scenario["score"]
                for i, scenario in enumerate(scenarios)
            )

            prepared.append({
                "name": name,
                "scenarios": scenarios,
                "normalized": normalized,
                "score": expected,
            })

        if error:
            st.session_state.decision_result = None
            st.warning(error)
        else:
            best_name = max(prepared, key=lambda x: x["score"])["name"]
            st.session_state.decision_result = {
                "question": question,
                "options": prepared,
                "best_name": best_name,
            }

    result = st.session_state.decision_result
    if result:
        st.subheader("Результат")
        columns = st.columns(len(result["options"]))
        for col, option in zip(columns, result["options"]):
            with col:
                st.metric(
                    label=("🌿 " if option["name"] == result["best_name"] else "") + option["name"],
                    value=f"{option['score']:.2f} / 5",
                )

        st.success(f"По указанным оценкам лидирует вариант: **{result['best_name']}**.")
        st.caption(
            "Это ориентир для размышления, а не автоматическое решение. "
            "Вероятности нормализуются отдельно внутри каждого варианта."
        )

        image = make_decision_png(
            result["question"],
            result["options"],
        )
        st.image(image, use_container_width=True)
        download_png("⬇️ Скачать дерево решений PNG", image, "derevo-resheniy.png", "download_decision")


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
            x for x in st.session_state.chain_links if x["id"] != link_id
        ]


def render_chain():
    initialize_chain()

    st.title("🔗 Цепочный анализ поведения (ДБТ)")
    st.write("Совместно исследуйте контекст, звенья цепочки и последствия.")
    st.info("Можно сделать паузу, пропустить поле или остановиться в любой момент.")

    st.text_area(
        "Факторы уязвимости",
        key="chain_vulnerability",
        placeholder="Что могло сделать ситуацию сложнее заранее?",
    )
    st.text_area(
        "Запускающее событие",
        key="chain_prompt",
        placeholder="Что произошло непосредственно перед поведением? Опишите факты.",
    )

    st.subheader("Звенья цепочки")
    for index, link in enumerate(list(st.session_state.chain_links), start=1):
        lid = link["id"]
        with st.container(border=True):
            head, delete = st.columns([5, 1.2])
            with head:
                st.markdown(f"**Звено {index}**")
            with delete:
                st.button(
                    "Удалить",
                    key=f"chain_del_{lid}",
                    disabled=len(st.session_state.chain_links) <= 1,
                    on_click=remove_chain_link,
                    args=(lid,),
                    use_container_width=True,
                )

            c1, c2 = st.columns(2)
            with c1:
                st.text_area("Мысли или образы", key=f"chain_thought_{lid}")
                st.text_area("Ощущения в теле", key=f"chain_body_{lid}")
            with c2:
                st.text_area("Эмоции", key=f"chain_emotion_{lid}")
                st.text_area("Импульсы или действия", key=f"chain_action_{lid}")

            st.slider(
                "Интенсивность (необязательно)",
                0, 10, 0,
                key=f"chain_intensity_{lid}",
            )
            st.checkbox(
                "Отметить как возможную точку вмешательства",
                key=f"chain_intervention_{lid}",
            )
            st.text_area(
                "Возможный другой шаг, навык или поддержка",
                key=f"chain_skill_{lid}",
            )

    st.button("＋ Добавить звено", on_click=add_chain_link)

    st.subheader("Целевое поведение и последствия")
    st.text_area("Целевое поведение", key="chain_target")
    c1, c2 = st.columns(2)
    with c1:
        st.text_area("Последствия сразу после", key="chain_immediate")
    with c2:
        st.text_area("Последствия позднее", key="chain_later")
    st.text_area("Восстановление ситуации или снижение последствий", key="chain_repair")

    if st.checkbox("Показать сводную карту", value=True, key="chain_summary_toggle"):
        sections = [
            ("Факторы уязвимости", st.session_state.get("chain_vulnerability", "")),
            ("Запускающее событие", st.session_state.get("chain_prompt", "")),
        ]

        for index, link in enumerate(st.session_state.chain_links, start=1):
            lid = link["id"]
            body = "\n".join(
                f"{label}: {st.session_state.get(key, '')}"
                for label, key in [
                    ("Мысли", f"chain_thought_{lid}"),
                    ("Эмоции", f"chain_emotion_{lid}"),
                    ("Ощущения", f"chain_body_{lid}"),
                    ("Импульсы / действия", f"chain_action_{lid}"),
                ]
                if st.session_state.get(key, "").strip()
            )
            if st.session_state.get(f"chain_intervention_{lid}", False):
                body += "\n[Отмечено как возможная точка вмешательства]"
                skill = st.session_state.get(f"chain_skill_{lid}", "").strip()
                if skill:
                    body += f"\nВозможная поддержка: {skill}"
            sections.append((f"Звено {index}", body))

        sections.extend([
            ("Целевое поведение", st.session_state.get("chain_target", "")),
            ("Последствия сразу после", st.session_state.get("chain_immediate", "")),
            ("Последствия позднее", st.session_state.get("chain_later", "")),
            ("Восстановление / поддержка", st.session_state.get("chain_repair", "")),
        ])

        with st.container(border=True):
            for heading, body in sections:
                st.markdown(f"**{heading}**")
                st.write(body or "—")

        png = make_vertical_map_png(
            "Цепочный анализ поведения",
            sections,
            "Карта для обсуждения; связи и гипотезы определяются участниками.",
        )
        download_png("⬇️ Скачать карту цепочки PNG", png, "cepochniy-analiz.png", "download_chain")


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
            x for x in st.session_state.exposure_steps if x["id"] != step_id
        ]


def render_exposure():
    initialize_exposure()

    st.title("🪜 Иерархия экспозиции")
    st.write("Составьте лестницу ситуаций для обсуждения и планирования практики.")
    st.info(
        "Практика должна быть добровольной и согласованной со специалистом. "
        "Не используйте упражнение для ситуаций с реальной опасностью."
    )

    st.text_area("Цель работы", key="exposure_goal")

    records = []
    for index, item in enumerate(list(st.session_state.exposure_steps), start=1):
        sid = item["id"]
        with st.container(border=True):
            head, delete = st.columns([5, 1.2])
            with head:
                st.markdown(f"**Ступень {index}**")
            with delete:
                st.button(
                    "Удалить",
                    key=f"exposure_del_{sid}",
                    disabled=len(st.session_state.exposure_steps) <= 1,
                    on_click=remove_exposure_step,
                    args=(sid,),
                    use_container_width=True,
                )

            situation = st.text_area("Ситуация", key=f"exp_situation_{sid}")
            distress = st.slider(
                "Ожидаемая тревога (0–10)",
                0, 10, 3,
                key=f"exp_distress_{sid}",
            )
            prediction = st.text_area("Прогноз или опасение", key=f"exp_prediction_{sid}")
            plan = st.text_area("Обсуждаемый посильный шаг", key=f"exp_plan_{sid}")
            status = st.selectbox(
                "Статус",
                ["Не обсуждали", "Обсудили", "Запланировали", "Попробовали"],
                key=f"exp_status_{sid}",
            )
            reflection = st.text_area(
                "Наблюдения после практики — необязательно",
                key=f"exp_reflection_{sid}",
            )

        records.append({
            "situation": situation,
            "distress": distress,
            "prediction": prediction,
            "plan": plan,
            "status": status,
            "reflection": reflection,
            "index": index,
        })

    st.button("＋ Добавить ступень", on_click=add_exposure_step)

    ordered = sorted(records, key=lambda x: (x["distress"], x["index"]))
    sections = [("Цель", st.session_state.get("exposure_goal", ""))]

    st.subheader("Лестница по ожидаемой тревоге")
    for position, item in enumerate(ordered, start=1):
        if not item["situation"].strip():
            continue

        with st.container(border=True):
            st.markdown(
                f"**{position}. {item['situation']}** — "
                f"ожидаемая тревога: **{item['distress']}/10**"
            )
            st.caption(f"Статус: {item['status']}")
            if item["prediction"]:
                st.write(f"**Прогноз:** {item['prediction']}")
            if item["plan"]:
                st.write(f"**Шаг:** {item['plan']}")
            if item["reflection"]:
                st.write(f"**Наблюдения:** {item['reflection']}")

        sections.append((
            f"Ступень {position} · тревога {item['distress']}/10 · {item['status']}",
            "\n".join([
                f"Ситуация: {item['situation']}",
                f"Прогноз: {item['prediction']}",
                f"Планируемый шаг: {item['plan']}",
                f"Наблюдения: {item['reflection']}",
            ]),
        ))

    if len(sections) > 1:
        png = make_vertical_map_png(
            "Иерархия экспозиции",
            sections,
            "Порядок ступеней — материал для обсуждения, а не автоматическое назначение.",
        )
        download_png("⬇️ Скачать лестницу PNG", png, "ierarhiya-ekspozicii.png", "download_exposure")


# -------------------------------------------------------------------
# ACT-матрица
# -------------------------------------------------------------------

def render_act_matrix():
    st.title("🧭 ACT-матрица")
    st.write("Исследуйте, что уводит от дискомфорта и какие действия приближают к важному.")
    st.info(
        "Матрица — материал для совместного исследования. Она не оценивает "
        "поведение как правильное или неправильное."
    )

    situation = st.text_area("Ситуация, которую хотите исследовать", key="act_situation")
    values = st.text_area(
        "Кто или что важно для вас? Какие качества жизни вы хотите воплощать?",
        key="act_values",
        placeholder="Например: близость, забота, любознательность, независимость.",
    )

    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown("### Действия «от дискомфорта»")
            away_actions = st.text_area(
                "Что вы делаете, чтобы избежать дискомфорта?",
                key="act_away_actions",
                placeholder="Например: откладываю разговор, отменяю встречу.",
            )
        with st.container(border=True):
            st.markdown("### Внутренний опыт")
            inner_experience = st.text_area(
                "Мысли, эмоции, телесные ощущения",
                key="act_inner_experience",
                placeholder="Что возникает внутри в этой ситуации?",
            )

    with right:
        with st.container(border=True):
            st.markdown("### Действия «к важному»")
            toward_actions = st.text_area(
                "Какое действие приближает к важному?",
                key="act_toward_actions",
                placeholder="Какой наблюдаемый шаг можно сделать?",
            )
        with st.container(border=True):
            st.markdown("### Внутренний опыт при движении к важному")
            toward_inner = st.text_area(
                "Что может возникать внутри при этом шаге?",
                key="act_toward_inner",
                placeholder="Например: волнение, сомнение, надежда.",
            )

    next_step = st.text_area(
        "Небольшой выбранный шаг",
        key="act_next_step",
        placeholder="Какой шаг вы сами хотели бы попробовать?",
    )

    if st.checkbox("Показать сводную матрицу", value=True, key="act_show_summary"):
        png = make_act_png(
            situation, values, away_actions, inner_experience,
            toward_actions, toward_inner, next_step,
        )
        st.image(png, use_container_width=True)
        download_png("⬇️ Скачать ACT-матрицу PNG", png, "act-matrix.png", "download_act")


# -------------------------------------------------------------------
# Главная, библиотека, о нас
# -------------------------------------------------------------------

def render_home():
    hero_html = """
    <div style="
        min-height:350px;
        display:flex;
        align-items:center;
        justify-content:center;
        padding:42px 25px;
        box-sizing:border-box;
        border:1px solid #C9E0EF;
        border-radius:30px;
        background:linear-gradient(135deg, rgba(229,243,252,.96), rgba(244,250,254,.96), rgba(220,239,250,.96));
        box-shadow:0 18px 42px rgba(48,105,145,.12);
        text-align:center;
        overflow:hidden;
        position:relative;
        font-family:'Nunito Sans',Arial,sans-serif;
    ">
      <svg viewBox="0 0 1200 480" preserveAspectRatio="xMidYMid slice"
           xmlns="http://www.w3.org/2000/svg"
           style="position:absolute;inset:0;width:100%;height:100%;opacity:.48;pointer-events:none">
        <g fill="none" stroke="#5794BB" stroke-width="2">
          <path d="M40 95 L170 155 L285 80 L420 145 L545 65"/>
          <path d="M170 155 L250 285 L390 250 L420 145"/>
          <path d="M390 250 L520 330 L650 260 L770 325"/>
          <path d="M545 65 L680 120 L810 65 L930 145"/>
          <path d="M680 120 L650 260"/>
          <path d="M930 145 L1080 90 L1170 170"/>
          <path d="M930 145 L980 285 L1130 330"/>
          <path d="M770 325 L850 415 L980 285"/>
        </g>
        <g fill="#4D8FB8" stroke="#F5FAFE" stroke-width="5">
          <circle cx="40" cy="95" r="10"/><circle cx="170" cy="155" r="13"/>
          <circle cx="285" cy="80" r="10"/><circle cx="420" cy="145" r="12"/>
          <circle cx="545" cy="65" r="9"/><circle cx="250" cy="285" r="10"/>
          <circle cx="390" cy="250" r="13"/><circle cx="520" cy="330" r="10"/>
          <circle cx="650" cy="260" r="12"/><circle cx="680" cy="120" r="9"/>
          <circle cx="810" cy="65" r="12"/><circle cx="930" cy="145" r="13"/>
          <circle cx="1080" cy="90" r="10"/><circle cx="980" cy="285" r="11"/>
          <circle cx="1130" cy="330" r="9"/><circle cx="850" cy="415" r="10"/>
        </g>
      </svg>
      <div style="position:relative;z-index:1;max-width:820px">
        <div style="
            color:#214D6C;font-size:clamp(3.8rem,9vw,6.7rem);
            font-weight:800;line-height:1;letter-spacing:.035em;
            text-shadow:0 3px 14px rgba(255,255,255,.75)">
            ПСИ-БЛОК
        </div>
        <div style="
            max-width:760px;margin:20px auto 0 auto;color:#476B85;
            font-size:1.2rem;line-height:1.7">
            Пространство с наглядными инструментами для совместной работы
            психолога и клиента. Мы создаём его, чтобы структурировать
            обсуждение и помогать возвращаться к важным идеям в ходе работы.
        </div>
      </div>
    </div>
    """
    components.html(hero_html, height=380, scrolling=False)

    left, right = st.columns(2)
    with left:
        st.button(
            "📚  Библиотека техник",
            type="primary",
            use_container_width=True,
            on_click=go_library,
        )
    with right:
        st.button(
            "ℹ️  О нас",
            type="primary",
            use_container_width=True,
            on_click=go_about,
        )

    st.divider()
    st.markdown("### Инструменты для совместной работы")
    st.write(
        "Выберите технику, чтобы открыть интерактивный черновик. "
        "Материалы поддерживают обсуждение, но не заменяют профессиональную "
        "оценку или терапевтическую работу."
    )


def render_library():
    st.title("📚 Библиотека техник")
    st.write("Выберите инструмент, который хотите открыть.")

    items = list(TECHNIQUES.items())
    for start in range(0, len(items), 2):
        columns = st.columns(2)
        for column, (technique_id, technique) in zip(columns, items[start:start + 2]):
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
        для психологических консультаций. Его цель — помочь специалисту
        и клиенту совместно структурировать обсуждение и наглядно фиксировать
        идеи. Инструменты не заменяют психолога и не принимают решения за клиента.
        """
    )

    st.divider()
    st.subheader("Команда разработчиков")

    developers = [
        {"name": "Имя Фамилия", "role": "Роль в проекте", "photo": "assets/developer1.jpg"},
        {"name": "Имя Фамилия", "role": "Роль в проекте", "photo": "assets/developer2.jpg"},
        {"name": "Имя Фамилия", "role": "Роль в проекте", "photo": "assets/developer3.jpg"},
    ]

    columns = st.columns(3)
    for column, person in zip(columns, developers):
        with column:
            with st.container(border=True):
                path = Path(person["photo"])
                if path.exists():
                    st.image(str(path), use_container_width=True)
                else:
                    st.markdown(
                        "<div style='height:220px;display:flex;align-items:center;"
                        "justify-content:center;border-radius:14px;"
                        "background:linear-gradient(135deg,#E3F2FB,#F4FAFE);"
                        "font-size:4rem'>👤</div>",
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"<div class='developer-name'>{safe_text(person['name'])}</div>"
                    f"<div class='developer-role'>{safe_text(person['role'])}</div>",
                    unsafe_allow_html=True,
                )

    st.divider()
    st.warning(
        "Это прототип. Не вводите идентифицирующие или особо чувствительные "
        "сведения: защищённое хранение клиентских данных пока не реализовано."
    )


def render_technique():
    technique_id = st.session_state.selected_technique
    technique = TECHNIQUES.get(technique_id)

    if not technique:
        st.warning("Техника не найдена.")
        st.button("Вернуться в библиотеку", on_click=go_library)
        return

    st.button("← К библиотеке", on_click=go_library)
    st.divider()

    if technique_id == "decision_tree":
        render_decision_tree()
    elif technique_id == "dbt_chain":
        render_chain()
    elif technique_id == "exposure":
        render_exposure()
    elif technique_id == "act_matrix":
        render_act_matrix()


# -------------------------------------------------------------------
# Роутинг
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
    render_technique()
else:
    st.session_state.page = "home"
    render_home()
