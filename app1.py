import cv2
import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Hộp Oxyz Thông Minh - AI Camera", layout="wide"
)

st.markdown(
    "### 🌐 AI Camera Radar - Mô hình Quỹ Đạo Bắn 3D Tương Tác (Hộp Oxyz)"
)

# Sidebar chọn chế độ
mode = st.sidebar.radio(
    "Chọn chế độ điều khiển:",
    ["Thủ công (Thanh trượt)", "Tự động (AI Camera - Webcam)"],
)

# Khởi tạo tọa độ mặc định
x_phao, y_phao, z_phao = 2.0, 1.0, 0.0
x_máy_bay, y_máy_bay, z_máy_bay = 8.0, 6.0, 5.0

if mode == "Thủ công (Thanh trượt)":
  st.sidebar.header("🎛️ Điều chỉnh Tọa độ")
  x_phao = st.sidebar.slider("Tọa độ X (Pháo cối)", 0.0, 10.0, 2.0, 0.5)
  y_phao = st.sidebar.slider("Tọa độ Y (Pháo cối)", 0.0, 10.0, 1.0, 0.5)
  x_máy_bay = st.sidebar.slider("Tọa độ X (Máy bay)", 0.0, 10.0, 8.0, 0.5)
  y_máy_bay = st.sidebar.slider("Tọa độ Y (Máy bay)", 0.0, 10.0, 6.0, 0.5)
  z_máy_bay = st.sidebar.slider("Cao độ Z (Máy bay)", 0.0, 10.0, 5.0, 0.5)

else:
  st.sidebar.header("📷 AI Camera Nhận diện")
  st.sidebar.info("Hệ thống đang mở Webcam liên tục...")

  # Dùng st.checkbox làm công tắc bật/tắt camera an toàn
  run_cam = st.checkbox("Bật Camera Radar", value=False)
  camera_placeholder = st.empty()
  stop_button = st.button("Dừng Camera")

  if run_cam and not stop_button:
    cap = cv2.VideoCapture(0)  # Mở webcam mặc định của máy tính

    # Vòng lặp liên tục cập nhật khung hình từ webcam để không bị đứng hình
    while cap.isOpened() and run_cam and not stop_button:
      ret, frame = cap.read()
      if not ret:
        st.warning(
          "Không thể kết nối với Webcam. Vui lòng kiểm tra lại thiết bị!"
        )
        break

      # Xử lý lật gương khung hình cho tự nhiên và chuyển màu sang RGB
      frame = cv2.flip(frame, 1)
      frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

      # Hiển thị video trực tiếp lên giao diện web
      camera_placeholder.image(
        frame_rgb,
        caption="Đang quét không gian Hộp Oxyz (Live Webcam)",
        channels="RGB",
      )

      # (Tùy chọn) Chèn logic gọi mô hình AI Teachable Machine ở đây để nhận diện tọa độ x, y, z thực tế từ biến `frame`

    cap.release()

# --- VẼ BIỂU ĐỒ 3D OXYZ ---
fig = go.Figure()

# 1. Vẽ điểm Pháo cối
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

# 2. Vẽ điểm Máy bay
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

# 3. Vẽ đường đạn thẳng nối từ Pháo cối đến Máy bay
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

# 4. Vẽ tam giác hình chiếu xuống mặt phẳng đáy Oxy
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