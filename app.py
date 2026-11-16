import html
import textwrap
import uuid
from pathlib import Path
from io import BytesIO

import streamlit as st
from PIL import Image, ImageDraw, ImageFont


st.set_page_config(
    page_title="ПСИ-БЛОК",
    page_icon="🌿",
    layout="wide",
)


# ---------------------------------------------------------------------
# Дизайн и нейронный узор
# ---------------------------------------------------------------------

NEURON_PATTERN = """
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
  <g fill="#4389B5" fill-opacity="0.17" stroke="#FFFFFF" stroke-opacity="0.75" stroke-width="3">
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

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700;800&display=swap');

    .stApp {
        background-color: #F3F9FD;
        color: #294A65;
    }

    [data-testid="stAppViewContainer"] {
        background-image:
            radial-gradient(ellipse at 10% 5%, rgba(196,228,248,.58), transparent 34%),
            radial-gradient(ellipse at 92% 18%, rgba(219,239,251,.68), transparent 36%);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1120px;
        padding-top: 1.2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3, h4, p, label, button, input, textarea {
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }

    h1, h2, h3, h4 {
        color: #294A65 !important;
        letter-spacing: -0.025em;
    }

    h1 { font-size: 2.6rem !important; font-weight: 800 !important; }
    h2 { font-size: 1.85rem !important; font-weight: 800 !important; }
    h3 { font-size: 1.3rem !important; font-weight: 800 !important; }

    p, label, [data-testid="stCaptionContainer"] {
        color: #54718A;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #D4E5F1 !important;
        border-radius: 20px !important;
        background: rgba(255,255,255,.93) !important;
        box-shadow: 0 10px 26px rgba(62,112,148,.08);
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {
        border: 1px solid #C9DDEB;
        border-radius: 13px;
        background: #FFFFFF;
        color: #294A65;
    }

    .stButton > button {
        min-height: 46px;
        border: 1px solid #C1D8E9;
        border-radius: 14px;
        background: #F4F9FD;
        color: #315773;
        font-size: 1rem;
        font-weight: 700;
        transition: .18s ease;
    }

    .stButton > button:hover:not(:disabled) {
        border-color: #8FB9D5;
        background: #E8F4FC;
        color: #234D6B;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(61,119,158,.12);
    }

    .stButton > button[kind="primary"] {
        min-height: 60px;
        border: 1px solid #79AFCF;
        border-radius: 16px;
        background: linear-gradient(135deg, #D9EEFA, #E5F3FC);
        color: #234D6B;
        font-size: 1.12rem;
        font-weight: 800;
        box-shadow: 0 7px 18px rgba(61,119,158,.10);
    }

    [data-testid="stDownloadButton"] > button {
        min-height: 46px;
        border: 1px solid #8FB9D5;
        border-radius: 14px;
        background: #E8F4FC;
        color: #234D6B;
        font-weight: 800;
    }

    [data-testid="stMetric"] {
        border: 1px solid #D4E5F1;
        border-radius: 17px;
        background: rgba(255,255,255,.94);
        padding: 14px;
    }

    [data-testid="stAlert"] {
        border-radius: 15px;
    }

    hr {
        border-color: #D4E5F1;
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


# ---------------------------------------------------------------------
# Навигация
# ---------------------------------------------------------------------

TECHNIQUES = {
    "decision_tree": {
        "title": "Дерево решений",
        "short": "Разложить сложный выбор на варианты и возможные последствия.",
        "description": "Сравнение вариантов, исходов, вероятностей и личных оценок.",
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
        "description": "Ситуации, прогнозы, посильные шаги и наблюдения.",
        "icon": "🪜",
    },
    "act_matrix": {
        "title": "ACT-матрица",
        "short": "Исследовать действия «от дискомфорта» и шаги «к ценностям».",
        "description": "Визуальная карта внутреннего опыта, поведения и выбранных действий.",
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
# PNG-экспорт на Pillow
# ---------------------------------------------------------------------

def load_font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ]

    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except (OSError, IOError):
            continue

    return ImageFont.load_default()


def wrap_text(text, max_chars=34):
    text = str(text or "").strip()
    if not text:
        return "—"
    return "\n".join(textwrap.wrap(text, width=max_chars) or ["—"])


def draw_centered_text(draw, text, xy, font, fill, max_chars=34, spacing=5):
    wrapped = wrap_text(text, max_chars)
    draw.multiline_text(
        xy,
        wrapped,
        font=font,
        fill=fill,
        anchor="mm",
        align="center",
        spacing=spacing,
    )


def draw_card(draw, box, title, body, fill="#FFFFFF", outline="#AFCFE2"):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(
        box,
        radius=22,
        fill=fill,
        outline=outline,
        width=3,
    )
    draw_centered_text(
        draw, title, ((x1 + x2) / 2, y1 + 28),
        load_font(20, bold=True), "#294A65", max_chars=32,
    )
    draw_centered_text(
        draw, body, ((x1 + x2) / 2, (y1 + y2) / 2 + 20),
        load_font(17), "#476B85", max_chars=max(16, int((x2 - x1) / 15)),
    )


def png_bytes(image):
    output = BytesIO()
    image.save(output, format="PNG", optimize=True)
    return output.getvalue()


def download_png(label, data, filename, key):
    st.download_button(
        label=label,
        data=data,
        file_name=filename,
        mime="image/png",
        key=key,
        use_container_width=True,
    )


def make_vertical_png(title, sections, note=""):
    width = 1200
    card_height = 130
    gap = 38
    top = 100
    height = max(400, top + len(sections) * (card_height + gap) + 100)

    image = Image.new("RGB", (width, height), "#F5FAFE")
    draw = ImageDraw.Draw(image)

    draw.text(
        (width // 2, 45),
        title,
        font=load_font(34, bold=True),
        fill="#294A65",
        anchor="mm",
    )

    colors = ["#EAF5FB", "#EFF8F6", "#F2F1FA", "#FFF6EC", "#FCEFF2"]

    for index, (heading, body) in enumerate(sections):
        y = top + index * (card_height + gap)
        box = (100, y, width - 100, y + card_height)
        draw_card(
            draw,
            box,
            heading,
            body,
            fill=colors[index % len(colors)],
        )

        if index < len(sections) - 1:
            cx = width // 2
            y1 = y + card_height + 4
            y2 = y + card_height + gap - 4
            draw.line((cx, y1, cx, y2), fill="#78A8BF", width=4)
            draw.polygon(
                [(cx - 10, y2 - 12), (cx + 10, y2 - 12), (cx, y2)],
                fill="#78A8BF",
            )

    if note:
        draw.text(
            (width // 2, height - 35),
            note,
            font=load_font(15),
            fill="#648198",
            anchor="mm",
        )

    return png_bytes(image)


def make_decision_png(question, options):
    width = max(1400, len(options) * 500)
    height = 1000
    image = Image.new("RGB", (width, height), "#F5FAFE")
    draw = ImageDraw.Draw(image)

    draw.text(
        (width // 2, 50),
        "Дерево решений",
        font=load_font(36, bold=True),
        fill="#294A65",
        anchor="mm",
    )
    draw.text(
        (width // 2, 110),
        wrap_text(question, max(90, width // 18)),
        font=load_font(21),
        fill="#476B85",
        anchor="mm",
    )

    root_x = width // 2
    root_y = 855
    root_box = (root_x - 220, root_y - 55, root_x + 220, root_y + 55)
    draw_card(draw, root_box, "Решение", question, fill="#F4E2D2", outline="#D8A77E")

    option_xs = [
        int(width * (i + 1) / (len(options) + 1))
        for i in range(len(options))
    ]
    palette = ["#80BFE0", "#71BFA9", "#E1AE83", "#A99BD0", "#D99BB2"]

    for oi, option in enumerate(options):
        ox = option_xs[oi]
        color = palette[oi % len(palette)]

        draw.line((root_x, root_y - 55, ox, 570), fill=color, width=8)
        draw.ellipse((ox - 16, 548, ox + 16, 580), fill=color)

        option_box = (ox - 190, 440, ox + 190, 545)
        draw_card(
            draw,
            option_box,
            option["name"],
            f"Итоговая оценка: {option['score']:.2f}",
            fill="#FFFFFF",
            outline=color,
        )

        scenarios = option["scenarios"]
        n = len(scenarios)
        spacing = min(320, 700 // max(n, 1))
        start_x = ox - (n - 1) * spacing // 2

        for si, scenario in enumerate(scenarios):
            sx = start_x + si * spacing
            draw.line((ox, 440, sx, 285), fill=color, width=5)
            draw.ellipse((sx - 13, 270, sx + 13, 296), fill=color)

            body = (
                f"{scenario['name']}\n"
                f"{option['normalized'][si]:.1f}% · оценка {scenario['score']:g}"
            )
            scenario_box = (sx - 145, 130, sx + 145, 260)
            draw_card(
                draw,
                scenario_box,
                f"Исход {si + 1}",
                body,
                fill="#FFFFFF",
                outline=color,
            )

    draw.text(
        (width // 2, 965),
        "Схема помогает обсуждению и не является автоматической рекомендацией.",
        font=load_font(16),
        fill="#648198",
        anchor="mm",
    )
    return png_bytes(image)


def make_act_png(situation, values, away_actions, inner, toward_actions, toward_inner, next_step):
    width, height = 1400, 1100
    image = Image.new("RGB", (width, height), "#F5FAFE")
    draw = ImageDraw.Draw(image)

    draw.text(
        (width // 2, 45),
        "ACT-матрица",
        font=load_font(36, bold=True),
        fill="#294A65",
        anchor="mm",
    )
    draw.text(
        (width // 2, 100),
        f"Ситуация: {wrap_text(situation, 95)}",
        font=load_font(18),
        fill="#476B85",
        anchor="mm",
    )
    draw.text(
        (width // 2, 145),
        f"Что важно: {wrap_text(values, 95)}",
        font=load_font(18),
        fill="#476B85",
        anchor="mm",
    )

    draw.line((width // 2, 200, width // 2, 900), fill="#9DBBD0", width=5)
    draw.line((100, 550, width - 100, 550), fill="#9DBBD0", width=5)

    draw_card(
        draw, (100, 220, 660, 520),
        "Действия «от дискомфорта»", away_actions,
        fill="#FFF1F1", outline="#D9A6A6",
    )
    draw_card(
        draw, (740, 220, 1300, 520),
        "Действия «к важному»", toward_actions,
        fill="#EAF7F1", outline="#9FC9B4",
    )
    draw_card(
        draw, (100, 590, 660, 890),
        "Внутренний опыт", inner,
        fill="#F2F5FC", outline="#B6C5DE",
    )
    draw_card(
        draw, (740, 590, 1300, 890),
        "Внутренний опыт при движении к важному", toward_inner,
        fill="#EFF8FC", outline="#AFCFE2",
    )

    draw.text(
        (width // 2, 970),
        f"Небольшой выбранный шаг: {wrap_text(next_step, 90)}",
        font=load_font(19, bold=True),
        fill="#315773",
        anchor="mm",
    )
    draw.text(
        (width // 2, 1040),
        "Карта для совместного исследования, а не диагноз или оценка.",
        font=load_font(16),
        fill="#648198",
        anchor="mm",
    )

    return png_bytes(image)


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
        item for item in st.session_state.dt_options
        if item["id"] != option_id
    ]
    clear_decision_result()


def add_scenario(option_id):
    for option in st.session_state.dt_options:
        if option["id"] == option_id:
            option["scenarios"].append(new_scenario())
            clear_decision_result()
            break


def delete_scenario(option_id, scenario_id):
    for option in st.session_state.dt_options:
        if option["id"] == option_id and len(option["scenarios"]) > 1:
            option["scenarios"] = [
                item for item in option["scenarios"]
                if item["id"] != scenario_id
            ]
            clear_decision_result()
            break


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

    st.caption("Для каждого варианта добавьте исходы, вероятности и личную оценку.")

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
                    on_click=delete_option,
                    args=(option_id,),
                    use_container_width=True,
                )

            st.text_input(
                "Название варианта",
                key=name_key,
                placeholder=f"Вариант {option_index}",
                on_change=clear_decision_result,
            )

            for scenario_index, scenario in enumerate(list(option["scenarios"]), start=1):
                scenario_id = scenario["id"]
                name_state_key = scenario_name_key(scenario_id)
                probability_state_key = probability_key(scenario_id)
                score_state_key = score_key(scenario_id)

                if name_state_key not in st.session_state:
                    st.session_state[name_state_key] = ""
                if probability_state_key not in st.session_state:
                    st.session_state[probability_state_key] = scenario["default_probability"]
                if score_state_key not in st.session_state:
                    st.session_state[score_state_key] = 0.0

                with st.container(border=True):
                    scenario_title_col, scenario_delete_col = st.columns([5, 1.5])
                    with scenario_title_col:
                        st.markdown(f"**Сценарий {scenario_index}**")
                    with scenario_delete_col:
                        st.button(
                            "Удалить сценарий",
                            key=f"dt_delete_scenario_{scenario_id}",
                            disabled=len(option["scenarios"]) <= 1,
                            on_click=delete_scenario,
                            args=(option_id, scenario_id),
                            use_container_width=True,
                        )

                    st.text_input(
                        "Описание возможного исхода",
                        key=name_state_key,
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
                            key=probability_state_key,
                            on_change=clear_decision_result,
                        )
                    with score_col:
                        st.slider(
                            "Оценка исхода",
                            min_value=-5.0,
                            max_value=5.0,
                            step=0.5,
                            key=score_state_key,
                            help="−5 — очень нежелательный, +5 — очень желательный.",
                            on_change=clear_decision_result,
                        )

            st.button(
                "＋ Добавить сценарий",
                key=f"dt_add_scenario_{option_id}",
                on_click=add_scenario,
                args=(option_id,),
            )

    add_col, remove_col, _ = st.columns([1.7, 1.9, 4])

    with add_col:
        st.button(
            "＋ Добавить вариант",
            key="dt_add_option",
            on_click=add_option,
            use_container_width=True,
        )

    with remove_col:
        st.button(
            "− Удалить последний",
            key="dt_remove_last",
            disabled=len(st.session_state.dt_options) <= 2,
            on_click=delete_option,
            args=(st.session_state.dt_options[-1]["id"],),
            use_container_width=True,
        )

    if st.button(
        "Рассчитать и построить дерево",
        type="primary",
        use_container_width=True,
    ):
        question = st.session_state.dt_question.strip()
        prepared_options = []
        used_names = set()
        error = None

        if not question:
            error = "Сначала сформулируйте решение."

        for option_index, option in enumerate(st.session_state.dt_options, start=1):
            if error:
                break

            option_name = st.session_state.get(
                option_name_key(option["id"]), ""
            ).strip()

            if not option_name:
                error = f"Введите название варианта {option_index}."
                break

            if option_name in used_names:
                error = f"Названия вариантов должны отличаться: «{option_name}»."
                break

            used_names.add(option_name)
            scenarios = []

            for scenario_index, scenario in enumerate(option["scenarios"], start=1):
                scenario_id = scenario["id"]
                scenario_name = st.session_state.get(
                    scenario_name_key(scenario_id), ""
                ).strip()

                if not scenario_name:
                    error = (
                        f"Заполните сценарий {scenario_index} "
                        f"варианта «{option_name}»."
                    )
                    break

                scenarios.append({
                    "name": scenario_name,
                    "probability": int(st.session_state[probability_key(scenario_id)]),
                    "score": float(st.session_state[score_key(scenario_id)]),
                })

            if error:
                break

            total_probability = sum(item["probability"] for item in scenarios)
            if total_probability == 0:
                error = f"Для варианта «{option_name}» задайте ненулевую вероятность."
                break

            normalized = [
                item["probability"] / total_probability * 100
                for item in scenarios
            ]
            expected_score = sum(
                normalized[index] / 100 * scenario["score"]
                for index, scenario in enumerate(scenarios)
            )

            prepared_options.append({
                "name": option_name,
                "scenarios": scenarios,
                "normalized": normalized,
                "score": expected_score,
            })

        if error:
            st.session_state.dt_result = None
            st.warning(error)
        else:
            best_name = max(
                prepared_options,
                key=lambda item: item["score"],
            )["name"]

            st.session_state.dt_result = {
                "question": question,
                "options": prepared_options,
                "best_name": best_name,
            }

    result = st.session_state.dt_result

    if result:
        st.subheader("Результат")
        columns = st.columns(len(result["options"]))

        for column, option in zip(columns, result["options"]):
            with column:
                label = (
                    "🌿 " if option["name"] == result["best_name"] else ""
                ) + option["name"]
                st.metric(label=label, value=f"{option['score']:.2f} / 5")

        st.info(
            f"По указанным оценкам лидирует вариант: **{result['best_name']}**. "
            "Это материал для размышления, а не автоматическое решение."
        )

        image_data = make_decision_png(
            result["question"],
            result["options"],
        )
        st.image(image_data, use_container_width=True)
        download_png(
            "⬇️ Скачать дерево решений в PNG",
            image_data,
            "derevo-resheniy.png",
            "download_decision_png",
        )


# ---------------------------------------------------------------------
# Цепочный анализ поведения
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
    st.write("Исследуйте контекст, звенья цепочки, поведение и последствия.")
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

    sections = [
        ("Факторы уязвимости", vulnerability),
        ("Запускающее событие", prompting),
    ]

    st.subheader("Звенья цепочки")

    for index, link in enumerate(list(st.session_state.chain_links), start=1):
        link_id = link["id"]

        with st.container(border=True):
            title_col, delete_col = st.columns([5, 1.5])
            with title_col:
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

            left, right = st.columns(2)
            with left:
                thought = st.text_area("Мысли или образы", key=f"chain_thought_{link_id}")
                body = st.text_area("Ощущения в теле", key=f"chain_body_{link_id}")
            with right:
                emotion = st.text_area("Эмоции", key=f"chain_emotion_{link_id}")
                action = st.text_area("Импульсы или действия", key=f"chain_action_{link_id}")

            st.slider(
                "Интенсивность (необязательно)",
                min_value=0,
                max_value=10,
                value=0,
                key=f"chain_intensity_{link_id}",
            )

            intervention = st.checkbox(
                "Отметить как возможную точку вмешательства",
                key=f"chain_intervention_{link_id}",
            )

            skill = st.text_area(
                "Возможный другой шаг, навык или поддержка",
                key=f"chain_skill_{link_id}",
            )

        description = "\n".join(
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
            description += "\nВозможная точка вмешательства"
        if skill.strip():
            description += f"\nВозможная поддержка: {skill}"

        sections.append((f"Звено {index}", description))

    st.button("＋ Добавить звено", on_click=add_chain_link)

    st.subheader("Целевое поведение и последствия")
    target = st.text_area("Целевое поведение", key="chain_target")

    left, right = st.columns(2)
    with left:
        immediate = st.text_area("Последствия сразу после", key="chain_immediate")
    with right:
        later = st.text_area("Последствия позднее", key="chain_later")

    repair = st.text_area(
        "Восстановление ситуации или поддержка",
        key="chain_repair",
    )

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

    image_data = make_vertical_png(
        "Цепочный анализ поведения",
        sections,
        "Карта для обсуждения, а не диагноз или автоматическая оценка.",
    )
    download_png(
        "⬇️ Скачать карту цепочки в PNG",
        image_data,
        "cepochniy-analiz.png",
        "download_chain_png",
    )


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
        step_id = step["id"]

        with st.container(border=True):
            title_col, delete_col = st.columns([5, 1.5])
            with title_col:
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

            situation = st.text_area("Ситуация", key=f"exp_situation_{step_id}")
            distress = st.slider(
                "Ожидаемая тревога (0–10)",
                min_value=0,
                max_value=10,
                value=3,
                key=f"exp_distress_{step_id}",
            )
            prediction = st.text_area("Прогноз или опасение", key=f"exp_prediction_{step_id}")
            plan = st.text_area("Обсуждаемый посильный шаг", key=f"exp_plan_{step_id}")
            status = st.selectbox(
                "Статус",
                ["Не обсуждали", "Обсудили", "Запланировали", "Попробовали"],
                key=f"exp_status_{step_id}",
            )
            reflection = st.text_area(
                "Наблюдения после практики — необязательно",
                key=f"exp_reflection_{step_id}",
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

    image_data = make_vertical_png(
        "Иерархия экспозиции",
        sections,
        "Порядок ступеней — материал для обсуждения, не автоматическое назначение.",
    )
    download_png(
        "⬇️ Скачать иерархию в PNG",
        image_data,
        "ierarhiya-ekspozicii.png",
        "download_exposure_png",
    )


# ---------------------------------------------------------------------
# ACT-матрица
# ---------------------------------------------------------------------

def make_act_png(situation, values, away_actions, inner, toward_actions, toward_inner, next_step):
    width, height = 1400, 1120
    image = Image.new("RGB", (width, height), "#F5FAFE")
    draw = ImageDraw.Draw(image)

    draw.text(
        (width // 2, 45),
        "ACT-матрица",
        font=load_font(36, bold=True),
        fill="#294A65",
        anchor="mm",
    )

    draw_centered_text(
        draw, f"Ситуация: {situation or '—'}", (width // 2, 100),
        load_font(18), "#476B85", max_chars=100,
    )
    draw_centered_text(
        draw, f"Что важно: {values or '—'}", (width // 2, 155),
        load_font(18), "#476B85", max_chars=100,
    )

    draw.line((width // 2, 220, width // 2, 900), fill="#9DBBD0", width=5)
    draw.line((100, 560, width - 100, 560), fill="#9DBBD0", width=5)

    draw_card(
        draw, (100, 240, 660, 520),
        "Действия «от дискомфорта»", away_actions,
        fill="#FFF1F1", outline="#D9A6A6",
    )
    draw_card(
        draw, (740, 240, 1300, 520),
        "Действия «к важному»", toward_actions,
        fill="#EAF7F1", outline="#9FC9B4",
    )
    draw_card(
        draw, (100, 600, 660, 880),
        "Внутренний опыт", inner,
        fill="#F2F5FC", outline="#B6C5DE",
    )
    draw_card(
        draw, (740, 600, 1300, 880),
        "Внутренний опыт при движении к важному", toward_inner,
        fill="#EFF8FC", outline="#AFCFE2",
    )

    draw_centered_text(
        draw,
        f"Небольшой выбранный шаг: {next_step or '—'}",
        (width // 2, 970),
        load_font(19, bold=True),
        "#315773",
        max_chars=100,
    )
    draw.text(
        (width // 2, 1060),
        "Карта для совместного исследования, а не диагноз или оценка.",
        font=load_font(16),
        fill="#648198",
        anchor="mm",
    )

    return png_bytes(image)


def render_act_matrix():
    st.title("🧭 ACT-матрица")
    st.write("Исследуйте, что уводит от дискомфорта и какие действия приближают к важному.")
    st.info(
        "Матрица — материал для совместного исследования. "
        "Она не оценивает поведение как правильное или неправильное."
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

    image_data = make_act_png(
        situation,
        values,
        away_actions,
        inner,
        toward_actions,
        toward_inner,
        next_step,
    )

    st.subheader("Предварительный вид карты")
    st.image(image_data, use_container_width=True)
    download_png(
        "⬇️ Скачать ACT-матрицу в PNG",
        image_data,
        "act-matrix.png",
        "download_act_png",
    )


# ---------------------------------------------------------------------
# Главная, библиотека и раздел «О нас»
# ---------------------------------------------------------------------

def render_home():
    st.markdown(
        f"""
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
            background-color:rgba(232,245,253,.94);
            background-image:url('data:image/svg+xml;base64,{__import__('base64').b64encode(NEURON_PATTERN.encode('utf-8')).decode('ascii')}');
            background-size:cover;
            box-shadow:0 18px 42px rgba(48,105,145,.12);
            text-align:center;
        ">
          <div style="
              max-width:820px;
              padding:24px;
              border-radius:24px;
              background:rgba(248,252,255,.88);
              box-shadow:0 8px 26px rgba(48,105,145,.07);
          ">
            <div style="
                color:#214D6C;
                font-family:Arial,sans-serif;
                font-size:clamp(3.8rem,9vw,6.7rem);
                font-weight:800;
                line-height:1;
                letter-spacing:.035em;">
                ПСИ-БЛОК
            </div>
            <div style="
                max-width:760px;
                margin:20px auto 0 auto;
                color:#476B85;
                font-family:Arial,sans-serif;
                font-size:1.2rem;
                line-height:1.7;">
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

        for column, (technique_id, technique) in zip(
            columns,
            items[start:start + 2],
        ):
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
                    f"<div class='developer-name'>{html.escape(person['name'])}</div>"
                    f"<div class='developer-role'>{html.escape(person['role'])}</div>",
                    unsafe_allow_html=True,
                )

    st.divider()
    st.warning(
        "Это прототип. Не вводите идентифицирующие или особо чувствительные "
        "сведения: защищённое хранение клиентских данных пока не реализовано."
    )


def render_selected_technique():
    technique_id = st.session_state.selected_technique

    if technique_id not in TECHNIQUES:
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
# Запуск
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
