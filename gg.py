import streamlit as st
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ตั้งค่าหน้ากระดาษ
st.set_page_config(page_title="Pile Deviation Calc", layout="wide")

# ─────────────────────────────────────────────────────
# ฟังก์ชันคำนวณ (Logic เดิมจาก Bakhoum 1992)
# ─────────────────────────────────────────────────────
def get_nom_positions(n, S):
    if n == 2: return [(-S/2, 0), (S/2, 0)]
    elif n == 3:
        h = S * math.sqrt(3) / 2
        return [(-S/2, -h/3), (S/2, -h/3), (0, 2*h/3)]
    elif n == 4: return [(-S/2, -S/2), (S/2, -S/2), (S/2, S/2), (-S/2, S/2)]
    elif n == 5: return [(-S/2, -S/2), (S/2, -S/2), (S/2, S/2), (-S/2, S/2), (0, 0)]
    elif n == 6: return [(-S, -S/2), (0, -S/2), (S, -S/2), (-S, S/2), (0, S/2), (S, S/2)]
    return []

def calculate(Q, n, S, ex_arr, ey_arr):
    nom = get_nom_positions(n, S)
    ax_ = [nom[i][0] + ex_arr[i] for i in range(n)]
    ay_ = [nom[i][1] + ey_arr[i] for i in range(n)]

    Xbar = sum(ax_) / n
    Ybar = sum(ay_) / n
    Mx = Q * Ybar
    My = Q * Xbar

    xi = [ax_[i] - Xbar for i in range(n)]
    yi = [ay_[i] - Ybar for i in range(n)]

    sumX2 = sum(x**2 for x in xi)
    sumY2 = sum(y**2 for y in yi)
    sumXY = sum(xi[i]*yi[i] for i in range(n))
    denom = sumX2*sumY2 - sumXY**2

    if abs(sumXY) < 1e-9 or abs(denom) < 1e-9:
        Pi = [Q/n + (My*xi[i]/sumX2 if sumX2 > 1e-9 else 0) + (Mx*yi[i]/sumY2 if sumY2 > 1e-9 else 0) for i in range(n)]
    else:
        m = (My*sumY2 - Mx*sumXY) / denom
        nv = (Mx*sumX2 - My*sumXY) / denom
        Pi = [Q/n + m*xi[i] + nv*yi[i] for i in range(n)]

    return dict(nom=nom, ax=ax_, ay=ay_, Xbar=Xbar, Ybar=Ybar, Mx=Mx, My=My, xi=xi, yi=yi, sumX2=sumX2, sumY2=sumY2, sumXY=sumXY, Pi=Pi)

# ─────────────────────────────────────────────────────
# UI Section
# ─────────────────────────────────────────────────────
st.title("🏗️ คำนวณแรงปฏิกิริยาเสาเข็มเยื้องศูนย์")
st.caption("อ้างอิง: Bakhoum (1992) — มยผ.1106-64")

with st.sidebar:
    st.header("พารามิเตอร์หลัก")
    Q = st.number_input("น้ำหนักบรรทุก Q (ตัน)", value=100.0)
    Qsafe = st.number_input("น้ำหนักปลอดภัย Q_safe (ตัน/ต้น)", value=40.0)
    S = st.number_input("ระยะห่างเสาเข็ม S (cm)", value=120.0)
    n = st.slider("จำนวนเสาเข็ม (n)", 2, 6, 4)

st.subheader("📍 ระยะเยื้องศูนย์แต่ละต้น (cm)")
cols = st.columns(n)
ex_arr = []
ey_arr = []

for i in range(n):
    with cols[i]:
        st.write(f"**ต้นที่ {i+1}**")
        ex = st.number_input(f"ex (ต้นที่ {i+1})", value=0.0, key=f"ex_{i}")
        ey = st.number_input(f"ey (ต้นที่ {i+1})", value=0.0, key=f"ey_{i}")
        ex_arr.append(ex)
        ey_arr.append(ey)

# ─────────────────────────────────────────────────────
# การคำนวณและแสดงผล
# ─────────────────────────────────────────────────────
res = calculate(Q, n, S, ex_arr, ey_arr)

col_res, col_plot = st.columns([1, 1.2])

with col_res:
    st.subheader("📊 ผลการคำนวณ")
    st.info(f"**Centroid ใหม่:** ({res['Xbar']:.3f}, {res['Ybar']:.3f}) cm")
    
    # ตารางสรุปแรง
    data_list = []
    for i, p in enumerate(res["Pi"]):
        pct = p / Qsafe * 100
        status = "✅ OK" if pct <= 80 else ("⚠️ เฝ้าระวัง" if pct <= 100 else "❌ เกิน!")
        data_list.append({
            "ต้นที่": i+1,
            "แรง P (ตัน)": round(p, 3),
            "Ratio (%)": f"{pct:.1f}%",
            "สถานะ": status
        })
    st.table(data_list)
    
    with st.expander("ดูค่าทางวิศวกรรม (Properties)"):
        st.write(f"Mx: {res['Mx']:.2f} t-cm")
        st.write(f"My: {res['My']:.2f} t-cm")
        st.write(f"Σx²: {res['sumX2']:.2f} | Σy²: {res['sumY2']:.2f} | Σxy: {res['sumXY']:.2f}")

with col_plot:
    st.subheader("🎨 ผังตำแหน่งเสาเข็ม")
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect("equal")
    ax.grid(True, linestyle="--", alpha=0.5)
    
    # วาด Pad
    pad = S * 0.5
    ax.set_xlim(min(res['ax'])-pad, max(res['ax'])+pad)
    ax.set_ylim(min(res['ay'])-pad, max(res['ay'])+pad)
    
    r = S * 0.08
    for i in range(n):
        # ตำแหน่งออกแบบ
        ax.add_patch(plt.Circle(res['nom'][i], r, color="#378ADD", fill=False, linestyle="--"))
        # ตำแหน่งจริง
        ax.add_patch(plt.Circle((res['ax'][i], res['ay'][i]), r, color="#D85A30", alpha=0.3))
        ax.text(res['ax'][i], res['ay'][i], str(i+1), ha="center", va="center", fontweight="bold")

    # จุด Centroid ใหม่
    ax.plot(res['Xbar'], res['Ybar'], "X", color="#1D9E75", markersize=10, label="New Centroid")
    ax.axhline(0, color="black", lw=0.5)
    ax.axvline(0, color="black", lw=0.5)
    
    st.pyplot(fig)
