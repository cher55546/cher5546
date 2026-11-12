import streamlit as st
import uuid
import plotly.graph_objects as go

st.set_page_config(
    page_title="Дерево решений",
    page_icon="🌤️",
    layout="wide"
)

# ---------- helpers ----------
def new_scenario(name="Сценарий", prob=50, score=1):
    return {
        "id": uuid.uuid4().hex,
        "name": name,
        "probability": prob,
        "score": score,
    }

def new_option(name="Вариант"):
    return {
        "id": uuid.uuid4().hex,
        "name": name,
        "scenarios": [new_scenario()],
    }

# default demo data
if "options" not in st.session_state:
    st.session_state.options = [
        {
            "id": "opt_a",
            "name": "Вариант 1 — Учиться",
            "scenarios": [
                {"id": "a1", "name": "Есть реальный прогресс", "probability": 45, "score": 5},
                {"id": "a2", "name": "Будет тяжело, но полезно", "probability": 30, "score": 1},
                {"id": "a3", "name": "Усталость перевесит пользу", "probability": 25, "score": -3},
            ],
        },
        {
            "id": "opt_b",
            "name": "Вариант 2 — Отдыхать",
            "scenarios": [
                {"id": "b1", "name": "Хорошо восстанавливает силы", "probability": 60, "score": 4},
                {"id": "b2", "name": "Отдых без пользы, но приятный", "probability": 25, "score": 2},
                {"id": "b3", "name": "Есть чувство, что время прошло зря", "probability": 15, "score": -1},
            ],
        },
        {
            "id": "opt_c",
            "name": "Вариант 3 — Сочетать учёбу и отдых",
            "scenarios": [
                {"id": "c1", "name": "Получится и развиваться, и восстанавливаться", "probability": 40, "score": 5},
                {"id": "c2", "name": "Будет напряжённо, но терпимо", "probability": 35, "score": 2},
                {"id": "c3", "name": "Кажется, что времени не хватило ни на одно, ни на другое", "probability": 25, "score": -2},
            ],
        },
    ]

def normalize(values):
    total = sum(values)
    if total == 0:
        return values
    return [v / total * 100 for v in values]

def calculate_results(options):
    results = []
    for option in options:
        raw_probs = [s["probability"] for s in option["scenarios"]]
        norm = normalize(raw_probs)
        weighted = sum((norm[i] / 100) * option["scenarios"][i]["score"] for i in range(len(option["scenarios"])))
        results.append({
            "name": option["name"],
            "score": weighted,
            "normalized": norm,
            "scenarios": option["scenarios"],
        })
    return results

# ---------- UI ----------
st.markdown(
    """
    <style>
    html, body {
        background: #0d1117;
        color: #e6edf3;
    }
    .stApp {
        background: #0d1117;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    h1, h2, h3, p, label {
        color: #f0f6fc;
    }
    div[data-testid="stContainer"] {
        border-radius: 18px;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.06);
        padding: 1rem;
    }
    .stTextInput input, .stNumberInput input {
        background: #111827;
        color: #f3f4f6;
        border: 1px solid #374151;
    }
    .stSlider > div > div > div > div {
        background: #f59e0b;
    }
    .stButton > button {
        background: #f59e0b;
        color: #111827;
        font-weight: 700;
        border: none;
        border-radius: 10px;
    }
    .stButton > button:hover {
        background: #fbbf24;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>🌤️ Дерево решений</h1>", unsafe_allow_html=True)
st.caption("Сравни варианты, оцени вероятности и выбирай осознанно.")

question = st.text_input("Какое решение нужно принять?", value="Что лучше сделать в выходные?")

with st.form("main_form", clear_on_submit=False):
    for option_index, option in enumerate(st.session_state.options):
        st.subheader(f"Вариант {option_index + 1} — {option['name']}")
        option_name = st.text_input(
            f"Название варианта {option_index + 1}",
            value=option["name"],
            key=f"opt_name_{option['id']}"
        )
        option["name"] = option_name

        for sc_index, scenario in enumerate(option["scenarios"]):
            st.write(f"{sc_index + 1}. {scenario['name']}")
            scenario_name = st.text_input(
                f"Название сценария {sc_index + 1} для варианта {option_name}",
                value=scenario["name"],
                key=f"sc_name_{scenario['id']}"
            )
            scenario["name"] = scenario_name

            probability = st.slider(
                f"Вероятность для «{scenario_name}»",
                min_value=0,
                max_value=100,
                value=int(scenario["probability"]),
                key=f"sc_prob_{scenario['id']}"
            )
            scenario["probability"] = probability

            score = st.number_input(
                f"Оценка для «{scenario_name}»",
                min_value=-5.0,
                max_value=5.0,
                value=float(scenario["score"]),
                step=0.5,
                key=f"sc_score_{scenario['id']}"
            )
            scenario["score"] = score

        if st.button(f"Добавить сценарий к «{option_name}»", key=f"add_scenario_{option['id']}"):
            option["scenarios"].append(new_scenario())
            st.rerun()

    submitted = st.form_submit_button("Рассчитать и показать дерево")

if submitted:
    results = calculate_results(st.session_state.options)
    best = max(results, key=lambda x: x["score"])
    st.success(f"Лидер: {best['name']}")

    for r in results:
        st.write(f"**{r['name']}** — итог: {r['score']:.2f}")

    # plotting tree
    fig = go.Figure()

    root_x = 0
    root_y = 0

    # horizontal positions
    positions = [-2, 0, 2]
    for idx, r in enumerate(results):
        x = positions[idx]
        y = 1.5
        fig.add_trace(go.Scatter(
            x=[root_x, x],
            y=[root_y, y],
            mode="lines",
            line=dict(color="#7FB3D5", width=2),
            showlegend=False
        ))

        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode="markers+text",
            marker=dict(size=20, color="#7FB3D5"),
            text=[f"{r['name']}<br>{r['score']:.2f}"],
            textposition="top center",
            showlegend=False
        ))

        for i, sc in enumerate(r["scenarios"]):
            sx = x + 2 if x >= 0 else x - 2
            sy = y - 1.6 + i * 1.5
            fig.add_trace(go.Scatter(
                x=[x, sx],
                y=[y, sy],
                mode="lines",
                line=dict(color="#82C9A5", width=1.5),
                showlegend=False
            ))

            fig.add_trace(go.Scatter(
                x=[sx],
                y=[sy],
                mode="markers+text",
                marker=dict(size=12, color="#82C9A5"),
                text=[f"{sc['name']}<br>{sc['probability']}%"],
                textposition="top center",
                showlegend=False
            ))

    fig.add_trace(go.Scatter(
        x=[root_x],
        y=[root_y],
        mode="markers+text",
        marker=dict(size=24, color="#F5C08D"),
        text=[question],
        textposition="top center",
        showlegend=False
    ))

    fig.update_layout(
        template="plotly_white",
        width=1200,
        height=700,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(color="#f3f4f6", size=12)
    )

    st.plotly_chart(fig, use_container_width=True)
