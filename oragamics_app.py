import streamlit as st

st.set_page_config(page_title="Oragamics", page_icon="🦢", layout="wide")

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
HOLIDAY_DISCOUNT = 0.10   # 10% off selected items
RUSH_FEE = 10             # cents, per line item, for next-day readiness
MAKERS = ["Aanya", "Aarav", "Kavin", "Chase"]

# Prices are stored in cents.
# "holiday" marks the items on holiday deal (the slide says "selected items";
# edit this list if different items should be discounted).
PRODUCTS = [
    {"key": "airplane", "name": "High Quality Paper Airplane", "price": 40,
     "emoji": "✈️", "blurb": "Sleek, sturdy, and built to glide."},
    {"key": "swan", "name": "Flappy Swan", "price": 20,
     "emoji": "🦢", "blurb": "Flap the wings and watch it go."},
    {"key": "med_claws", "name": "Med Claws", "price": 25,
     "emoji": "🦀", "blurb": "A classic claw fidget."},
    {"key": "dragon_claws", "name": "Awesome Dragon Claws", "price": 60,
     "emoji": "🐉", "blurb": "Our best claw. Snaps and clicks.", "holiday": True},
    {"key": "small_slinky", "name": "Small Slinky", "price": 50,
     "emoji": "🌀", "blurb": "Tumbles down stairs, fidgets in hand."},
    {"key": "big_slinky", "name": "Big Slinky", "price": 100,
     "emoji": "🌀", "blurb": "The full-size classic.", "holiday": True},
    {"key": "kaleidoscope", "name": "Kaleidoscope", "price": 75,
     "emoji": "🔺", "blurb": "Turn it and see a new pattern.", "holiday": True},
    {"key": "fortune_tellers", "name": "Fortune Tellers", "price": 25,
     "emoji": "🔮", "blurb": "Pick a color, pick a number, see your future."},
    {"key": "paper_book", "name": "Paper Bound Book (we supply paper)", "price": 200,
     "emoji": "📓", "blurb": "Hand-bound book.", "holiday": True},
    {"key": "paper_book_own", "name": "Paper Bound Book (you provide paper)", "price": 100,
     "emoji": "📓", "blurb": "Bring your own paper and pay less."},
    {"key": "gift_envelopes", "name": "Gift Envelopes", "price": 100,
     "emoji": "✉️", "blurb": "Handmade envelopes for your gifts."},
    {"key": "bookmarks", "name": "Bookmarks", "price": 10,
     "emoji": "🔖", "blurb": "Small, cheap, and handy."},
]
PRODUCTS_BY_KEY = {p["key"]: p for p in PRODUCTS}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def cents(value: int) -> str:
    return f"${value / 100:.2f}"


def unit_price(product: dict) -> int:
    price = product["price"]
    if product.get("holiday"):
        price = round(price * (1 - HOLIDAY_DISCOUNT))
    return price


def line_total(item: dict) -> int:
    total = item["unit"] * item["qty"]
    if item["rush"]:
        total += RUSH_FEE
    return total


def add_to_cart(product: dict, qty: int, rush: bool) -> None:
    cart = st.session_state.cart
    if product["key"] in cart:
        cart[product["key"]]["qty"] += qty
        cart[product["key"]]["rush"] = cart[product["key"]]["rush"] or rush
    else:
        cart[product["key"]] = {
            "name": product["name"],
            "unit": unit_price(product),
            "qty": qty,
            "rush": rush,
        }


if "cart" not in st.session_state:
    st.session_state.cart = {}
if "last_order" not in st.session_state:
    st.session_state.last_order = None


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    "<h1 style='text-align:center; margin-bottom:0;'>Oragamics</h1>"
    "<h3 style='text-align:center; margin-top:0; font-weight:400;'>"
    "The best of the best paper fidgets</h3>",
    unsafe_allow_html=True,
)

home_tab, shop_tab, order_tab = st.tabs(["🏠 Home", "🛍️ Shop", "🧾 Your Order"])

# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------
with home_tab:
    left, right = st.columns(2)

    with left:
        st.success("🎄 **Holiday deals: 10% off selected items!**")

        st.markdown("### Meet the makers")
        st.write(", ".join(MAKERS[:-1]) + f", or {MAKERS[-1]} to buy.")

        st.markdown("### How ordering works")
        st.write(
            "- Items are ready **next day** if you pay an extra **10c** per item.\n"
            "- Otherwise, the item will be ready in **2–5 days**."
        )

    with right:
        st.markdown("### Our paper fidgets")
        for p in PRODUCTS:
            price_text = cents(unit_price(p))
            if p.get("holiday"):
                price_text += " 🎄"
            st.write(f"{p['emoji']} **{p['name']}** — {price_text}")
        st.caption("Paper Bound Book is $1 if you provide the paper. 🎄 = holiday deal.")


# ---------------------------------------------------------------------------
# Shop
# ---------------------------------------------------------------------------
with shop_tab:
    st.subheader("Choose your fidgets")
    cols = st.columns(3)

    for i, p in enumerate(PRODUCTS):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"#### {p['emoji']} {p['name']}")
                st.caption(p["blurb"])

                price_line = f"**{cents(unit_price(p))}** each"
                if p.get("holiday"):
                    price_line += f"  ~~{cents(p['price'])}~~ 🎄 10% off"
                st.markdown(price_line)

                qty = st.number_input(
                    "Quantity", min_value=0, max_value=50, value=0,
                    key=f"qty_{p['key']}",
                )
                rush = st.checkbox(
                    f"Rush: ready next day (+{cents(RUSH_FEE)})",
                    key=f"rush_{p['key']}",
                )
                if st.button(
                    "Add to order",
                    key=f"add_{p['key']}",
                    disabled=qty == 0,
                    use_container_width=True,
                ):
                    add_to_cart(p, qty, rush)
                    st.toast(f"Added {qty} × {p['name']}")


# ---------------------------------------------------------------------------
# Order & checkout
# ---------------------------------------------------------------------------
with order_tab:
    cart = st.session_state.cart

    if st.session_state.last_order:
        st.success(st.session_state.last_order)
        if st.button("Start a new order"):
            st.session_state.last_order = None
            st.rerun()

    if not cart:
        st.info("Your order is empty. Head to the Shop tab to add some fidgets!")
    else:
        st.subheader("Your order")
        subtotal = 0
        for key, item in list(cart.items()):
            total = line_total(item)
            subtotal += total
            c1, c2, c3 = st.columns([5, 2, 1])
            rush_note = " · rush" if item["rush"] else ""
            c1.write(f"**{item['name']}** × {item['qty']}{rush_note}")
            c2.write(cents(total))
            if c3.button("✕", key=f"remove_{key}", help="Remove"):
                del cart[key]
                st.rerun()

        st.markdown(f"### Total: {cents(subtotal)}")

        st.divider()
        st.subheader("Checkout")
        with st.form("checkout_form"):
            name = st.text_input("Your name")
            contact = st.text_input("Phone or email (so we can let you know it's ready)")
            pickup = st.radio("Pickup or delivery?", ["Pickup", "Delivery"], horizontal=True)
            notes = st.text_area("Notes (optional)")
            submitted = st.form_submit_button("Place order", type="primary")

        if submitted:
            if not name.strip() or not contact.strip():
                st.error("Please add your name and a way to reach you.")
            else:
                lines = [
                    f"- {item['qty']} × {item['name']}"
                    + (" (rush)" if item["rush"] else "")
                    + f" — {cents(line_total(item))}"
                    for item in cart.values()
                ]
                st.session_state.last_order = (
                    f"Thanks, {name.strip()}! Your order is in.\n\n"
                    + "\n".join(lines)
                    + f"\n\n**Total: {cents(subtotal)}** · {pickup}"
                )
                st.session_state.cart = {}
                st.rerun()
