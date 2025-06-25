import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets 認證
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Google Sheets 表單 ID
sheet_id = "1w79j08ldJIlgEuPWWo4Vi_QPOlZSUGiLSaC-p3jjMRE"
sheet = client.open_by_key(sheet_id).get_worksheet(2)  # 工作表3（從0開始）

# 讀取資料
data = sheet.get_all_records()
df = pd.DataFrame(data)

# debug：確認欄位名稱和資料內容
st.write("📋 DataFrame 欄位列表：", df.columns.tolist())
st.write("🧪 頭幾列資料：", df.head())

# 找出第一個未打標的
unmarked_rows = df[df["篩選結果"] == ""]
if len(unmarked_rows) == 0:
    st.success("✅ 已經全部篩選完畢！")
    st.stop()

row = unmarked_rows.iloc[0]
index = row.name  # 在 DataFrame 中的 index

st.markdown("## 👤 IG帳號：" + row["IG帳號"])
st.markdown(f"[🔗 點我查看 IG 連結]({row['IG連結']})")

st.markdown("---")

col1, col2, col3 = st.columns(3)

if col1.button("✅ 聯繫"):
    sheet.update_cell(index + 2, 3, "聯繫")
    st.rerun()

if col2.button("❌ 不聯繫"):
    sheet.update_cell(index + 2, 3, "不聯繫")
    st.rerun()

if col3.button("⏭ 跳過"):
    sheet.update_cell(index + 2, 3, "跳過")
    st.rerun()

st.markdown("---")
st.write(f"目前進度：第 {index + 1} 筆 / 共 {len(df)} 筆")
