"""
คำนวณแรงปฏิกิริยาเสาเข็มเมื่อเกิดการเยื้องศูนย์
อ้างอิงสูตร: Bakhoum (1992) — มยผ.1106-64

รันด้วย:
    pip install matplotlib
    python pile_calc.py
"""

import math
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.rcParams['font.family'] = 'Tahoma'


# ─────────────────────────────────────────────────────
# ตำแหน่ง layout มาตรฐาน
# ─────────────────────────────────────────────────────
def get_nom_positions(n, S):
    if n == 2:
        return [(-S/2, 0), (S/2, 0)]
    elif n == 3:
        h = S * math.sqrt(3) / 2
        return [(-S/2, -h/3), (S/2, -h/3), (0, 2*h/3)]
    elif n == 4:
        return [(-S/2, -S/2), (S/2, -S/2), (S/2, S/2), (-S/2, S/2)]
    elif n == 5:
        return [(-S/2, -S/2), (S/2, -S/2), (S/2, S/2), (-S/2, S/2), (0, 0)]
    elif n == 6:
        return [(-S, -S/2), (0, -S/2), (S, -S/2),
                (-S,  S/2), (0,  S/2), (S,  S/2)]


# ─────────────────────────────────────────────────────
# คำนวณ
# ─────────────────────────────────────────────────────
def calculate(Q, Qsafe, n, S, ex_arr, ey_arr):
    nom = get_nom_positions(n, S)
    ax_ = [nom[i][0] + ex_arr[i] for i in range(n)]
    ay_ = [nom[i][1] + ey_arr[i] for i in range(n)]

    Xbar = sum(ax_) / n
    Ybar = sum(ay_) / n
    Mx   = Q * Ybar
    My   = Q * Xbar

    xi = [ax_[i] - Xbar for i in range(n)]
    yi = [ay_[i] - Ybar for i in range(n)]

    sumX2 = sum(x**2 for x in xi)
    sumY2 = sum(y**2 for y in yi)
    sumXY = sum(xi[i]*yi[i] for i in range(n))
    denom = sumX2*sumY2 - sumXY**2

    if abs(sumXY) < 1e-9 or abs(denom) < 1e-9:
        Pi = [
            Q/n
            + (My*xi[i]/sumX2 if sumX2 > 1e-9 else 0)
            + (Mx*yi[i]/sumY2 if sumY2 > 1e-9 else 0)
            for i in range(n)
        ]
    else:
        m  = (My*sumY2 - Mx*sumXY) / denom
        nv = (Mx*sumX2 - My*sumXY) / denom
        Pi = [Q/n + m*xi[i] + nv*yi[i] for i in range(n)]

    return dict(nom=nom, ax=ax_, ay=ay_, Xbar=Xbar, Ybar=Ybar,
                Mx=Mx, My=My, xi=xi, yi=yi,
                sumX2=sumX2, sumY2=sumY2, sumXY=sumXY, Pi=Pi)


# ─────────────────────────────────────────────────────
# วาดแผนภาพ
# ─────────────────────────────────────────────────────
def draw_diagram(ax, res, S, ex_arr, ey_arr):
    ax.clear()
    ax.set_facecolor("#F9F8F5")
    ax.set_aspect("equal")
    ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.4, color="#aaa")
    ax.axhline(0, color="#bbb", linewidth=0.6, linestyle="--")
    ax.axvline(0, color="#bbb", linewidth=0.6, linestyle="--")

    nom     = res["nom"]
    actual_x= res["ax"]
    actual_y= res["ay"]
    Xbar    = res["Xbar"]
    Ybar    = res["Ybar"]
    n       = len(nom)

    # กล่องฐานราก
    pad = S * 0.4
    bx1, bx2 = min(actual_x)-pad, max(actual_x)+pad
    by1, by2 = min(actual_y)-pad, max(actual_y)+pad
    rect = mpatches.FancyBboxPatch(
        (bx1, by1), bx2-bx1, by2-by1,
        boxstyle="round,pad=0", linewidth=0.8,
        edgecolor="#aaa", facecolor="#378ADD11"
    )
    ax.add_patch(rect)

    r = S * 0.07

    # ตำแหน่งออกแบบ (วงกลมประ)
    for p in nom:
        c = plt.Circle(p, r, color="#378ADD", fill=False,
                       linestyle="--", linewidth=1.5)
        ax.add_patch(c)

    # เส้นเยื้อง + วงกลมตำแหน่งจริง
    for i in range(n):
        nx, ny = nom[i]
        axi, ayi = actual_x[i], actual_y[i]

        if ex_arr[i] != 0 or ey_arr[i] != 0:
            ax.annotate("", xy=(axi, ayi), xytext=(nx, ny),
                        arrowprops=dict(arrowstyle="->",
                                        color="#EF9F27", lw=1.8))

        c2 = plt.Circle((axi, ayi), r, color="#D85A30",
                        fill=True, alpha=0.15, linewidth=0)
        ax.add_patch(c2)
        c3 = plt.Circle((axi, ayi), r, color="#D85A30",
                        fill=False, linewidth=2)
        ax.add_patch(c3)
        ax.text(axi, ayi, str(i+1), ha="center", va="center",
                fontsize=9, fontweight="bold", color="#2C2C2A")

        if ex_arr[i] != 0 or ey_arr[i] != 0:
            lbl = f"({ex_arr[i]:+g},{ey_arr[i]:+g})"
            ax.text(axi, ayi + r*1.6, lbl, ha="center",
                    fontsize=8, color="#EF9F27")

    # Centroid ใหม่
    if abs(Xbar) > 0.01 or abs(Ybar) > 0.01:
        ax.plot(Xbar, Ybar, "+", color="#1D9E75",
                markersize=16, markeredgewidth=2.5)
        ax.plot(Xbar, Ybar, "o", color="#1D9E75", markersize=5)
        ax.annotate(f"  Centroid ใหม่\n  ({Xbar:.2f}, {Ybar:.2f})",
                    xy=(Xbar, Ybar), fontsize=8, color="#1D9E75", va="bottom")

    # O(0,0)
    ax.plot(0, 0, "o", color="#888780", markersize=5)
    ax.text(0, 0, "  O(0,0)", fontsize=8, color="#888780", va="bottom")

    leg_handles = [
        mpatches.Patch(edgecolor="#378ADD", facecolor="none",
                       linestyle="--", label="ตำแหน่งออกแบบ"),
        mpatches.Patch(edgecolor="#D85A30", facecolor="#D85A3030",
                       label="ตำแหน่งจริง (เยื้อง)"),
        mpatches.Patch(color="#EF9F27", label="ระยะเยื้อง"),
        mpatches.Patch(color="#1D9E75", label="Centroid ใหม่"),
    ]
    ax.legend(handles=leg_handles, fontsize=8, loc="upper right",
              framealpha=0.9)
    ax.set_xlabel("X (cm)", fontsize=9)
    ax.set_ylabel("Y (cm)", fontsize=9)
    ax.set_title("ผังตำแหน่งเสาเข็ม", fontsize=11)


# ─────────────────────────────────────────────────────
# GUI หลัก
# ─────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("คำนวณแรงปฏิกิริยาเสาเข็มเยื้องศูนย์")
        self.configure(bg="#F5F4F0")
        self.resizable(True, True)

        self.pile_ex = []
        self.pile_ey = []
        self._build_ui()

    # ── สร้าง UI ──────────────────────────────────
    def _build_ui(self):
        # ── LEFT PANEL ────────────────────────────
        left = tk.Frame(self, bg="#F5F4F0", padx=12, pady=12)
        left.grid(row=0, column=0, sticky="nsew")

        self._section(left, "พารามิเตอร์หลัก", 0)

        params = tk.Frame(left, bg="#fff", bd=0, relief="flat",
                          highlightbackground="#ddd", highlightthickness=1)
        params.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        self.Q      = self._entry_row(params, 0, "น้ำหนักบรรทุก Q (ตัน)", "100")
        self.Qsafe  = self._entry_row(params, 1, "น้ำหนักปลอดภัย (ตัน/ต้น)", "40")
        self.S_var  = self._entry_row(params, 2, "ระยะห่างเสาเข็ม S (cm)", "120")

        # slider จำนวนเสาเข็ม
        tk.Label(params, text="จำนวนเสาเข็ม (n)",
                 bg="#fff", font=("Tahoma", 10),
                 fg="#5F5E5A").grid(row=3, column=0, sticky="w",
                                   padx=10, pady=4)
        self.n_var = tk.IntVar(value=4)
        frm_sl = tk.Frame(params, bg="#fff")
        frm_sl.grid(row=3, column=1, sticky="w", padx=10)
        sl = tk.Scale(frm_sl, from_=2, to=6, orient="horizontal",
                      variable=self.n_var, length=120, bg="#fff",
                      command=lambda _: self._rebuild_pile_inputs())
        sl.pack(side="left")
        self.n_label = tk.Label(frm_sl, text="4 ต้น", bg="#fff",
                                font=("Tahoma", 10, "bold"), fg="#2C2C2A")
        self.n_label.pack(side="left", padx=4)

        # ── pile input area ───────────────────────
        self._section(left, "ระยะเยื้องศูนย์แต่ละต้น (cm)", 2)

        note = tk.Label(left,
            text="+eₓ=ขวา  −eₓ=ซ้าย  +ey=ขึ้น  −ey=ลง",
            bg="#E6F1FB", fg="#185FA5", font=("Tahoma", 9),
            padx=8, pady=4)
        note.grid(row=3, column=0, sticky="ew", pady=(0, 6))

        self.pile_frame = tk.Frame(left, bg="#F5F4F0")
        self.pile_frame.grid(row=4, column=0, sticky="ew")
        self._rebuild_pile_inputs()

        # คำนวณ button
        btn = tk.Button(left, text="คำนวณแรงปฏิกิริยา",
                        command=self._calculate,
                        bg="#2C2C2A", fg="white",
                        font=("Tahoma", 11, "bold"),
                        relief="flat", padx=10, pady=8,
                        cursor="hand2")
        btn.grid(row=5, column=0, sticky="ew", pady=10)

        # ── result text ───────────────────────────
        self._section(left, "ผลลัพธ์", 6)
        self.result_text = tk.Text(left, width=38, height=18,
                                   font=("Courier New", 9),
                                   bg="#fff", fg="#2C2C2A",
                                   relief="flat", bd=1,
                                   highlightbackground="#ddd",
                                   highlightthickness=1)
        self.result_text.grid(row=7, column=0, sticky="ew")
        left.columnconfigure(0, weight=1)

        # ── RIGHT PANEL (matplotlib) ───────────────
        right = tk.Frame(self, bg="#F5F4F0", padx=8, pady=12)
        right.grid(row=0, column=1, sticky="nsew")

        self.fig, self.ax_plot = plt.subplots(figsize=(6, 5.5))
        self.fig.patch.set_facecolor("#F5F4F0")
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    # ── helpers ───────────────────────────────────
    def _section(self, parent, text, row):
        tk.Label(parent, text=text.upper(),
                 bg="#F5F4F0", fg="#5F5E5A",
                 font=("Tahoma", 9, "bold")).grid(
            row=row, column=0, sticky="w", pady=(10, 2))

    def _entry_row(self, parent, row, label, default):
        tk.Label(parent, text=label, bg="#fff",
                 font=("Tahoma", 10), fg="#5F5E5A").grid(
            row=row, column=0, sticky="w", padx=10, pady=4)
        var = tk.StringVar(value=default)
        e = tk.Entry(parent, textvariable=var, width=10,
                     font=("Tahoma", 10), bg="#F1EFE8",
                     relief="flat", bd=1,
                     highlightbackground="#ccc", highlightthickness=1)
        e.grid(row=row, column=1, sticky="w", padx=10, pady=4)
        return var

    def _rebuild_pile_inputs(self):
        n = self.n_var.get()
        self.n_label.config(text=f"{n} ต้น")
        for w in self.pile_frame.winfo_children():
            w.destroy()
        self.pile_ex = []
        self.pile_ey = []
        for i in range(n):
            frm = tk.Frame(self.pile_frame, bg="#F1EFE8", bd=0,
                           highlightbackground="#ddd", highlightthickness=1)
            frm.grid(row=i//4, column=i%4, padx=4, pady=4, sticky="ew")

            tk.Label(frm, text=f"ต้นที่ {i+1}", bg="#F1EFE8",
                     font=("Tahoma", 9, "bold"), fg="#2C2C2A").grid(
                row=0, column=0, columnspan=3, sticky="w", padx=6, pady=(4, 0))

            ex_var = tk.StringVar(value="0")
            ey_var = tk.StringVar(value="0")

            tk.Label(frm, text="eₓ", bg="#F1EFE8",
                     font=("Tahoma", 9), fg="#5F5E5A").grid(
                row=1, column=0, padx=(6,2), pady=2)
            tk.Entry(frm, textvariable=ex_var, width=6,
                     font=("Tahoma", 9), bg="#fff",
                     relief="flat", bd=1,
                     highlightbackground="#ccc", highlightthickness=1).grid(
                row=1, column=1, pady=2)
            tk.Label(frm, text="cm", bg="#F1EFE8",
                     font=("Tahoma", 9), fg="#888").grid(row=1, column=2, padx=2)

            tk.Label(frm, text="e_y", bg="#F1EFE8",
                     font=("Tahoma", 9), fg="#5F5E5A").grid(
                row=2, column=0, padx=(6,2), pady=(0,4))
            tk.Entry(frm, textvariable=ey_var, width=6,
                     font=("Tahoma", 9), bg="#fff",
                     relief="flat", bd=1,
                     highlightbackground="#ccc", highlightthickness=1).grid(
                row=2, column=1, pady=(0,4))
            tk.Label(frm, text="cm", bg="#F1EFE8",
                     font=("Tahoma", 9), fg="#888").grid(row=2, column=2, padx=2)

            self.pile_ex.append(ex_var)
            self.pile_ey.append(ey_var)

    # ── คำนวณและแสดงผล ────────────────────────────
    def _calculate(self):
        try:
            Q     = float(self.Q.get())
            Qsafe = float(self.Qsafe.get())
            n     = self.n_var.get()
            S     = float(self.S_var.get())
            ex_arr= [float(v.get()) for v in self.pile_ex]
            ey_arr= [float(v.get()) for v in self.pile_ey]
        except ValueError:
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกตัวเลขให้ครบถ้วน")
            return

        res = calculate(Q, Qsafe, n, S, ex_arr, ey_arr)

        # ── text result ───────────────────────────
        self.result_text.delete("1.0", "end")
        self.result_text.insert("end",
            f"{'─'*36}\n"
            f"  จุด Centroid ใหม่\n"
            f"  X̄ = {res['Xbar']:8.3f} cm\n"
            f"  Ȳ = {res['Ybar']:8.3f} cm\n"
            f"  Mₓ = Q × Ȳ = {res['Mx']:8.2f} ตัน-cm\n"
            f"  My = Q × X̄ = {res['My']:8.2f} ตัน-cm\n"
            f"  Σx² = {res['sumX2']:8.2f} cm²\n"
            f"  Σy² = {res['sumY2']:8.2f} cm²\n"
            f"  Σxy = {res['sumXY']:8.2f} cm²\n"
            f"{'─'*36}\n"
            f"  แรงปฏิกิริยาแต่ละต้น\n"
            f"{'─'*36}\n"
        )
        for i, p in enumerate(res["Pi"]):
            pct = p / Qsafe * 100
            status = "OK" if pct <= 80 else ("เฝ้าระวัง" if pct <= 100 else "เกิน!")
            self.result_text.insert("end",
                f"  ต้น {i+1}: x={res['xi'][i]:6.2f} y={res['yi'][i]:6.2f}\n"
                f"         P = {p:8.3f} ตัน  ({pct:.0f}%) {status}\n"
            )
        self.result_text.insert("end", f"{'─'*36}\n")

        # ── แผนภาพ ───────────────────────────────
        draw_diagram(self.ax_plot, res, S, ex_arr, ey_arr)
        self.canvas.draw()


# ─────────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
