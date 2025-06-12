import streamlit as st
import matplotlib.pyplot as plt
from sympy import sympify, expand
import re

fixed_values = {"a": 3, "b": 2}

def preprocess_expression(expr):
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    expr = re.sub(r'(\d)\(', r'\1*(', expr)
    return expr.replace("^", "**")

def regular_triangle(x_center, y_center, size):
    # 正三角形（頂点が上、底辺が下）
    h = size * (3 ** 0.5) / 2
    return [
        (x_center, y_center + h / 2),
        (x_center - size / 2, y_center - h / 2),
        (x_center + size / 2, y_center - h / 2)
    ], h

def draw_diagram(mode):
    fig, ax = plt.subplots(figsize=(7, 1.5))
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 2)
    ax.axis('off')

    y = 1.0  # 全ての図形・文字・矢印のy座標を統一
    rect_w, rect_h = 1.0, 0.8
    tri_size = rect_w  # 三角形の底辺の長さを四角形の幅に合わせる

    # 入れる数の位置（左）
    input_x = 0.8

    # 四角形と三角形の中心x座標
    if mode == "add_then_mul":
        rect_x = 2.5
        tri_x = 4.5
    else:
        tri_x = 2.5
        rect_x = 4.5

    # 結果表示の位置（右）
    result_x = 6.2

    # 入力値表示（数字）
    ax.text(input_x, y, "0", ha='center', va='center', fontsize=20, fontweight='bold', color="#444")  # 仮の数字

    # 四角形描画
    rect = plt.Rectangle((rect_x - rect_w / 2, y - rect_h / 2), rect_w, rect_h,
                         facecolor='lightblue', edgecolor='black', linewidth=2)
    ax.add_patch(rect)

    # 四角形内の文字
    rect_label = "b" if mode == "add_then_mul" else "-3b"
    ax.text(rect_x, y, rect_label, ha='center', va='center', fontsize=18, fontweight='bold', color="#0D3B66")

    # 三角形描画
    tri_points, tri_h = regular_triangle(tri_x, y, tri_size)
    tri = plt.Polygon(tri_points, closed=True, facecolor='lightgreen', edgecolor='black', linewidth=2)
    ax.add_patch(tri)

    # 三角形内の文字
    tri_label = "2a" if mode == "add_then_mul" else "a"
    ax.text(tri_x, y, tri_label, ha='center', va='center', fontsize=18, fontweight='bold', color="#006400")

    # 矢印（四角→三角 or 三角→四角）
    arrow_params = dict(arrowstyle="->", linewidth=3, color="#333333")
    if mode == "add_then_mul":
        ax.annotate("", xy=(tri_x - tri_size / 2 - 0.05, y), xytext=(rect_x + rect_w / 2 + 0.05, y),
                    arrowprops=arrow_params)
    else:
        ax.annotate("", xy=(rect_x - rect_w / 2 - 0.05, y), xytext=(tri_x + tri_size / 2 + 0.05, y),
                    arrowprops=arrow_params)

    # 結果表示位置の初期表示（0）
    ax.text(result_x, y, "0", ha='center', va='center', fontsize=20, fontweight='bold', color="#444")

    return fig, input_x, result_x

st.set_page_config(page_title="図形と式の計算", layout="centered")
st.title("図形と式の計算（Streamlit版）")

mode = st.radio("計算の順番を選択してください", ["add_then_mul", "mul_then_add"],
                format_func=lambda x: "四角→三角" if x == "add_then_mul" else "三角→四角")

# 入力欄は図形の上に独立配置
expr_str = st.text_input("入れる数や式を入力してください（例: 7, 3*a, 2+5）")

fig, input_x, result_x = draw_diagram(mode)

# 計算結果の表示文字列（初期は0）
result_display = "0"
input_display = "0"

if expr_str:
    try:
        expr = sympify(preprocess_expression(expr_str))
        a, b = fixed_values["a"], fixed_values["b"]

        if mode == "add_then_mul":
            res = expand((expr + b) * (2 * a))
        else:
            res = expand(expr * a + (-3 * b))

        res_num = res.subs(fixed_values).evalf()
        # 小数点以下切り捨てて整数表示
        res_int = int(res_num)
        result_display = str(res_int)

        # 入力は文字列をevalして値を求め、整数なら整数表示
        expr_val = expr.subs(fixed_values).evalf()
        input_display = str(int(expr_val)) if expr_val == int(expr_val) else str(expr_val)

    except Exception:
        result_display = "エラー"
        input_display = expr_str

# Matplotlibのテキストを上書きして、入力・結果数字を並べるためにキャンバスを再描画
fig, ax = plt.subplots(figsize=(7, 1.5))
ax.set_xlim(0, 7)
ax.set_ylim(0, 2)
ax.axis('off')

y = 1.0
rect_w, rect_h = 1.0, 0.8
tri_size = rect_w

if mode == "add_then_mul":
    rect_x = 2.5
    tri_x = 4.5
else:
    tri_x = 2.5
    rect_x = 4.5

# 入力値表示（左）
ax.text(input_x, y, input_display, ha='center', va='center', fontsize=20, fontweight='bold', color="#444")

# 四角形描画
rect = plt.Rectangle((rect_x - rect_w / 2, y - rect_h / 2), rect_w, rect_h,
                     facecolor='lightblue', edgecolor='black', linewidth=2)
ax.add_patch(rect)
rect_label = "b" if mode == "add_then_mul" else "-3b"
ax.text(rect_x, y, rect_label, ha='center', va='center', fontsize=18, fontweight='bold', color="#0D3B66")

# 三角形描画
tri_points, tri_h = regular_triangle(tri_x, y, tri_size)
tri = plt.Polygon(tri_points, closed=True, facecolor='lightgreen', edgecolor='black', linewidth=2)
ax.add_patch(tri)
tri_label = "2a" if mode == "add_then_mul" else "a"
ax.text(tri_x, y, tri_label, ha='center', va='center', fontsize=18, fontweight='bold', color="#006400")

# 矢印描画
arrow_params = dict(arrowstyle="->", linewidth=3, color="#333333")
if mode == "add_then_mul":
    ax.annotate("", xy=(tri_x - tri_size / 2 - 0.05, y), xytext=(rect_x + rect_w / 2 + 0.05, y),
                arrowprops=arrow_params)
else:
    ax.annotate("", xy=(rect_x - rect_w / 2 - 0.05, y), xytext=(tri_x + tri_size / 2 + 0.05, y),
                arrowprops=arrow_params)

# 結果表示（右）
ax.text(result_x, y, result_display, ha='center', va='center', fontsize=20, fontweight='bold', color="#444")

st.pyplot(fig)
