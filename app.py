import base64
import html
import textwrap
import uuid
from pathlib import Path
from urllib.parse import quote

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="ПСИ-БЛОК",
    layout="wide",
)


# ---------------------------------------------------------------------
# Фон сайта: полупрозрачные нейронные связи
# ---------------------------------------------------------------------

NEURON_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="800" viewBox="0 0 1000 800">
  <g fill="none" stroke="#4389B5" stroke-opacity="0.14" stroke-width="2">
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
  <g fill="#4389B5" fill-opacity="0.18" stroke="#FFFFFF" stroke-opacity="0.8" stroke-width="3">
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

NEURON_BACKGROUND = base64.b64encode(
    NEURON_SVG.encode("utf-8")
).decode("ascii")


# ---------------------------------------------------------------------
# Сине-голубая тема
# ---------------------------------------------------------------------

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700;800&display=swap');

    :root {{
        color-scheme: light;
        --background-color: #F3F9FD;
        --secondary-background-color: #EAF4FB;
        --text-color: #294A65;
        --primary-color: #5B9BC4;
    }}

    html, body, [data-testid="stAppViewContainer"] {{
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
        opacity: .58;
        background-image: url("data:image/svg+xml;base64,{NEURON_BACKGROUND}");
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

    input, textarea, select,
    [data-baseweb="input"],
    [data-baseweb="textarea"],
    [data-baseweb="select"] > div,
    [data-baseweb="popover"],
    [data-baseweb="menu"] {{
        color: #294A65 !important;
        background-color: #FFFFFF !important;
        border-color: #AFCFE2 !important;
    }}

    input::placeholder, textarea::placeholder {{
        color: #7893A8 !important;
        opacity: 1 !important;
    }}

    [data-baseweb="select"] span,
    [data-baseweb="menu"] li {{
        color: #294A65 !important;
    }}

    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {{
        border: 1px solid #AFCFE2 !important;
        border-radius: 13px !important;
        background: #FFFFFF !important;
        color: #294A65 !important;
        caret-color: #315773 !important;
    }}

    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {{
        border-color: #5B9BC4 !important;
        box-shadow: 0 0 0 2px rgba(91,155,196,.18) !important;
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
        min-height: 60px;
        border: 1px solid #6EA7CB !important;
        border-radius: 16px !important;
        background: linear-gradient(135deg, #D9EEFA, #E5F3FC) !important;
        color: #234D6B !important;
        font-size: 1.12rem;
        font-weight: 800;
    }}

    [data-testid="stDownloadButton"] > button {{
        min-height: 46px;
        border: 1px solid #6EA7CB !important;
        border-radius: 14px !important;
        background: #E7F4FC !important;
        color: #234D6B !important;
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
# Каталог и навигация
# ---------------------------------------------------------------------

TECHNIQUES = {
    "decision_tree": {
        "title": "Дерево решений",
        "short": "Разложить сложный выбор на варианты и возможные последствия.",
        "description": "Сравнение вариантов, исходов, вероятностей и личных оценок.",
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
# SVG-схемы с масштабированием и PNG-скачиванием
# ---------------------------------------------------------------------

def svg_escape(value):
    return html.escape(str(value or ""), quote=True)


def wrap_svg_text(value, width=28, max_lines=5):
    value = str(value or "").strip()

    if not value:
        return ["—"]

    lines = []
    for paragraph in value.splitlines():
        lines.extend(textwrap.wrap(paragraph, width=width) or [""])

    return lines[:max_lines] or ["—"]


def svg_multiline(
    value,
    x,
    y,
    width=28,
    font_size=16,
    fill="#294A65",
    anchor="middle",
    max_lines=5,
    line_height=None,
):
    lines = wrap_svg_text(value, width, max_lines)
    line_height = line_height or int(font_size * 1.35)
    spans = []

    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_height
        spans.append(
            f'<tspan x="{x}" dy="{dy}">{svg_escape(line)}</tspan>'
        )

    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'font-family="Arial, sans-serif" font-size="{font_size}" '
        f'fill="{fill}">{"".join(spans)}</text>'
    )


def svg_card(x, y, width, height, title, body, fill="#F8FCFF", stroke="#AFCFE2"):
    title_y = y + 32
    body_y = y + 62
    max_chars = max(14, int(width / 12))

    return f"""
    <rect x="{x}" y="{y}" width="{width}" height="{height}" rx="22"
          fill="{fill}" stroke="{stroke}" stroke-width="3"/>
    {svg_multiline(title, x + width / 2, title_y, width=max_chars,
                   font_size=18, fill="#294A65", max_lines=2)}
    {svg_multiline(body, x + width / 2, body_y, width=max_chars,
                   font_size=15, fill="#476B85", max_lines=5)}
    """


def svg_document(title, content, width, height):
    return f"""<svg xmlns="http://www.w3.org/2000/svg"
        width="{width}" height="{height}" viewBox="0 0 {width} {height}">
      <rect width="100%" height="100%" fill="#F5FAFE"/>
      <text x="{width / 2}" y="48" text-anchor="middle"
        font-family="Arial, sans-serif" font-size="30" font-weight="bold"
        fill="#294A65">{svg_escape(title)}</text>
      {content}
    </svg>"""


def render_interactive_diagram(svg, component_key, height=760):
    safe_key = "".join(
        char for char in component_key
        if char.isalnum() or char == "_"
    )
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
          padding: 6px 2px 10px 2px;
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
          margin-left: 6px;
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

      <div class="viewport" id="viewport">
        DIAGRAM_SVG
      </div>

      <script>
        (() => {
          const svg = document.getElementById("DIAGRAM_ID");
          const viewport = document.getElementById("viewport");
          const initial = svg.viewBox.baseVal;

          const base = {
            x: initial.x,
            y: initial.y,
            width: initial.width,
            height: initial.height
          };
          const view = { ...base };

          function applyViewBox() {
            svg.setAttribute(
              "viewBox",
              `${view.x} ${view.y} ${view.width} ${view.height}`
            );
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
            applyViewBox();
          }

          document.getElementById("zoomIn").addEventListener(
            "click", () => zoom(0.8)
          );
          document.getElementById("zoomOut").addEventListener(
            "click", () => zoom(1.25)
          );
          document.getElementById("reset").addEventListener("click", () => {
            view.x = base.x;
            view.y = base.y;
            view.width = base.width;
            view.height = base.height;
            applyViewBox();
          });

          viewport.addEventListener("wheel", event => {
            event.preventDefault();
            zoom(event.deltaY < 0 ? 0.9 : 1.1, event.clientX, event.clientY);
          }, { passive: false });

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
            const scaleX = view.width / rect.width;
            const scaleY = view.height / rect.height;

            view.x -= (event.clientX - lastX) * scaleX;
            view.y -= (event.clientY - lastY) * scaleY;
            lastX = event.clientX;
            lastY = event.clientY;
            applyViewBox();
          });

          function stopDragging() {
            dragging = false;
            viewport.classList.remove("dragging");
          }

          viewport.addEventListener("pointerup", stopDragging);
          viewport.addEventListener("pointercancel", stopDragging);

          document.getElementById("downloadPng").addEventListener("click", () => {
            const clone = svg.cloneNode(true);
            clone.removeAttribute("id");
            clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
            clone.setAttribute("width", base.width);
            clone.setAttribute("height", base.height);
            clone.setAttribute(
              "viewBox",
              `${base.x} ${base.y} ${base.width} ${base.height}`
            );

            const source = new XMLSerializer().serializeToString(clone);
            const blob = new Blob(
              [source],
              { type: "image/svg+xml;charset=utf-8" }
            );
            const url = URL.createObjectURL(blob);
            const image = new Image();

            image.onload = () => {
              const canvas = document.createElement("canvas");
              canvas.width = Math.round(base.width * 2);
              canvas.height = Math.round(base.height * 2);

              const context = canvas.getContext("2d");
              context.fillStyle = "#F5FAFE";
              context.fillRect(0, 0, canvas.width, canvas.height);
              context.drawImage(image, 0, 0, canvas.width, canvas.height);
              URL.revokeObjectURL(url);

              canvas.toBlob(pngBlob => {
                if (!pngBlob) {
                  alert("Не удалось создать PNG. Попробуйте ещё раз.");
                  return;
                }

                const link = document.createElement("a");
                link.href = URL.createObjectURL(pngBlob);
                link.download = "FILENAME.png";
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
          });
        })();
      </script>
    </body>
    </html>
    """

    component_html = (
        template
        .replace("DIAGRAM_ID", svg_id)
        .replace("DIAGRAM_SVG", diagram_svg)
        .replace("FILENAME", safe_key)
    )

    components.html(component_html, height=height, scrolling=False)


# ---------------------------------------------------------------------
# Схемы для техник
# ---------------------------------------------------------------------

def make_decision_svg(question, options):
    width = max(1100, len(options) * 430)
    height = 850
    content = []

    root_x = width / 2
    root_y = 735
    option_y = 480
    scenario_y = 180
    colors = ["#6AAED0", "#65B99C", "#76A5D2", "#8BB7D8", "#5F9FC4"]
    option_xs = [
        width * (index + 1) / (len(options) + 1)
        for index in range(len(options))
    ]

    for option_index, option in enumerate(options):
        option_x = option_xs[option_index]
        color = colors[option_index % len(colors)]

        content.append(
            f'<path d="M {root_x} {root_y - 60} '
            f'C {root_x} {root_y - 150}, {option_x} {option_y + 110}, '
            f'{option_x} {option_y + 45}" fill="none" '
            f'stroke="{color}" stroke-width="7"/>'
        )

        scenarios = option["scenarios"]
        spacing = min(300, 700 / max(1, len(scenarios)))
        start_x = option_x - (len(scenarios) - 1) * spacing / 2

        for scenario_index, scenario in enumerate(scenarios):
            scenario_x = start_x + scenario_index * spacing

            content.append(
                f'<path d="M {option_x} {option_y - 25} '
                f'C {option_x} {option_y - 100}, {scenario_x} {scenario_y + 160}, '
                f'{scenario_x} {scenario_y + 100}" fill="none" '
                f'stroke="{color}" stroke-width="4"/>'
            )
            content.append(
                f'<circle cx="{scenario_x}" cy="{scenario_y + 90}" '
                f'r="12" fill="{color}"/>'
            )

            scenario_text = (
                f"{scenario['name']}\n"
                f"{option['normalized'][scenario_index]:.1f}% · "
                f"оценка {scenario['score']:g}"
            )
            content.append(
                svg_card(
                    scenario_x - 135, scenario_y - 5, 270, 105,
                    f"Исход {scenario_index + 1}",
                    scenario_text, "#FFFFFF", color,
                )
            )

        content.append(
            f'<circle cx="{option_x}" cy="{option_y}" r="14" '
            f'fill="{color}" stroke="#FFFFFF" stroke-width="4"/>'
        )
        content.append(
            svg_card(
                option_x - 160, option_y + 25, 320, 100,
                option["name"],
                f"Итоговая оценка: {option['score']:.2f}",
                "#FFFFFF", color,
            )
        )

    content.append(
        svg_card(
            root_x - 230, root_y - 55, 460, 110,
            "Решение", question, "#E4F2FA", "#78A9C9",
        )
    )

    return svg_document("Дерево решений", "".join(content), width, height)


def make_vertical_svg(title, sections, note):
    width = 1100
    card_height = 115
    gap = 45
    top = 95
    height = max(550, top + len(sections) * (card_height + gap) + 90)
    content = []

    for index, (heading, body) in enumerate(sections):
        y = top + index * (card_height + gap)
        fill = "#E8F4FB" if index % 2 == 0 else "#F2F8FC"

        content.append(
            svg_card(
                115, y, 870, card_height, heading, body,
                fill, "#AFCFE2",
            )
        )

        if index < len(sections) - 1:
            content.append(
                f'<path d="M 550 {y + card_height} '
                f'L 550 {y + card_height + gap - 4}" '
                'stroke="#6EA7CB" stroke-width="4" fill="none"/>'
            )
            content.append(
                f'<path d="M 540 {y + card_height + gap - 15} '
                f'L 550 {y + card_height + gap - 4} '
                f'L 560 {y + card_height + gap - 15}" '
                'fill="none" stroke="#6EA7CB" stroke-width="4"/>'
            )

    content.append(
        f'<text x="550" y="{height - 28}" text-anchor="middle" '
        'font-family="Arial, sans-serif" font-size="14" fill="#54718A">'
        f'{svg_escape(note)}</text>'
    )

    return svg_document(title, "".join(content), width, height)


def make_act_svg(
    situation,
    values,
    away_actions,
    inner,
    toward_actions,
    toward_inner,
    next_step,
):
    width, height = 1200, 930
    content = []

    content.append(
        svg_multiline(
            f"Ситуация: {situation or '—'}",
            600, 88, 90, 16, "#476B85", max_lines=2,
        )
    )
    content.append(
        svg_multiline(
            f"Что важно: {values or '—'}",
            600, 128, 90, 16, "#476B85", max_lines=2,
        )
    )

    content.append(
        '<line x1="600" y1="170" x2="600" y2="760" '
        'stroke="#8DB6D0" stroke-width="5"/>'
    )
    content.append(
        '<line x1="70" y1="465" x2="1130" y2="465" '
        'stroke="#8DB6D0" stroke-width="5"/>'
    )

    content.append(
        svg_card(
            85, 195, 480, 235,
            "Действия «от дискомфорта»",
            away_actions,
            "#EAF5FC", "#8DB6D0",
        )
    )
    content.append(
        svg_card(
            635, 195, 480, 235,
            "Действия «к важному»",
            toward_actions,
            "#E4F3FA", "#78A9C9",
        )
    )
    content.append(
        svg_card(
            85, 500, 480, 235,
            "Внутренний опыт",
            inner,
            "#EEF6FB", "#A5C6DA",
        )
    )
    content.append(
        svg_card(
            635, 500, 480, 235,
            "Внутренний опыт при движении к важному",
            toward_inner,
            "#E8F4FB", "#8DB6D0",
        )
    )
    content.append(
        svg_multiline(
            f"Небольшой выбранный шаг: {next_step or '—'}",
            600, 815, 90, 17, "#315773", max_lines=3,
        )
    )

    return svg_document("ACT-матрица", "".join(content), width, height)


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
            return


def delete_scenario(option_id, scenario_id):
    for option in st.session_state.dt_options:
        if option["id"] == option_id and len(option["scenarios"]) > 1:
            option["scenarios"] = [
                item for item in option["scenarios"]
                if item["id"] != scenario_id
            ]
            clear_decision_result()
            return


def render_decision_tree():
    initialize_decision_tree()

    st.title("Дерево решений")
    st.write("Разложите сложный выбор на варианты и возможные последствия.")

    st.text_input(
        "Какое решение нужно принять?",
        key="dt_question",
        placeholder="Например: «Стоит ли менять работу?»",
        on_change=clear_decision_result,
    )

    st.caption("Для каждого варианта добавьте исходы, вероятности и личную оценку.")

    for option_index, option in enumerate(
        list(st.session_state.dt_options), start=1
    ):
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

            for scenario_index, scenario in enumerate(
                list(option["scenarios"]), start=1
            ):
                scenario_id = scenario["id"]
                name_state_key = scenario_name_key(scenario_id)
                probability_state_key = probability_key(scenario_id)
                score_state_key = score_key(scenario_id)

                if name_state_key not in st.session_state:
                    st.session_state[name_state_key] = ""
                if probability_state_key not in st.session_state:
                    st.session_state[probability_state_key] = (
                        scenario["default_probability"]
                    )
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
                "Добавить сценарий",
                key=f"dt_add_scenario_{option_id}",
                on_click=add_scenario,
                args=(option_id,),
            )

    add_col, remove_col, _ = st.columns([1.7, 1.9, 4])

    with add_col:
        st.button(
            "Добавить вариант",
            key="dt_add_option",
            on_click=add_option,
            use_container_width=True,
        )

    with remove_col:
        st.button(
            "Удалить последний вариант",
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

        for option_index, option in enumerate(
            st.session_state.dt_options, start=1
        ):
            if error:
                break

            name = st.session_state.get(
                option_name_key(option["id"]), ""
            ).strip()

            if not name:
                error = f"Введите название варианта {option_index}."
                break

            if name in used_names:
                error = f"Названия вариантов должны отличаться: «{name}»."
                break

            used_names.add(name)
            scenarios = []

            for scenario_index, scenario in enumerate(
                option["scenarios"], start=1
            ):
                scenario_id = scenario["id"]
                scenario_name = st.session_state.get(
                    scenario_name_key(scenario_id), ""
                ).strip()

                if not scenario_name:
                    error = (
                        f"Заполните сценарий {scenario_index} "
                        f"варианта «{name}»."
                    )
                    break

                scenarios.append({
                    "name": scenario_name,
                    "probability": int(
                        st.session_state[probability_key(scenario_id)]
                    ),
                    "score": float(
                        st.session_state[score_key(scenario_id)]
                    ),
                })

            if error:
                break

            total_probability = sum(
                item["probability"] for item in scenarios
            )

            if total_probability == 0:
                error = (
                    f"Для варианта «{name}» задайте ненулевую вероятность."
                )
                break

            normalized = [
                item["probability"] / total_probability * 100
                for item in scenarios
            ]

            expected_score = sum(
                normalized[index] / 100 * item["score"]
                for index, item in enumerate(scenarios)
            )

            prepared_options.append({
                "name": name,
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
                    "Лидер по оценке: "
                    if option["name"] == result["best_name"]
                    else ""
                ) + option["name"]

                st.metric(
                    label=label,
                    value=f"{option['score']:.2f} / 5",
                )

        st.info(
            "Результат — ориентир для обсуждения, а не автоматическое решение. "
            "Вероятности нормализуются отдельно внутри каждого варианта."
        )

        diagram = make_decision_svg(
            result["question"],
            result["options"],
        )
        render_interactive_diagram(
            diagram,
            "derevo_resheniy",
            height=760,
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

    st.title("Цепочный анализ поведения (ДБТ)")
    st.write(
        "Исследуйте контекст, звенья цепочки, поведение и последствия."
    )
    st.info(
        "Можно сделать паузу, пропустить поле или остановиться в любой момент."
    )

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
    link_data = []

    for index, link in enumerate(
        list(st.session_state.chain_links), start=1
    ):
        link_id = link["id"]

        with st.container(border=True):
            header, delete_col = st.columns([5, 1.5])

            with header:
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
                thought = st.text_area(
                    "Мысли или образы",
                    key=f"chain_thought_{link_id}",
                )
                body = st.text_area(
                    "Ощущения в теле",
                    key=f"chain_body_{link_id}",
                )

            with right:
                emotion = st.text_area(
                    "Эмоции",
                    key=f"chain_emotion_{link_id}",
                )
                action = st.text_area(
                    "Импульсы или действия",
                    key=f"chain_action_{link_id}",
                )

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

        description_parts = [
            f"{label}: {value}"
            for label, value in [
                ("Мысли", thought),
                ("Эмоции", emotion),
                ("Ощущения в теле", body),
                ("Импульсы или действия", action),
            ]
            if value.strip()
        ]

        if intervention:
            description_parts.append("Возможная точка вмешательства")

        if skill.strip():
            description_parts.append(f"Возможная поддержка: {skill}")

        link_data.append((
            f"Звено {index}",
            "\n".join(description_parts),
        ))

    st.button("Добавить звено", on_click=add_chain_link)

    st.subheader("Целевое поведение и последствия")
    target = st.text_area(
        "Целевое поведение",
        key="chain_target",
    )

    left, right = st.columns(2)
    with left:
        immediate = st.text_area(
            "Последствия сразу после",
            key="chain_immediate",
        )
    with right:
        later = st.text_area(
            "Последствия позднее",
            key="chain_later",
        )

    repair = st.text_area(
        "Восстановление ситуации или поддержка",
        key="chain_repair",
    )

    sections = [
        ("Факторы уязвимости", vulnerability),
        ("Запускающее событие", prompting),
        *link_data,
        ("Целевое поведение", target),
        ("Последствия сразу после", immediate),
        ("Последствия позднее", later),
        ("Восстановление или поддержка", repair),
    ]

    with st.expander("Показать сводную карту", expanded=True):
        for heading, body in sections:
            st.markdown(f"**{heading}**")
            st.write(body or "—")

    diagram = make_vertical_svg(
        "Цепочный анализ поведения",
        sections,
        "Карта для обсуждения, а не диагноз или автоматическая оценка.",
    )
    render_interactive_diagram(
        diagram,
        "cepochnyy_analiz",
        height=760,
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
    st.write(
        "Составьте лестницу ситуаций для обсуждения и планирования практики."
    )
    st.info(
        "Практика должна быть добровольной и согласованной со специалистом. "
        "Не используйте упражнение для ситуаций с реальной опасностью."
    )

    goal = st.text_area(
        "Цель работы",
        key="exposure_goal",
    )

    records = []

    for index, step in enumerate(
        list(st.session_state.exposure_steps), start=1
    ):
        step_id = step["id"]

        with st.container(border=True):
            header, delete_col = st.columns([5, 1.5])

            with header:
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

            situation = st.text_area(
                "Ситуация",
                key=f"exp_situation_{step_id}",
            )
            distress = st.slider(
                "Ожидаемая тревога (0–10)",
                min_value=0,
                max_value=10,
                value=3,
                key=f"exp_distress_{step_id}",
            )
            prediction = st.text_area(
                "Прогноз или опасение",
                key=f"exp_prediction_{step_id}",
            )
            plan = st.text_area(
                "Обсуждаемый посильный шаг",
                key=f"exp_plan_{step_id}",
            )
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

    ordered = sorted(
        records,
        key=lambda item: (item["distress"], item["index"]),
    )
    sections = [("Цель", goal)]

    st.subheader("Лестница по ожидаемой тревоге")
    display_position = 0

    for item in ordered:
        if not item["situation"].strip():
            continue

        display_position += 1

        with st.container(border=True):
            st.markdown(
                f"**{display_position}. {item['situation']}** — "
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
            f"Ступень {display_position} · тревога "
            f"{item['distress']}/10 · {item['status']}",
            "\n".join([
                f"Ситуация: {item['situation']}",
                f"Прогноз: {item['prediction']}",
                f"Шаг: {item['plan']}",
                f"Наблюдения: {item['reflection']}",
            ]),
        ))

    diagram = make_vertical_svg(
        "Иерархия экспозиции",
        sections,
        "Порядок ступеней — материал для обсуждения, а не автоматическое назначение.",
    )
    render_interactive_diagram(
        diagram,
        "ierarhiya_ekspozicii",
        height=760,
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

    situation = st.text_area(
        "Ситуация, которую хотите исследовать",
        key="act_situation",
    )
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

    diagram = make_act_svg(
        situation,
        values,
        away_actions,
        inner,
        toward_actions,
        toward_inner,
        next_step,
    )

    st.subheader("Матрица")
    render_interactive_diagram(
        diagram,
        "act_matrix",
        height=800,
    )


# ---------------------------------------------------------------------
# Главная, библиотека, раздел «О нас»
# ---------------------------------------------------------------------

def render_home():
    neuron_data_uri = (
        "data:image/svg+xml,"
        + quote(NEURON_SVG, safe="")
    )

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
            border:1px solid #BBD9EC;
            border-radius:30px;
            background-color:rgba(232,245,253,.94);
            background-image:url('{neuron_data_uri}');
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
        "Материалы поддерживают обсуждение, но не заменяют профессиональную "
        "оценку или терапевтическую работу."
    )


def render_library():
    st.title("Библиотека техник")
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
            "photo": "developer1.jpg",
        },
        {
            "name": "Имя Фамилия",
            "role": "Роль в проекте",
            "photo": "developer2.jpg",
        },
        {
            "name": "Имя Фамилия",
            "role": "Роль в проекте",
            "photo": "developer3.jpg",
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
                            background:linear-gradient(135deg,#DDEFFA,#F2F8FC);
                            color:#5F86A0;
                            font-family:Arial,sans-serif;
                            font-size:1.2rem;">
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
