import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Oragamics", page_icon="🦢", layout="centered")

# Rainbow theme
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #ffd6d6, #ffe9c7, #fff9c4,
                                    #d6f5d6, #c7ecff, #d9d1ff, #f5d1ff);
    }
    h1, h3 {
        background: linear-gradient(90deg, #ff0000, #ff8c00, #e6c200,
                                    #00b050, #0070c0, #7030a0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
# Deals start at midnight on Nov 23 in New York time. The countdown uses this
# exact moment, so each visitor sees it in their own local time zone.
DEALS_START_ISO = "2026-11-23T00:00:00-05:00"
HOLIDAY_DISCOUNT = 0.10   # 10% off selected items (none on sale yet)
RUSH_FEE = 10             # cents per item for next-day readiness
MAKERS = ["Aanya", "Aarav", "Kavin", "Chase"]

# Prices are in cents. Set "holiday": True on the items on holiday deal.
PRODUCTS = [
    {"name": "High Quality Paper Airplane", "price": 40, "emoji": "✈️",
     "desc": "Sleek, sturdy, and built to glide."},
    {"name": "Flappy Swan", "price": 20, "emoji": "🦢",
     "desc": "Flap the wings and watch it go."},
    {"name": "Med Claws", "price": 25, "emoji": "🦀",
     "desc": "Will make you feel like wolferine"},
    {"name": "Awesome Dragon Claws", "price": 60, "emoji": "🐉",
     "desc": "They are much longer, faster, and even have a scaly design"},
    {"name": "Small Slinky", "price": 50, "emoji": "🌀",
     "desc": "Great toy and fidget"},
    {"name": "Big Slinky", "price": 100, "emoji": "🌀",
     "desc": "The full-size classic."},
    {"name": "Kaleidoscope", "price": 75, "emoji": "🔺",
     "desc": "Turn it and see a new pattern."},
    {"name": "Fortune Tellers", "price": 25, "emoji": "🔮",
     "desc": "Pick a color, pick a number, see your future."},
    {"name": "Paper Bound Book (we supply paper)", "price": 200, "emoji": "📓",
     "desc": "Hand-bound book."},
    {"name": "Paper Bound Book (you provide paper)", "price": 100, "emoji": "📓",
     "desc": "Bring your own paper and pay less."},
    {"name": "Gift Envelopes", "price": 100, "emoji": "✉️",
     "desc": "Handmade envelopes for your gifts."},
    {"name": "Bookmarks", "price": 10, "emoji": "🔖",
     "desc": "Small, cheap, and handy."},
]


def cents(value: int) -> str:
    if value < 100:
        return f"{value}c"
    return f"${value / 100:.2f}"


def unit_price(product: dict) -> int:
    price = product["price"]
    if product.get("holiday"):
        price = round(price * (1 - HOLIDAY_DISCOUNT))
    return price


def countdown(target_iso: str) -> None:
    # Runs in the visitor's browser, so times show in their local time zone.
    components.html(
        f"""
        <div style="font-family: sans-serif; color: #222;">
          <div id="cd" style="font-size: 1.3rem; font-weight: 600;"></div>
          <div id="start" style="font-size: 0.9rem; opacity: 0.8; margin-top: 4px;"></div>
        </div>
        <script>
          const target = new Date("{target_iso}");
          document.getElementById("start").textContent =
            "Starts " + target.toLocaleString(undefined, {{
              dateStyle: "full", timeStyle: "short"
            }}) + " your time";

          function tick() {{
            const diff = target - new Date();
            const el = document.getElementById("cd");
            if (diff <= 0) {{
              el.textContent = "🎉 Deals are live!";
              return;
            }}
            const s = Math.floor(diff / 1000);
            const d = Math.floor(s / 86400);
            const h = Math.floor((s % 86400) / 3600);
            const m = Math.floor((s % 3600) / 60);
            const sec = s % 60;
            const pad = (n) => String(n).padStart(2, "0");
            el.textContent = "⏳ " + d + "d " + pad(h) + "h " + pad(m) +
              "m " + pad(sec) + "s until deals start";
          }}
          tick();
          setInterval(tick, 1000);
        </script>
        """,
        height=90,
    )


# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------
st.markdown(
    "<h1 style='text-align:center; margin-bottom:0;'>Oragamics</h1>"
    "<h3 style='text-align:center; margin-top:0; font-weight:400;'>"
    "The best of the best paper fidgets</h3>",
    unsafe_allow_html=True,
)

st.success("🎄 **Holiday deals: 10% off selected items!**")
st.caption("Deals start 23 of November.")
countdown(DEALS_START_ISO)

st.markdown("### Meet the makers")
st.write(", ".join(MAKERS[:-1]) + f", or {MAKERS[-1]} to buy.")

st.markdown("### How ordering works")
st.write(
    "**Write down your order and hand it to one of the makers.**\n\n"
    "- Items are ready **next day** if you pay an extra **10c** per item.\n"
    "- Otherwise, the item will be ready in **2–5 days**.\n"
    "- Any item **$1 or above** will be ready in **2 days** unless you pay **20c**. "
    "Then it will still be **next day**."
)

st.markdown("### Our paper fidgets")
for p in PRODUCTS:
    price_text = cents(unit_price(p))
    if p.get("holiday"):
        price_text += " 🎄"
    st.markdown(f"{p['emoji']} **{p['name']}** — {price_text}  \n*{p['desc']}*")
st.caption("Paper Bound Book is $1 if you provide the paper.")
st.caption("Tax is 5% for all items.")
