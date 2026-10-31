
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="ReliefRoute | Disaster Resource Allocation", page_icon="🚑", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
.hero {padding: 1.25rem 1.5rem; border-radius: 16px; background: linear-gradient(120deg,#0b2545,#134074); color: white; margin-bottom: 1rem;}
.hero h1 {color: white; margin-bottom: .25rem;}
.hero p {color: #e5eef8; margin-bottom: 0;}
.small-note {font-size: .85rem; color: #64748b;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>🚑 ReliefRoute</h1>
<p>Intelligent Disaster Relief Resource Allocation & Decision Support Simulator</p>
</div>
""", unsafe_allow_html=True)

st.info("Educational prototype using simulated data. Allocation suggestions support planning demonstrations; they are not for real emergency operations.")

def sample_data():
    return pd.DataFrame({
        "Area": ["Riverside", "Old Town", "Central Ward", "Hillview"],
        "People Affected": [800, 450, 650, 300],
        "Urgency (1-5)": [5, 4, 3, 5],
        "Food Need (packets)": [500, 300, 400, 200],
        "Water Need (litres)": [1200, 700, 900, 500],
        "Medical Kits Need": [100, 80, 90, 60],
    })

if "areas" not in st.session_state:
    st.session_state.areas = sample_data()

with st.sidebar:
    st.header("⚙️ Scenario Settings")
    st.caption("Edit the sample data or enter your own simulated scenario.")
    total_food = st.number_input("Available food packets", min_value=0, max_value=100000, value=800, step=50)
    total_water = st.number_input("Available water (litres)", min_value=0, max_value=1000000, value=1800, step=100)
    total_medical = st.number_input("Available medical kits", min_value=0, max_value=100000, value=220, step=10)
    st.divider()
    method = st.selectbox("Allocation strategy", ["Priority-weighted greedy", "Proportional fair-share"])
    st.caption("Priority-weighted uses urgency and affected population. Fair-share allocates according to each area's requested quantity.")

st.subheader("1. Affected Areas & Estimated Needs")
st.write("Edit values directly in the table. Urgency ranges from 1 (lower) to 5 (critical).")
edited = st.data_editor(
    st.session_state.areas,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Area": st.column_config.TextColumn("Area name", required=True),
        "People Affected": st.column_config.NumberColumn(min_value=0, step=50),
        "Urgency (1-5)": st.column_config.NumberColumn(min_value=1, max_value=5, step=1),
        "Food Need (packets)": st.column_config.NumberColumn(min_value=0, step=10),
        "Water Need (litres)": st.column_config.NumberColumn(min_value=0, step=50),
        "Medical Kits Need": st.column_config.NumberColumn(min_value=0, step=5),
    }
)
st.session_state.areas = edited.copy()

def allocate_one(df, need_col, total, urgency_weight=True):
    needs = pd.to_numeric(df[need_col], errors="coerce").fillna(0).clip(lower=0).to_numpy(dtype=float)
    total = max(0, float(total))
    if len(needs) == 0:
        return np.array([])
    if needs.sum() <= total:
        return needs
    if needs.sum() == 0 or total == 0:
        return np.zeros(len(needs))
    if urgency_weight:
        urgency = pd.to_numeric(df["Urgency (1-5)"], errors="coerce").fillna(1).clip(1,5).to_numpy(dtype=float)
        people = pd.to_numeric(df["People Affected"], errors="coerce").fillna(0).clip(lower=0).to_numpy(dtype=float)
        # A transparent priority weight: urgency x (1 + normalized affected population).
        pop_factor = 1 + (people / max(people.max(), 1))
        weights = urgency * pop_factor
        scores = np.where(needs > 0, weights, 0)
    else:
        scores = needs.copy()
    allocation = np.zeros(len(needs), dtype=float)
    remaining = total
    active = needs > 0
    # Weighted water-filling: respect each area's requested need cap.
    for _ in range(len(needs) + 2):
        if remaining <= 1e-8 or not active.any():
            break
        active_scores = scores * active
        if active_scores.sum() <= 0:
            active_scores = needs * active
        proposed = remaining * active_scores / active_scores.sum()
        capacity = needs - allocation
        add = np.minimum(proposed, capacity)
        allocation += add
        used = add.sum()
        remaining -= used
        active = (needs - allocation) > 1e-8
        if used <= 1e-8:
            break
    return allocation

def round_allocations(values, needs, total):
    vals = np.floor(np.minimum(values, needs)).astype(int)
    remaining = int(max(0, round(total) - vals.sum()))
    fractions = values - np.floor(values)
    order = np.argsort(-fractions)
    for i in order:
        if remaining <= 0:
            break
        if vals[i] < int(np.floor(needs[i])):
            vals[i] += 1
            remaining -= 1
    return vals

if st.button("🚨 Generate Allocation Plan", type="primary", use_container_width=True):
    df = edited.copy()
    required = ["Area", "People Affected", "Urgency (1-5)", "Food Need (packets)", "Water Need (litres)", "Medical Kits Need"]
    if df.empty:
        st.error("Add at least one affected area.")
    elif df["Area"].astype(str).str.strip().eq("").any():
        st.error("Every row must have an area name.")
    else:
        for c in required[1:]:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
        df["Urgency (1-5)"] = df["Urgency (1-5)"].clip(1,5)
        if method == "Priority-weighted greedy":
            weighted = True
        else:
            weighted = False
        allocations = {}
        for need_col, total, out_col in [
            ("Food Need (packets)", total_food, "Food Allocated"),
            ("Water Need (litres)", total_water, "Water Allocated"),
            ("Medical Kits Need", total_medical, "Medical Kits Allocated"),
        ]:
            raw = allocate_one(df, need_col, total, urgency_weight=weighted)
            allocations[out_col] = round_allocations(raw, df[need_col].to_numpy(dtype=float), total)
        result = df[["Area", "People Affected", "Urgency (1-5)", "Food Need (packets)", "Water Need (litres)", "Medical Kits Need"]].copy()
        result["Food Allocated"] = allocations["Food Allocated"]
        result["Food Shortage"] = result["Food Need (packets)"] - result["Food Allocated"]
        result["Water Allocated"] = allocations["Water Allocated"]
        result["Water Shortage"] = result["Water Need (litres)"] - result["Water Allocated"]
        result["Medical Kits Allocated"] = allocations["Medical Kits Allocated"]
        result["Medical Shortage"] = result["Medical Kits Need"] - result["Medical Kits Allocated"]
        st.session_state.result = result
        st.session_state.method = method

if "result" in st.session_state:
    result = st.session_state.result
    st.subheader("2. Allocation Results")
    food_need = result["Food Need (packets)"].sum()
    water_need = result["Water Need (litres)"].sum()
    med_need = result["Medical Kits Need"].sum()
    food_given = result["Food Allocated"].sum()
    water_given = result["Water Allocated"].sum()
    med_given = result["Medical Kits Allocated"].sum()
    total_need = food_need + water_need + med_need
    total_given = food_given + water_given + med_given
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Food supplied", f"{food_given:,.0f} / {food_need:,.0f}")
    c2.metric("Water supplied", f"{water_given:,.0f} / {water_need:,.0f} L")
    c3.metric("Medical kits supplied", f"{med_given:,.0f} / {med_need:,.0f}")
    c4.metric("Overall demand coverage", f"{(total_given/total_need*100 if total_need else 100):.1f}%")
    st.caption(f"Strategy used: **{st.session_state.get('method', 'Priority-weighted greedy')}**")
    st.dataframe(result, use_container_width=True, hide_index=True)
    chart_df = result.melt(id_vars="Area", value_vars=["Food Allocated", "Water Allocated", "Medical Kits Allocated"], var_name="Resource", value_name="Quantity")
    fig = px.bar(chart_df, x="Area", y="Quantity", color="Resource", barmode="group", title="Allocated resources by area")
    st.plotly_chart(fig, use_container_width=True)
    shortage_df = result.melt(id_vars="Area", value_vars=["Food Shortage", "Water Shortage", "Medical Shortage"], var_name="Resource", value_name="Unmet demand")
    fig2 = px.bar(shortage_df, x="Area", y="Unmet demand", color="Resource", barmode="group", title="Remaining unmet demand")
    st.plotly_chart(fig2, use_container_width=True)
    csv = result.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download allocation report (CSV)", csv, "reliefroute_allocation_report.csv", "text/csv")
    st.success("Allocation plan generated. Review the unmet-demand columns before interpreting the result.")
else:
    st.subheader("2. Allocation Results")
    st.write("Click **Generate Allocation Plan** to calculate the distribution.")
    st.caption("The starter scenario is provided for demonstration; edit it to test different disaster conditions.")

with st.expander("🧮 How the allocation logic works"):
    st.markdown("""
    **Priority-weighted greedy strategy**
    1. Each area receives a priority weight based on urgency (1–5) and affected population.
    2. Available supplies are distributed using those weights.
    3. No area receives more than its estimated demand.
    4. The process repeats until the resource stock is exhausted or all demand is met.

    **Proportional fair-share strategy**
    - Available stock is allocated proportionally to each area's requested quantity, subject to demand caps.

    This is a simplified educational heuristic, not a validated emergency-management model. Real deployment would require verified data, logistics constraints, expert oversight and field validation.
    """)

st.markdown("---")
st.markdown('<p class="small-note">ReliefRoute prototype • Simulated data only • For academic demonstration, not operational emergency decisions.</p>', unsafe_allow_html=True)
