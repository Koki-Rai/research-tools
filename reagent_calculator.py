import streamlit as st
import pandas as pd
import numpy as np

st.title("試薬必要量計算ツール")
st.markdown("分子量または原液濃度と終濃度を入力すると、各試薬の必要量が計算されます。")
st.subheader("総体積 (L)")
st.markdown("調整したい試料の体積を入力してください。")
total_volume = st.number_input("総体積 (L)", min_value=0.0, value=0.0,  label_visibility="collapsed")

st.subheader("固体試薬")
st.markdown("各固体試料の名前・分子量・終濃度*を入力してください。")
# 初期データ(空の行を1つ用意しておくパターン)
df_sol = pd.DataFrame(
    {"試薬名": [""], "分子量 (g/mol)": [0.0], "終濃度 (M)": [0.0], "必要量 (g)": [0.0]}
)

edited_sol = st.data_editor(
    df_sol,
    num_rows="dynamic",   # これでユーザーが行を追加・削除できる
    key="solid",          # 複数の表を置くとき衝突しないよう key を付ける
)
st.subheader("液体試薬")
st.markdown("各液体試料の名前・原液濃度・終濃度*を入力してください。")
# 初期データ(空の行を1つ用意しておくパターン)
df_liq = pd.DataFrame(
    {"試薬名": [""], "原液濃度 (M)": [0.0], "終濃度 (M)": [0.0], "必要量 (L)": [0.0]}
)

edited_liq = st.data_editor(
    df_liq,
    num_rows="dynamic",   # これでユーザーが行を追加・削除できる
    key="liquid",         # 複数の表を置くとき衝突しないよう key を付ける
)

if st.button("計算"):
    # 固体
    edited_sol["必要量 (g)"] = edited_sol["分子量 (g/mol)"] * edited_sol["終濃度 (M)"] * total_volume
    st.dataframe(edited_sol, hide_index=True)
    # 液体
    edited_liq["必要量 (L)"] = edited_liq["終濃度 (M)"] / edited_liq["原液濃度 (M)"] * total_volume
    edited_liq["必要量 (L)"] = edited_liq["必要量 (L)"].replace([np.inf, -np.inf], 0.0).fillna(0.0)
    st.dataframe(edited_liq, hide_index=True)
    # 溶媒量
    st.subheader("溶媒量 (L)")
    solvent = total_volume - edited_liq["必要量 (L)"].sum()
    st.write(solvent)