"""Chestnut Picking — a tiny app to collect small positive things, one at a time."""
# TODO: have an LLM summarize the collected good things (recurring themes, patterns over time).
import random
from datetime import date

import streamlit as st
import streamlit.components.v1 as components

from storage import load_good_things, save_good_thing

CELEBRATION_EMOJIS = [
    "🌰", "❤️", "💛", "🤎", "✨",
    "🐿️", "🍂", "🎉", "🥳", "🌟",
]


def show_celebration(count: int = 20, height: int = 160) -> None:
    """Rain chestnuts, hearts, squirrels and other fun things after a good thing is added."""
    pieces = []
    for _ in range(count):
        left = random.randint(0, 92)
        size = random.randint(22, 40)
        delay = random.uniform(0, 0.5)
        duration = random.uniform(1.4, 2.4)
        sway = random.uniform(-40, 40)
        spin = random.choice([-1, 1]) * random.randint(180, 420)
        emoji = random.choice(CELEBRATION_EMOJIS)
        pieces.append(
            f'<span class="piece" style="left:{left}%; font-size:{size}px; '
            f'--sway:{sway:.0f}px; --spin:{spin}deg; '
            f'animation-delay:{delay:.2f}s; animation-duration:{duration:.2f}s;">{emoji}</span>'
        )
    components.html(
        f"""
        <div style="position:relative; height:{height}px; overflow:hidden;">
          <style>
            .piece {{
              position:absolute;
              top:-40px;
              animation-name: fall;
              animation-timing-function: ease-in;
              animation-fill-mode: forwards;
            }}
            @keyframes fall {{
              0%   {{ transform: translate(0, 0) rotate(0deg) scale(0.8); opacity:1; }}
              50%  {{ transform: translate(var(--sway), {height // 2}px) rotate(var(--spin)) scale(1.15); opacity:1; }}
              100% {{ transform: translate(0, {height + 40}px) rotate(var(--spin)) scale(0.9); opacity:0; }}
            }}
          </style>
          {''.join(pieces)}
        </div>
        """,
        height=height,
    )

st.set_page_config(page_title="Chestnut Picking", page_icon="🌰")

st.markdown(
    """
    <style>
    html, body, [class*="st-"], p, li, label, span, div {
        font-size: 1.15rem !important;
    }
    h1 { font-size: 2.4rem !important; }
    textarea, input { font-size: 1.15rem !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 style='text-align:center; font-size:4.5rem !important;'>🌰 Chestnut Picking</h1>", unsafe_allow_html=True)
st.caption("A tiny positive thing is enough — though of course it can be big too.")

with st.form("add_good_thing", clear_on_submit=True):
    good_thing_text = st.text_area("A good thing, big or small", height=130)
    submitted = st.form_submit_button("Add")

if submitted and good_thing_text.strip():
    save_good_thing(good_thing_text.strip())
    st.success("Saved.")
    show_celebration()

st.divider()

all_good_things = load_good_things()
today_count = sum(1 for g in all_good_things if g["date"].startswith(str(date.today())))
st.caption(f"✨ {today_count} good thing(s) today")

if "show_history" not in st.session_state:
    st.session_state.show_history = False

if st.button("Show history" if not st.session_state.show_history else "Hide history"):
    st.session_state.show_history = not st.session_state.show_history
    st.rerun()

if st.session_state.show_history:
    view = st.radio("Show", ["Today", "All"], horizontal=True)

    good_things = all_good_things
    if view == "Today":
        good_things = [g for g in good_things if g["date"].startswith(str(date.today()))]

    if good_things:
        st.caption("🤖 TODO: have an LLM summarize these (recurring themes, patterns over time).")
        for item in reversed(good_things):
            st.write(f"**{item['date']}** — {item['text']}")
    else:
        st.caption("Nothing logged yet — add your first good thing above.")

