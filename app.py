import uuid

import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Дерево решений",
    page_icon="🌿",
    layout="wide",
)


# ---------- Небесная пастельная тема, крупный шрифт ----------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        color-scheme: light;
        --ink: #36546c;
        --muted: #71879a;
        --sky: #9bc9e8;
        --sky-light: #edf6fc;
        --mint: #a9d8ca;
        --peach: #f0ceb0;
        --border: #dce8f0;
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse at 10% 4%, #e8f4fb 0, transparent 38%),
            radial-gradient(ellipse at 92% 10%, #eef7fc 0, transparent 34%),
            linear-gradient(145deg, #f5f9fc, #fbfdfe);
        color: var(--ink);
        font-family: "Nunito Sans", "Segoe UI", sans-serif;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1050px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3, h4 {
        color: var(--ink) !important;
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
        letter-spacing: -0.3px;
    }

    h1 {
        font-size: 2.65rem !important;
        font-weight: 800 !important;
    }

    h2 {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
    }

    h3 {
        font-size: 1.45rem !important;
        font-weight: 800 !important;
    }

    p, label, [data-testid="stMarkdownContainer"] {
        color: var(--ink);
        font-family: "Nunito Sans", "Segoe UI", sans-serif;
        font-size: 1.05rem;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--muted);
        font-size: 1rem;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid var(--border) !important;
        border-radius: 22px !important;
        background: rgba(255, 255, 255, 0.82) !important;
        box-shadow: 0 10px 28px rgba(89, 128, 153, 0.07);
    }

    div[data-testid="stTextInput"] input {
        min-height: 48px;
        border: 1px solid #d5e3ed;
        border-radius: 14px;
        background: #ffffff;
        color: var(--ink);
        font-family: "Nunito Sans", "Segoe UI", sans-serif;
        font-size: 1.05rem;
    }

    div[data-testid="stSlider"] {
        padding-top: 0.25rem;
    }

    div[data-testid="stSlider"] [role="slider"] {
        background: #81b9dc;
    }

    .stButton > button {
        min-height: 44px;
        border: 1px solid #d1e2ee;
        border-radius: 14px;
        background: #f3f8fc;
        color: #42637a;
        font-family: "Nunito Sans", "Segoe UI", sans-serif;
        font-size: 1rem;
        font-weight: 700;
        transition: 0.18s ease;
    }

    .stButton > button:hover:not(:disabled) {
        border-color: #aacde2;
        background: #e8f3fa;
        color: #31556e;
        transform: translateY(-1px);
        box-shadow: 0 5px 14px rgba(89, 128, 153, 0.10);
    }

    .stButton > button:disabled {
        opacity: 0.52;
        cursor: not-allowed;
    }

    .stButton > button[kind="primary"] {
        min-height: 50px;
        border: 1px solid #a9cfe5;
        background: linear-gradient(100deg, #dceefa, #eaf4fb);
        color: #34566e;
        font-size: 1.05rem;
    }

    [data-testid="stMetric"] {
        padding: 16px;
        border: 1px solid var(--border);
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.8);
    }

    [data-testid="stAlert"] {
        border-radius: 16px;
    }

    hr {
        border-color: var(--border);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Состояние приложения ----------

def new_scenario(first=False):
    return {
        "id": uuid.uuid4().hex,
        "probability": 100 if first else 0,
    }


def new_option():
    return {
        "id": uuid.uuid4().hex,
        "scenarios": [new_scenario(first=True)],
    }


if "options" not in st.session_state:
    st.session_state.options = [new_option(), new_option()]

if "calculation" not in st.session_state:
    st.session_state.calculation = None


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


# ---------- Заголовок ----------

st.markdown(
    "<h1 style='text-align:center; margin-bottom:0'>🌿 Дерево решений</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    """
    <p style="text-align:center; color:#71879a; font-size:1.12rem;">
    Разложите сложный выбор на варианты и возможные последствия.
    </p>
    """,
    unsafe_allow_html=True,
)

st.text_input(
    "Какое решение нужно принять?",
    placeholder="Например: «Стоит ли менять работу?»",
    key="decision_question",
)


# ---------- Редактор вариантов ----------

st.subheader("1. Добавьте варианты")
st.caption(
    "Заполните названия вариантов и возможные исходы. "
    "Для каждого исхода укажите вероятность и оценку."
)

for option_index, option in enumerate(list(st.session_state.options)):
    option_id = option["id"]
    name_key = option_name_key(option_id)

    with st.container(border=True):
        header_col, delete_col = st.columns([5, 1.6])

        with header_col:
            st.markdown(f"### Вариант {option_index + 1}")

        with delete_col:
            st.button(
                "Удалить вариант",
                key=f"delete_option_{option_id}",
                disabled=len(st.session_state.options) <= 2,
                help=(
                    "Для сравнения нужно оставить не менее двух вариантов."
                    if len(st.session_state.options) <= 2
                    else "Удалить этот вариант"
                ),
                use_container_width=True,
                on_click=lambda oid=option_id: delete_option(oid),
            )

        st.text_input(
            "Название варианта",
            placeholder=f"Например: «Вариант {option_index + 1}»",
            key=name_key,
        )

        for scenario_index, scenario in enumerate(list(option["scenarios"])):
            scenario_id = scenario["id"]

            with st.container(border=True):
                scenario_header, scenario_delete = st.columns([5, 1.6])

                with scenario_header:
                    st.markdown(f"**Сценарий {scenario_index + 1}**")

                with scenario_delete:
                    st.button(
                        "Удалить сценарий",
                        key=f"delete_scenario_{scenario_id}",
                        disabled=len(option["scenarios"]) <= 1,
                        help=(
                            "У варианта должен остаться хотя бы один сценарий."
                            if len(option["scenarios"]) <= 1
                            else "Удалить этот сценарий"
                        ),
                        use_container_width=True,
                        on_click=lambda oid=option_id, sid=scenario_id:
                            delete_scenario(oid, sid),
                    )

                st.text_input(
                    "Описание возможного исхода",
                    placeholder="Например: «Найду более интересную работу»",
                    key=scenario_name_key(scenario_id),
                )

                probability_col, score_col = st.columns(2)

                with probability_col:
                    st.slider(
                        "Вероятность, %",
                        min_value=0,
                        max_value=100,
                        value=int(scenario["probability"]),
                        step=1,
                        key=probability_key(scenario_id),
                    )

                with score_col:
                    st.slider(
                        "Оценка исхода",
                        min_value=-5.0,
                        max_value=5.0,
                        value=0.0,
                        step=0.5,
                        key=score_key(scenario_id),
                        help="−5 — очень нежелательный исход, +5 — очень желательный.",
                    )

        st.button(
            "＋ Добавить сценарий",
            key=f"add_scenario_{option_id}",
            on_click=lambda oid=option_id: add_scenario(oid),
        )


# ---------- Обработчики кнопок ----------

def delete_option(option_id):
    if len(st.session_state.options) > 2:
        st.session_state.options = [
            option for option in st.session_state.options
            if option["id"] != option_id
        ]
        clear_results()


def delete_scenario(option_id, scenario_id):
    for option in st.session_state.options:
        if option["id"] == option_id and len(option["scenarios"]) > 1:
            option["scenarios"] = [
                scenario for scenario in option["scenarios"]
                if scenario["id"] != scenario_id
            ]
            clear_results()
            break


def add_scenario(option_id):
    for option in st.session_state.options:
        if option["id"] == option_id:
            option["scenarios"].append(new_scenario())
            clear_results()
            break


def add_option():
    st.session_state.options.append(new_option())
    clear_results()


def remove_last_option():
    if len(st.session_state.options) > 2:
        st.session_state.options.pop()
        clear_results()


# Кнопки добавления / удаления вариантов
add_col, remove_col, _ = st.columns([1.7, 1.9, 3])

with add_col:
    st.button(
        "＋ Добавить вариант",
        key="add_option_button",
        on_click=add_option,
        use_container_width=True,
    )

with remove_col:
    st.button(
        "− Удалить последний",
        key="remove_last_option_button",
        disabled=len(st.session_state.options) <= 2,
        help="Для сравнения нужно оставить не менее двух вариантов.",
        on_click=remove_last_option,
        use_container_width=True,
    )


# ---------- Расчёт ----------

st.divider()

if st.button(
    "Рассчитать и построить дерево",
    type="primary",
    use_container_width=True,
):
    question = st.session_state.get("decision_question", "").strip()
    error = None
    prepared_options = []
    used_names = set()

    if not question:
        error = "Сначала сформулируйте решение."

    for option_index, option in enumerate(st.session_state.options):
        if error:
            break

        option_name = st.session_state.get(
            option_name_key(option["id"]), ""
        ).strip()

        if not option_name:
            error = f"Введите название варианта {option_index + 1}."
            break

        if option_name in used_names:
            error = f"Названия вариантов должны отличаться: «{option_name}»."
            break

        used_names.add(option_name)
        prepared_scenarios = []

        for scenario_index, scenario in enumerate(option["scenarios"]):
            scenario_name = st.session_state.get(
                scenario_name_key(scenario["id"]), ""
            ).strip()

            if not scenario_name:
                error = (
                    f"Заполните сценарий {scenario_index + 1} "
                    f"в варианте «{option_name}»."
                )
                break

            prepared_scenarios.append({
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

        if sum(item["probability"] for item in prepared_scenarios) == 0:
            error = (
                f"В варианте «{option_name}» задайте ненулевую "
                "вероятность хотя бы одному сценарию."
            )
            break

        prepared_options.append({
            "name": option_name,
            "scenarios": prepared_scenarios,
        })

    if error:
        st.session_state.calculation = None
        st.warning(error)
    else:
        results = []

        for option in prepared_options:
            total_probability = sum(
                scenario["probability"]
                for scenario in option["scenarios"]
            )

            normalized = [
                scenario["probability"] / total_probability * 100
                for scenario in option["scenarios"]
            ]

            expected_score = sum(
                normalized[index] / 100 * scenario["score"]
                for index, scenario in enumerate(option["scenarios"])
            )

            results.append({
                **option,
                "normalized": normalized,
                "score": expected_score,
            })

        st.session_state.calculation = {
            "question": question,
            "options": results,
            "best": max(results, key=lambda item: item["score"])["name"],
        }


# ---------- Визуализация дерева ----------

def build_tree(options, best_name):
    colors = ["#8BBFE0", "#83C5B0", "#DDBB98", "#B6A9D7", "#D7A9BD"]

    leaf_x = {}
    option_x = {}
    cursor = 0.0
    gap = 1.2

    for index, option in enumerate(options):
        count = len(option["scenarios"])
        positions = [cursor + item * gap for item in range(count)]
        leaf_x[index] = positions
        option_x[index] = sum(positions) / len(positions)
        cursor = positions[-1] + gap * 1.7

    all_leaf_x = [
        x for positions in leaf_x.values() for x in positions
    ]
    root_x = sum(all_leaf_x) / len(all_leaf_x)

    root_y, option_y, scenario_y = 3.2, 2.0, 0.65
    fig = go.Figure()

    for index, option in enumerate(options):
        color = (
            "#70B99F"
            if option["name"] == best_name
            else colors[index % len(colors)]
        )

        fig.add_trace(go.Scatter(
            x=[root_x, option_x[index]],
            y=[root_y, option_y],
            mode="lines",
            line=dict(color=color, width=3),
            hoverinfo="skip",
            showlegend=False,
        ))

        for scenario_index in range(len(option["scenarios"])):
            fig.add_trace(go.Scatter(
                x=[option_x[index], leaf_x[index][scenario_index]],
                y=[option_y, scenario_y],
                mode="lines",
                line=dict(color=color, width=2),
                hoverinfo="skip",
                showlegend=False,
            ))

    fig.add_trace(go.Scatter(
        x=[root_x],
        y=[root_y],
        mode="markers+text",
        marker=dict(
            size=32,
            color="#F0CEB0",
            line=dict(color="white", width=3),
        ),
        text=["Ваше решение"],
        textposition="top center",
        textfont=dict(size=15, color="#36546C"),
        hoverinfo="skip",
        showlegend=False,
    ))

    for index, option in enumerate(options):
        color = (
            "#70B99F"
            if option["name"] == best_name
            else colors[index % len(colors)]
        )

        fig.add_trace(go.Scatter(
            x=[option_x[index]],
            y=[option_y],
            mode="markers+text",
            marker=dict(
                size=27,
                color=color,
                line=dict(color="white", width=3),
            ),
            text=[f"{option['name']}<br>Оценка: {option['score']:.2f}"],
            textposition="top center",
            textfont=dict(size=13, color="#36546C"),
            hoverinfo="skip",
            showlegend=False,
        ))

        for scenario_index, scenario in enumerate(option["scenarios"]):
            probability = option["normalized"][scenario_index]

            fig.add_trace(go.Scatter(
                x=[leaf_x[index][scenario_index]],
                y=[scenario_y],
                mode="markers+text",
                marker=dict(
                    size=18,
                    color=color,
                    line=dict(color="white", width=2),
                ),
                text=[
                    f"{scenario['name']}<br>"
                    f"{probability:.1f}% · оценка {scenario['score']:g}"
                ],
                textposition="bottom center",
                textfont=dict(size=11, color="#36546C"),
                hovertemplate=(
                    f"<b>{scenario['name']}</b><br>"
                    f"Вероятность: {probability:.1f}%<br>"
                    f"Оценка: {scenario['score']:g}<extra></extra>"
                ),
                showlegend=False,
            ))

    fig.update_layout(
        height=max(600, 470 + len(all_leaf_x) * 24),
        margin=dict(l=40, r=40, t=90, b=110),
        paper_bgcolor="#FBFDFE",
        plot_bgcolor="#FBFDFE",
        font=dict(
            family="Nunito Sans, Arial, sans-serif",
            color="#36546C",
            size=13,
        ),
        showlegend=False,
    )
    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(
        visible=False,
        range=[0, 4],
        autorange="reversed",
        fixedrange=True,
    )
    return fig


# ---------- Результаты ----------

result = st.session_state.calculation

if result:
    st.divider()
    st.subheader("2. Результат")
    st.write(f"**Решение:** {result['question']}")

    metric_columns = st.columns(len(result["options"]))

    for column, option in zip(metric_columns, result["options"]):
        with column:
            label = option["name"]
            if label == result["best"]:
                label = f"🌿 {label}"

            st.metric(
                label=label,
                value=f"{option['score']:.2f} / 5",
            )

    st.success(f"По указанным оценкам лидирует вариант: **{result['best']}**.")
    st.caption(
        "Это ориентир для размышления, а не автоматическое решение. "
        "Вероятности сценариев внутри каждого варианта приводятся к 100%."
    )

    st.subheader("Вертикальное дерево возможных исходов")
    st.plotly_chart(
        build_tree(result["options"], result["best"]),
        use_container_width=True,
        config={"displayModeBar": False},
    )
