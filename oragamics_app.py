import streamlit as st

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
HOLIDAY_DISCOUNT = 0.10   # 10% off selected items
RUSH_FEE = 10             # cents per item for next-day readiness
MAKERS = ["Aanya", "Aarav", "Kavin", "Chase"]

# Prices are in cents. Set "holiday": True on the items on holiday deal.
PRODUCTS = [
    {"name": "High Quality Paper Airplane", "price": 40, "emoji": "✈️"},
    {"name": "Flappy Swan", "price": 20, "emoji": "🦢"},
    {"name": "Med Claws", "price": 25, "emoji": "🦀"},
    {"name": "Awesome Dragon Claws", "price": 60, "emoji": "🐉"},
    {"name": "Small Slinky", "price": 50, "emoji": "🌀"},
    {"name": "Big Slinky", "price": 100, "emoji": "🌀"},
    {"name": "Kaleidoscope", "price": 75, "emoji": "🔺"},
    {"name": "Fortune Tellers", "price": 25, "emoji": "🔮"},
    {"name": "Paper Bound Book (we supply paper)", "price": 200, "emoji": "📓"},
    {"name": "Paper Bound Book (you provide paper)", "price": 100, "emoji": "📓"},
    {"name": "Gift Envelopes", "price": 100, "emoji": "✉️"},
    {"name": "Bookmarks", "price": 10, "emoji": "🔖"},
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
    st.write(f"{p['emoji']} **{p['name']}** — {price_text}")
st.caption("Paper Bound Book is $1 if you provide the paper. 🎄 = holiday deal.")
st.caption("Tax is 5% for all items.")
