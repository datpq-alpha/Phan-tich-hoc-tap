import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Phân tích Kết quả Học tập", layout="wide")

st.title("🎓 DỰ ÁN PHÂN TÍCH DỮ LIỆU HỌC TẬP")
st.markdown("---")

# --- 1. LOAD & KHÁM PHÁ DỮ LIỆU (DATA EXPLORATION) ---
st.header("1. Khám phá Dữ liệu (Exploration)")
st.caption("Mục tiêu: Hiểu cấu trúc, kích thước và độ sạch của dữ liệu.")

# Đọc dữ liệu
try:
    df = pd.read_csv('data5.8.csv')
except:
    st.error("Không tìm thấy file data5.8.csv")
    st.stop()

# Chia 2 cột để hiển thị thông tin cơ bản
col1, col2 = st.columns(2)

with col1:
    st.write("📋 **5 dòng dữ liệu đầu tiên:**")
    st.dataframe(df.head())

with col2:
    st.write("ℹ️ **Thông tin bộ dữ liệu:**")
    so_dong, so_cot = df.shape
    st.write(f"- Số dòng: **{so_dong}**")
    st.write(f"- Số cột: **{so_cot}**")
    
    # Kiểm tra dữ liệu trống
    null_check = df.isnull().sum().sum()
    if null_check == 0:
        st.success("- Kiểm tra lỗi: Dữ liệu sạch (Không có ô trống).")
    else:
        st.warning(f"- Kiểm tra lỗi: Có {null_check} ô trống.")

st.markdown("---")

# --- 2. PHÂN TÍCH MÔ TẢ (DESCRIPTIVE ANALYTICS) ---
st.header("2. Phân tích Mô tả (Descriptive)")
st.caption("Mục tiêu: Tóm tắt đặc điểm và trực quan hóa những gì đã diễn ra.")

# A. Thống kê (Statistics)
st.subheader("a) Thống kê các chỉ số quan trọng")
# Tính toán các chỉ số
avg_score = df['Điểm Số'].mean()
max_score = df['Điểm Số'].max()
avg_hours = df['Số Giờ Học'].mean()

# Hiển thị bằng Metric cards
m1, m2, m3 = st.columns(3)
m1.metric("Điểm trung bình", f"{avg_score:.2f}")
m2.metric("Điểm cao nhất", f"{max_score}")
m3.metric("Giờ học trung bình", f"{avg_hours:.2f} giờ")

# B. Trực quan hóa (Visualization)
st.subheader("b) Biểu đồ trực quan")

c1, c2 = st.columns(2)

with c1:
    st.write("🌍 **Phân bố học sinh theo Tỉnh/Thành phố**")
    # Đếm số lượng học sinh theo địa chỉ
    city_counts = df['Địa Chỉ'].value_counts()
    st.bar_chart(city_counts)

with c2:
    st.write("📊 **Phổ điểm của học sinh**")
    # Vẽ Histogram bằng Matplotlib để đẹp hơn
    fig_hist, ax_hist = plt.subplots()
    ax_hist.hist(df['Điểm Số'], bins=10, color='skyblue', edgecolor='black')
    ax_hist.set_xlabel("Điểm số")
    ax_hist.set_ylabel("Số lượng học sinh")
    st.pyplot(fig_hist)

# C. Truy sâu (Drill-down)
st.subheader("c) Truy sâu dữ liệu (Drill-down)")
st.write("Lọc danh sách học sinh theo Tỉnh/Thành phố:")
# Tạo hộp chọn
selected_city = st.selectbox("Chọn Thành phố:", df['Địa Chỉ'].unique())
# Lọc dữ liệu
df_filtered = df[df['Địa Chỉ'] == selected_city]
st.write(f"Danh sách học sinh tại **{selected_city}** ({len(df_filtered)} em):")
st.dataframe(df_filtered)

st.markdown("---")

# --- 3. PHÂN TÍCH CHẨN ĐOÁN (DIAGNOSTIC ANALYTICS) ---
st.header("3. Phân tích Chẩn đoán (Diagnostic)")
st.caption("Mục tiêu: Tìm nguyên nhân và các mối tương quan (Tại sao kết quả lại như vậy?)")

# A. Phân tích tương quan (Correlation)
st.subheader("a) Tương quan: Thời gian học vs Kết quả")
st.write("Liệu học nhiều giờ hơn thì điểm có cao hơn không?")

col_diag1, col_diag2 = st.columns([2, 1])

with col_diag1:
    # Vẽ biểu đồ phân tán (Scatter Plot) với đường hồi quy
    fig_corr, ax_corr = plt.subplots()
    sns.regplot(data=df, x='Số Giờ Học', y='Điểm Số', ax=ax_corr, line_kws={"color": "red"})
    ax_corr.set_title("Biểu đồ tương quan Giờ học - Điểm số")
    st.pyplot(fig_corr)

with col_diag2:
    st.info("""
    **Nhận xét:**
    - Đường màu đỏ đi lên cho thấy mối tương quan **thuận**.
    - Tức là: Xu hướng chung là càng học nhiều giờ, điểm số càng cao.
    - Tuy nhiên, vẫn có những điểm ngoại lai (học ít điểm cao hoặc ngược lại).
    """)

# B. So sánh nhóm (Comparison)
st.subheader("b) So sánh chất lượng học tập giữa các khu vực")
# Gom nhóm và tính trung bình điểm
avg_score_city = df.groupby('Địa Chỉ')['Điểm Số'].mean().sort_values(ascending=False)
st.write("Điểm trung bình theo từng thành phố:")
st.bar_chart(avg_score_city)

# --- 4. KHAI PHÁ DỮ LIỆU (DATA MINING - Đơn giản hóa) ---
st.header("4. Khai phá Quy luật (Simple Mining)")
st.caption("Mục tiêu: Tìm ra quy luật tiềm ẩn (Pattern Discovery).")

# Tìm quy luật: Nhóm học sinh chăm chỉ (Top 25% giờ học) thì điểm số thế nào?
# Xác định ngưỡng "Chăm chỉ" (Q3 - 75th percentile)
gio_hoc_threshold = df['Số Giờ Học'].quantile(0.75)

st.write(f"👉 **Giả thuyết:** Những bạn thuộc nhóm Chăm chỉ (học trên **{gio_hoc_threshold}** giờ) thì điểm số ra sao?")

# Tách nhóm
nhom_cham_chi = df[df['Số Giờ Học'] > gio_hoc_threshold]
diem_tb_cham_chi = nhom_cham_chi['Điểm Số'].mean()
diem_tb_toan_bo = df['Điểm Số'].mean()

col_m1, col_m2 = st.columns(2)
col_m1.metric("Điểm TB nhóm Chăm chỉ", f"{diem_tb_cham_chi:.2f}")
col_m2.metric("Điểm TB toàn bộ lớp", f"{diem_tb_toan_bo:.2f}")

delta = diem_tb_cham_chi - diem_tb_toan_bo
if delta > 0:
    st.success(f"💡 **Kết luận (Insight):** Nhóm chăm chỉ có điểm trung bình cao hơn mặt bằng chung **{delta:.2f}** điểm. => Quy luật: Tăng thời gian học làm tăng khả năng đạt điểm cao.")
else:
    st.warning("💡 **Kết luận:** Không thấy sự khác biệt rõ rệt.")
