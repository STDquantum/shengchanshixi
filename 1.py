import streamlit as st
import matplotlib.pyplot as plt

# Material 类
class Material:
    def __init__(self, name, density, thermal_conductivity=None, youngs_modulus=None, poisong_ratio=None):
        self.name = name
        self.density = density
        self.thermal_conductivity = thermal_conductivity
        self.youngs_modulus = youngs_modulus
        self.poisong_ratio = poisong_ratio

# 计算复合材料属性
def compute_composite_properties(total_thickness, thickness_ratios, materials):
    w = thickness_ratios
    k_list = [m.thermal_conductivity for m in materials]
    E_list = [m.youngs_modulus for m in materials]
    nu_list = [m.poisong_ratio for m in materials]
    rho_list = [m.density for m in materials]

    # 热导率
    k_parallel = sum(w[i] * k_list[i] for i in range(4))
    k_perpendicular = 1.0 / sum(w[i] / k_list[i] for i in range(4))

    # 杨氏模量
    E_parallel = sum(w[i] * E_list[i] for i in range(4))
    E_perpendicular = 1.0 / sum(w[i] / E_list[i] for i in range(4))

    # 泊松比（工程近似）
    nu_parallel = sum(w[i] * nu_list[i] for i in range(4))
    nu_perpendicular = sum(w[i] * nu_list[i] for i in range(4))

    # 密度（平均即可）
    density = sum(w[i] * rho_list[i] for i in range(4))

    return {
        "parallel": {
            "thermal_conductivity": k_parallel,
            "youngs_modulus": E_parallel,
            "poisson_ratio": nu_parallel
        },
        "perpendicular": {
            "thermal_conductivity": k_perpendicular,
            "youngs_modulus": E_perpendicular,
            "poisson_ratio": nu_perpendicular
        },
        "density": density
    }

# 设置页面
st.title("📊 多层复合材料性能计算器")
st.markdown("### 滑动设置各层厚度比例，并观察材料性能变化")

# 材料定义
materials = [
    Material("A", 2700, 200, 70e9, 0.33),
    Material("B", 1900, 0.5, 3e9, 0.25),
    Material("C", 1500, 1.0, 2e9, 0.3),
    Material("D", 1200, 0.05, 1e9, 0.2),
]
colors = ['red', 'blue', 'green', 'orange']

# 总厚度滑动条
total_thickness = st.slider("总厚度 (cm)", min_value=5.0, max_value=10.0, value=6.0, step=0.1) / 100  # m

# 比例滑动条：动态归一化
st.markdown("### 各层厚度比例设置")
ratios = [st.slider(f"层 {i+1} 比例", 0.0, 1.0, 0.25, 0.01, key=f"layer_{i}") for i in range(4)]

total_ratio = sum(ratios)
if total_ratio == 0:
    ratios = [0.25] * 4
else:
    ratios = [r / total_ratio for r in ratios]

# 可视化厚度比例
st.markdown("### 📐 层厚度可视化")
fig, ax = plt.subplots(figsize=(2, 6))
y = 0
for i, r in enumerate(ratios):
    ax.bar(0, r, bottom=y, color=colors[i], label=f"{materials[i].name} ({r:.2f})")
    y += r
ax.set_ylim(0, 1)
ax.axis('off')
ax.legend(loc='upper right')
st.pyplot(fig)

# 计算结果
result = compute_composite_properties(total_thickness, ratios, materials)

# 显示参数
st.markdown("### 📈 有效性能参数")
st.write(f"**密度**: {result['density']:.2f} kg/m³")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**🔁 平行方向**")
    st.write(f"热导率: {result['parallel']['thermal_conductivity']:.4f} W/mK")
    st.write(f"杨氏模量: {result['parallel']['youngs_modulus']/1e9:.2f} GPa")
    st.write(f"泊松比: {result['parallel']['poisson_ratio']:.3f}")

with col2:
    st.markdown("**⏫ 垂直方向**")
    st.write(f"热导率: {result['perpendicular']['thermal_conductivity']:.4f} W/mK")
    st.write(f"杨氏模量: {result['perpendicular']['youngs_modulus']/1e9:.2f} GPa")
    st.write(f"泊松比: {result['perpendicular']['poisson_ratio']:.3f}")
