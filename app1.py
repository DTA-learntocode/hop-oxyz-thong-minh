import numpy as np
import plotly.graph_objects as go
from scipy.optimize import minimize
import streamlit as st

st.set_page_config(
    page_title="Hộp Oxyz Thông Minh - Hoàn chỉnh 4 Nhiệm vụ", layout="wide"
)

st.markdown(
    "### 🚀 DỰ ÁN STEM: CHIẾN DỊCH CỨU TRỢ - HỘP OXYZ THÔNG MINH (4 NHIỆM VỤ)"
)

# Chia giao diện thành 2 cột: Cột trái (Nhập liệu & Tính toán), Cột phải (Mô hình 3D)
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("📷 1. AI Camera & Nhập liệu tọa độ sa bàn")
    img_file = st.camera_input("Chụp ảnh các điểm A, B, C thực tế trên hộp sa bàn")

    if img_file is not None:
        st.success("✅ Đã ghi nhận hình ảnh từ Camera Web!")

    st.markdown("#### ⚙️ Tọa độ các mốc chính (Theo chuẩn sa bàn):")

    # Cấu hình các điểm cơ bản (O là gốc tọa độ 0,0,0)
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        xA = st.number_input("Ax", value=2.0, step=0.5)
    with col_a2:
        yA = st.number_input("Ay", value=3.0, step=0.5)
    with col_a3:
        zA = st.number_input("Az", value=1.0, step=0.5)

    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        xB = st.number_input("Bx", value=8.0, step=0.5)
    with col_b2:
        yB = st.number_input("By", value=6.0, step=0.5)
    with col_b3:
        zB = st.number_input("Bz", value=4.0, step=0.5)

    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        xC = st.number_input("Cx", value=5.0, step=0.5)
    with col_c2:
        yC = st.number_input("Cy", value=1.0, step=0.5)
    with col_c3:
        zC = st.number_input("Cz", value=3.0, step=0.5)

    # Khởi tạo vector mảng numpy
    O = np.array([0.0, 0.0, 0.0])
    A = np.array([xA, yA, zA])
    B = np.array([xB, yB, zB])
    C = np.array([xC, yC, zC])

    st.markdown("---")
    st.subheader("📊 Kết quả giải quyết 4 Nhiệm vụ")

    # --- NHIỆM VỤ 1 ---
    st.markdown("##### 📌 Nhiệm vụ 1: Định vị & Quy tắc vectơ đường bay")
    vec_AC = C - A
    vec_CB = B - C
    vec_AB = B - A

    # Chuyển kiểu dữ liệu numpy sang list thường để hiển thị công thức đẹp mắt
    list_AC = [float(val) for val in vec_AC]
    list_CB = [float(val) for val in vec_CB]
    list_AB = [float(val) for val in vec_AB]
    check_nv1 = np.allclose(vec_AC + vec_CB, vec_AB)

    st.markdown(
        f"- $\\vec{{AC}} = {list_AC}$, $\\vec{{CB}} = {list_CB}$, $\\vec{{AB}}"
        f" = {list_AB}$"
    )
    st.write(
        f"- Kiểm chứng quy tắc ba điểm $\\vec{{AB}} = \\vec{{AC}} +"
        f" \\vec{{CB}}$: **{'Đúng (Thỏa mãn)' if check_nv1 else 'Sai'}**"
    )

    # --- NHIỆM VỤ 2 ---
    st.markdown("##### 📌 Nhiệm vụ 2: Tối ưu hóa nhiên liệu & Quãng đường")
    d_AB = np.linalg.norm(vec_AB)
    d_AC_CB = np.linalg.norm(vec_AC) + np.linalg.norm(vec_CB)
    st.write(f"- Quãng đường bay thẳng $AB$: **{d_AB:.2f} km**")
    st.write(
        f"- Quãng đường qua trạm trung chuyển $AC + CB$: **{d_AC_CB:.2f} km**"
    )

    # --- NHIỆM VỤ 3 ---
    st.markdown(
        "##### 📌 Nhiệm vụ 3: Trạm thả hàng dự phòng ($AD = 2\\vec{AC}$)"
    )
    D = A + 2 * vec_AC
    st.write(
        f"- Tọa độ trạm dự phòng $D$: **({D[0]:.1f}; {D[1]:.1f}; {D[2]:.1f})**"
    )

    # --- NHIỆM VỤ 4 ---
    st.markdown("##### 📌 Nhiệm vụ 4: Trạm Radar mặt đất ($T_{\\min}$)")


    # Hàm mục tiêu cho Nhiệm vụ 4
    def objective_T(vars):
      x, y = vars
      M_pt = np.array([x, y, 0.0])
      val = (
          np.linalg.norm(M_pt - A)
          + 2 * np.linalg.norm(M_pt - B)
          - np.linalg.norm(M_pt - C)
      )
      return abs(val)


    res = minimize(objective_T, [6.5, 7.0], method="Nelder-Mead")
    x_opt, y_opt = res.x
    M_radar = np.array([x_opt, y_opt, 0.0])
    st.success(
        f"🎯 Tọa độ Radar tối ưu $M({x_opt:.2f}; {y_opt:.2f}; 0)$ đạt giá trị"
        f" tối thiểu!"
    )

with col_right:
    st.subheader("🌐 Mô hình Không gian 3D Oxyz Chuẩn Sa Bàn")

    # Vẽ biểu đồ 3D bằng Plotly
    fig = go.Figure()

    # 1. Vẽ các điểm cốt lõi O, A, B, C, D, M
    points_dict = {
        "O (Sở chỉ huy)": (O, "black"),
        "A (Kho hàng)": (A, "orange"),
        "B (Vùng cứu trợ)": (B, "red"),
        "C (Trạm trung chuyển)": (C, "green"),
        "D (Điểm dự phòng - NV3)": (D, "purple"),
        "M (Radar - NV4)": (M_radar, "cyan"),
    }

    for name, (pt, color) in points_dict.items():
        fig.add_trace(
            go.Scatter3d(
                x=[pt[0]],
                y=[pt[1]],
                z=[pt[2]],
                mode="markers+text",
                marker=dict(size=8, color=color),
                text=[name],
                textposition="top center",
                name=name,
            )
        )

    # 2. Vẽ đường bay Nhiệm vụ 1 & 2 (A -> C -> B)
    fig.add_trace(
        go.Scatter3d(
            x=[A[0], C[0], B[0]],
            y=[A[1], C[1], B[1]],
            z=[A[2], C[2], B[2]],
            mode="lines+markers",
            line=dict(color="blue", width=5),
            name="Đường bay qua C (NV1-2)",
        )
    )

    # 3. Vẽ đường vector Nhiệm vụ 3 (A -> D)
    fig.add_trace(
        go.Scatter3d(
            x=[A[0], D[0]],
            y=[A[1], D[1]],
            z=[A[2], D[2]],
            mode="lines",
            line=dict(color="purple", width=4, dash="dash"),
            name="Vectơ AD dự phòng (NV3)",
        )
    )

    # Cấu hình khung không gian 3D với trục Oz thẳng đứng giữa sa bàn
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[0, 11], title="Trục Ox (km)", zeroline=True),
            yaxis=dict(range=[0, 11], title="Trục Oy (km)", zeroline=True),
            zaxis=dict(range=[0, 11], title="Trục Oz (km)", zeroline=True),
            # Khóa góc nhìn camera để Oz thẳng đứng, Ox sang phải, Oy hướng ra ngoài
            camera=dict(
                eye=dict(x=1.6, y=-1.6, z=1.2), up=dict(x=0, y=0, z=1)
            ),
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        legend=dict(x=0.0, y=0.9),
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption(
    "💡 Dự án STEM 'Hộp Oxyz Thông Minh' - Sẵn sàng nộp bài và chấm điểm."
)
