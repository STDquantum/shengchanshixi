import matplotlib.pyplot as plt
import numpy as np

# 材料参数
k_pu = 0.03  # W/m·K
k_kao = 0.06
k_aero = 0.018

rho_pu = 50
rho_kao = 128
rho_aero = 250

cost_pu = 2153.5
cost_kao = 1380.5
cost_aero = 5588

# 总厚度
total_thickness = 0.10  # m
aero_thickness = 0.04  # m 固定SiC_Aerogel 4cm
remain_thickness = total_thickness - aero_thickness

# 交换 aero 和 kao
k_kao, k_aero, rho_kao, rho_aero, cost_kao, cost_aero = k_aero, k_kao, rho_aero, rho_kao, cost_aero, cost_kao

ratios = np.arange(0.1, 1.0, 0.1)
R_list = []
mass_list = []
cost_list = []

for r in ratios:
    pu_thickness = remain_thickness * r
    kao_thickness = remain_thickness * (1 - r)
    
    # 总热阻
    R_total = pu_thickness / k_pu + kao_thickness / k_kao + aero_thickness / k_aero
    R_list.append(R_total)
    
    # 总质量
    mass_total = pu_thickness * rho_pu + kao_thickness * rho_kao + aero_thickness * rho_aero
    mass_list.append(R_total / mass_total)  # 热阻质量比

    # 总成本
    cost_total = pu_thickness * cost_pu + kao_thickness * cost_kao + aero_thickness * cost_aero
    cost_list.append(R_total / cost_total)  # 热阻成本比

# 绘图
plt.figure(figsize=(12, 6))
# 设置图形
plt.rcParams["font.family"] = "SimSun"
font = {"family": "SimSun", "weight": "bold", "size": "13"}
plt.rc("font", **font)  # 步骤一（设置字体的更多属性）
# plt.rc("axes", unicode_minus=False)  # 步骤二（解决坐标轴负数的负号显示问题）

plt.subplot(1, 3, 1)
plt.plot(ratios, R_list, marker='o')
plt.title('总热阻 vs PU:Kaowool 厚度比')
plt.xlabel('PU 占比 (在 PU + Kao 中)')
plt.ylabel('总热阻 (m²·K/W)')

plt.subplot(1, 3, 2)
plt.plot(ratios, mass_list, marker='o', color='green')
plt.title('单位质量热阻')
plt.xlabel('PU 占比')
plt.ylabel('R / Mass')

plt.subplot(1, 3, 3)
plt.plot(ratios, cost_list, marker='o', color='orange')
plt.title('单位成本热阻')
plt.xlabel('PU 占比')
plt.ylabel('R / Cost')

plt.tight_layout()
plt.show()
