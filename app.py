import html
import textwrap
import uuid
from pathlib import Path
from urllib.parse import quote

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="ПСИ-БЛОК",
    page_icon="favicon.png"
    layout="wide",
)


# ---------------------------------------------------------------------
# Фон сайта: нейронные связи
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
  <g fill="#4389B5" fill-opacity="0.17" stroke="#FFFFFF" stroke-opacity="0.8" stroke-width="3">
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


# ---------------------------------------------------------------------
# Light theme for all inputs and cards
# ---------------------------------------------------------------------

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700;800&display=swap');

    :root {{
        color-scheme: light !important;
    }}

    html, body, [data-testid="stAppViewContainer"] {{
        color-scheme: light !important;
        background-color: #F3F9FD !important;
        color: #294A65 !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background-image:
            radial-gradient(ellipse at 10% 5%, rgba(196,228,248,.58), transparent 34%),
            radial-gradient(ellipse at 92% 18%, rgba(219,239,251,.68), transparent 36%);
    }}

    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        opacity: .56;
        background-image: url("data:image/svg+xml,{quote(NEURON_SVG, safe='')}");
        background-repeat: repeat;
        background-size: 1000px 800px;
        background-position: left top;
    }}

    [data-testid="stAppViewContainer"] > .main {{
        position: relative;
        z-index: 1;
    }}

    [data-testid="stHeader"] {{
        background: transparent !important;
    }}

    .block-container {{
        max-width: 1120px;
        padding-top: 1.2rem;
        padding-bottom: 4rem;
    }}

    h1, h2, h3, h4, p, label, button, input, textarea, select {{
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }}

    h1, h2, h3, h4 {{
        color: #294A65 !important;
        letter-spacing: -0.025em;
    }}

    h1 {{ font-size: 2.6rem !important; font-weight: 800 !important; }}
    h2 {{ font-size: 1.85rem !important; font-weight: 800 !important; }}
    h3 {{ font-size: 1.3rem !important; font-weight: 800 !important; }}

    p, label, [data-testid="stCaptionContainer"],
    [data-testid="stMarkdownContainer"] {{
        color: #476B85 !important;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        border: 1px solid #C9DFEF !important;
        border-radius: 20px !important;
        background: rgba(248,252,255,.96) !important;
        box-shadow: 0 10px 26px rgba(62,112,148,.08);
    }}

    [data-testid="stTextInput"] [data-baseweb="input"],
    [data-testid="stTextArea"] [data-baseweb="textarea"],
    [data-testid="stNumberInput"] [data-baseweb="input"],
    [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    [data-baseweb="input"],
    [data-baseweb="textarea"] {{
        color-scheme: light !important;
        background: #FFFFFF !important;
        border: 1px solid #C9DDEB !important;
        border-radius: 12px !important;
        box-shadow: none !important;
        outline: none !important;
    }}

    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] input,
    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea {{
        color: #294A65 !important;
        background: #FFFFFF !important;
        -webkit-text-fill-color: #294A65 !important;
        border: 0 !important;
        box-shadow: none !important;
        outline: none !important;
        caret-color: #315773 !important;
    }}

    [data-testid="stTextInput"] [data-baseweb="input"]:focus-within,
    [data-testid="stTextArea"] [data-baseweb="textarea"]:focus-within,
    [data-testid="stNumberInput"] [data-baseweb="input"]:focus-within,
    [data-baseweb="input"]:focus-within,
    [data-baseweb="textarea"]:focus-within {{
        border: 1px solid #6EA7CB !important;
        box-shadow: 0 0 0 3px rgba(110,167,203,.16) !important;
    }}

    input::placeholder,
    textarea::placeholder {{
        color: #7893A8 !important;
        -webkit-text-fill-color: #7893A8 !important;
        opacity: 1 !important;
    }}

    [data-baseweb="select"] span,
    [data-baseweb="menu"] li {{
        color: #294A65 !important;
    }}

    [data-baseweb="popover"],
    [data-baseweb="menu"] {{
        color-scheme: light !important;
        background: #FFFFFF !important;
    }}

    [data-testid="stCheckbox"] label,
    [data-testid="stRadio"] label {{
        color: #315773 !important;
    }}

    .stButton > button {{
        min-height: 46px;
        border: 1px solid #AFCFE2 !important;
        border-radius: 14px !important;
        background: #F1F8FD !important;
        color: #315773 !important;
        font-size: 1rem;
        font-weight: 700;
        transition: .18s ease;
    }}

    .stButton > button:hover:not(:disabled) {{
        border-color: #6EA7CB !important;
        background: #E0F0FA !important;
        color: #234D6B !important;
        transform: translateY(-1px);
    }}

    .stButton > button[kind="primary"] {{
        min-height: 56px;
        border: 1px solid #6EA7CB !important;
        border-radius: 16px !important;
        background: linear-gradient(135deg, #D9EEFA, #E5F3FC) !important;
        color: #234D6B !important;
        font-size: 1.08rem;
        font-weight: 800;
    }}

    [data-testid="stAlert"] {{
        border: 1px solid #BCD9EB !important;
        border-radius: 15px !important;
        background: #EAF5FC !important;
        color: #315773 !important;
    }}

    [data-testid="stAlert"] * {{
        color: #315773 !important;
    }}

    [data-testid="stMetric"] {{
        border: 1px solid #C9DFEF;
        border-radius: 17px;
        background: rgba(248,252,255,.96);
        padding: 14px;
    }}

    hr {{
        border-color: #C9DFEF !important;
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
# Навигация и каталог
# ---------------------------------------------------------------------

TECHNIQUES = {
    "decision_tree": {
        "title": "Дерево решений",
        "short": "Разложить сложный выбор на варианты и возможные последствия.",
        "description": "Сравнение вариантов, исходов, вероятностей и оценок.",
    },
    "dbt_chain": {
        "title": "Цепочный анализ поведения (ДБТ)",
        "short": "Исследовать последовательность событий, реакций и последствий.",
        "description": "Карта контекста, звеньев цепочки и возможных точек вмешательства.",
    },
    "exposure": {
        "title": "Иерархия экспозиции",
        "short": "Составить и обсудить лестницу ситуаций для постепенной практики.",
        "description": "Ситуации, прогнозы, посильные шаги и наблюдения.",
    },
    "act_matrix": {
        "title": "ACT-матрица",
        "short": "Исследовать действия «от дискомфорта» и шаги «к ценностям».",
        "description": "Визуальная карта внутреннего опыта, поведения и выбранных действий.",
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
        st.button("Главная", on_click=go_home, use_container_width=True)

    with library_col:
        st.button("Библиотека", on_click=go_library, use_container_width=True)


# ---------------------------------------------------------------------
# SVG helpers
# ---------------------------------------------------------------------

def svg_escape(value):
    return html.escape(str(value or ""), quote=True)


def svg_wrap(value, width=30, max_lines=5):
    value = str(value or "").strip()
    if not value:
        return ["—"]

    lines = []
    for paragraph in value.splitlines():
        wrapped = textwrap.wrap(paragraph, width=width) or [""]
        lines.extend(wrapped)

    return lines[:max_lines] or ["—"]


def svg_text(value, x, y, width=30, font_size=16,
             fill="#294A65", max_lines=5, line_height=None):
    lines = svg_wrap(value, width, max_lines)
    line_height = line_height or int(font_size * 1.35)
    spans = []

    for i, line in enumerate(lines):
        dy = 0 if i == 0 else line_height
        spans.append(f'<tspan x="{x}" dy="{dy}">{svg_escape(line)}</tspan>')

    return (
        f'<text x="{x}" y="{y}" text-anchor="middle" '
        f'font-family="Arial, sans-serif" font-size="{font_size}" '
        f'fill="{fill}">{"".join(spans)}</text>'
    )


def svg_card(x, y, width, height, title, body,
             fill="#F8FCFF", stroke="#AFCFE2"):
    max_chars = max(15, int(width / 12))
    return f"""
    <rect x="{x}" y="{y}" width="{width}" height="{height}"
          rx="20" fill="{fill}" stroke="{stroke}" stroke-width="3"/>
    {svg_text(title, x + width / 2, y + 32, max_chars, 17, "#294A65", 2)}
    {svg_text(body, x + width / 2, y + 62, max_chars, 14, "#476B85", 5)}
    """


def svg_document(title, content, width, height):
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         width="{width}" height="{height}"
         viewBox="0 0 {width} {height}">
      <rect width="100%" height="100%" fill="#F5FAFE"/>
      <text x="{width / 2}" y="45" text-anchor="middle"
            font-family="Arial, sans-serif" font-size="29"
            font-weight="bold" fill="#294A65">
        {svg_escape(title)}
      </text>
      {content}
    </svg>
    """


def render_interactive_diagram(svg, key, height=740):
    safe_key = "".join(ch for ch in key if ch.isalnum() or ch == "_")
    svg_id = f"diagram_{safe_key}"
    diagram_svg = svg.replace("<svg ", f'<svg id="{svg_id}" ', 1)

    template = r"""
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        html, body {
          margin: 0;
          padding: 0;
          width: 100%;
          height: 100%;
          overflow: hidden;
          background: transparent;
          font-family: Arial, sans-serif;
        }
        .toolbar {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          align-items: center;
          padding: 6px 2px 10px;
        }
        .toolbar button {
          border: 1px solid #9FC5DE;
          border-radius: 10px;
          background: #EAF5FC;
          color: #294A65;
          padding: 8px 13px;
          font-weight: 700;
          cursor: pointer;
        }
        .toolbar button:hover {
          background: #D9EDF9;
        }
        .hint {
          color: #54718A;
          font-size: 13px;
          margin-left: 5px;
        }
        .viewport {
          width: 100%;
          height: calc(100% - 58px);
          overflow: hidden;
          border: 1px solid #BBD7E8;
          border-radius: 16px;
          background: #F5FAFE;
          cursor: grab;
          touch-action: none;
        }
        .viewport.dragging {
          cursor: grabbing;
        }
        #DIAGRAM_ID {
          display: block;
          width: 100%;
          height: 100%;
          user-select: none;
        }
      </style>
    </head>
    <body>
      <div class="toolbar">
        <button id="zoomIn">Увеличить</button>
        <button id="zoomOut">Уменьшить</button>
        <button id="reset">Сбросить вид</button>
        <button id="downloadPng">Скачать PNG</button>
        <span class="hint">Колесо мыши — масштаб; перетаскивание — перемещение</span>
      </div>
      <div class="viewport" id="viewport">DIAGRAM_SVG</div>

      <script>
        (() => {
          const svg = document.getElementById("DIAGRAM_ID");
          const viewport = document.getElementById("viewport");
          const vb = svg.viewBox.baseVal;
          const base = {x: vb.x, y: vb.y, width: vb.width, height: vb.height};
          const view = {...base};

          function applyView() {
            svg.setAttribute("viewBox", `${view.x} ${view.y} ${view.width} ${view.height}`);
          }

          function zoom(factor, clientX, clientY) {
            const rect = svg.getBoundingClientRect();
            const px = clientX === undefined ? rect.left + rect.width / 2 : clientX;
            const py = clientY === undefined ? rect.top + rect.height / 2 : clientY;
            const rx = (px - rect.left) / rect.width;
            const ry = (py - rect.top) / rect.height;
            const oldWidth = view.width;
            const oldHeight = view.height;

            view.width *= factor;
            view.height *= factor;
            view.x += (oldWidth - view.width) * rx;
            view.y += (oldHeight - view.height) * ry;
            applyView();
          }

          document.getElementById("zoomIn").onclick = () => zoom(0.8);
          document.getElementById("zoomOut").onclick = () => zoom(1.25);
          document.getElementById("reset").onclick = () => {
            Object.assign(view, base);
            applyView();
          };

          viewport.addEventListener("wheel", event => {
            event.preventDefault();
            zoom(event.deltaY < 0 ? 0.9 : 1.1, event.clientX, event.clientY);
          }, {passive: false});

          let dragging = false;
          let lastX = 0;
          let lastY = 0;

          viewport.addEventListener("pointerdown", event => {
            dragging = true;
            lastX = event.clientX;
            lastY = event.clientY;
            viewport.classList.add("dragging");
            viewport.setPointerCapture(event.pointerId);
          });

          viewport.addEventListener("pointermove", event => {
            if (!dragging) return;
            const rect = svg.getBoundingClientRect();
            view.x -= (event.clientX - lastX) * view.width / rect.width;
            view.y -= (event.clientY - lastY) * view.height / rect.height;
            lastX = event.clientX;
            lastY = event.clientY;
            applyView();
          });

          function stopDragging() {
            dragging = false;
            viewport.classList.remove("dragging");
          }

          viewport.addEventListener("pointerup", stopDragging);
          viewport.addEventListener("pointercancel", stopDragging);

          document.getElementById("downloadPng").onclick = () => {
            const clone = svg.cloneNode(true);
            clone.removeAttribute("id");
            clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
            clone.setAttribute("width", base.width);
            clone.setAttribute("height", base.height);
            clone.setAttribute("viewBox", `${base.x} ${base.y} ${base.width} ${base.height}`);

            const source = new XMLSerializer().serializeToString(clone);
            const blob = new Blob([source], {type: "image/svg+xml;charset=utf-8"});
            const url = URL.createObjectURL(blob);
            const image = new Image();

            image.onload = () => {
              const canvas = document.createElement("canvas");
              canvas.width = Math.round(base.width * 2);
              canvas.height = Math.round(base.height * 2);
              const ctx = canvas.getContext("2d");
              ctx.fillStyle = "#F5FAFE";
              ctx.fillRect(0, 0, canvas.width, canvas.height);
              ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
              URL.revokeObjectURL(url);

              canvas.toBlob(png => {
                if (!png) {
                  alert("Не удалось создать PNG. Попробуйте ещё раз.");
                  return;
                }
                const link = document.createElement("a");
                link.href = URL.createObjectURL(png);
                link.download = "PNG_FILENAME.png";
                document.body.appendChild(link);
                link.click();
                link.remove();
                setTimeout(() => URL.revokeObjectURL(link.href), 1500);
              }, "image/png");
            };

            image.onerror = () => {
              URL.revokeObjectURL(url);
              alert("Не удалось подготовить изображение для скачивания.");
            };

            image.src = url;
          };
        })();
      </script>
    </body>
    </html>
    """

    html_blob = (
        template
        .replace("DIAGRAM_ID", svg_id)
        .replace("DIAGRAM_SVG", diagram_svg)
        .replace("PNG_FILENAME", safe_key)
    )
    components.html(html_blob, height=height, scrolling=False)


def make_vertical_diagram(title, sections, note):
    width = 1100
    card_height = 120
    gap = 40
    top = 90
    height = max(540, top + len(sections) * (card_height + gap) + 70)
    content = []

    for i, (heading, body) in enumerate(sections):
        y = top + i * (card_height + gap)
        fill = "#E8F4FB" if i % 2 == 0 else "#F3F8FC"
        content.append(
            svg_card(115, y, 870, card_height, heading, body, fill, "#AFCFE2")
        )
        if i < len(sections) - 1:
            content.append(
                f'<line x1="550" y1="{y + card_height}" '
                f'x2="550" y2="{y + card_height + gap - 6}" '
                'stroke="#6EA7CB" stroke-width="4"/>'
            )
            content.append(
                f'<path d="M540 {y + card_height + gap - 15} '
                f'L550 {y + card_height + gap - 6} '
                f'L560 {y + card_height + gap - 15}" '
                'fill="none" stroke="#6EA7CB" stroke-width="4"/>'
            )

    content.append(
        f'<text x="550" y="{height - 20}" text-anchor="middle" '
        'font-family="Arial, sans-serif" font-size="13" fill="#54718A">'
        f'{svg_escape(note)}</text>'
    )
    return svg_document(title, "".join(content), width, height)


def make_decision_diagram(question, options):
    card_w = 290
    card_h = 150
    option_w = 300
    option_h = 120
    leaf_spacing = 330
    left_margin = 170
    top_y = 105
    option_y = 410
    root_y = 680
    root_w = 440
    root_h = 110
    root_x = 0

    # Рассчёт ширины в зависимости от количества исходов
    total_leaf_count = sum(len(option["scenarios"]) for option in options)
    total_leaf_count = max(total_leaf_count, 1)
    width = left_margin * 2 + (total_leaf_count - 1) * leaf_spacing + card_w
    root_x = width / 2
    height = 850

    colors = ["#6AAED0", "#65B99C", "#76A5D2", "#8BB7D8", "#5F9FC4"]
    content = []

    option_layout = []
    next_leaf_index = 0
    for option_index, option in enumerate(options):
        scenario_centers = [
            left_margin + card_w / 2 + (next_leaf_index + i) * leaf_spacing
            for i in range(len(option["scenarios"]))
        ]
        next_leaf_index += len(option["scenarios"])
        option_layout.append({
            "option": option,
            "color": colors[option_index % len(colors)],
            "scenario_centers": scenario_centers,
            "center_x": sum(scenario_centers) / len(scenario_centers),
        })

    # Линии от исходов к вариантам
    for entry in option_layout:
        for sx in entry["scenario_centers"]:
            content.append(
                f'<path d="M {sx} {top_y + card_h} '
                f'C {sx} 325, {entry["center_x"]} 330, {entry["center_x"]} {option_y}" '
                f'fill="none" stroke="{entry["color"]}" stroke-width="4"/>'
            )

    # Линии от вариантов к решению
    for entry in option_layout:
        content.append(
            f'<path d="M {entry["center_x"]} {option_y + option_h} '
            f'C {entry["center_x"]} 560, {root_x} 570, {root_x} {root_y}" '
            f'fill="none" stroke="{entry["color"]}" stroke-width="6"/>'
        )

    # Карточки исходов
    current_leaf_index = 0
    for entry in option_layout:
        option = entry["option"]
        for si, scenario in enumerate(option["scenarios"]):
            sx = left_margin + card_w / 2 + current_leaf_index * leaf_spacing
            current_leaf_index += 1
            body = (
                f"{scenario['name']}\n"
                f"{option['normalized'][si]:.1f}% · оценка {scenario['score']:g}"
            )
            content.append(
                svg_card(
                    sx - card_w / 2,
                    top_y,
                    card_w,
                    card_h,
                    f"Исход {si + 1}",
                    body,
                    "#FFFFFF",
                    entry["color"],
                )
            )

    # Карточки вариантов
    for entry in option_layout:
        content.append(
            svg_card(
                entry["center_x"] - option_w / 2,
                option_y,
                option_w,
                option_h,
                entry["option"]["name"],
                f"Итоговая оценка: {entry['option']['score']:.2f}",
                "#FFFFFF",
                entry["color"],
            )
        )

    # Карточка решения
    content.append(
        svg_card(
            root_x - root_w / 2,
            root_y,
            root_w,
            root_h,
            "Решение",
            question,
            "#E4F2FA",
            "#78A9C9",
        )
    )

    return svg_document("Дерево решений", "".join(content), int(width), height)


def make_act_diagram(situation, values, away, inner, toward, toward_inner, step):
    width, height = 1200, 900
    content = [
        svg_text(f"Ситуация: {situation or '—'}", 600, 85, 90, 16, "#476B85", 2),
        svg_text(f"Что важно: {values or '—'}", 600, 125, 90, 16, "#476B85", 2),
        '<line x1="600" y1="165" x2="600" y2="735" stroke="#8DB6D0" stroke-width="5"/>',
        '<line x1="70" y1="450" x2="1130" y2="450" stroke="#8DB6D0" stroke-width="5"/>',
        svg_card(85, 185, 480, 225, "Действия «от дискомфорта»", away, "#EAF5FC", "#8DB6D0"),
        svg_card(635, 185, 480, 225, "Действия «к важному»", toward, "#E4F3FA", "#78A9C9"),
        svg_card(85, 490, 480, 225, "Внутренний опыт", inner, "#EEF6FB", "#A5C6DA"),
        svg_card(635, 490, 480, 225, "Внутренний опыт при движении к важному", toward_inner, "#E8F4FB", "#8DB6D0"),
        svg_text(f"Небольшой выбранный шаг: {step or '—'}", 600, 790, 90, 17, "#315773", 3),
    ]
    return svg_document("ACT-матрица", "".join(content), width, height)


# ---------------------------------------------------------------------
# Дерево решений: интерфейс
# ---------------------------------------------------------------------

def new_scenario(first=False):
    return {"id": uuid.uuid4().hex, "default_probability": 100 if first else 0}


def new_option():
    return {"id": uuid.uuid4().hex, "scenarios": [new_scenario(first=True)]}


def decision_option_key(option_id):
    return f"dt_option_{option_id}"


def decision_scenario_key(scenario_id):
    return f"dt_scenario_{scenario_id}"


def clear_decision_result():
    st.session_state.dt_result = None


def add_decision_option():
    st.session_state.dt_options.append(new_option())
    clear_decision_result()


def delete_decision_option(option_id):
    if len(st.session_state.dt_options) > 2:
        st.session_state.dt_options = [
            option for option in st.session_state.dt_options
            if option["id"] != option_id
        ]
        clear_decision_result()


def add_decision_scenario(option_id):
    for option in st.session_state.dt_options:
        if option["id"] == option_id:
            option["scenarios"].append(new_scenario())
            clear_decision_result()
            return


def delete_decision_scenario(option_id, scenario_id):
    for option in st.session_state.dt_options:
        if option["id"] == option_id and len(option["scenarios"]) > 1:
            option["scenarios"] = [
                scenario for scenario in option["scenarios"]
                if scenario["id"] != scenario_id
            ]
            clear_decision_result()
            return


def render_decision_tree():
    if "dt_options" not in st.session_state:
        st.session_state.dt_options = [new_option(), new_option()]
    if "dt_result" not in st.session_state:
        st.session_state.dt_result = None

    st.title("Дерево решений")
    st.write("Разложите сложный выбор на варианты и возможные последствия.")

    question = st.text_input(
        "Какое решение нужно принять?",
        key="dt_question",
        placeholder="Например: «Стоит ли менять работу?»",
        on_change=clear_decision_result,
    )
    st.caption("Для каждого варианта добавьте исходы, вероятности и личную оценку.")

    for oi, option in enumerate(list(st.session_state.dt_options), start=1):
        option_id = option["id"]
        option_key = decision_option_key(option_id)

        with st.container(border=True):
            left_col, right_col = st.columns([5, 1.5])
            with left_col:
                st.markdown(f"### Вариант {oi}")
            with right_col:
                st.button(
                    "Удалить вариант",
                    key=f"delete_option_{option_id}",
                    disabled=len(st.session_state.dt_options) <= 2,
                    on_click=delete_decision_option,
                    args=(option_id,),
                    use_container_width=True,
                )

            if option_key not in st.session_state:
                st.session_state[option_key] = ""
            st.text_input(
                "Название варианта",
                key=option_key,
                placeholder=f"Вариант {oi}",
                on_change=clear_decision_result,
            )

            for si, scenario in enumerate(list(option["scenarios"]), start=1):
                scenario_id = scenario["id"]
                scenario_key = decision_scenario_key(scenario_id)
                probability_key = f"dt_probability_{scenario_id}"
                score_key = f"dt_score_{scenario_id}"

                if scenario_key not in st.session_state:
                    st.session_state[scenario_key] = ""
                if probability_key not in st.session_state:
                    st.session_state[probability_key] = scenario["default_probability"]
                if score_key not in st.session_state:
                    st.session_state[score_key] = 0.0

                with st.container(border=True):
                    left_col, right_col = st.columns([5, 1.5])
                    with left_col:
                        st.markdown(f"**Сценарий {si}**")
                    with right_col:
                        st.button(
                            "Удалить сценарий",
                            key=f"delete_scenario_{scenario_id}",
                            disabled=len(option["scenarios"]) <= 1,
                            on_click=delete_decision_scenario,
                            args=(option_id, scenario_id),
                            use_container_width=True,
                        )

                    st.text_input(
                        "Описание возможного исхода",
                        key=scenario_key,
                        placeholder="Например: «Найду более интересную работу»",
                        on_change=clear_decision_result,
                    )

                    c1, c2 = st.columns(2)
                    with c1:
                        st.slider(
                            "Вероятность, %",
                            0, 100, step=1,
                            key=probability_key,
                            on_change=clear_decision_result,
                        )
                    with c2:
                        st.slider(
                            "Оценка исхода",
                            -5.0, 5.0, step=0.5,
                            key=score_key,
                            help="−5 — очень нежелательный, +5 — очень желательный.",
                            on_change=clear_decision_result,
                        )

            st.button(
                "Добавить сценарий",
                key=f"add_scenario_{option_id}",
                on_click=add_decision_scenario,
                args=(option_id,),
            )

    add_col, remove_col, _ = st.columns([1.6, 2.1, 4])
    with add_col:
        st.button(
            "Добавить вариант",
            on_click=add_decision_option,
            use_container_width=True,
        )
    with remove_col:
        st.button(
            "Удалить последний вариант",
            disabled=len(st.session_state.dt_options) <= 2,
            on_click=delete_decision_option,
            args=(st.session_state.dt_options[-1]["id"],),
            use_container_width=True,
        )

    if st.button(
        "Рассчитать и построить дерево",
        type="primary",
        use_container_width=True,
    ):
        error = None
        prepared = []
        used_names = set()

        if not question.strip():
            error = "Сначала сформулируйте решение."

        for oi, option in enumerate(st.session_state.dt_options, start=1):
            if error:
                break

            name = st.session_state.get(decision_option_key(option["id"]), "").strip()
            if not name:
                error = f"Введите название варианта {oi}."
                break
            if name in used_names:
                error = f"Названия вариантов должны отличаться: «{name}»."
                break
            used_names.add(name)

            scenarios = []
            for si, scenario in enumerate(option["scenarios"], start=1):
                scenario_id = scenario["id"]
                scenario_name = st.session_state.get(decision_scenario_key(scenario_id), "").strip()
                if not scenario_name:
                    error = f"Заполните сценарий {si} варианта «{name}»."
                    break

                scenarios.append({
                    "name": scenario_name,
                    "probability": int(st.session_state[f"dt_probability_{scenario_id}"]),
                    "score": float(st.session_state[f"dt_score_{scenario_id}"]),
                })

            if error:
                break

            total = sum(item["probability"] for item in scenarios)
            if total == 0:
                error = f"Для варианта «{name}» задайте ненулевую вероятность."
                break

            normalized = [
                item["probability"] / total * 100
                for item in scenarios
            ]
            score = sum(
                normalized[i] / 100 * item["score"]
                for i, item in enumerate(scenarios)
            )

            prepared.append({
                "name": name,
                "scenarios": scenarios,
                "normalized": normalized,
                "score": score,
            })

        if error:
            st.session_state.dt_result = None
            st.warning(error)
        else:
            leader = max(prepared, key=lambda item: item["score"])["name"]
            st.session_state.dt_result = {
                "question": question.strip(),
                "options": prepared,
                "leader": leader,
            }

    result = st.session_state.dt_result
    if result:
        st.subheader("Результат")
        cols = st.columns(len(result["options"]))
        for col, option in zip(cols, result["options"]):
            with col:
                label = (
                    "Лидер по оценке: "
                    if option["name"] == result["leader"]
                    else ""
                ) + option["name"]
                st.metric(label, f"{option['score']:.2f} / 5")

        st.info(
            "Результат служит ориентиром для обсуждения, а не автоматическим решением. "
            "Вероятности нормализуются отдельно внутри каждого варианта."
        )

        render_interactive_diagram(
            make_decision_diagram(result["question"], result["options"]),
            "derevo_resheniy",
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
            link for link in st.session_state.chain_links
            if link["id"] != link_id
        ]


def render_chain():
    initialize_chain()

    st.title("Цепочный анализ поведения (ДБТ)")
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

    st.subheader("Звенья цепочки")
    links = []

    for index, link in enumerate(list(st.session_state.chain_links), start=1):
        link_id = link["id"]

        with st.container(border=True):
            left_col, right_col = st.columns([5, 1.5])
            with left_col:
                st.markdown(f"**Звено {index}**")
            with right_col:
                st.button(
                    "Удалить",
                    key=f"remove_chain_{link_id}",
                    disabled=len(st.session_state.chain_links) <= 1,
                    on_click=remove_chain_link,
                    args=(link_id,),
                    use_container_width=True,
                )

            c1, c2 = st.columns(2)
            with c1:
                thought = st.text_area("Мысли или образы", key=f"thought_{link_id}")
                body = st.text_area("Ощущения в теле", key=f"body_{link_id}")
            with c2:
                emotion = st.text_area("Эмоции", key=f"emotion_{link_id}")
                action = st.text_area("Импульсы или действия", key=f"action_{link_id}")

            intensity = st.slider(
                "Интенсивность (необязательно)",
                0, 10, 0,
                key=f"intensity_{link_id}",
            )
            intervention = st.checkbox(
                "Отметить как возможную точку вмешательства",
                key=f"intervention_{link_id}",
            )
            skill = st.text_area(
                "Возможный другой шаг, навык или поддержка",
                key=f"skill_{link_id}",
            )

        parts = [
            f"{label}: {value}"
            for label, value in [
                ("Мысли", thought),
                ("Эмоции", emotion),
                ("Ощущения в теле", body),
                ("Импульсы или действия", action),
                ("Интенсивность", str(intensity)),
            ]
            if value
        ]
        if intervention:
            parts.append("Возможная точка вмешательства")
        if skill.strip():
            parts.append(f"Возможная поддержка: {skill}")
        links.append((f"Звено {index}", "\n".join(parts)))

    st.button("Добавить звено", on_click=add_chain_link)

    st.subheader("Целевое поведение и последствия")
    target = st.text_area("Целевое поведение", key="chain_target")
    c1, c2 = st.columns(2)
    with c1:
        immediate = st.text_area("Последствия сразу после", key="chain_immediate")
    with c2:
        later = st.text_area("Последствия позднее", key="chain_later")
    repair = st.text_area(
        "Восстановление ситуации или поддержка",
        key="chain_repair",
    )

    sections = [
        ("Факторы уязвимости", vulnerability),
        ("Запускающее событие", prompting),
        *links,
        ("Целевое поведение", target),
        ("Последствия сразу после", immediate),
        ("Последствия позднее", later),
        ("Восстановление или поддержка", repair),
    ]

    with st.expander("Показать сводную карту", expanded=True):
        for heading, body in sections:
            st.markdown(f"**{heading}**")
            st.write(body or "—")

    render_interactive_diagram(
        make_vertical_diagram(
            "Цепочный анализ поведения",
            sections,
            "Карта для обсуждения, а не диагноз или автоматическая оценка.",
        ),
        "cepochnyy_analiz",
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

    st.title("Иерархия экспозиции")
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
            left_col, right_col = st.columns([5, 1.5])
            with left_col:
                st.markdown(f"**Ступень {index}**")
            with right_col:
                st.button(
                    "Удалить",
                    key=f"remove_exposure_{step_id}",
                    disabled=len(st.session_state.exposure_steps) <= 1,
                    on_click=remove_exposure_step,
                    args=(step_id,),
                    use_container_width=True,
                )

            situation = st.text_area("Ситуация", key=f"exp_situation_{step_id}")
            distress = st.slider(
                "Ожидаемая тревога (0–10)",
                0, 10, 3,
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

    st.button("Добавить ступень", on_click=add_exposure_step)

    ordered = sorted(records, key=lambda item: (item["distress"], item["index"]))
    sections = [("Цель", goal)]
    position = 0

    st.subheader("Лестница по ожидаемой тревоге")
    for item in ordered:
        if not item["situation"].strip():
            continue

        position += 1
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

    render_interactive_diagram(
        make_vertical_diagram(
            "Иерархия экспозиции",
            sections,
            "Порядок ступеней — материал для обсуждения, а не автоматическое назначение.",
        ),
        "ierarhiya_ekspozicii",
    )


# ---------------------------------------------------------------------
# ACT-матрица
# ---------------------------------------------------------------------

def render_act_matrix():
    st.title("ACT-матрица")
    st.write(
        "Исследуйте, что уводит от дискомфорта и какие действия приближают к важному."
    )
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
            away = st.text_area(
                "Что вы делаете, чтобы избежать дискомфорта?",
                key="act_away",
                placeholder="Например: откладываю разговор, отменяю встречу.",
            )
        with st.container(border=True):
            st.markdown("### Внутренний опыт")
            inner = st.text_area(
                "Мысли, эмоции, телесные ощущения",
                key="act_inner",
                placeholder="Что возникает внутри в этой ситуации?",
            )

    with right:
        with st.container(border=True):
            st.markdown("### Действия «к важному»")
            toward = st.text_area(
                "Какое действие приближает к важному?",
                key="act_toward",
                placeholder="Какой наблюдаемый шаг можно сделать?",
            )
        with st.container(border=True):
            st.markdown("### Внутренний опыт при движении к важному")
            toward_inner = st.text_area(
                "Что может возникать внутри при этом шаге?",
                key="act_toward_inner",
                placeholder="Например: волнение, сомнение, надежда.",
            )

    step = st.text_area(
        "Небольшой выбранный шаг",
        key="act_step",
        placeholder="Какой шаг вы сами хотели бы попробовать?",
    )

    render_interactive_diagram(
        make_act_diagram(
            situation, values, away, inner, toward, toward_inner, step
        ),
        "act_matrix",
        height=780,
    )


# ---------------------------------------------------------------------
# Главная, библиотека и раздел «О нас»
# ---------------------------------------------------------------------

def render_home():
    neuron_uri = "data:image/svg+xml," + quote(NEURON_SVG, safe="")

    st.markdown(
        f"""
        <div style="
            min-height:350px;
            display:flex;
            align-items:center;
            justify-content:center;
            padding:42px 25px;
            margin:20px 0 26px;
            box-sizing:border-box;
            border:1px solid #BBD9EC;
            border-radius:30px;
            background-color:rgba(232,245,253,.94);
            background-image:url('{neuron_uri}');
            background-size:cover;
            box-shadow:0 18px 42px rgba(48,105,145,.12);
            text-align:center;
        ">
          <div style="
              max-width:820px;
              padding:24px;
              border-radius:24px;
              background:rgba(248,252,255,.92);
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
                margin:20px auto 0;
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
            "Библиотека техник",
            type="primary",
            use_container_width=True,
            on_click=go_library,
        )
    with right:
        st.button(
            "О нас",
            type="primary",
            use_container_width=True,
            on_click=go_about,
        )

    st.divider()
    st.markdown("### Инструменты для совместной работы")
    st.write(
        "Выберите технику, чтобы открыть интерактивный черновик. "
        "Материалы помогают структурировать обсуждение."
    )


def render_library():
    st.title("Библиотека техник")
    st.write("Выберите инструмент, который хотите открыть.")

    items = list(TECHNIQUES.items())
    for start in range(0, len(items), 2):
        columns = st.columns(2)
        for column, (technique_id, technique) in zip(columns, items[start:start + 2]):
            with column:
                with st.container(border=True):
                    st.markdown(f"### {technique['title']}")
                    st.write(technique["short"])
                    st.caption(technique["description"])
                    st.button(
                        "Открыть технику",
                        key=f"open_{technique_id}",
                        on_click=open_technique,
                        args=(technique_id,),
                        use_container_width=True,
                    )


def render_about():
    st.title("О нас")
    st.markdown(
        """
        **ПСИ-БЛОК** — библиотека интерактивных инструментов
        для психологических консультаций. Она помогает специалисту
        и клиенту совместно структурировать обсуждение и наглядно фиксировать идеи.
        """
    )

    st.divider()
    st.subheader("Команда разработчиков")

    developers = [
        {"name": "Артём Черемкин", "role": "Разработчик сайта, практикующий психолог", "photo": "developer1.jpg"},
        {"name": "Анна Пыжьянова", "role": "Практикующий психолог", "photo": "developer2.jpg"},
        {"name": "Ферузахон Сайдазимова", "role": "Практикующий психолог", "photo": "developer3.jpg"},
    ]

    columns = st.columns(3)
    app_dir = Path(__file__).resolve().parent

    for column, person in zip(columns, developers):
        with column:
            with st.container(border=True):
                photo_path = app_dir / person["photo"]
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
                            background:linear-gradient(135deg,#DDEFFA,#F2F8FC);
                            color:#5F86A0;
                            font-family:Arial,sans-serif;
                            font-size:1.1rem;">
                            Фото разработчика
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"<div class='developer-name'>{html.escape(person['name'])}</div>"
                    f"<div class='developer-role'>{html.escape(person['role'])}</div>",
                    unsafe_allow_html=True,
                )


def render_selected_technique():
    technique_id = st.session_state.selected_technique

    if technique_id not in TECHNIQUES:
        st.warning("Техника не найдена.")
        st.button("Вернуться в библиотеку", on_click=go_library)
        return

    st.button("К библиотеке", on_click=go_library)
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
