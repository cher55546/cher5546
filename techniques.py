"""Interactive technique worksheets and visual exports for the Streamlit app."""

import html
import streamlit as st
import streamlit.components.v1 as components


COLORS = {
    "ink": "#234D6B",
    "text": "#476B85",
    "line": "#80AFCB",
    "border": "#B9D9EB",
    "panel": "#F7FBFF",
    "pale": "#E7F3FB",
    "white": "#FFFFFF",
    "accent": "#D9EEFA",
}


def esc(value):
    return html.escape(str(value or "—"), quote=True)


def svg_lines(value, limit=34, max_lines=4):
    """Return escaped, word-wrapped SVG tspans for user-provided text."""
    text = " ".join(str(value or "—").split())
    words = text.split()
    lines, line = [], ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if len(candidate) > limit and line:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][:max(1, limit - 1)] + "…"
    return "".join(
        f'<tspan x="{{x}}" dy="{0 if i == 0 else 18}">{esc(line)}</tspan>'
        for i, line in enumerate(lines)
    )


def text_element(x, y, value, *, size=14, weight=400, color=None, limit=34, max_lines=4):
    color = color or COLORS["text"]
    tspans = svg_lines(value, limit=limit, max_lines=max_lines).replace("{x}", str(x))
    return (
        f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{color}">{tspans}</text>'
    )


def svg_document(width, height, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
      <rect width="100%" height="100%" fill="{COLORS["panel"]}"/>
      {text_element(32, 42, title, size=24, weight=700, color=COLORS["ink"], limit=75, max_lines=1)}
      <g id="scene">{body}</g>
    </svg>'''


def render_visualization(svg, filename, caption):
    """Display a pannable/zoomable SVG with SVG and PNG export controls."""
    st.subheader("Визуализация")
    st.caption(caption)
    # SVG is built only by this module; every user-provided value is XML-escaped.
    html_doc = f'''<!doctype html><html><head><meta charset="utf-8"><style>
      * {{ box-sizing: border-box; }} body {{ margin: 0; font: 14px Arial,sans-serif; color: #234D6B; }}
      .toolbar {{ display:flex; gap:8px; align-items:center; flex-wrap:wrap; padding:8px; background:#F3F9FD; border:1px solid #D4E6F2; border-radius:12px 12px 0 0; }}
      button {{ border:1px solid #AFCFE2; border-radius:8px; background:white; color:#315773; padding:7px 11px; cursor:pointer; font-weight:600; }}
      #zoom-label {{ min-width:48px; text-align:center; }}
      .viewport {{ height:520px; overflow:auto; border:1px solid #D4E6F2; border-top:0; border-radius:0 0 12px 12px; background:white; touch-action:none; }}
      svg {{ display:block; width:100%; height:100%; min-width:720px; }}
      @media (max-width: 700px) {{ .viewport {{ height:430px; }} }}
    </style></head><body>
      <div class="toolbar">
        <button id="minus" type="button" aria-label="Уменьшить">−</button>
        <button id="plus" type="button" aria-label="Увеличить">+</button>
        <button id="reset" type="button">Сбросить вид</button>
        <span id="zoom-label">100%</span>
        <button id="save-svg" type="button">Скачать SVG</button>
        <button id="save-png" type="button">Скачать PNG</button>
      </div>
      <div class="viewport" id="viewport">{svg}</div>
      <script>
        (() => {{
          const svg = document.querySelector('#viewport svg');
          const scene = svg && svg.querySelector('#scene');
          const label = document.getElementById('zoom-label');
          if (!svg || !scene) return;
          let scale = 1, tx = 0, ty = 0, drag = null;
          const update = () => {{ scene.setAttribute('transform', `translate(${{tx}} ${{ty}}) scale(${{scale}})`); label.textContent = `${{Math.round(scale*100)}}%`; }};
          document.getElementById('plus').onclick = () => {{ scale = Math.min(4, scale * 1.2); update(); }};
          document.getElementById('minus').onclick = () => {{ scale = Math.max(.4, scale / 1.2); update(); }};
          document.getElementById('reset').onclick = () => {{ scale = 1; tx = 0; ty = 0; update(); }};
          svg.addEventListener('wheel', (event) => {{ event.preventDefault(); scale = Math.max(.4, Math.min(4, scale * (event.deltaY < 0 ? 1.1 : .9))); update(); }}, {{passive:false}});
          svg.addEventListener('pointerdown', (event) => {{ if (event.target.closest('button')) return; drag = {{x:event.clientX-tx, y:event.clientY-ty}}; svg.setPointerCapture(event.pointerId); }});
          svg.addEventListener('pointermove', (event) => {{ if (!drag) return; tx = event.clientX-drag.x; ty = event.clientY-drag.y; update(); }});
          svg.addEventListener('pointerup', () => drag = null);
          svg.addEventListener('pointercancel', () => drag = null);
          const serialized = () => {{
            const clone = svg.cloneNode(true);
            clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
            return new XMLSerializer().serializeToString(clone);
          }};
          const save = (blob, name) => {{ const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=name; a.click(); setTimeout(()=>URL.revokeObjectURL(a.href),1000); }};
          document.getElementById('save-svg').onclick = () => save(new Blob([serialized()], {{type:'image/svg+xml;charset=utf-8'}}), {filename!r});
          document.getElementById('save-png').onclick = () => {{
            const source = serialized(); const blob = new Blob([source], {{type:'image/svg+xml;charset=utf-8'}}); const url = URL.createObjectURL(blob); const image = new Image();
            image.onload = () => {{ const canvas=document.createElement('canvas'); canvas.width=svg.viewBox.baseVal.width*2; canvas.height=svg.viewBox.baseVal.height*2; const ctx=canvas.getContext('2d'); ctx.fillStyle='#F7FBFF'; ctx.fillRect(0,0,canvas.width,canvas.height); ctx.drawImage(image,0,0,canvas.width,canvas.height); canvas.toBlob(png=>{{if(png) save(png,{filename.replace('.svg', '.png')!r}); URL.revokeObjectURL(url);}},'image/png'); }};
            image.onerror = () => URL.revokeObjectURL(url); image.src=url;
          }};
        }})();
      </script></body></html>'''
    components.html(html_doc, height=590, scrolling=False)


def remember_result(key, payload):
    st.session_state[key] = payload


def render_decision_tree():
    st.title("Дерево решений")
    st.write("Для каждого ва��ианта опишите возможные сценарии, оцените их вероятность и удовлетворённость исходом.")
    st.caption("Вероятности сценариев внутри одного варианта должны в сумме составлять 100%. Оценка — ваша субъективная удовлетворённость от −5 до +5.")
    question = st.text_input("Какое решение нужно принять?", key="decision_question", placeholder="Например: Стоит ли менять работу?")
    option_count = int(st.number_input("Количество вариантов", min_value=2, max_value=5, value=2, step=1, key="decision_option_count"))
    options = []
    for oi in range(option_count):
        with st.container(border=True):
            st.markdown(f"### Вариант {oi + 1}")
            name = st.text_input("Название варианта", key=f"decision_name_{oi}", placeholder=f"Вариант {oi + 1}")
            count = int(st.number_input("Количество сценариев", min_value=2, max_value=6, value=2, step=1, key=f"decision_scenario_count_{oi}"))
            scenarios = []
            for si in range(count):
                with st.expander(f"Сценарий {si + 1}", expanded=(si == 0)):
                    title = st.text_input("Название сценария", key=f"decision_scenario_title_{oi}_{si}", placeholder="Например: адаптация проходит успешно")
                    outcome = st.text_area("Возможные последствия", key=f"decision_scenario_outcome_{oi}_{si}")
                    probability = st.slider("Вероятность, %", 0, 100, 100 // count, key=f"decision_scenario_probability_{oi}_{si}")
                    satisfaction = st.slider("Удовлетворённость исходом", -5.0, 5.0, 0.0, 0.5, key=f"decision_scenario_satisfaction_{oi}_{si}")
                    scenarios.append({"title": title, "outcome": outcome, "probability": probability, "satisfaction": satisfaction})
            options.append({"name": name, "scenarios": scenarios})

    if st.button("Сформировать дерево и сравнить", key="decision_calculate", type="primary", use_container_width=True):
        errors = []
        if not question.strip():
            errors.append("Сформулируйте решение.")
        if any(not option["name"].strip() for option in options):
            errors.append("Укажите название каждого варианта.")
        for oi, option in enumerate(options, 1):
            total = sum(s["probability"] for s in option["scenarios"])
            if any(not s["title"].strip() for s in option["scenarios"]):
                errors.append(f"Заполните названия сценариев варианта {oi}.")
            if total != 100:
                errors.append(f"Вероятности сценариев варианта {oi} составляют {total}%, а должны составлять 100%.")
        if errors:
            for error in errors:
                st.warning(error)
            st.session_state.pop("result_decision_tree", None)
        else:
            prepared = []
            for option in options:
                expected = sum(s["probability"] * s["satisfaction"] for s in option["scenarios"]) / 100
                prepared.append({**option, "expected": expected})
            remember_result("result_decision_tree", {"question": question, "options": prepared})

    result = st.session_state.get("result_decision_tree")
    if result:
        options = result["options"]
        best = max(options, key=lambda x: x["expected"])
        st.subheader("Ожидаемая удовлетворённость (для обсуждения)")
        cols = st.columns(len(options))
        for col, option in zip(cols, options):
            with col:
                st.metric(option["name"], f'{option["expected"]:.2f} / 5')
                st.caption("Лидер по введённым оценкам" if option is best else "")
        width, col_w, row_h = 440, 400, 118
        height = 130 + max(len(o["scenarios"]) for o in options) * row_h
        body = f'<text x="32" y="82" font-family="Arial" font-size="16" fill="{COLORS["text"]}">{esc(result["question"])}</text>'
        root_x, root_y = 32, 108
        body += f'<rect x="{root_x}" y="{root_y}" width="{col_w}" height="62" rx="14" fill="{COLORS["accent"]}" stroke="{COLORS["line"]}"/>'
        body += text_element(root_x + 16, root_y + 27, "Решение", size=17, weight=700, color=COLORS["ink"], limit=42, max_lines=1)
        body += text_element(root_x + 16, root_y + 49, result["question"], size=13, limit=53, max_lines=1)
        for oi, option in enumerate(options):
            x = 520 + oi * width
            opt_y = 108
            body += f'<line x1="{root_x + col_w}" y1="{root_y + 31}" x2="{x}" y2="{opt_y + 32}" stroke="{COLORS["line"]}" stroke-width="2"/>'
            body += f'<rect x="{x}" y="{opt_y}" width="{col_w}" height="64" rx="14" fill="{COLORS["pale"]}" stroke="{COLORS["line"]}"/>'
            body += text_element(x + 14, opt_y + 25, option["name"], size=16, weight=700, color=COLORS["ink"], limit=44, max_lines=1)
            body += text_element(x + 14, opt_y + 48, f'Ожидаемая удовлетворённость: {option["expected"]:.2f}', size=12, limit=48, max_lines=1)
            for si, scenario in enumerate(option["scenarios"]):
                sy = 198 + si * row_h
                body += f'<line x1="{x + 30}" y1="{opt_y + 64}" x2="{x + 30}" y2="{sy}" stroke="{COLORS["line"]}" stroke-width="2"/>'
                body += f'<rect x="{x + 48}" y="{sy}" width="{col_w - 48}" height="100" rx="12" fill="{COLORS["white"]}" stroke="{COLORS["border"]}"/>'
                body += text_element(x + 62, sy + 23, scenario["title"], size=14, weight=700, color=COLORS["ink"], limit=41, max_lines=1)
                body += text_element(x + 62, sy + 45, f'Вероятность {scenario["probability"]}% · удовлетворённость {scenario["satisfaction"]:+.1f}', size=12, limit=42, max_lines=1)
                body += text_element(x + 62, sy + 68, scenario["outcome"], size=12, limit=42, max_lines=2)
        svg = svg_document(520 + len(options) * width, height, "Дерево решений", body)
        render_visualization(svg, "decision_tree.svg", "Сценарии показаны внутри каждого варианта; ожидаемая оценка рассчитана по взвешенной сумме вероятностей.")
        st.info("Оценка не выбирает решение за вас: используйте её как основу для обсуждения предпочтений, ценностей и неопределённости.")


def render_chain():
    st.title("Цепочный анализ поведения (ДБТ)")
    st.write("Последовательно восстановите событие, звенья цепочки, последствия и точки для решения/профилактики.")
    st.info("Можно пропустить поле или остановиться. Если речь идёт о непосредственной опасности для вас или другого человека, обратитесь за срочной помощью к местным службам или специалисту.")
    vulnerability = st.text_area("Факторы уязвимости", key="chain_vulnerability", placeholder="Например: недосып, стресс, боль, конфликт")
    trigger = st.text_area("Провоцирующее событие", key="chain_trigger", placeholder="Последнее событие, запустившее последовательность")
    target = st.text_area("Проблемное / целевое поведение", key="chain_target", placeholder="Конкретно: что произошло, без оценочных ярлыков")
    count = int(st.number_input("Количество звеньев", min_value=1, max_value=8, value=4, step=1, key="chain_link_count"))
    links = []
    for i in range(count):
        with st.expander(f"Звено {i + 1}: что произошло дальше?", expanded=(i < 2)):
            cols = st.columns(2)
            with cols[0]:
                thought = st.text_area("Мысль / интерпретация", key=f"chain_thought_{i}")
                emotion = st.text_input("Эмоция", key=f"chain_emotion_{i}")
                urge = st.text_input("Побуждение / импульс", key=f"chain_urge_{i}")
            with cols[1]:
                body = st.text_input("Телесные ощущения", key=f"chain_body_{i}")
                action = st.text_area("Действие / следующий шаг", key=f"chain_action_{i}")
                intervention = st.text_area("Что могло бы помочь именно здесь?", key=f"chain_intervention_{i}")
            skill = st.text_input("Навык или поддержка для этой точки", key=f"chain_skill_{i}", placeholder="Например: пауза, заземление, обратиться за поддержкой")
            links.append({"thought": thought, "emotion": emotion, "urge": urge, "body": body, "action": action, "intervention": intervention, "skill": skill})
    c1, c2 = st.columns(2)
    with c1:
        immediate = st.text_area("Последствия сразу после (для себя / других)", key="chain_immediate")
        immediate_positive = st.text_area("Что могло подкрепить поведение сразу?", key="chain_immediate_positive")
    with c2:
        later = st.text_area("Отсроченные последствия", key="chain_later")
        later_positive = st.text_area("Отсроченные последствия, которые поддерживают повторение", key="chain_later_positive")
    prevention = st.text_area("План профилактики на будущее", key="chain_prevention", placeholder="Какие уязвимости можно уменьшить? Что подготовить заранее?")
    repair = st.text_area("Восстановление / исправление последствий (если необходимо)", key="chain_repair")

    if st.button("Сформировать карту цепочки", key="chain_build", type="primary", use_container_width=True):
        if not target.strip():
            st.warning("Опишите поведение, которое анализируете, чтобы собрать цепочку.")
            st.session_state.pop("result_dbt_chain", None)
        else:
            remember_result("result_dbt_chain", {"vulnerability": vulnerability, "trigger": trigger, "target": target, "links": links, "immediate": immediate, "immediate_positive": immediate_positive, "later": later, "later_positive": later_positive, "prevention": prevention, "repair": repair})

    result = st.session_state.get("result_dbt_chain")
    if result:
        st.subheader("Сводка и анализ решений")
        for title, value in [("Уязвимости", result["vulnerability"]), ("Провоцирующее событие", result["trigger"]), ("Проблемное поведение", result["target"]), ("Непосредственные последствия", result["immediate"]), ("Что подкрепляло поведение", result["immediate_positive"]), ("Отсроченные последствия", result["later"]), ("План профилактики", result["prevention"]), ("Восстановление", result["repair"])]:
            st.markdown(f"**{title}:** {value or '—'}")
        for i, link in enumerate(result["links"], 1):
            with st.expander(f"Звено {i}", expanded=False):
                st.write(f'Мысль: {link["thought"] or "—"} · Эмоция: {link["emotion"] or "—"} · Импульс: {link["urge"] or "—"} · Ощущения: {link["body"] or "—"}')
                st.write(f'Действие: {link["action"] or "—"}')
                st.write(f'Точка вмешательства: {link["intervention"] or "—"} · Навык/поддержка: {link["skill"] or "—"}')
        width, row_h = 1180, 150
        height = 180 + len(result["links"]) * row_h + 210
        body = ""
        boxes = [("Факторы уязвимости", result["vulnerability"]), ("Провоцирующее событие", result["trigger"])]
        for i, (label, value) in enumerate(boxes):
            x, y = 40, 88 + i * 76
            body += f'<rect x="{x}" y="{y}" width="{width - 80}" height="58" rx="12" fill="{COLORS["pale"]}" stroke="{COLORS["line"]}"/>'
            body += text_element(x + 14, y + 23, label, size=13, weight=700, color=COLORS["ink"], limit=36, max_lines=1)
            body += text_element(x + 250, y + 23, value, size=13, limit=92, max_lines=2)
        previous_y = 240
        for i, link in enumerate(result["links"]):
            y = 240 + i * row_h
            body += f'<line x1="590" y1="{previous_y + (58 if i == 0 else 100)}" x2="590" y2="{y}" stroke="{COLORS["line"]}" stroke-width="2"/>' if i == 0 else ""
            body += f'<rect x="40" y="{y}" width="{width - 80}" height="120" rx="14" fill="{COLORS["white"]}" stroke="{COLORS["border"]}"/>'
            body += text_element(58, y + 24, f'Звено {i + 1}', size=14, weight=700, color=COLORS["ink"], limit=20, max_lines=1)
            body += text_element(200, y + 24, f'Мысль: {link["thought"]} · Эмоция: {link["emotion"]} · Импульс: {link["urge"]}', size=12, limit=115, max_lines=2)
            body += text_element(200, y + 62, f'Ощущения: {link["body"]} · Действие: {link["action"]}', size=12, limit=115, max_lines=2)
            body += text_element(200, y + 98, f'Точка вмешательства: {link["intervention"]} · Навык: {link["skill"]}', size=12, limit=115, max_lines=2)
            if i < len(result["links"]) - 1:
                body += f'<line x1="590" y1="{y + 120}" x2="590" y2="{y + row_h}" stroke="{COLORS["line"]}" stroke-width="2"/>'
        end_y = 240 + len(result["links"]) * row_h
        for i, (label, value) in enumerate([("Последствия сразу", result["immediate"]), ("Отсроченные последствия", result["later"]), ("Профилактика / восстановление", f'{result["prevention"]} · {result["repair"]}')]):
            y = end_y + i * 58
            body += f'<rect x="40" y="{y}" width="{width - 80}" height="48" rx="10" fill="{COLORS["accent"]}" stroke="{COLORS["line"]}"/>'
            body += text_element(55, y + 19, label, size=12, weight=700, color=COLORS["ink"], limit=35, max_lines=1)
            body += text_element(290, y + 19, value, size=12, limit=100, max_lines=1)
        svg = svg_document(width, height, "ДБТ · анализ цепочки и решений", body)
        render_visualization(svg, "dbt_chain.svg", "Карта показывает уязвимости, запускающее событие, последовательные звенья, последствия и возможные места для навыков/поддержки.")


def render_exposure():
    st.title("Иерархия экспозиции")
    st.write("Составьте добровольную лестницу практики и фиксируйте прогнозы, опыт и то, что удалось узнать.")
    st.info("Практикуйте только добровольно и в безопасных ситуациях; не используйте экспозицию для реальной опасности. Не обязательно ждать, пока тревога исчезнет: важны безопасный опыт и проверка прогнозов. План согласуйте со специалистом, если это необходимо.")
    goal = st.text_area("Цель / ситуация, с которой хотите работать", key="exposure_goal")
    count = int(st.number_input("Количество ступеней", min_value=1, max_value=10, value=3, step=1, key="exposure_count"))
    steps = []
    for i in range(count):
        with st.expander(f"Ступень {i + 1}", expanded=(i < 2)):
            situation = st.text_input("Ситуация / упражнение", key=f"exposure_situation_{i}")
            cols = st.columns(2)
            with cols[0]:
                expected = st.slider("Ожидаемая тревога (0–10)", 0, 10, 3, key=f"exposure_distress_{i}")
                prediction = st.text_area("Прогноз / чего опасаетесь?", key=f"exposure_prediction_{i}")
                plan = st.text_area("Посильный план практики", key=f"exposure_plan_{i}")
            with cols[1]:
                practiced = st.checkbox("Практика выполнена", key=f"exposure_practiced_{i}")
                start = st.slider("Тревога в начале (0–10)", 0, 10, 0, key=f"exposure_start_{i}")
                peak = st.slider("Максимальная тревога (0–10)", 0, 10, 0, key=f"exposure_peak_{i}")
                after = st.slider("Тревога после практики (0–10)", 0, 10, 0, key=f"exposure_after_{i}")
                outcome = st.text_area("Что произошло на самом деле?", key=f"exposure_outcome_{i}")
                learning = st.text_area("Что вы узнали / что попробовать дальше?", key=f"exposure_learning_{i}")
            steps.append({"situation": situation, "expected": expected, "prediction": prediction, "plan": plan, "practiced": practiced, "start": start, "peak": peak, "after": after, "outcome": outcome, "learning": learning})

    if st.button("Сформировать лестницу", key="exposure_build", type="primary", use_container_width=True):
        completed = [s for s in steps if s["situation"].strip()]
        if not completed:
            st.warning("Добавьте описание хотя бы одной ступени.")
            st.session_state.pop("result_exposure", None)
        else:
            remember_result("result_exposure", {"goal": goal, "steps": sorted(completed, key=lambda s: s["expected"])})

    result = st.session_state.get("result_exposure")
    if result:
        st.subheader("Лестница от меньшей ожидаемой тревоги к большей")
        for i, step in enumerate(result["steps"], 1):
            with st.container(border=True):
                st.markdown(f'**{i}. {step["situation"]}** · ожидаемая тревога {step["expected"]}/10')
                if step["prediction"]: st.write(f'Прогноз: {step["prediction"]}')
                if step["plan"]: st.write(f'План: {step["plan"]}')
                if step["practiced"]:
                    st.write(f'Практика: тревога в начале {step["start"]}/10, максимум {step["peak"]}/10, после {step["after"]}/10.')
                    if step["outcome"]: st.write(f'Наблюдаемый исход: {step["outcome"]}')
                    if step["learning"]: st.write(f'Вывод / следующий шаг: {step["learning"]}')
        width, row_h = 1100, 110
        height = 120 + len(result["steps"]) * row_h
        body = text_element(32, 78, f'Цель: {result["goal"]}', size=14, limit=100, max_lines=1)
        for i, step in enumerate(result["steps"]):
            x, y = 45, 98 + i * row_h
            bar_width = 180 + step["expected"] * 55
            body += f'<rect x="{x}" y="{y}" width="{bar_width}" height="72" rx="12" fill="{COLORS["accent"]}" stroke="{COLORS["line"]}"/>'
            body += text_element(x + 12, y + 23, f'{i + 1}. {step["situation"]}', size=13, weight=700, color=COLORS["ink"], limit=36, max_lines=1)
            body += text_element(x + 12, y + 48, f'Ожидаемая тревога: {step["expected"]}/10', size=12, limit=35, max_lines=1)
            if step["practiced"]:
                gx = 600
                body += text_element(gx, y + 22, f'Фактические оценки · начало {step["start"]} / пик {step["peak"]} / после {step["after"]}', size=12, limit=68, max_lines=1)
                body += text_element(gx, y + 49, f'Наблюдение: {step["outcome"] or step["learning"] or "пока не записано"}', size=12, limit=68, max_lines=1)
            if i < len(result["steps"]) - 1:
                body += f'<line x1="{x + 26}" y1="{y + 72}" x2="{x + 26}" y2="{y + row_h}" stroke="{COLORS["line"]}" stroke-width="2"/>'
        svg = svg_document(width, height, "Иерархия экспозиции", body)
        render_visualization(svg, "exposure_hierarchy.svg", "Ступени упорядочены по субъективной ожидаемой тревоге. После практики отображаются фактические оценки и наблюдения.")


def render_act_matrix():
    st.title("ACT-матрица")
    st.write("Заметьте внутренний и внешний опыт, движения от дискомфорта и действия в сторону того, что важно.")
    st.info("Матрица — не оценка поведения, а способ исследовать выбор и психологическую гибкость. Записывайте пункты через новую строку.")
    situation = st.text_area("Ситуация / контекст", key="act_situation")
    values = st.text_area("Люди и ценности, которые важны", key="act_values", placeholder="Например: близкие отношения, забота, обучение")
    col1, col2 = st.columns(2)
    with col1:
        external = st.text_area("Внешний опыт (что замечаете пятью чувствами?)", key="act_external", placeholder="События вокруг, что можно увидеть или услышать")
        inner = st.text_area("Внутренний опыт (что замечает ум/тело?)", key="act_inner", placeholder="Мысли, чувства, воспоминания, импульсы, телесные ощущения")
    with col2:
        away = st.text_area("Действия от дискомфорта (что делаете, чтобы уйти от неприятного?)", key="act_away")
        toward = st.text_area("Действия к важному (что помогает приближаться к ценностям?)", key="act_toward")
    step = st.text_area("Один небольшой выбранный шаг к важному", key="act_step")

    if st.button("Сформировать ACT-матрицу", key="act_build", type="primary", use_container_width=True):
        if not situation.strip():
            st.warning("Добавьте ситуацию, которую исследуете.")
            st.session_state.pop("result_act_matrix", None)
        else:
            remember_result("result_act_matrix", {"situation": situation, "values": values, "external": external, "inner": inner, "away": away, "toward": toward, "step": step})
    result = st.session_state.get("result_act_matrix")
    if result:
        st.subheader("Сводка")
        st.write(f'**Ситуация:** {result["situation"]}')
        st.write(f'**Что важно:** {result["values"] or "—"}')
        st.write(f'**Выбранный шаг:** {result["step"] or "—"}')
        width, height, mid_x, mid_y = 1120, 760, 560, 390
        left, right, top, bottom = 55, 1065, 120, 650
        box_w, box_h = 490, 245
        quadrants = [
            (left, top, "ВНЕШНИЙ ОПЫТ · ПЯТЬ ЧУВСТВ", result["external"]),
            (mid_x + 15, top, "ДЕЙСТВИЯ К ВАЖНОМУ", result["toward"]),
            (left, mid_y + 15, "ВНУТРЕННИЙ ОПЫТ · УМ/ТЕЛО", result["inner"]),
            (mid_x + 15, mid_y + 15, "ДЕЙСТВИЯ ОТ ДИСКОМФОРТА", result["away"]),
        ]
        body = ""
        for x, y, label, value in quadrants:
            body += f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="16" fill="{COLORS["white"]}" stroke="{COLORS["line"]}" stroke-width="2"/>'
            body += text_element(x + 18, y + 30, label, size=14, weight=700, color=COLORS["ink"], limit=52, max_lines=1)
            for idx, item in enumerate([v.strip() for v in (value or "").splitlines() if v.strip()][:7]):
                body += f'<circle cx="{x + 25}" cy="{y + 67 + idx * 25}" r="4" fill="{COLORS["line"]}"/>'
                body += text_element(x + 38, y + 72 + idx * 25, item, size=13, limit=53, max_lines=1)
            if not value.strip():
                body += text_element(x + 18, y + 68, "—", size=13, limit=53, max_lines=1)
        body += f'<line x1="{mid_x}" y1="{top - 12}" x2="{mid_x}" y2="{bottom + 8}" stroke="{COLORS["ink"]}" stroke-width="3"/>'
        body += f'<line x1="{left - 8}" y1="{mid_y}" x2="{right + 8}" y2="{mid_y}" stroke="{COLORS["ink"]}" stroke-width="3"/>'
        body += text_element(45, 82, f'Контекст: {result["situation"]}', size=14, weight=600, color=COLORS["text"], limit=100, max_lines=1)
        body += text_element(45, 708, f'Ценности / люди: {result["values"] or "—"} · Небольшой шаг: {result["step"] or "—"}', size=13, limit=118, max_lines=2)
        svg = svg_document(width, height, "ACT-матрица · замечать и выбирать", body)
        render_visualization(svg, "act_matrix.svg", "В матрице четыре области: внешний опыт, внутренний опыт, действия к важному и действия от дискомфорта.")


def render_selected_technique(technique_id):
    renderers = {
        "decision_tree": render_decision_tree,
        "dbt_chain": render_chain,
        "exposure": render_exposure,
        "act_matrix": render_act_matrix,
    }
    renderer = renderers.get(technique_id)
    if renderer:
        renderer()
    else:
        st.warning("Техника не найдена.")
