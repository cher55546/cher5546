import uuid
import html

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Дерево решений",
    page_icon="🌿",
    layout="wide",
)


# ---------- Вспомогательные функции ----------

def new_scenario(first=False):
    return {
        "id": uuid.uuid4().hex,
        "probability": 100 if first else 0,
        "score": 0.0,
        "name": "",
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
        probability_values = [scenario["probability"] for scenario in option["scenarios"]]
        normalized = normalize(probability_values)

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


def build_tree_svg(options, best_name, question):
    """
    Рисует дерево в виде SVG:
    - корень снизу,
    - от корня идут ветви к вариантам,
    - от вариантов — ещё ветви к сценариям.
    """

    # Параметры макета
    leaf_w = 200
    leaf_h = 118
    leaf_gap = 22
    option_w = 240
    option_h = 90
    group_gap = 52
    root_box_w = max(280, min(430, len(question) * 8.4))

    # Расчёт координат
    group_widths = [
        max(
            leaf_w,
            len(option["scenarios"]) * leaf_w + (len(option["scenarios"]) - 1) * leaf_gap,
        )
        for option in options
    ]

    svg_width = 120 + sum(group_widths) + max(0, len(options) - 1) * group_gap
    svg_height = 760

    groups = []
    current_x = 70

    for option in options:
        count = len(option["scenarios"])
        content_width = count * leaf_w + (count - 1) * leaf_gap
        free_space = max(0, group_widths[options.index(option)] - content_width)
        first_leaf_x = current_x + free_space / 2
        leaves = [
            first_leaf_x + i * (leaf_w + leaf_gap)
            for i in range(count)
        ]

        groups.append({
            "option": option,
            "x": current_x,
            "content_x": first_leaf_x,
            "leaves": leaves,
            "center_x": current_x + group_widths[options.index(option)] / 2,
        })

        current_x += group_widths[options.index(option)] + group_gap

    root_x = (groups[0]["x"] + groups[-1]["x"] + group_widths[-1]) / 2
    root_y = 620
    option_y = 390
    leaf_y = 120

    palette = ["#8BBFE0", "#83C5B0", "#DDBB98", "#B6A9D7", "#D7A9BD"]

    def card_name(name):
        clean = html.escape(str(name))
        return clean[:34] + "…" if len(clean) > 34 else clean

    def scenario_name(name):
        clean = html.escape(str(name))
        if len(clean) > 22:
            return clean[:21] + "…"
        return clean

    parts = [
        f"""
        <svg xmlns="http://www.w3.org/2000/svg"
             width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}"
             role="img" aria-label="Дерево решений">
        <defs>
          <filter id="shadow" x="-20%" y="-20%" width="150%" height="170%">
            <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#6F8CA0" flood-opacity="0.12"/>
          </filter>
          <linearGradient id="trunkGradient" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stop-color="#C9A47E"/>
            <stop offset="100%" stop-color="#A77E5A"/>
          </linearGradient>
        </defs>
        <rect width="100%" height="100%" fill="#F8FBFD" rx="28"/>
        """
    ]

    # Корень
    parts.append(f"""
        <rect x="{root_x - root_box_w/2}" y="{root_y - 28}"
              width="{root_box_w}" height="58" rx="22"
              fill="#F6D8BA" stroke="#D7A981" stroke-width="2"
              filter="url(#shadow)"/>
        <text x="{root_x}" y="{root_y + 10}" text-anchor="middle"
              font-family="Nunito Sans, Arial, sans-serif"
              font-size="16" font-weight="800" fill="#4A5E6E">
          {html.escape(question)}
        </text>
    """)

    # Ствол
    parts.append(f"""
        <path d="M {root_x} {root_y}
                 C {root_x - 12} 600, {root_x + 12} 540, {root_x} 505"
              fill="none" stroke="url(#trunkGradient)" stroke-width="16" stroke-linecap="round"/>
    """)

    # Варианты и ветви
    for index, group in enumerate(groups):
        option = group["option"]
        color = "#70B99F" if option["name"] == best_name else palette[index % len(palette)]
        option_center_x = group["center_x"]

        parts.append(f"""
            <path d="M {root_x} 507
                     C {root_x} 500, {option_center_x} 455, {option_center_x} {option_y + option_h}"
                  fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round"/>
        """)

        # Карточка варианта
        parts.append(f"""
            <rect x="{option_center_x - option_w/2}" y="{option_y}"
                  width="{option_w}" height="{option_h}" rx="22"
                  fill="#FFFFFF" stroke="{color}" stroke-width="3"
                  filter="url(#shadow)"/>
            <circle cx="{option_center_x - option_w/2 + 18}" cy="{option_y + 22}" r="7" fill="{color}"/>
            <text x="{option_center_x}" y="{option_y + 42}"
                  text-anchor="middle"
                  font-family="Nunito Sans, Arial, sans-serif"
                  font-size="16" font-weight="800" fill="#36546C">
              {card_name(option["name"])}
            </text>
            <text x="{option_center_x}" y="{option_y + 66}"
                  text-anchor="middle"
                  font-family="Nunito Sans, Arial, sans-serif"
                  font-size="13" fill="#5A778B">
              Итоговая оценка: {option["score"]:.2f}
            </text>
        """)

        # От варианта к сценариям
        for leaf_x in group["leaves"]:
            leaf_center_x = leaf_x + leaf_w / 2
            parts.append(f"""
                <path d="M {option_center_x} {option_y}
                         C {option_center_x} 320, {leaf_center_x} 300, {leaf_center_x} {leaf_y + leaf_h}"
                      fill="none" stroke="{color}" stroke-width="4" stroke-linecap="round"/>
            """)

        # Листья-сценарии
        for scenario_index, scenario in enumerate(option["scenarios"]):
            leaf_x = group["leaves"][scenario_index]
            center_x = leaf_x + leaf_w / 2
            probability = option["normalized"][scenario_index]
            score = scenario["score"]

            parts.append(f"""
                <path d="M {leaf_x + 20} {leaf_y + 10}
                         C {leaf_x + 12} {leaf_y + 10}, {leaf_x + 10} {leaf_y + 12},
                           {leaf_x + 16} {leaf_y + leaf_h / 2}
                         C {leaf_x + 26} {leaf_y + leaf_h - 20},
                           {leaf_x + leaf_w - 26} {leaf_y + leaf_h - 20},
                           {leaf_x + leaf_w - 16} {leaf_y + leaf_h / 2}
                         C {leaf_x + leaf_w - 10} {leaf_y + 12},
                           {leaf_x + leaf_w - 12} {leaf_y + 10},
                           {leaf_x + leaf_w - 20} {leaf_y + 10} Z"
                      fill="{color}" fill-opacity="0.18" stroke="{color}" stroke-width="2"/>
            """)

            parts.append(f"""
                <text x="{center_x}" y="{leaf_y + 28}"
                      text-anchor="middle"
                      font-family="Nunito Sans, Arial, sans-serif"
                      font-size="12.5" font-weight="700" fill="#36546C">
                  {scenario_name(scenario['name'])}
                </text>
                <text x="{center_x}" y="{leaf_y + 53}"
                      text-anchor="middle"
                      font-family="Nunito Sans, Arial, sans-serif"
                      font-size="12" fill="#607B8E">
                  {probability:.1f}% · оценка {score:g}
                </text>
            """)

    parts.append("</svg>")
    return "".join(parts)


# ---------- Инициализация состояния ----------

if "options" not in st.session_state:
    st.session_state.options = [new_option(), new_option()]

if "calculation" not in st.session_state:
    st.session_state.calculation = None


# ---------- Стили ----------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --ink: #36546C;
        --muted: #71879A;
        --sky-soft: #EEF7FD;
        --sky: #A9D8F6;
        --mint: #A9D8CA;
        --peach: #F1D2AF;
        --border: #DCEAF5;
        --cloud: rgba(255,255,255,0.82);
    }

    html, body, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 12% 8%, #EAF7FF 0%, transparent 28%),
            radial-gradient(circle at 88% 12%, #F0F8FF 0%, transparent 32%),
            linear-gradient(145deg, #F5F9FC 0%, #F7FBFD 100%);
        font-family: "Nunito Sans", "Segoe UI", sans-serif;
        color: var(--ink);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, h4, p, label, div, button, input {
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }

    h1 {
        color: var(--ink) !important;
        font-weight: 800 !important;
        font-size: 3rem !important;
        letter-spacing: -0.04em;
    }

    h2 {
        color: var(--ink) !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
        letter-spacing: -0.03em;
    }

    h3 {
        color: var(--ink) !important;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
    }

    .stContainer > div {
        border: 1px solid var(--border);
        border-radius: 22px;
        background: rgba(255,255,255,0.76);
        box-shadow: 0 12px 28px rgba(114, 138, 155, 0.06);
    }

    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input {
        min-height: 48px;
        border-radius: 14px;
        border: 1px solid #D7E3EE;
        background: #fff;
        color: var(--ink);
        font-size: 1.02rem;
    }

    .stSlider [role="slider"] {
        background: #8ABEDF;
    }

    .stButton > button {
        min-height: 42px;
        border-radius: 12px;
        border: 1px solid #D1E3F0;
        background: #F3F8FC;
        color: var(--ink);
        font-weight: 700;
        font-size: 0.98rem;
        transition: 0.18s ease;
    }

    .stButton > button:hover {
        background: #EAF4FB;
        border-color: #B5D4EA;
        transform: translateY(-1px);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #EAF6FF, #EEF7F7);
        border: 1px solid #B6D4E9;
        color: var(--ink);
    }

    [data-testid="stMetric"] {
        border: 1px solid var(--border);
        border-radius: 18px;
        background: rgba(255,255,255,0.82);
    }

    [data-testid="stAlert"] {
        border-radius: 16px;
    }

    hr {
        border-color: #DCEAF5;
    }
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
    <p style="text-align:center; color:#71879A; font-size:1.15rem; margin-top:0.35rem;">
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


# ---------- Редактор вариантов ----------

st.subheader("1. Добавьте варианты")
st.caption("Заполните названия вариантов, а затем для каждого варианта опишите исходы.")

# Добавление/удаление варианта
if st.button("＋ Добавить вариант", use_container_width=True):
    st.session_state.options.append(new_option())
    st.session_state.calculation = None

for option_index, option in enumerate(st.session_state.options):
    option_id = option["id"]

    with st.container(border=True):
        col_title, col_delete = st.columns([5, 2])
        with col_title:
            st.markdown(f"### Вариант {option_index + 1}")

        with col_delete:
            if len(st.session_state.options) > 2:
                if st.button(
                    "Удалить вариант",
                    key=f"delete_option_{option_id}",
                    use_container_width=True,
                ):
                    st.session_state.options = [
                        item for item in st.session_state.options
                        if item["id"] != option_id
                    ]
                    st.session_state.calculation = None
                    st.rerun()
            else:
                st.button(
                    "Удалить вариант",
                    key=f"delete_option_disabled_{option_id}",
                    disabled=True,
                    use_container_width=True,
                )

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
                col_scenario, col_delete_scenario = st.columns([5, 2])

                with col_scenario:
                    st.markdown(f"**Сценарий {scenario_index + 1}**")

                with col_delete_scenario:
                    if len(option["scenarios"]) > 1:
                        if st.button(
                            "Удалить сценарий",
                            key=f"delete_scenario_{scenario_id}",
                            use_container_width=True,
                        ):
                            option["scenarios"] = [
                                item for item in option["scenarios"]
                                if item["id"] != scenario_id
                            ]
                            st.session_state.calculation = None
                            st.rerun()
                    else:
                        st.button(
                            "Удалить сценарий",
                            key=f"delete_scenario_disabled_{scenario_id}",
                            disabled=True,
                            use_container_width=True,
                        )

                st.text_input(
                    "Описание исхода",
                    key=scenario_name_key(scenario_id),
                    value=scenario.get("name", ""),
                    placeholder="Например: «Найду более интересную работу»",
                )

                scenario["name"] = st.session_state.get(scenario_name_key(scenario_id), "")

                prob_col, score_col = st.columns(2)

                with prob_col:
                    sc_prob = st.slider(
                        "Вероятность, %",
                        min_value=0,
                        max_value=100,
                        value=int(scenario.get("probability", 0)),
                        step=1,
                        key=probability_key(scenario_id),
                    )
                    scenario["probability"] = sc_prob

                with score_col:
                    sc_score = st.slider(
                        "Оценка исхода",
                        min_value=-5.0,
                        max_value=5.0,
                        value=float(scenario.get("score", 0.0)),
                        step=0.5,
                        key=score_key(scenario_id),
                        help="−5 — очень нежелательный исход, +5 — очень желательный.",
                    )
                    scenario["score"] = sc_score

            if st.button(
                "＋ Добавить сценарий",
                key=f"add_scenario_{option_id}",
                use_container_width=True,
            ):
                option["scenarios"].append(new_scenario())
                st.session_state.calculation = None
                st.rerun()


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
        error_message = ""

        for option_index, option in enumerate(st.session_state.options):
            option_name = (option.get("name") or "").strip()
            if not option_name:
                valid = False
                error_message = f"Введите название варианта {option_index + 1}."
                break

            if option_name in used_names:
                valid = False
                error_message = f"Названия вариантов должны отличаться: «{option_name}»."
                break

            used_names.add(option_name)

            scenario_list = []

            for scenario_index, scenario in enumerate(option["scenarios"]):
                scenario_name = (scenario.get("name") or "").strip()
                if not scenario_name:
                    valid = False
                    error_message = (
                        f"Заполните описание сценария {scenario_index + 1} "
                        f"в варианте «{option_name}»."
                    )
                    break

                scenario_list.append({
                    "name": scenario_name,
                    "probability": int(scenario.get("probability", 0)),
                    "score": float(scenario.get("score", 0.0)),
                })

            if not valid:
                break

            if sum(item["probability"] for item in scenario_list) == 0:
                valid = False
                error_message = (
                    f"В варианте «{option_name}» хотя бы один сценарий "
                    "должен иметь ненулевую вероятность."
                )
                break

            options_to_process.append({
                "name": option_name,
                "scenarios": scenario_list,
            })

        if not valid:
            st.session_state.calculation = None
            st.warning(error_message)
        else:
            calculated = calculate_results(options_to_process)
            st.session_state.calculation = {
                "question": question,
                "options": calculated,
                "best_name": max(calculated, key=lambda item: item["score"])["name"],
            }


# ---------- Вывод результатов ----------

result = st.session_state.calculation

if result:
    st.divider()
    st.subheader("2. Результат")

    st.write(f"**Решение:** {result['question']}")

    cols = st.columns(len(result["options"]))
    for idx, option in enumerate(result["options"]):
        with cols[idx]:
            title = option["name"]
            if title == result["best_name"]:
                title = f"🌿 {title}"

            st.metric(
                label=title,
                value=f"{option['score']:.2f}",
            )

    st.success(
        f"По текущим оценкам лидирует вариант: **{result['best_name']}**."
    )
    st.caption(
        "Это ориентир для размышления, а не автоматическое решение. "
        "Вероятности сценариев внутри каждого варианта приводятся к 100%."
    )

    st.subheader("Вертикальное дерево возможных исходов")

    tree_svg = build_tree_svg(
        result["options"],
        result["best_name"],
        result["question"],
    )

    components.html(
        tree_svg,
        height=760,
        scrolling=False,
    )
