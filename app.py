import base64
import html
import textwrap
import uuid

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Дерево решений",
    page_icon="🌿",
    layout="wide",
)


# ---------- Декоративные листья для фона страницы ----------

LEAF_BACKGROUND_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1000" viewBox="0 0 1440 1000">
  <g fill="#8DBBD0" fill-opacity="0.13" stroke="#8DBBD0" stroke-opacity="0.12" stroke-width="2">
    <path d="M110 100 C155 55 210 70 215 115 C185 155 140 155 110 100Z"/>
    <path d="M365 265 C400 210 465 220 470 270 C435 315 390 315 365 265Z"/>
    <path d="M690 105 C735 55 795 75 795 125 C760 165 715 155 690 105Z"/>
    <path d="M1035 280 C1070 225 1130 240 1130 290 C1090 330 1050 325 1035 280Z"/>
    <path d="M1270 105 C1310 55 1370 70 1370 120 C1335 160 1290 150 1270 105Z"/>
    <path d="M180 550 C220 500 280 520 280 570 C245 610 200 600 180 550Z"/>
    <path d="M505 710 C545 655 605 675 605 725 C570 765 525 755 505 710Z"/>
    <path d="M875 565 C915 510 975 530 975 580 C940 620 895 610 875 565Z"/>
    <path d="M1160 770 C1200 715 1260 735 1260 785 C1225 825 1180 815 1160 770Z"/>
    <path d="M40 850 C80 795 140 815 140 865 C105 905 60 895 40 850Z"/>
  </g>
  <g fill="none" stroke="#78A8BF" stroke-opacity="0.12" stroke-width="3">
    <path d="M115 98 Q160 105 205 113"/>
    <path d="M370 263 Q415 270 460 273"/>
    <path d="M695 103 Q740 110 785 123"/>
    <path d="M1040 278 Q1085 285 1120 291"/>
    <path d="M1275 103 Q1320 110 1360 118"/>
    <path d="M185 548 Q230 555 270 572"/>
    <path d="M510 708 Q555 715 595 727"/>
    <path d="M880 563 Q925 570 965 582"/>
    <path d="M1165 768 Q1210 775 1250 787"/>
  </g>
</svg>
"""

LEAF_BACKGROUND_B64 = base64.b64encode(
    LEAF_BACKGROUND_SVG.encode("utf-8")
).decode("ascii")


# ---------- Управление данными и состоянием ----------

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
    return f"option_name_{option_id}"


def scenario_name_key(scenario_id):
    return f"scenario_name_{scenario_id}"


def probability_key(scenario_id):
    return f"probability_{scenario_id}"


def score_key(scenario_id):
    return f"score_{scenario_id}"


def clear_results():
    st.session_state.calculation = None


def add_option():
    st.session_state.options.append(new_option())
    clear_results()


def delete_option(option_id):
    if len(st.session_state.options) > 2:
        st.session_state.options = [
            option
            for option in st.session_state.options
            if option["id"] != option_id
        ]
        clear_results()


def add_scenario(option_id):
    for option in st.session_state.options:
        if option["id"] == option_id:
            option["scenarios"].append(new_scenario())
            clear_results()
            return


def delete_scenario(option_id, scenario_id):
    for option in st.session_state.options:
        if option["id"] == option_id and len(option["scenarios"]) > 1:
            option["scenarios"] = [
                scenario
                for scenario in option["scenarios"]
                if scenario["id"] != scenario_id
            ]
            clear_results()
            return


if "options" not in st.session_state:
    st.session_state.options = [new_option(), new_option()]

if "calculation" not in st.session_state:
    st.session_state.calculation = None

if "decision_question" not in st.session_state:
    st.session_state.decision_question = ""


# ---------- Небесная пастельная тема ----------

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700;800&display=swap');

    .stApp {{
        background-color: #F7FBFD;
        background-image:
            radial-gradient(ellipse at 12% 8%, rgba(226, 242, 251, .82), transparent 34%),
            radial-gradient(ellipse at 88% 18%, rgba(235, 246, 251, .75), transparent 36%),
            url("data:image/svg+xml;base64,{LEAF_BACKGROUND_B64}");
        background-size: auto, auto, cover;
        background-position: center, center, center top;
        background-repeat: no-repeat;
        background-attachment: scroll, scroll, fixed;
        color: #36546C;
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    .block-container {{
        max-width: 1120px;
        padding-top: 1.8rem;
        padding-bottom: 4rem;
    }}

    h1, h2, h3, h4, p, label, button, input {{
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }}

    h1, h2, h3, h4 {{
        color: #36546C !important;
        letter-spacing: -0.025em;
    }}

    h1 {{
        font-size: 2.8rem !important;
        font-weight: 800 !important;
    }}

    h2 {{
        font-size: 1.9rem !important;
        font-weight: 800 !important;
    }}

    h3 {{
        font-size: 1.4rem !important;
        font-weight: 800 !important;
    }}

    p, label, [data-testid="stCaptionContainer"] {{
        color: #58748A;
        font-size: 1.04rem;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        border: 1px solid #DCE8F0 !important;
        border-radius: 20px !important;
        background: rgba(255,255,255,0.84) !important;
        box-shadow: 0 10px 24px rgba(89, 128, 151, 0.07);
    }}

    div[data-testid="stTextInput"] input {{
        min-height: 47px;
        border: 1px solid #D5E3ED;
        border-radius: 13px;
        background: #FFFFFF;
        color: #36546C;
        font-size: 1.02rem;
    }}

    .stButton > button {{
        min-height: 42px;
        border: 1px solid #D3E2EC;
        border-radius: 13px;
        background: #F3F8FC;
        color: #3D5F77;
        font-size: 0.98rem;
        font-weight: 700;
        transition: 0.18s ease;
    }}

    .stButton > button:hover:not(:disabled) {{
        border-color: #B5D3E5;
        background: #EAF4FA;
        color: #34566E;
        transform: translateY(-1px);
    }}

    .stButton > button:disabled {{
        opacity: 0.55;
    }}

    .stButton > button[kind="primary"] {{
        min-height: 49px;
        border: 1px solid #B6D4E7;
        border-radius: 15px;
        background: linear-gradient(135deg, #E9F5FC, #EEF7F5);
        color: #36546C;
        font-size: 1.05rem;
    }}

    [data-testid="stMetric"] {{
        border: 1px solid #DCE8F0;
        border-radius: 17px;
        background: rgba(255,255,255,0.88);
        padding: 14px;
    }}

    [data-testid="stAlert"] {{
        border-radius: 15px;
    }}

    hr {{
        border-color: #DCE8F0;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Заголовок ----------

st.markdown(
    "<h1 style='text-align:center; margin-bottom:0;'>🌿 Дерево решений</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    """
    <p style="text-align:center; color:#71879A; font-size:1.12rem;">
    Разложите сложный выбор на варианты и возможные последствия.
    </p>
    """,
    unsafe_allow_html=True,
)

st.text_input(
    "Какое решение нужно принять?",
    key="decision_question",
    placeholder="Например: «Стоит ли менять работу?»",
    on_change=clear_results,
)

st.subheader("1. Добавьте варианты")
st.caption(
    "Для каждого варианта укажите возможные исходы, их вероятность "
    "и оценку для вас."
)


# ---------- Редактор вариантов и сценариев ----------

for option_index, option in enumerate(list(st.session_state.options)):
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
                disabled=len(st.session_state.options) <= 2,
                help="Нужно оставить хотя бы два варианта.",
                on_click=delete_option,
                args=(option_id,),
                use_container_width=True,
            )

        st.text_input(
            "Название варианта",
            key=name_key,
            placeholder=f"Например: «Вариант {option_index + 1}»",
            on_change=clear_results,
        )

        for scenario_index, scenario in enumerate(list(option["scenarios"])):
            scenario_id = scenario["id"]
            name_key_scenario = scenario_name_key(scenario_id)
            probability_state_key = probability_key(scenario_id)
            score_state_key = score_key(scenario_id)

            if name_key_scenario not in st.session_state:
                st.session_state[name_key_scenario] = ""

            if probability_state_key not in st.session_state:
                st.session_state[probability_state_key] = scenario[
                    "default_probability"
                ]

            if score_state_key not in st.session_state:
                st.session_state[score_state_key] = 0.0

            with st.container(border=True):
                scenario_title_col, scenario_delete_col = st.columns([5, 1.7])

                with scenario_title_col:
                    st.markdown(f"**Сценарий {scenario_index + 1}**")

                with scenario_delete_col:
                    st.button(
                        "Удалить сценарий",
                        key=f"delete_scenario_{scenario_id}",
                        disabled=len(option["scenarios"]) <= 1,
                        help="У варианта должен остаться хотя бы один сценарий.",
                        on_click=delete_scenario,
                        args=(option_id, scenario_id),
                        use_container_width=True,
                    )

                st.text_input(
                    "Описание возможного исхода",
                    key=name_key_scenario,
                    placeholder="Например: «Найду более интересную работу»",
                    on_change=clear_results,
                )

                probability_col, score_col = st.columns(2)

                with probability_col:
                    st.slider(
                        "Вероятность, %",
                        min_value=0,
                        max_value=100,
                        step=1,
                        key=probability_state_key,
                        on_change=clear_results,
                    )

                with score_col:
                    st.slider(
                        "Оценка исхода",
                        min_value=-5.0,
                        max_value=5.0,
                        step=0.5,
                        key=score_state_key,
                        help="−5 — очень нежелательный исход, +5 — очень желательный.",
                        on_change=clear_results,
                    )

        # Важно: кнопка расположена после цикла сценариев.
        # Поэтому для каждого варианта создаётся ровно одна такая кнопка.
        st.button(
            "＋ Добавить сценарий",
            key=f"add_scenario_{option_id}",
            on_click=add_scenario,
            args=(option_id,),
        )


add_col, remove_col, _ = st.columns([1.7, 1.8, 4])

with add_col:
    st.button(
        "＋ Добавить вариант",
        key="add_option",
        on_click=add_option,
        use_container_width=True,
    )

with remove_col:
    st.button(
        "− Удалить последний",
        key="remove_last_option",
        disabled=len(st.session_state.options) <= 2,
        on_click=lambda: delete_option(st.session_state.options[-1]["id"]),
        use_container_width=True,
    )


# ---------- Рисование дерева в SVG ----------

def wrap_label(value, width=22, max_lines=2):
    lines = textwrap.wrap(str(value), width=width) or [""]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: max(1, width - 1)] + "…"
    return lines


def build_tree_svg(options, best_name, question):
    """
    Рисует дерево снизу вверх:
    решение у основания, варианты на крупных ветвях,
    сценарии — круглые узлы в верхней части.
    """

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

    svg_width = (
        100
        + sum(group_widths)
        + group_gap * max(0, len(options) - 1)
    )

    groups = []
    cursor_x = 50

    for index, option in enumerate(options):
        group_width = group_widths[index]
        scenario_count = len(option["scenarios"])
        content_width = (
            scenario_count * leaf_w
            + (scenario_count - 1) * leaf_gap
        )
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

    root_x = (
        groups[0]["center_x"] + groups[-1]["center_x"]
    ) / 2

    colors = ["#80BFE0", "#71BFA9", "#E1AE83", "#A99BD0", "#D99BB2"]

    def esc(value):
        return html.escape(str(value))

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

    # Ветви рисуются первыми: карточки и узлы будут поверх линий.
    # Поэтому ветка у корня не пересечёт текст решения.
    for index, group in enumerate(groups):
        option = group["option"]
        color = (
            "#65AD91"
            if option["name"] == best_name
            else colors[index % len(colors)]
        )
        option_x = group["center_x"]

        # Главная ветвь от развилки ствола к узлу варианта.
        parts.append(f"""
          <path d="M {root_x} {trunk_fork_y}
                   C {root_x} {trunk_fork_y - 65},
                     {option_x} {option_y + 125},
                     {option_x} {option_y + 20}"
                fill="none"
                stroke="{color}"
                stroke-width="9"
                stroke-linecap="round"/>
        """)

        # Веточки от варианта вверх к сценариям.
        for leaf_x in group["leaf_centers"]:
            parts.append(f"""
              <path d="M {option_x} {option_y - 18}
                       C {option_x} {option_y - 95},
                         {leaf_x} {leaf_y + 100},
                         {leaf_x} {leaf_y + 24}"
                    fill="none"
                    stroke="{color}"
                    stroke-width="5"
                    stroke-linecap="round"/>
            """)

    # Ствол выходит из верхней стороны карточки решения.
    # Он начинается выше карточки, а не проходит через её текст.
    parts.append(f"""
      <path d="M {root_x} {root_card_y}
               C {root_x - 8} {root_card_y - 35},
                 {root_x + 10} {trunk_fork_y + 55},
                 {root_x} {trunk_fork_y}"
            fill="none"
            stroke="url(#wood)"
            stroke-width="22"
            stroke-linecap="round"/>
    """)

    # Узлы вариантов и подписи.
    for index, group in enumerate(groups):
        option = group["option"]
        color = (
            "#65AD91"
            if option["name"] == best_name
            else colors[index % len(colors)]
        )
        option_x = group["center_x"]
        option_label = esc(option["name"])

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

          <text x="{option_x}" y="{option_y + 54}"
                text-anchor="middle"
                font-family="Nunito Sans, Arial, sans-serif"
                font-size="14" font-weight="800" fill="#36546C">
            {option_label}
          </text>

          <text x="{option_x}" y="{option_y + 78}"
                text-anchor="middle"
                font-family="Nunito Sans, Arial, sans-serif"
                font-size="12" fill="#58748A">
            Итоговая оценка: {option["score"]:.2f}
          </text>
        """)

        # Сценарии — круглые узлы-листья с отдельными подписями.
        for scenario_index, scenario in enumerate(option["scenarios"]):
            leaf_x = group["leaf_centers"][scenario_index]
            probability = option["normalized"][scenario_index]
            scenario_lines = wrap_label(scenario["name"])

            parts.append(f"""
              <circle cx="{leaf_x}" cy="{leaf_y}" r="22"
                      fill="{color}" fill-opacity="0.78"
                      stroke="{color}" stroke-width="3"
                      filter="url(#tree-shadow)"/>
              <circle cx="{leaf_x}" cy="{leaf_y}" r="14"
                      fill="none"
                      stroke="#FFFFFF"
                      stroke-opacity="0.78"
                      stroke-width="2"/>
            """)

            card_y = leaf_y + 38
            parts.append(f"""
              <rect x="{leaf_x - 96}" y="{card_y}"
                    width="192" height="76" rx="16"
                    fill="#FFFFFF" fill-opacity="0.97"
                    stroke="{color}" stroke-opacity="0.72"
                    stroke-width="1.5"/>
            """)

            for line_index, line in enumerate(scenario_lines):
                parts.append(f"""
                  <text x="{leaf_x}" y="{card_y + 23 + line_index * 17}"
                        text-anchor="middle"
                        font-family="Nunito Sans, Arial, sans-serif"
                        font-size="12" font-weight="700" fill="#36546C">
                    {esc(line)}
                  </text>
                """)

            parts.append(f"""
              <text x="{leaf_x}" y="{card_y + 63}"
                    text-anchor="middle"
                    font-family="Nunito Sans, Arial, sans-serif"
                    font-size="11" fill="#58748A">
                {probability:.1f}% · оценка {scenario["score"]:g}
              </text>
            """)

    # Карточку решения рисуем последней: она закрывает концы линий,
    # а текст остаётся чистым и не пересекается со стволом.
    question_lines = wrap_label(question, width=42, max_lines=2)
    root_box_width = 390
    root_box_height = 66

    parts.append(f"""
      <rect x="{root_x - root_box_width / 2}" y="{root_card_y}"
            width="{root_box_width}" height="{root_box_height}" rx="23"
            fill="#F4D6B8" stroke="#D8A77E" stroke-width="2"
            filter="url(#tree-shadow)"/>
    """)

    first_text_y = root_card_y + (
        27 if len(question_lines) == 1 else 23
    )

    for line_index, line in enumerate(question_lines):
        parts.append(f"""
          <text x="{root_x}" y="{first_text_y + line_index * 19}"
                text-anchor="middle"
                font-family="Nunito Sans, Arial, sans-serif"
                font-size="15" font-weight="800" fill="#604B3D">
            {esc(line)}
          </text>
        """)

    parts.append("</svg>")

    return f"""
    <div style="
        width:100%;
        overflow-x:auto;
        border:1px solid #DCE8F0;
        border-radius:24px;
        background:#F8FBFD;
        padding:12px;
        box-sizing:border-box;">
        {''.join(parts)}
    </div>
    """


# ---------- Расчёт ----------

st.divider()

if st.button(
    "Рассчитать и построить дерево",
    type="primary",
    use_container_width=True,
):
    question = st.session_state.decision_question.strip()
    error = None
    prepared_options = []
    used_names = set()

    if not question:
        error = "Сначала сформулируйте решение."

    for option_index, option in enumerate(st.session_state.options):
        if error:
            break

        option_name = st.session_state[
            option_name_key(option["id"])
        ].strip()

        if not option_name:
            error = f"Введите название варианта {option_index + 1}."
            break

        if option_name in used_names:
            error = f"Названия вариантов должны отличаться: «{option_name}»."
            break

        used_names.add(option_name)
        scenarios = []

        for scenario_index, scenario in enumerate(option["scenarios"]):
            scenario_name = st.session_state[
                scenario_name_key(scenario["id"])
            ].strip()

            if not scenario_name:
                error = (
                    f"Заполните описание сценария {scenario_index + 1} "
                    f"в варианте «{option_name}»."
                )
                break

            scenarios.append({
                "name": scenario_name,
                "probability": int(
                    st.session_state[probability_key(scenario["id"])]
                ),
                "score": float(
                    st.session_state[score_key(scenario["id"])]
                ),
            })

        if error:
            break

        total_probability = sum(
            scenario["probability"] for scenario in scenarios
        )

        if total_probability == 0:
            error = (
                f"В варианте «{option_name}» задайте ненулевую "
                "вероятность хотя бы одному сценарию."
            )
            break

        # Сохраняем прежнее поведение: сценарии нормализуются
        # отдельно внутри каждого варианта.
        normalized = [
            scenario["probability"] / total_probability * 100
            for scenario in scenarios
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
        st.session_state.calculation = None
        st.warning(error)
    else:
        best_name = max(
            prepared_options,
            key=lambda item: item["score"],
        )["name"]

        st.session_state.calculation = {
            "question": question,
            "options": prepared_options,
            "best_name": best_name,
        }


# ---------- Результаты и дерево ----------

result = st.session_state.calculation

if result:
    st.divider()
    st.subheader("2. Результат")
    st.write(f"**Решение:** {result['question']}")

    metric_columns = st.columns(len(result["options"]))

    for column, option in zip(metric_columns, result["options"]):
        with column:
            label = option["name"]
            if label == result["best_name"]:
                label = f"🌿 {label}"

            st.metric(
                label=label,
                value=f"{option['score']:.2f} / 5",
            )

    st.success(
        f"По указанным оценкам лидирует вариант: **{result['best_name']}**."
    )
    st.caption(
        "Это ориентир для размышления, а не автоматическое решение. "
        "Вероятности сценариев рассчитываются отдельно для каждого варианта."
    )

    st.subheader("Дерево возможных исходов")

    components.html(
        build_tree_svg(
            result["options"],
            result["best_name"],
            result["question"],
        ),
        height=780,
        scrolling=True,
    )
