# app.py

import streamlit as st
from sympy import sympify, expand
import re

# 固定値
fixed_values = {"a": 3, "b": 2}

def preprocess_expression(expr):
    import re
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    expr = re.sub(r'(\d)\(', r'\1*(', expr)
    expr = expr.replace("^", "**")
    return expr

def display_expression(expr):
    return str(expr).replace("*", "")

# ページ設定
st.set_page_config(page_title="図形と式の計算", layout="centered")
st.title("図形と式の計算")
st.write("図形に書かれた式に従って、もとの数や式を変形します。")

# 操作モード
mode = st.radio(
    "計算の順番を選んでください：",
    ("四角 → 三角（+して×）", "三角 → 四角（×して+）")
)

# 入力
input_str = st.text_input("もとの数や式を入力してください：", key="input_expr")

# 図形内の固定式を表示
if mode == "四角 → 三角（+して×）":
    st.markdown("#### 四角に入っている式：`b`")
    st.markdown("#### 三角に入っている式：`2a`")
else:
    st.markdown("#### 三角に入っている式：`a`")
    st.markdown("#### 四角に入っている式：`-3b`")

# 計算ボタン
if st.button("計算する"):
    try:
        if not input_str.strip():
            st.error("入力が空です。")
        else:
            input_expr = sympify(preprocess_expression(input_str))

            a = fixed_values["a"]
            b = fixed_values["b"]

            if mode == "四角 → 三角（+して×）":
                result = expand((input_expr + b) * (2 * a))
            else:
                result = expand(input_expr * a + (-3 * b))

            result_num = result.subs(fixed_values)

            st.success(f"結果： {result_num}")
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
