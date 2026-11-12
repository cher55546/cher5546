import uuid

import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Дерево решений",
    page_icon="🌿",
    layout="wide",
)


# ---------- Мягкий дизайн ----------

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse at 10% 5%, #e8f3fa 0, transparent 35%),
            linear-gradient(145deg, #f5f9fc, #fbfcfd);
        color: #40566b;
    }
    [data-testid="stHeader"] { background: transparent; }
    .block-container {
        max-width: 1050px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }
    h1, h2, h3 { color: #3f5c73 !important; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #e1eaf1;
        border-radius: 20px;
        background: rgba(255,255,255,.82);
        box-shadow: 0 8px 24px rgba(90,125,151,.06);
    }
    div[data-testid="stTextInput"] input {
        border-radius: 12px;
        border-color: #d9e4ec;
        background: white;
    }
    .stButton > button {
        border-radius: 13px;
        border: 1px solid #d7e5ef;
        background: #f3f8fb;
        color: #45647b;
        font-weight: 600;
    }
    .stButton > button:hover {
        border-color: #b8d2e4;
        background: #eaf3f9;
        color: #34566f;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Данные и стабильные ключи ----------

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
    # Пустые заготовки, а не заполненный пример.
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


def invalidate_results():
    st.session_state.calculation = None


# ---------- Заголовок ----------

st.markdown(
    "<h1 style='text-align:center; margin-bottom:0'>🌿 Дерево решений</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center; color:#718497'>"
    "Разложите сложный выбор на варианты и возможные последствия."
    "</p>",
    unsafe_allow_html=True,
)

st.text_input(
    "Какое решение нужно принять?",
    placeholder="Например: «Стоит ли менять работу?»",
    key="decision_question",
)


# ---------- Редактор вариантов ----------

st.subheader("1. Добавьте варианты")
st.caption("Введите названия вариантов и опишите возможные исходы каждого.")

for option_index, option in enumerate(list(st.session_state.options)):
    option_id = option["id"]
    name_key = option_name_key(option_id)

    with st.container(border=True):
        header, remove_column = st.columns([5, 1])

        with header:
            st.markdown(f"### Вариант {option_index + 1}")

        with remove_column:
            if len(st.session_state.options) > 2:
                if st.button(
                    "Удалить",
                    key=f"remove_option_{option_id}",
                    use_container_width=True,
                ):
                    st.session_state.options = [
                        item for item in st.session_state.options
                        if item["id"] != option_id
                    ]
                    invalidate_results()
                    st.rerun()

        st.text_input(
            "Название варианта",
            placeholder=f"Например: «Вариант {option_index + 1}»",
            key=name_key,
        )

        for scenario_index, scenario in enumerate(list(option["scenarios"])):
            scenario_id = scenario["id"]

            with st.container(border=True):
                scenario_header, scenario_remove = st.columns([5, 1])

                with scenario_header:
                    st.markdown(f"**Сценарий {scenario_index + 1}**")

                with scenario_remove:
                    if len(option["scenarios"]) > 1:
                        if st.button(
                            "Убрать",
                            key=f"remove_scenario_{scenario_id}",
                            use_container_width=True,
                        ):
                            current_option = next(
                                item for item in st.session_state.options
                                if item["id"] == option_id
                            )
                            current_option["scenarios"] = [
                                item for item in current_option["scenarios"]
                                if item["id"] != scenario_id
                            ]
                            invalidate_results()
                            st.rerun()

                st.text_input(
                    "Описание исхода",
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

        if st.button(
            "＋ Добавить сценарий",
            key=f"add_scenario_{option_id}",
        ):
            current_option = next(
                item for item in st.session_state.options
                if item["id"] == option_id
            )
            current_option["scenarios"].append(new_scenario())
            invalidate_results()
            st.rerun()


# Эти кнопки находятся вне формы — Streamlit разрешает ими пользоваться.
add_col, remove_col, _ = st.columns([1.5, 1.7, 3])

with add_col:
    if st.button("＋ Добавить вариант", use_container_width=True):
        st.session_state.options.append(new_option())
        invalidate_results()
        st.rerun()

with remove_col:
    if len(st.session_state.options) > 2:
        if st.button("− Удалить последний", use_container_width=True):
            st.session_state.options.pop()
            invalidate_results()
            st.rerun()


# ---------- Расчёт ----------

st.divider()

if st.button("Рассчитать и построить дерево", type="primary"):
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
        scenarios = []

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

        if sum(item["probability"] for item in scenarios) == 0:
            error = (
                f"В варианте «{option_name}» задайте ненулевую "
                "вероятность хотя бы одному сценарию."
            )
            break

        prepared_options.append({
            "name": option_name,
            "scenarios": scenarios,
        })

    if error:
        st.session_state.calculation = None
        st.warning(error)
    else:
        results = []

        for option in prepared_options:
            total = sum(
                scenario["probability"]
                for scenario in option["scenarios"]
            )
            normalized = [
                scenario["probability"] / total * 100
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


# ---------- Вертикальное дерево ----------

def build_tree(options, best_name):
    palette = ["#8BBDE0", "#82BDA8", "#D9B58F", "#B5A9D7", "#D8A9BE"]

    leaves = {}
    option_x = {}
    cursor = 0.0
    gap = 1.25

    for index, option in enumerate(options):
        count = len(option["scenarios"])
        positions = [cursor + j * gap for j in range(count)]
        leaves[index] = positions
        option_x[index] = sum(positions) / len(positions)
        cursor = positions[-1] + gap * 1.7

    all_x = [x for group in leaves.values() for x in group]
    root_x = sum(all_x) / len(all_x)

    root_y, option_y, scenario_y = 3.2, 2.0, 0.65
    fig = go.Figure()

    # Ветви: решение → варианты → сценарии.
    for index, option in enumerate(options):
        color = "#70B99F" if option["name"] == best_name else palette[index % len(palette)]

        fig.add_trace(go.Scatter(
            x=[root_x, option_x[index]],
            y=[root_y, option_y],
            mode="lines",
            line=dict(color=color, width=3),
            hoverinfo="skip",
            showlegend=False,
        ))

        for scenario_index, _scenario in enumerate(option["scenarios"]):
            fig.add_trace(go.Scatter(
                x=[option_x[index], leaves[index][scenario_index]],
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
        marker=dict(size=30, color="#E9C29F", line=dict(color="white", width=2)),
        text=["Ваше решение"],
        textposition="top center",
        textfont=dict(size=13, color="#40566B"),
        hoverinfo="skip",
        showlegend=False,
    ))

    for index, option in enumerate(options):
        color = "#70B99F" if option["name"] == best_name else palette[index % len(palette)]

        fig.add_trace(go.Scatter(
            x=[option_x[index]],
            y=[option_y],
            mode="markers+text",
            marker=dict(size=25, color=color, line=dict(color="white", width=2)),
            text=[f"{option['name']}<br>Оценка: {option['score']:.2f}"],
            textposition="top center",
            textfont=dict(size=12, color="#40566B"),
            hoverinfo="skip",
            showlegend=False,
        ))

        for scenario_index, scenario in enumerate(option["scenarios"]):
            probability = option["normalized"][scenario_index]
            fig.add_trace(go.Scatter(
                x=[leaves[index][scenario_index]],
                y=[scenario_y],
                mode="markers+text",
                marker=dict(size=16, color=color, line=dict(color="white", width=2)),
                text=[f"{scenario['name']}<br>{probability:.1f}% · оценка {scenario['score']:g}"],
                textposition="bottom center",
                textfont=dict(size=10, color="#40566B"),
                hovertemplate=(
                    f"<b>{scenario['name']}</b><br>"
                    f"Вероятность после нормализации: {probability:.1f}%<br>"
                    f"Оценка: {scenario['score']:g}<extra></extra>"
                ),
                showlegend=False,
            ))

    fig.update_layout(
        height=max(560, 450 + 25 * len(all_x)),
        margin=dict(l=35, r=35, t=80, b=100),
        paper_bgcolor="#FBFCFD",
        plot_bgcolor="#FBFCFD",
        showlegend=False,
        font=dict(family="Arial", color="#40566B"),
    )
    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, range=[0, 4], autorange="reversed", fixedrange=True)
    return fig


# ---------- Результаты ----------

result = st.session_state.calculation

if result:
    st.divider()
    st.subheader("2. Результат")
    st.write(f"**Решение:** {result['question']}")

    columns = st.columns(len(result["options"]))
    for column, option in zip(columns, result["options"]):
        with column:
            st.metric(
                label=f"{'🌿 ' if option['name'] == result['best'] else ''}{option['name']}",
                value=f"{option['score']:.2f} / 5",
            )

    st.success(f"По указанным оценкам лидирует вариант: **{result['best']}**.")
    st.caption(
        "Это ориентир для размышления, а не автоматическое решение. "
        "Вероятности внутри каждого варианта нормализуются до 100%."
    )

    st.subheader("Вертикальное дерево возможных исходов")
    st.plotly_chart(
        build_tree(result["options"], result["best"]),
        use_container_width=True,
        config={"displayModeBar": False},
    )
