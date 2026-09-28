import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Mini Mart Project", page_icon="🛒", layout="wide")

# Products list
products = [
    {"pid": 101, "name": "Shampoo", "category": "Cosmetics", "price": 120, "stock": 50},
    {"pid": 102, "name": "Soap", "category": "Cosmetics", "price": 40, "stock": 5},
    {"pid": 103, "name": "Rice", "category": "Grocery", "price": 60, "stock": 100},
    {"pid": 104, "name": "Wheat", "category": "Grocery", "price": 70, "stock": 150},
    {"pid": 105, "name": "Biscuits", "category": "Grocery", "price": 50, "stock": 3}
]

# Sales history
if "sales" not in st.session_state:
    st.session_state.sales = []
if "transaction_id" not in st.session_state:
    st.session_state.transaction_id = 1000

# Menu choice
choice = st.selectbox(
    "Choose an option:",
    ["View All Products", "Search Product", "Purchase Product", "View Sales History", "Sales Analysis", "Low Stock Products", "Exit"]
)

# 1. View All Products
if choice == "View All Products":
    st.subheader("All Products")
    for p in products:
        st.write(f"ID:{p['pid']} | Name:{p['name']} | Category:{p['category']} | Price:{p['price']} | Stock:{p['stock']}")

# 2. Search Product
elif choice == "Search Product":
    pid = st.number_input("Enter Product ID:", min_value=101, max_value=105, step=1, key="search_pid")
    found = next((p for p in products if p["pid"] == pid), None)
    if found:
        st.success(f"Found → {found['name']} | Category:{found['category']} | Price:{found['price']} | Stock:{found['stock']}")
    else:
        st.error("❌ Product not found!")

# 3. Purchase Product
elif choice == "Purchase Product":
    pid = st.number_input("Enter Product ID:", min_value=101, max_value=105, step=1, key="purchase_pid")
    qty = st.number_input("Enter Quantity:", min_value=1, step=1, key="purchase_qty")
    discount = st.number_input("Enter Discount %:", min_value=0, step=1, key="purchase_discount")

    product = next((p for p in products if p["pid"] == pid), None)
    if product:
        if product["stock"] >= qty:
            total = product["price"] * qty
            discount_amt = total * (discount / 100)
            final_price = total - discount_amt
            product["stock"] -= qty
            st.session_state.transaction_id += 1
            st.session_state.sales.append((
                st.session_state.transaction_id, pid, product["name"], qty, final_price,
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ))
            st.success(f"✅ Purchase Successful! Transaction ID: {st.session_state.transaction_id}")
            st.info(f"Bill → Total: ₹{total}, Discount: ₹{discount_amt}, Final: ₹{final_price}")
        else:
            st.error("❌ Insufficient stock!")
    else:
        st.error("❌ Product not found!")

# 4. View Sales History
elif choice == "View Sales History":
    st.subheader("Sales History")
    for s in st.session_state.sales:
        st.write(f"TID:{s[0]} | PID:{s[1]} | Name:{s[2]} | Qty:{s[3]} | Total:₹{s[4]} | Date:{s[5]}")

# 5. Sales Analysis
elif choice == "Sales Analysis":
    st.subheader("Sales Analysis")
    total_sales = sum(s[4] for s in st.session_state.sales)
    st.write(f"Total Sales: ₹{total_sales}")
    if st.session_state.sales:
        best_product = max(st.session_state.sales, key=lambda x: x[3])
        st.write(f"Best Selling Product: {best_product[2]}")

# 6. Low Stock Products
elif choice == "Low Stock Products":
    st.subheader("Low Stock Products")
    for p in products:
        if p["stock"] <= 10:
            st.warning(f"{p['name']} → Stock:{p['stock']}")

# 7. Exit
elif choice == "Exit":
    st.write("Exiting... Thank you!")
