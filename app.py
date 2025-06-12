import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(layout="centered")

st.title("図形を使った計算")

# タブ
mode = st.radio("計算の順序を選んでください", ("四角 → 三角", "三角 → 四角"))

# 入力フィールド
user_input = st.text_input("入れる数", "")

# 定数定義
a_val = 3
b_val = 2

# 変数
a, b = sp.symbols('a b')

# 計算と図形内容の設定
if mode == "四角 → 三角":
    shape1_label = "b"
    shape2_label = "2a"
    try:
        input_expr = sp.sympify(user_input)
        result_expr = (input_expr + b_val) * (2 * a_val)
        result_display = str(sp.simplify(result_expr))
    except Exception as e:
        result_display = f"エラー: {e}"
else:
    shape1_label = "a"
    shape2_label = "-3b"
    try:
        input_expr = sp.sympify(user_input)
        result_expr = (a_val * input_expr) + (-3 * b_val)
        result_display = str(sp.simplify(result_expr))
    except Exception as e:
        result_display = f"エラー: {e}"

# 描画関数
def draw_diagram():
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.set_xlim(0, 600)
    ax.set_ylim(0, 200)
    ax.set_aspect('equal')
    ax.axis('off')

    if mode == "四角 → 三角":
        # 四角
        rect = patches.Rectangle((60, 100), 60, 40, facecolor='lightblue', edgecolor='black')
        ax.add_patch(rect)
        ax.text(90, 120, shape1_label, ha='center', va='center', fontsize=14)

        # →
        ax.annotate("", xy=(150, 120), xytext=(120, 120), arrowprops=dict(arrowstyle="->", linewidth=2))

        # 三角（底辺下向き）
        triangle = patches.Polygon([[200, 140], [160, 100], [240, 100]], closed=True, facecolor='lightgreen', edgecolor='black')
        ax.add_patch(triangle)
        ax.text(200, 120, shape2_label, ha='center', va='center', fontsize=14)

        # →
        ax.annotate("", xy=(290, 120), xytext=(250, 120), arrowprops=dict(arrowstyle="->", linewidth=2))

        # 結果
        ax.text(310, 120, result_display, ha='left', va='center', fontsize=14)

    else:
        # 三角（底辺下向き）
        triangle = patches.Polygon([[60, 140], [20, 100], [100, 100]], closed=True, facecolor='lightgreen', edgecolor='black')
        ax.add_patch(triangle)
        ax.text(60, 120, shape1_label, ha='center', va='center', fontsize=14)

        # →
        ax.annotate("", xy=(150, 120), xytext=(100, 120), arrowprops=dict(arrowstyle="->", linewidth=2))

        # 四角
        rect = patches.Rectangle((160, 100), 60, 40, facecolor='lightblue', edgecolor='black')
        ax.add_patch(rect)
        ax.text(190, 120, shape2_label, ha='center', va='center', fontsize=14)

        # →
        ax.annotate("", xy=(270, 120), xytext=(220, 120), arrowprops=dict(arrowstyle="->", linewidth=2))

        # 結果
        ax.text(290, 120, result_display, ha='left', va='center', fontsize=14)

    st.pyplot(fig)

# 描画実行
draw_diagram()
