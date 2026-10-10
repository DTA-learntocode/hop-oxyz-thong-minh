import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Hộp Oxyz Thông Minh - Camera Web", layout="wide"
)

st.markdown("### 📷 Ứng dụng Quỹ Đạo Hộp Oxyz Thông Minh (Camera Web)")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Chụp ảnh vật thể / Mô hình thực tế")
    # Widget chụp ảnh trực tiếp từ camera trình duyệt (hoạt động hoàn hảo trên Streamlit Cloud)
    img_file_buffer = st.camera_input(
        "Chụp ảnh vị trí mục tiêu hoặc hộp Oxyz của bạn"
    )

    if img_file_buffer is not None:
        st.success("✨ Đã ghi nhận hình ảnh từ camera!")
        # Bạn có thể xử lý thêm hình ảnh ở đây nếu cần

with col2:
    st.subheader("2. Mô hình Không gian 3D Oxyz & Tính toán Quỹ Đạo")

    # Các thanh trượt điều chỉnh tọa độ
    x_phao = st.slider("Tọa độ X (Pháo cối/Gốc)", 0.0, 10.0, 2.0, 0.5)
    y_phao = st.slider("Tọa độ Y (Pháo cối/Gốc)", 0.0, 10.0, 1.0, 0.5)
    z_phao = 0.0

    x_mb = st.slider("Tọa độ X (Mục tiêu/Máy bay)", 0.0, 10.0, 8.0, 0.5)
    y_mb = st.slider("Tọa độ Y (Mục tiêu/Máy bay)", 0.0, 10.0, 6.0, 0.5)
    z_mb = st.slider("Cao độ Z (Mục tiêu/Máy bay)", 0.0, 10.0, 5.0, 0.5)

    # Tính toán khoảng cách không gian
    khoang_cach = np.sqrt(
        (x_mb - x_phao) ** 2 + (y_mb - y_phao) ** 2 + (z_mb - z_phao) ** 2
    )
    st.info(f"📏 Khoảng cách không gian tính toán: **{khoang_cach:.2f} đơn vị**")

    # Vẽ biểu đồ không gian 3D với Plotly
    fig = go.Figure()

    # Điểm pháo cối
    fig.add_trace(
        go.Scatter3d(
            x=[x_phao],
            y=[y_phao],
            z=[z_phao],
            mode="markers+text",
            marker=dict(size=8, color="red"),
            text=["Vị trí Pháo (Gốc)"],
            textposition="top center",
            name="Pháo cối",
        )
    )

    # Điểm mục tiêu
    fig.add_trace(
        go.Scatter3d(
            x=[x_mb],
            y=[y_mb],
            z=[z_mb],
            mode="markers+text",
            marker=dict(size=10, color="cyan", symbol="diamond"),
            text=["Vị trí Mục tiêu"],
            textposition="top center",
            name="Mục tiêu",
        )
    )

    # Đường đạn nối thẳng
    fig.add_trace(
        go.Scatter3d(
            x=[x_phao, x_mb],
            y=[y_phao, y_mb],
            z=[z_phao, z_mb],
            mode="lines",
            line=dict(color="red", width=5),
            name="Quỹ đạo đường đạn",
        )
    )

    # Cấu hình không gian 3D
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[0, 10], title="Trục Ox"),
            yaxis=dict(range=[0, 10], title="Trục Oy"),
            zaxis=dict(range=[0, 10], title="Trục Oz"),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        legend=dict(x=0.05, y=0.9),
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption(
    "🚀 Dự án Smart Oxyz Box - Đảm bảo tương thích hoàn toàn trên Streamlit"
    " Cloud."
)
