import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(layout="centered")

st.title("図形を使った計算")

# 入力フィールド
user_input = st.text_input("入れる数", "")

# 定数定義
a_val = 3
b_val = 2

# 計算（三角→四角→結果）
try:
    user_expr = sp.sympify(user_input)
    a, b = sp.symbols('a b')
    triangle_expr = a
    rect_expr = -3 * b

    # 代入して数値結果を計算
    result_expr = (triangle_expr.subs({a: a_val}) * user_expr) + rect_expr.subs({b: b_val})
    result_simplified = sp.simplify(result_expr)

    # 結果を文字列に
    result_display = str(result_simplified)
except Exception as e:
    result_display = f"エラー: {e}"

# 描画関数
def draw_diagram():
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.set_xlim(0, 600)
    ax.set_ylim(0, 200)
    ax.set_aspect('equal')
    ax.axis('off')

    # 三角形（左）
    triangle = patches.Polygon([[100, 140], [60, 100], [140, 100]], closed=True, facecolor='lightgreen', edgecolor='black')
    ax.add_patch(triangle)
    ax.text(100, 120, "a", ha='center', va='center', fontsize=14)

    # 矢印1
    ax.annotate("", xy=(200, 120), xytext=(150, 120),
                arrowprops=dict(arrowstyle="->", linewidth=2))

    # 四角形（中央）
    rect = patches.Rectangle((240, 100), 60, 40, facecolor='lightblue', edgecolor='black')
    ax.add_patch(rect)
    ax.text(270, 120, "-3b", ha='center', va='center', fontsize=14)

    # 矢印2
    ax.annotate("", xy=(370, 120), xytext=(320, 120),
                arrowprops=dict(arrowstyle="->", linewidth=2))

    # 結果
    ax.text(400, 120, result_display, ha='left', va='center', fontsize=14)

    st.pyplot(fig)

# 描画実行
draw_diagram()
