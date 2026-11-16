import base64
import html
import textwrap
import uuid
from pathlib import Path

import streamlit as st


# ---------------------------------------------------------------------
# Настройки страницы
# ---------------------------------------------------------------------

st.set_page_config(
    page_title="ПСИ-БЛОК",
    page_icon="🌿",
    layout="wide",
)


# ---------------------------------------------------------------------
# Декоративный фон с полупрозрачными нейронами
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
  <g fill="#4389B5" fill-opacity="0.18" stroke="#FFFFFF" stroke-opacity="0.75" stroke-width="3">
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

NEURON_BACKGROUND = base64.b64encode(
    NEURON_SVG.encode("utf-8")
).decode("ascii")


# ---------------------------------------------------------------------
# Дизайн
# ---------------------------------------------------------------------

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700;800&display=swap');

    .stApp {{
        background-color: #F3F9FD;
        background-image:
            radial-gradient(ellipse at 10% 5%, rgba(196, 228, 248, .62), transparent 34%),
            radial-gradient(ellipse at 92% 18%, rgba(219, 239, 251, .72), transparent 36%),
            url("data:image/svg+xml;base64,{NEURON_BACKGROUND}");
        background-size: auto, auto, 1000px 800px;
        background-position: center, center, left top;
        background-repeat: no-repeat, no-repeat, repeat;
        background-attachment: fixed, fixed, fixed;
        color: #294A65;
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    .block-container {{
        max-width: 1120px;
        padding-top: 1.2rem;
        padding-bottom: 4rem;
    }}

    h1, h2, h3, h4, p, label, button, input, textarea {{
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }}

    h1, h2, h3, h4 {{
        color: #294A65 !important;
        letter-spacing: -0.025em;
    }}

    h1 {{ font-size: 2.6rem !important; font-weight: 800 !important; }}
    h2 {{ font-size: 1.85rem !important; font-weight: 800 !important; }}
    h3 {{ font-size: 1.3rem !important; font-weight: 800 !important; }}

    p, label, [data-testid="stCaptionContainer"] {{
        color: #54718A;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        border: 1px solid #D4E5F1 !important;
        border-radius: 20px !important;
        background: rgba(255,255,255,0.93) !important;
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


# ---------------------------------------------------------------------
# Общие функции
# ---------------------------------------------------------------------

def escape_text(value):
    return html.escape(str(value or ""))


def svg_text_lines(text, x, y, max_chars=24, font_size=13, color="#294A65"):
    """Создаёт SVG text с переносами строк."""
    text = str(text or "").strip()
    if not text:
        text = "—"

    lines = textwrap.wrap(text, width=max_chars) or ["—"]
    lines = lines[:4]

    spans = []
    for index, line in enumerate(lines):
        dy = "0" if index == 0 else str(font_size + 4)
        spans.append(
            f'<tspan x="{x}" dy="{dy}">{escape_text(line)}</tspan>'
        )

    return (
        f'<text x="{x}" y="{y}" text-anchor="middle" '
        f'font-family="Arial, sans-serif" font-size="{font_size}" '
        f'fill="{color}">{"".join(spans)}</text>'
    )


def svg_card(x, y, width, height, title, body, fill="#FFFFFF", stroke="#B8D5E7"):
    title_y = y + 27
    body_y = y + 52
    return f"""
    <rect x="{x}" y="{y}" width="{width}" height="{height}" rx="16"
          fill="{fill}" stroke="{stroke}" stroke-width="2"/>
    <text x="{x + width / 2}" y="{title_y}" text-anchor="middle"
          font-family="Arial, sans-serif" font-size="14"
          font-weight="bold" fill="#294A65">{escape_text(title)}</text>
    {svg_text_lines(body, x + width / 2, body_y, max_chars=max(12, int(width / 8)), font_size=12)}
    """


def svg_document(title, content, width=1000, height=700):
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"
         viewBox="0 0 {width} {height}">
      <rect width="100%" height="100%" rx="24" fill="#F5FAFE"/>
      <text x="{width / 2}" y="42" text-anchor="middle"
            font-family="Arial, sans-serif" font-size="25"
            font-weight="bold" fill="#294A65">{escape_text(title)}</text>
      {content}
    </svg>
    """


def download_svg(label, svg, filename, key):
    st.download_button(
        label=label,
        data=svg.encode("utf-8"),
        file_name=filename,
        mime="image/svg+xml",
        key=key,
        use_container_width=True,
    )


# ---------------------------------------------------------------------
# Каталог и навигация
# ---------------------------------------------------------------------

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
    home_col, library_col, _ = st.columns([1.2, 1.2, 5])

    with home_col:
        st.button("⌂ Главная", on_click=go_home, use_container_width=True)

    with library_col:
        st.button("Библиотека", on_click=go_library, use_container_width=True)


# ---------------------------------------------------------------------
# Скачиваемые карты SVG
# ---------------------------------------------------------------------

def make_decision_svg(question, options):
    width = max(1000, len(options) * 370)
    height = 720
    content = []

    root_x = width / 2
    root_y = 620
    content.append(
        f'<line x1="{root_x}" y1="565" x2="{root_x}" y2="{root_y}" '
        'stroke="#B98D6C" stroke-width="10" stroke-linecap="round"/>'
    )
    content.append(svg_card(root_x - 190, 555, 380, 85, "Решение", question, "#F4E2D2", "#D8A77E"))

    option_xs = [
        width * (index + 1) / (len(options) + 1)
        for index in range(len(options))
    ]
    palette = ["#80BFE0", "#71BFA9", "#E1AE83", "#A99BD0", "#D99BB2"]

    for oi, option in enumerate(options):
        ox = option_xs[oi]
        color = palette[oi % len(palette)]
        content.append(
            f'<line x1="{root_x}" y1="555" x2="{ox}" y2="430" '
            f'stroke="{color}" stroke-width="6" stroke-linecap="round"/>'
        )
        content.append(
            f'<circle cx="{ox}" cy="430" r="14" fill="{color}" stroke="white" stroke-width="4"/>'
        )
        content.append(
            svg_card(ox - 135, 350, 270, 75, option["name"],
                     f"Итоговая оценка: {option['score']:.2f}", "#FFFFFF", color)
        )

        scenarios = option["scenarios"]
        n = len(scenarios)
        spacing = min(260, 700 / max(n, 1))
        start_x = ox - (n - 1) * spacing / 2

        for si, scenario in enumerate(scenarios):
            sx = start_x + si * spacing
            content.append(
                f'<line x1="{ox}" y1="350" x2="{sx}" y2="220" '
                f'stroke="{color}" stroke-width="3"/>'
            )
            content.append(
                f'<circle cx="{sx}" cy="220" r="11" fill="{color}" stroke="white" stroke-width="3"/>'
            )
            body = (
                f"{scenario['name']} · {option['normalized'][si]:.1f}% "
                f"· оценка {scenario['score']:g}"
            )
            content.append(
                svg_card(sx - 120, 95, 240, 110, f"Исход {si + 1}", body, "#FFFFFF", color)
            )

    return svg_document("Дерево решений", "".join(content), width, height)


def make_vertical_svg(title, sections, note=""):
    width = 1000
    card_height = 90
    gap = 22
    top = 85
    height = max(250, top + len(sections) * (card_height + gap) + 90)
    content = []

    for index, (heading, body) in enumerate(sections):
        y = top + index * (card_height + gap)
        fill = "#EAF5FB" if index % 2 == 0 else "#F1F8FC"
        content.append(svg_card(100, y, 800, card_height, heading, body, fill, "#AFCFE2"))

        if index < len(sections) - 1:
            content.append(
                f'<line x1="500" y1="{y + card_height}" x2="500" y2="{y + card_height + gap - 4}" '
                'stroke="#78A8BF" stroke-width="3"/>'
            )
            content.append(
                f'<circle cx="500" cy="{y + card_height + gap / 2}" r="5" fill="#78A8BF"/>'
            )

    if note:
        content.append(
            f'<text x="500" y="{height - 24}" text-anchor="middle" '
            'font-family="Arial, sans-serif" font-size="12" fill="#648198">'
            f'{escape_text(note)}</text>'
        )

    return svg_document(title, "".join(content), width, height)


def make_act_svg(situation, values, away_actions, inner, toward_actions, toward_inner, next_step):
    content = []

    content.append(
        f'<text x="500" y="82" text-anchor="middle" font-family="Arial" font-size="14" fill="#476B85">'
        f'Ситуация: {escape_text(situation or "—")}</text>'
    )
    content.append(
        f'<text x="500" y="108" text-anchor="middle" font-family="Arial" font-size="14" fill="#476B85">'
        f'Что важно: {escape_text(values or "—")}</text>'
    )

    content.append('<line x1="500" y1="145" x2="500" y2="600" stroke="#9DBBD0" stroke-width="3"/>')
    content.append('<line x1="70" y1="370" x2="930" y2="370" stroke="#9DBBD0" stroke-width="3"/>')

    content.append(svg_card(80, 155, 390, 195, "Действия «от дискомфорта»", away_actions, "#FFF1F1", "#D9A6A6"))
    content.append(svg_card(530, 155, 390, 195, "Действия «к важному»", toward_actions, "#EAF7F1", "#9FC9B4"))
    content.append(svg_card(80, 390, 390, 195, "Внутренний опыт", inner, "#F2F5FC", "#B6C5DE"))
    content.append(svg_card(530, 390, 390, 195, "Внутренний опыт при движении к важному", toward_inner, "#EFF8FC", "#AFCFE2"))

    content.append(
        f'<text x="500" y="640" text-anchor="middle" font-family="Arial" '
        f'font-size="14" font-weight="bold" fill="#315773">'
        f'Небольшой выбранный шаг: {escape_text(next_step or "—")}</text>'
    )

    return svg_document("ACT-матрица", "".join(content), 1000, 690)


# ---------------------------------------------------------------------
# Дерево решений
# ---------------------------------------------------------------------

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


def initialize_decision_tree():
    if "dt_options" not in st.session_state:
        st.session_state.dt_options = [new_option(), new_option()]
    if "dt_result" not in st.session_state:
        st.session_state.dt_result = None
    if "dt_question" not in st.session_state:
        st.session_state.dt_question = ""


def clear_decision_result():
    st.session_state.dt_result = None


def option_name_key(option_id):
    return f"dt_option_name_{option_id}"


def scenario_name_key(scenario_id):
    return f"dt_scenario_name_{scenario_id}"


def probability_key(scenario_id):
    return f"dt_probability_{scenario_id}"


def score_key(scenario_id):
    return f"dt_score_{scenario_id}"


def add_option():
    st.session_state.dt_options.append(new_option())
    clear_decision_result()


def delete_option(option_id):
    if len(st.session_state.dt_options) <= 2:
        return
    st.session_state.dt_options = [
        option for option in st.session_state.dt_options
        if option["id"] != option_id
    ]
    clear_decision_result()


def add_scenario(option_id):
    for option in st.session_state.dt_options:
        if option["id"] == option_id:
            option["scenarios"].append(new_scenario())
            clear_decision_result()
            return


def delete_scenario(option_id, scenario_id):
    for option in st.session_state.dt_options:
        if option["id"] == option_id and len(option["scenarios"]) > 1:
            option["scenarios"] = [
                scenario for scenario in option["scenarios"]
                if scenario["id"] != scenario_id
            ]
            clear_decision_result()
            return


def render_decision_tree():
    initialize_decision_tree()

    st.title("🌿 Дерево решений")
    st.write("Разложите сложный выбор на варианты и возможные последствия.")

    st.text_input(
        "Какое решение нужно принять?",
        key="dt_question",
        placeholder="Например: «Стоит ли менять работу?»",
        on_change=clear_decision_result,
    )

    st.caption("Для каждого варианта добавьте исходы, их вероятности и личную оценку.")

    for oi, option in enumerate(list(st.session_state.dt_options), start=1):
        oid = option["id"]
        name_key = option_name_key(oid)

        if name_key not in st.session_state:
            st.session_state[name_key] = ""

        with st.container(border=True):
            header, delete_col = st.columns([5, 1.5])
            with header:
                st.markdown(f"### Вариант {oi}")
            with delete_col:
                st.button(
                    "Удалить вариант",
                    key=f"dt_delete_option_{oid}",
                    disabled=len(st.session_state.dt_options) <= 2,
                    on_click=delete_option,
                    args=(oid,),
                    use_container_width=True,
                )

            st.text_input(
                "Название варианта",
                key=name_key,
                placeholder=f"Вариант {oi}",
                on_change=clear_decision_result,
            )

            for si, scenario in enumerate(list(option["scenarios"]), start=1):
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
                    row1, row2 = st.columns([5, 1.5])
                    with row1:
                        st.markdown(f"**Сценарий {si}**")
                    with row2:
                        st.button(
                            "Удалить сценарий",
                            key=f"dt_delete_scenario_{sid}",
                            disabled=len(option["scenarios"]) <= 1,
                            on_click=delete_scenario,
                            args=(oid, sid),
                            use_container_width=True,
                        )

                    st.text_input(
                        "Описание возможного исхода",
                        key=nkey,
                        placeholder="Например: «Найду более интересную работу»",
                        on_change=clear_decision_result,
                    )

                    c1, c2 = st.columns(2)
                    with c1:
                        st.slider(
                            "Вероятность, %",
                            min_value=0,
                            max_value=100,
                            step=1,
                            key=pkey,
                            on_change=clear_decision_result,
                        )
                    with c2:
                        st.slider(
                            "Оценка исхода",
                            min_value=-5.0,
                            max_value=5.0,
                            step=0.5,
                            key=skey,
                            help="−5 — очень нежелательный, +5 — очень желательный.",
                            on_change=clear_decision_result,
                        )

            st.button(
                "＋ Добавить сценарий",
                key=f"dt_add_scenario_{oid}",
                on_click=add_scenario,
                args=(oid,),
            )

    c1, c2, _ = st.columns([1.7, 1.9, 4])
    with c1:
        st.button(
            "＋ Добавить вариант",
            key="dt_add_option",
            on_click=add_option,
            use_container_width=True,
        )
    with c2:
        st.button(
            "− Удалить последний",
            key="dt_remove_last",
            disabled=len(st.session_state.dt_options) <= 2,
            on_click=delete_option,
            args=(st.session_state.dt_options[-1]["id"],),
            use_container_width=True,
        )

    if st.button("Рассчитать и построить дерево", type="primary", use_container_width=True):
        question = st.session_state.dt_question.strip()
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
                scenario_name = st.session_state.get(scenario_name_key(sid), "").strip()

                if not scenario_name:
                    error = f"Заполните сценарий {si} варианта «{name}»."
                    break

                scenarios.append({
                    "name": scenario_name,
                    "probability": int(st.session_state[probability_key(sid)]),
                    "score": float(st.session_state[score_key(sid)]),
                })

            if error:
                break

            total = sum(item["probability"] for item in scenarios)
            if total == 0:
                error = f"Для варианта «{name}» задайте ненулевую вероятность."
                break

            normalized = [item["probability"] / total * 100 for item in scenarios]
            expected = sum(
                normalized[index] / 100 * item["score"]
                for index, item in enumerate(scenarios)
            )

            prepared.append({
                "name": name,
                "scenarios": scenarios,
                "normalized": normalized,
                "score": expected,
            })

        if error:
            st.session_state.dt_result = None
            st.warning(error)
        else:
            best_name = max(prepared, key=lambda item: item["score"])["name"]
            st.session_state.dt_result = {
                "question": question,
                "options": prepared,
                "best_name": best_name,
            }

    result = st.session_state.dt_result
    if result:
        st.subheader("Результат")
        columns = st.columns(len(result["options"]))

        for column, option in zip(columns, result["options"]):
            with column:
                label = ("🌿 " if option["name"] == result["best_name"] else "") + option["name"]
                st.metric(label=label, value=f"{option['score']:.2f} / 5")

        st.info(
            f"По указанным оценкам лидирует вариант: **{result['best_name']}**. "
            "Это материал для размышления, а не автоматическое решение."
        )

        svg = make_decision_svg(result["question"], result["options"])
        st.image(svg.encode("utf-8"), use_container_width=True)
        download_svg("⬇️ Скачать дерево решений (SVG)", svg, "derevo-resheniy.svg", "download_decision_svg")


# ---------------------------------------------------------------------
# Цепочный анализ ДБТ
# ---------------------------------------------------------------------

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


def render_chain():
    initialize_chain()

    st.title("🔗 Цепочный анализ поведения (ДБТ)")
    st.write("Исследуйте контекст, последовательность реакций, поведение и последствия.")
    st.info("Можно сделать паузу, пропустить поле или остановиться в любой момент.")

    vulnerability = st.text_area(
        "Факторы уязвимости",
        key="chain_vulnerability",
        placeholder="Что могло сделать ситуацию сложнее заранее?",
    )
    prompting = st.text_area(
        "Запускающее событие",
        key="chain_prompt",
        placeholder="Что произошло непосредственно перед поведением? Опишите факты.",
    )

    st.subheader("Звенья цепочки")
    sections = [
        ("Факторы уязвимости", vulnerability),
        ("Запускающее событие", prompting),
    ]

    for index, link in enumerate(list(st.session_state.chain_links), start=1):
        lid = link["id"]

        with st.container(border=True):
            title_col, delete_col = st.columns([5, 1.5])
            with title_col:
                st.markdown(f"**Звено {index}**")
            with delete_col:
                st.button(
                    "Удалить",
                    key=f"chain_delete_{lid}",
                    disabled=len(st.session_state.chain_links) <= 1,
                    on_click=remove_chain_link,
                    args=(lid,),
                    use_container_width=True,
                )

            c1, c2 = st.columns(2)
            with c1:
                thought = st.text_area("Мысли или образы", key=f"chain_thought_{lid}")
                body = st.text_area("Ощущения в теле", key=f"chain_body_{lid}")
            with c2:
                emotion = st.text_area("Эмоции", key=f"chain_emotion_{lid}")
                action = st.text_area("Импульсы или действия", key=f"chain_action_{lid}")

            st.slider(
                "Интенсивность (необязательно)",
                min_value=0,
                max_value=10,
                value=0,
                key=f"chain_intensity_{lid}",
            )
            intervention = st.checkbox(
                "Отметить как возможную точку вмешательства",
                key=f"chain_intervention_{lid}",
            )
            skill = st.text_area(
                "Возможный другой шаг, навык или поддержка",
                key=f"chain_skill_{lid}",
            )

        body_text = "\n".join(
            f"{label}: {value}"
            for label, value in [
                ("Мысли", thought),
                ("Эмоции", emotion),
                ("Ощущения в теле", body),
                ("Импульсы / действия", action),
            ]
            if value.strip()
        )
        if intervention:
            body_text += "\nВозможная точка вмешательства"
        if skill.strip():
            body_text += f"\nВозможная поддержка: {skill}"

        sections.append((f"Звено {index}", body_text))

    st.button("＋ Добавить звено", on_click=add_chain_link)

    st.subheader("Целевое поведение и последствия")
    target = st.text_area("Целевое поведение", key="chain_target")
    c1, c2 = st.columns(2)
    with c1:
        immediate = st.text_area("Последствия сразу после", key="chain_immediate")
    with c2:
        later = st.text_area("Последствия позднее", key="chain_later")
    repair = st.text_area("Восстановление ситуации или поддержка", key="chain_repair")

    sections.extend([
        ("Целевое поведение", target),
        ("Последствия сразу после", immediate),
        ("Последствия позднее", later),
        ("Восстановление / поддержка", repair),
    ])

    with st.expander("Показать сводную карту", expanded=True):
        for heading, body in sections:
            st.markdown(f"**{heading}**")
            st.write(body or "—")

    svg = make_vertical_svg(
        "Цепочный анализ поведения",
        sections,
        "Карта для обсуждения, а не диагноз или автоматическая оценка.",
    )
    download_svg("⬇️ Скачать карту цепочки (SVG)", svg, "cepochniy-analiz.svg", "download_chain_svg")


# ---------------------------------------------------------------------
# Иерархия экспозиции
# ---------------------------------------------------------------------

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
            item for item in st.session_state.exposure_steps
            if item["id"] != step_id
        ]


def render_exposure():
    initialize_exposure()

    st.title("🪜 Иерархия экспозиции")
    st.write("Составьте лестницу ситуаций для обсуждения и планирования практики.")
    st.info(
        "Практика должна быть добровольной и согласованной со специалистом. "
        "Не используйте упражнение для ситуаций с реальной опасностью."
    )

    goal = st.text_area("Цель работы", key="exposure_goal")
    records = []

    for index, step in enumerate(list(st.session_state.exposure_steps), start=1):
        sid = step["id"]

        with st.container(border=True):
            title_col, delete_col = st.columns([5, 1.5])
            with title_col:
                st.markdown(f"**Ступень {index}**")
            with delete_col:
                st.button(
                    "Удалить",
                    key=f"exposure_delete_{sid}",
                    disabled=len(st.session_state.exposure_steps) <= 1,
                    on_click=remove_exposure_step,
                    args=(sid,),
                    use_container_width=True,
                )

            situation = st.text_area("Ситуация", key=f"exp_situation_{sid}")
            distress = st.slider(
                "Ожидаемая тревога (0–10)",
                min_value=0,
                max_value=10,
                value=3,
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

    ordered = sorted(records, key=lambda item: (item["distress"], item["index"]))
    sections = [("Цель", goal)]

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
                st.write(f"**Обсуждаемый шаг:** {item['plan']}")
            if item["reflection"]:
                st.write(f"**Наблюдения:** {item['reflection']}")

        sections.append((
            f"Ступень {position} · тревога {item['distress']}/10 · {item['status']}",
            "\n".join([
                f"Ситуация: {item['situation']}",
                f"Прогноз: {item['prediction']}",
                f"Шаг: {item['plan']}",
                f"Наблюдения: {item['reflection']}",
            ]),
        ))

    svg = make_vertical_svg(
        "Иерархия экспозиции",
        sections,
        "Порядок ступеней — материал для обсуждения, не автоматическое назначение.",
    )
    download_svg("⬇️ Скачать лестницу (SVG)", svg, "ierarhiya-ekspozicii.svg", "download_exposure_svg")


# ---------------------------------------------------------------------
# ACT-матрица
# ---------------------------------------------------------------------

def render_act_matrix():
    st.title("🧭 ACT-матрица")
    st.write("Исследуйте, что уводит от дискомфорта и какие действия приближают к важному.")
    st.info("Матрица — материал для совместного исследования, а не оценка правильности поведения.")

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
            inner = st.text_area(
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

    svg = make_act_svg(
        situation,
        values,
        away_actions,
        inner,
        toward_actions,
        toward_inner,
        next_step,
    )

    st.subheader("Предварительный вид карты")
    st.image(svg.encode("utf-8"), use_container_width=True)
    download_svg("⬇️ Скачать ACT-матрицу (SVG)", svg, "act-matrix.svg", "download_act_svg")


# ---------------------------------------------------------------------
# Страницы сайта
# ---------------------------------------------------------------------

def render_home():
    st.markdown(
        """
        <div style="
            min-height:350px;
            display:flex;
            align-items:center;
            justify-content:center;
            padding:42px 25px;
            margin:20px 0 26px 0;
            box-sizing:border-box;
            border:1px solid #C9E0EF;
            border-radius:30px;
            background:linear-gradient(135deg,rgba(229,243,252,.96),rgba(244,250,254,.96),rgba(220,239,250,.96));
            box-shadow:0 18px 42px rgba(48,105,145,.12);
            text-align:center;
        ">
          <div style="max-width:820px">
            <div style="
                color:#214D6C;
                font-family:Arial,sans-serif;
                font-size:clamp(3.8rem,9vw,6.7rem);
                font-weight:800;
                line-height:1;
                letter-spacing:.035em;
                text-shadow:0 3px 14px rgba(255,255,255,.75)">
                ПСИ-БЛОК
            </div>
            <div style="
                max-width:760px;
                margin:20px auto 0 auto;
                color:#476B85;
                font-family:Arial,sans-serif;
                font-size:1.2rem;
                line-height:1.7">
                Пространство с наглядными инструментами для совместной работы
                психолога и клиента. Мы создаём его, чтобы структурировать
                обсуждение и помогать возвращаться к важным идеям в ходе работы.
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
        {
            "name": "Имя Фамилия",
            "role": "Роль в проекте",
            "photo": "assets/developer3.jpg",
        },
    ]

    columns = st.columns(3)
    for column, person in zip(columns, developers):
        with column:
            with st.container(border=True):
                photo_path = Path(person["photo"])

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
                            background:linear-gradient(135deg,#E3F2FB,#F4FAFE);
                            font-size:4rem;">
                            👤
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"<div class='developer-name'>{escape_text(person['name'])}</div>"
                    f"<div class='developer-role'>{escape_text(person['role'])}</div>",
                    unsafe_allow_html=True,
                )

    st.divider()
    st.warning(
        "Это прототип. Не вводите идентифицирующие или особо чувствительные "
        "сведения: защищённое хранение клиентских данных пока не реализовано."
    )


def render_selected_technique():
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


# ---------------------------------------------------------------------
# Запуск приложения
# ---------------------------------------------------------------------

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
