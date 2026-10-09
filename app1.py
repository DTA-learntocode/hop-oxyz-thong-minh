import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Hộp Oxyz Thông Minh - Mô hình 3D", layout="wide"
)

st.markdown(
    "### 🌐 Mô hình Quỹ Đạo Bắn 3D Tương Tác (Chiến dịch Cứu trợ / Oxyz)"
)

st.sidebar.header("🎛️ Điều chỉnh Tọa độ vật thể")
x_phao = st.sidebar.slider("Tọa độ X (Pháo cối)", 0.0, 10.0, 2.0, 0.5)
y_phao = st.sidebar.slider("Tọa độ Y (Pháo cối)", 0.0, 10.0, 1.0, 0.5)
z_phao = 0.0  # Pháo cối nằm trên mặt đất

x_máy_bay = st.sidebar.slider("Tọa độ X (Máy bay)", 0.0, 10.0, 8.0, 0.5)
y_máy_bay = st.sidebar.slider("Tọa độ Y (Máy bay)", 0.0, 10.0, 6.0, 0.5)
z_máy_bay = st.sidebar.slider("Cao độ Z (Máy bay)", 0.0, 10.0, 5.0, 0.5)

# Tạo figure 3D bằng Plotly
fig = go.Figure()

# 1. Vẽ điểm Pháo cối (Z = 0.0)
fig.add_trace(
    go.Scatter3d(
        x=[x_phao],
        y=[y_phao],
        z=[z_phao],
        mode="markers+text",
        marker=dict(size=8, color="red"),
        text=[f"Pháo cối (Z={z_phao})"],
        textposition="top center",
        name="Pháo cối",
    )
)

# 2. Vẽ điểm Máy bay (Z cao độ)
fig.add_trace(
    go.Scatter3d(
        x=[x_máy_bay],
        y=[y_máy_bay],
        z=[z_máy_bay],
        mode="markers+text",
        marker=dict(size=10, color="cyan", symbol="diamond"),
        text=[f"Máy bay (Z={z_máy_bay})"],
        textposition="top center",
        name="Máy bay",
    )
)

# 3. Vẽ đường đạn thẳng nối từ Pháo cối đến Máy bay (Màu đỏ)
fig.add_trace(
    go.Scatter3d(
        x=[x_phao, x_máy_bay],
        y=[y_phao, y_máy_bay],
        z=[z_phao, z_máy_bay],
        mode="lines",
        line=dict(color="red", width=6),
        name="Đường đạn thẳng",
    )
)

# 4. Vẽ tam giác hình chiếu xuống mặt phẳng đáy Oxy (Màu xanh đứt nét)
fig.add_trace(
    go.Scatter3d(
        x=[x_máy_bay, x_máy_bay, x_phao, x_máy_bay],
        y=[y_máy_bay, y_phao, y_phao, y_máy_bay],
        z=[0, 0, 0, 0],
        mode="lines",
        line=dict(color="blue", width=3, dash="dash"),
        name="Tam giác hình chiếu",
    )
)

# Cấu hình không gian trục Oxyz
fig.update_layout(
    scene=dict(
        xaxis=dict(range=[0, 11], title="Trục Ox"),
        yaxis=dict(range=[0, 11], title="Trục Oy"),
        zaxis=dict(range=[0, 11], title="Trục Oz (0-11)"),
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
    ),
    margin=dict(l=0, r=0, b=0, t=30),
    legend=dict(x=0.05, y=0.9),
)

st.plotly_chart(fig, use_container_width=True)

st.info(
    "💡 Bạn có thể dùng thanh trượt ở menu bên trái để thay đổi tọa độ hoặc dùng"
    " chuột xoay trực tiếp mô hình 3D!"
)
