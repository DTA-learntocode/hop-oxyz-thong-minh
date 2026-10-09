import cv2
import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Hộp Oxyz Thông Minh - Camera AI", layout="wide"
)

st.markdown("### 📷 Camera AI & Mô hình Quỹ Đạo Bắn 3D")

# Mở webcam (0 là camera mặc định của máy)
cap = cv2.VideoCapture(0)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Khung hình Camera trực tiếp")
    camera_placeholder = st.empty()
    run_cam = st.checkbox("Bật Camera", value=True)

with col2:
    st.subheader("Mô hình 3D Oxyz")

    # Nhận giá trị tọa độ từ giao diện hoặc mô phỏng từ AI
    x_phao = st.slider("Tọa độ X (Pháo)", 0.0, 10.0, 2.0, 0.5)
    y_phao = st.slider("Tọa độ Y (Pháo)", 0.0, 10.0, 1.0, 0.5)
    z_phao = 0.0

    x_mb = st.slider("Tọa độ X (Mục tiêu)", 0.0, 10.0, 8.0, 0.5)
    y_mb = st.slider("Tọa độ Y (Mục tiêu)", 0.0, 10.0, 6.0, 0.5)
    z_mb = st.slider("Cao độ Z (Mục tiêu)", 0.0, 10.0, 5.0, 0.5)

    # Vẽ biểu đồ 3D
    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=[x_phao, x_mb],
            y=[y_phao, y_mb],
            z=[z_phao, z_mb],
            mode="lines+markers",
            marker=dict(size=8, color=["red", "cyan"]),
            line=dict(color="red", width=5),
            name="Quỹ đạo",
        )
    )
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[0, 10]),
            yaxis=dict(range=[0, 10]),
            zaxis=dict(range=[0, 10]),
        ),
        margin=dict(l=0, r=0, b=0, t=0),
    )
    st.plotly_chart(fig, use_container_width=True)

# Xử lý khung hình camera
if run_cam:
    ret, frame = cap.read()
    if ret:
        # Chuyển màu từ BGR sang RGB để Streamlit hiển thị đúng màu
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        camera_placeholder.image(
            frame, channels="RGB", use_container_width=True
        )
    else:
        st.warning("Không thể kết nối với webcam.")
else:
    camera_placeholder.info("Camera đang tắt.")

# Giải phóng camera khi dừng app
cap.release()
