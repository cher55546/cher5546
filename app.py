import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Дерево решений", page_icon="🌤️", layout="wide")

st.title("🌤️ Дерево решений")
st.caption("Сравни варианты, оцени вероятности и выбирай осознанно")

question = st.text_input(
    "Какое решение нужно принять?",
    value="Что лучше сделать в выходные?"
)

# --- База вариантов ---
default_options = [
    {
        "name": "Вариант 1 — Учиться",
        "scenarios": [
            {"name": "Есть реальный прогресс", "probability": 45, "score": 5},
            {"name": "Будет тяжело, но полезно", "probability": 30, "score": 1},
            {"name": "Усталость перевесит пользу", "probability": 25, "score": -3},
        ],
    },
    {
        "name": "Вариант 2 — Отдыхать",
        "scenarios": [
            {"name": "Хорошо восстанавливает силы", "probability": 60, "score": 4},
            {"name": "Отдых без пользы, но приятный", "probability": 25, "score": 2},
            {"name": "Есть чувство, что время прошло зря", "probability": 15, "score": -1},
        ],
    },
    {
        "name": "Вариант 3 — Сочетать учёбу и отдых",
        "scenarios": [
            {"name": "Получится и развиваться, и восстанавливаться", "probability": 40, "score": 5},
            {"name": "Будет напряжённо, но терпимо", "probability": 35, "score": 2},
            {"name": "Кажется, что времени не хватило ни на одно, ни на другое", "probability": 25, "score": -2},
        ],
    },
]

if "options" not in st.session_state:
    st.session_state.options = default_options

def normalize(probabilities):
    total = sum(probabilities)
    if total == 0:
        return probabilities
    return [p / total * 100 for p in probabilities]

def calc_scores(options):
    results = []
    for option in options:
        probs = [s["probability"] for s in option["scenarios"]]
        normalized = normalize(probs)
        weighted = sum(
            normalized[i] / 100 * option["scenarios"][i]["score"]
            for i in range(len(option["scenarios"]))
        )
        results.append({
            "name": option["name"],
            "score": weighted,
            "normalized": normalized,
            "scenarios": option["scenarios"],
        })
    return results

with st.container():
    cols = st.columns(3)
    for i, option in enumerate(st.session_state.options):
        with cols[i]:
            st.subheader(option["name"])

            for j, scenario in enumerate(option["scenarios"]):
                st.write(f"{j+1}. {scenario['name']}")
                scenario["probability"] = st.slider(
                    f"Вероятность для {scenario['name']}",
                    min_value=0,
                    max_value=100,
                    value=int(scenario["probability"]),
                    key=f"{option['name']}_{scenario['name']}_prob"
                )
                scenario["score"] = st.number_input(
                    f"Оценка для {scenario['name']}",
                    min_value=-5,
                    max_value=5,
                    value=float(scenario["score"]),
                    step=0.5,
                    key=f"{option['name']}_{scenario['name']}_score"
                )

# Кнопка расчёта
if st.button("Рассчитать и показать дерево"):
    results = calc_scores(st.session_state.options)
    best = max(results, key=lambda x: x["score"])
    st.success(f"Лидирует: {best['name']}")

    # Таблица итогов
    st.subheader("Итоги")
    for r in results:
        st.write(f"- **{r['name']}**: {r['score']:.2f}")

    # --- Рисуем дерево ---
    fig = go.Figure()

    root_x = 0
    root_y = 0

    option_positions = {
        "Вариант 1 — Учиться": -2,
        "Вариант 2 — Отдыхать": 0,
        "Вариант 3 — Сочетать учёбу и отдых": 2,
    }

    scenario_positions = {
        "Вариант 1 — Учиться": [-3, 0, 3],
        "Вариант 2 — Отдыхать": [-3, 0, 3],
        "Вариант 3 — Сочетать учёбу и отдых": [-3, 0, 3],
    }

    # Корень
    fig.add_trace(go.Scatter(
        x=[root_x], y=[root_y],
        mode="markers+text",
        marker=dict(size=22, color="#F5C08D"),
        text=[question],
        textposition="top center",
        showlegend=False
    ))

    # Варианты
    for result in results:
        option_name = result["name"]
        option_x = option_positions.get(option_name, 0)
        option_y = 1
        fig.add_trace(go.Scatter(
            x=[root_x, option_x],
            y=[root_y, option_y],
            mode="lines",
            line=dict(color="#7FB3D5", width=2),
            showlegend=False
        ))

        fig.add_trace(go.Scatter(
            x=[option_x], y=[option_y],
            mode="markers+text",
            marker=dict(size=18, color="#7FB3D5"),
            text=[f"{option_name}<br>{result['score']:.2f}"],
            textposition="top center",
            showlegend=False
        ))

        for idx, scenario in enumerate(result["scenarios"]):
            scenario_x = option_x + (2 if option_x >= 0 else -2)
            scenario_y = option_y + (idx - 1) * 1.3

            fig.add_trace(go.Scatter(
                x=[option_x, scenario_x],
                y=[option_y, scenario_y],
                mode="lines",
                line=dict(color="#82C9A5", width=1.5),
                showlegend=False
            ))

            fig.add_trace(go.Scatter(
                x=[scenario_x], y=[scenario_y],
                mode="markers+text",
                marker=dict(size=13, color="#82C9A5"),
                text=[f"{scenario['name']}<br>{scenario['probability']}%"],
                textposition="top center",
                showlegend=False
            ))

    fig.update_layout(
        template="plotly_white",
        width=1200,
        height=650,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        paper_bgcolor="#f5f7fb",
        plot_bgcolor="#f5f7fb",
        font=dict(size=12)
    )

    st.plotly_chart(fig, use_container_width=True)
