import uuid
import html
import textwrap

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Дерево решений",
    page_icon="🌿",
    layout="wide",
)


# ---------- Фоновый SVG с листьями ----------

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

LEAF_BACKGROUND_B64 = __import__("base64").b64encode(
    LEAF_BACKGROUND_SVG.encode("utf-8")
).decode("ascii")


# ---------- Вспомогательные функции ----------

def new_scenario(first=False):
    return {
        "id": uuid.uuid4().hex,
        "name": "",
        "probability": 100 if first else 0,
        "score": 0.0,
    }


def new_option():
    return {
        "id": uuid.uuid4().hex,
        "name": "",
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


def normalize(values):
    total = sum(values)
    if total == 0:
        return values
    return [v / total * 100 for v in values]


def calculate_results(options):
    results = []
    for option in options:
        probabilities = [s["probability"] for s in option["scenarios"]]
        normalized = normalize(probabilities)

        expected_score = sum(
            (normalized[i] / 100) * option["scenarios"][i]["score"]
            for i in range(len(option["scenarios"]))
        )

        results.append({
            "name": option["name"],
            "scenarios": option["scenarios"],
            "normalized": normalized,
            "score": expected_score,
        })

    return results


def wrap_label(value, width=22, max_lines=2):
    lines = textwrap.wrap(str(value), width=width) or [""]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][:width - 1] + "…"
    return lines


def build_tree_svg(options, best_name, question):
    """
    Дерево в стиле "ветка/ствол":
    корень решения внизу,
    варианты выше,
    сценарии в верхней части.
    """
    leaf_w = 220
    leaf_h = 96
    leaf_gap = 32
    group_gap = 52
    option_y = 420
    leaf_y = 150
    root_y = 620

    group_widths = [
        max(
            leaf_w,
            len(option["scenarios"]) * leaf_w + (len(option["scenarios"]) - 1) * leaf_gap,
        )
        for option in options
    ]

    svg_width = 100 + sum(group_widths) + group_gap * max(0, len(options) - 1)
    svg_height = 760

    groups = []
    cursor_x = 60

    for index, option in enumerate(options):
        group_width = group_widths[index]
        count = len(option["scenarios"])
        content_width = count * leaf_w + (count - 1) * leaf_gap
        first_leaf_x = cursor_x + (group_width - content_width) / 2
        leaf_centers = [
            first_leaf_x + i * (leaf_w + leaf_gap) + leaf_w / 2
            for i in range(count)
        ]

        groups.append({
            "option": option,
            "center_x": cursor_x + group_width / 2,
            "leaf_centers": leaf_centers,
        })

        cursor_x += group_width + group_gap

    root_x = (groups[0]["center_x"] + groups[-1]["center_x"]) / 2

    colors = ["#80BFE0", "#71BFA9", "#E1AE83", "#A99BD0", "#D99BB2"]

    def esc(value):
        return html.escape(str(value))

    parts = [
        f"""
        <svg xmlns="http://www.w3.org/2000/svg"
             width="{svg_width}" height="{svg_height}"
             viewBox="0 0 {svg_width} {svg_height}"
             role="img" aria-label="Дерево решений">
          <defs>
            <filter id="soft-shadow" x="-30%" y="-30%" width="170%" height="180%">
              <feDropShadow dx="0" dy="6" stdDeviation="7"
                            flood-color="#5E7B8E" flood-opacity="0.12"/>
            </filter>
            <linearGradient id="wood" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stop-color="#A77E60"/>
              <stop offset="100%" stop-color="#9A7258"/>
            </linearGradient>
          </defs>
          <rect width="100%" height="100%" fill="#F8FBFD" rx="28"/>
        """
    ]

    # Корень решения внизу
    root_box_w = max(300, min(390, len(question) * 8.5))
    question_lines = wrap_label(question, width=32, max_lines=2)

    parts.append(f"""
      <rect x="{root_x - root_box_w / 2}" y="{root_y - 28}"
            width="{root_box_w}" height="62" rx="22"
            fill="#F2D8B6" stroke="#D8A77E" stroke-width="2"
            filter="url(#soft-shadow)"/>
    """)

    for line_index, line in enumerate(question_lines):
        parts.append(f"""
          <text x="{root_x}" y="{root_y + 10 + line_index * 16}"
                text-anchor="middle"
                font-family="Nunito Sans, Arial, sans-serif"
                font-size="15" font-weight="800" fill="#4F5E6C">
            {esc(line)}
          </text>
        """)

    # Ствол
    parts.append(f"""
      <path d="M {root_x} {root_y}
               C {root_x - 10} {root_y - 55},
                 {root_x + 8} {root_y - 120},
                 {root_x} {root_y - 180}"
            fill="none" stroke="url(#wood)" stroke-width="20"
            stroke-linecap="round"/>
    """)

    for index, group in enumerate(groups):
        option = group["option"]
        color = (
            "#69B792" if option["name"] == best_name else colors[index % len(colors)]
        )
        option_x = group["center_x"]

        # Ветви от ствола к вариантам
        parts.append(f"""
          <path d="M {root_x} {root_y - 180}
                   C {root_x} {root_y - 230},
                     {option_x} {option_y - 50},
                     {option_x} {option_y + 18}"
                fill="none" stroke="{color}" stroke-width="8"
                stroke-linecap="round"/>
        """)

        # Вертушки от варианта к сценарием
        for leaf_x in group["leaf_centers"]:
            parts.append(f"""
              <path d="M {option_x} {option_y + 18}
                       C {option_x} {option_y - 35},
                         {leaf_x} {leaf_y + 52},
                         {leaf_x} {leaf_y + 20}"
                    fill="none" stroke="{color}" stroke-width="5"
                    stroke-linecap="round"/>
            """)

        # Вариант — круглый узел с подписью
        parts.append(f"""
          <circle cx="{option_x}" cy="{option_y}" r="18"
                  fill="{color}" stroke="white" stroke-width="5"
                  filter="url(#soft-shadow)"/>
          <rect x="{option_x - 108}" y="{option_y + 24}"
                width="216" height="70" rx="18"
                fill="#FFFFFF" stroke="{color}" stroke-width="2"
                filter="url(#soft-shadow)"/>
          <text x="{option_x}" y="{option_y + 54}"
                text-anchor="middle"
                font-family="Nunito Sans, Arial, sans-serif"
                font-size="12.5" font-weight="800" fill="#36546C">
            {esc(option['name'][:30])}
          </text>
          <text x="{option_x}" y="{option_y + 77}"
                text-anchor="middle"
                font-family="Nunito Sans, Arial, sans-serif"
                font-size="11.5" fill="#5A778B">
            Итог: {option["score"]:.2f}
          </text>
        """)

        # Сценарии — конечные листочки
        for scenario_index, scenario in enumerate(option["scenarios"]):
            leaf_x = group["leaf_centers"][scenario_index]
            probability = option["normalized"][scenario_index]
            scenario_text = wrap_label(scenario["name"], width=22, max_lines=2)

            parts.append(f"""
              <circle cx="{leaf_x}" cy="{leaf_y}" r="20"
                      fill="{color}" stroke="white" stroke-width="4"
                      filter="url(#soft-shadow)"/>
              <circle cx="{leaf_x}" cy="{leaf_y}" r="11"
                      fill="none" stroke="#FFFFFF" stroke-opacity="0.75" stroke-width="2"/>
            """)

            card_y = leaf_y + 32
            parts.append(f"""
              <rect x="{leaf_x - 96}" y="{card_y}"
                    width="192" height="68" rx="16"
                    fill="#FFFFFF" fill-opacity="0.96"
                    stroke="{color}" stroke-width="1.5"
                    filter="url(#soft-shadow)"/>
            """)

            for i, line in enumerate(scenario_text):
                parts.append(f"""
                  <text x="{leaf_x}" y="{card_y + 22 + i * 16}"
                        text-anchor="middle"
                        font-family="Nunito Sans, Arial, sans-serif"
                        font-size="12" font-weight="700" fill="#36546C">
                    {esc(line)}
                  </text>
                """)

            parts.append(f"""
              <text x="{leaf_x}" y="{card_y + 58}"
                    text-anchor="middle"
                    font-family="Nunito Sans, Arial, sans-serif"
                    font-size="11" fill="#58748A">
                {probability:.1f}% · оценка {scenario['score']:g}
              </text>
            """)

    parts.append("</svg>")

    return """
    <div style="
        width:100%;
        overflow-x:auto;
        padding:12px;
        box-sizing:border-box;
        border-radius:28px;
        background:rgba(255,255,255,0.12);
    ">
        """ + "".join(parts) + """
    </div>
    """


# ---------- Инициализация ----------

if "options" not in st.session_state:
    st.session_state.options = [new_option(), new_option()]
    st.session_state.calculation = None


# ---------- CSS ----------

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700;800&display=swap');

    html, body, .stApp {{
        background-color: #F7FBFD;
        background-image:
            radial-gradient(ellipse at 12% 8%, rgba(226, 242, 251, .82), transparent 34%),
            radial-gradient(ellipse at 88% 18%, rgba(235, 246, 251, .75), transparent 36%),
            url("data:image/svg+xml;base64,{LEAF_BACKGROUND_B64}");
        background-size: auto, auto, cover;
        background-position: center, center, center top;
        background-repeat: no-repeat;
        background-attachment: scroll, scroll, fixed;
    }}

    .block-container {{
        max-width: 1200px;
        padding-top: 1.6rem;
        padding-bottom: 4rem;
    }}

    h1, h2, h3, h4, p, label, button, input, div {{
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }}

    h1 {{
        color: #36546C !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.05em;
    }}

    h2 {{
        color: #36546C !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.04em;
    }}

    h3 {{
        color: #36546C !important;
        font-size: 1.5rem !important;
        font-weight: 800 !important;
    }}

    p, label, .stMarkdownContainer {{
        color: #36546C;
        font-size: 1.08rem;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        border: 1px solid #DEEAF2 !important;
        border-radius: 22px !important;
        background: rgba(255,255,255,0.78) !important;
        box-shadow: 0 12px 26px rgba(88, 120, 140, 0.08);
    }}

    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input {{
        min-height: 48px;
        border-radius: 14px;
        border: 1px solid #D5E3ED;
        background: #fff;
        font-size: 1.02rem;
        color: #36546C;
    }}

    .stButton > button {{
        min-height: 42px;
        border-radius: 12px;
        background: #F3F8FC;
        border: 1px solid #D3E2EF;
        color: #3B5E77;
        font-weight: 700;
    }}

    .stButton > button:hover {{
        background: #E8F5FB;
        border-color: #BCD9EA;
    }}

    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #EAF6FF, #EDF7F5);
        border: 1px solid #B8D6EC;
    }}

    [data-testid="stMetric"] {{
        border: 1px solid #DCEAF5;
        border-radius: 18px;
        background: rgba(255,255,255,0.82);
    }}

    [data-testid="stAlert"] {{
        border-radius: 16px;
    }}

    hr {{
        border-color: #D9E8F1;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Редактор вариантов ----------

st.markdown(
    "<h1 style='text-align:center; margin-bottom:0'>🌿 Дерево решений</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    """
    <p style="text-align:center; color:#71879A; font-size:1.12rem; margin-top:0.4rem;">
    Разложите сложный выбор на варианты и возможные последствия.
    </p>
    """,
    unsafe_allow_html=True,
)

st.text_input(
    "Какое решение нужно принять?",
    key="decision_question",
    placeholder="Например: «Стоит ли менять работу?»",
)

for option_index, option in enumerate(st.session_state.options):
    option_id = option["id"]

    with st.container(border=True):
        col_head, col_delete = st.columns([5, 2])

        with col_head:
            st.markdown(f"### Вариант {option_index + 1}")

        with col_delete:
            if len(st.session_state.options) > 2:
                if st.button("Удалить вариант", key=f"del_option_{option_id}", use_container_width=True):
                    st.session_state.options = [
                        item for item in st.session_state.options if item["id"] != option_id
                    ]
                    st.session_state.calculation = None
                    st.rerun()
            else:
                st.button("Удалить вариант", key=f"del_option_disabled_{option_id}", disabled=True, use_container_width=True)

        st.text_input(
            "Название варианта",
            key=option_name_key(option_id),
            value=option.get("name", ""),
            placeholder=f"Например: «Вариант {option_index + 1}»",
        )
        option["name"] = st.session_state.get(option_name_key(option_id), "")

        for scenario_index, scenario in enumerate(option["scenarios"]):
            scenario_id = scenario["id"]

            with st.container(border=True):
                col_s, col_del = st.columns([5, 2])

                with col_s:
                    st.markdown(f"**Сценарий {scenario_index + 1}**")

                with col_del:
                    if len(option["scenarios"]) > 1:
                        if st.button("Удалить сценарий", key=f"del_scenario_{scenario_id}", use_container_width=True):
                            option["scenarios"] = [
                                item for item in option["scenarios"] if item["id"] != scenario_id
                            ]
                            st.session_state.calculation = None
                            st.rerun()
                    else:
                        st.button("Удалить сценарий", key=f"del_scenario_disabled_{scenario_id}", disabled=True, use_container_width=True)

                st.text_input(
                    "Описание исхода",
                    key=scenario_name_key(scenario_id),
                    value=scenario.get("name", ""),
                    placeholder="Например: «Найду более интересную работу»",
                )
                scenario["name"] = st.session_state.get(scenario_name_key(scenario_id), "")

                col_prob, col_score = st.columns(2)

                with col_prob:
                    p = st.slider(
                        "Вероятность, %",
                        min_value=0,
                        max_value=100,
                        value=int(scenario.get("probability", 0)),
                        step=1,
                        key=probability_key(scenario_id),
                    )
                    scenario["probability"] = p

                with col_score:
                    s = st.slider(
                        "Оценка исхода",
                        min_value=-5.0,
                        max_value=5.0,
                        value=float(scenario.get("score", 0.0)),
                        step=0.5,
                        key=score_key(scenario_id),
                    )
                    scenario["score"] = s

            if st.button("＋ Добавить сценарий", key=f"add_scenario_{option_id}", use_container_width=True):
                option["scenarios"].append(new_scenario())
                st.session_state.calculation = None
                st.rerun()

if st.button("＋ Добавить вариант", use_container_width=True):
    st.session_state.options.append(new_option())
    st.session_state.calculation = None


# ---------- Расчёт ----------

st.divider()

if st.button("Рассчитать и построить дерево", type="primary", use_container_width=True):
    question = st.session_state.get("decision_question", "").strip()
    if not question:
        st.warning("Сначала сформулируйте решение.")
        st.session_state.calculation = None
    else:
        options_to_process = []
        used_names = set()
        valid = True
        error = ""

        for option_index, option in enumerate(st.session_state.options):
            name = (option.get("name") or "").strip()
            if not name:
                valid = False
                error = f"Введите название варианта {option_index + 1}."
                break

            if name in used_names:
                valid = False
                error = f"Названия вариантов должны отличаться: «{name}»."
                break

            used_names.add(name)

            scenarios = []
            for scenario_index, scenario in enumerate(option["scenarios"]):
                scenario_name = (scenario.get("name") or "").strip()
                if not scenario_name:
                    valid = False
                    error = (
                        f"Заполните описание сценария {scenario_index + 1} "
                        f"в варианте «{name}»."
                    )
                    break

                scenarios.append({
                    "name": scenario_name,
                    "probability": int(scenario.get("probability", 0)),
                    "score": float(scenario.get("score", 0.0)),
                })

            if not valid:
                break

            if sum(item["probability"] for item in scenarios) == 0:
                valid = False
                error = (
                    f"В варианте «{name}» хотя бы один сценарий "
                    "должен иметь ненулевую вероятность."
                )
                break

            options_to_process.append({
                "name": name,
                "scenarios": scenarios,
            })

        if not valid:
            st.warning(error)
            st.session_state.calculation = None
        else:
            calculated = calculate_results(options_to_process)
            st.session_state.calculation = {
                "question": question,
                "options": calculated,
                "best_name": max(calculated, key=lambda item: item["score"])["name"],
            }


# ---------- Отображение результата и дерева ----------

result = st.session_state.calculation

if result:
    st.divider()
    st.subheader("2. Результат")

    st.write(f"**Решение:** {result['question']}")

    cols = st.columns(len(result["options"]))
    for idx, option in enumerate(result["options"]):
        with cols[idx]:
            label = option["name"]
            if label == result["best_name"]:
                label = f"🌿 {label}"
            st.metric(
                label=label,
                value=f"{option['score']:.2f}",
            )

    st.success(f"По текущим оценкам лидирует вариант: **{result['best_name']}**.")
    st.caption(
        "Это ориентир для размышления, а не автоматическое решение. "
        "Вероятности сценариев внутри каждого варианта приводятся к 100%."
    )

    st.subheader("Дерево возможных исходов")

    tree_svg = build_tree_svg(
        result["options"],
        result["best_name"],
        result["question"],
    )

    components.html(
        tree_svg,
        height=780,
        scrolling=True,
    )
