import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "SimSun"
font = {"family": "SimSun", "weight": "bold", "size": "13"}
plt.rc("font", **font)  # 步骤一（设置字体的更多属性）
# 材料信息
layers = [
    {"name": "PU Foam", "thickness": 40, "color": "#ffcc99"},
    {"name": "Kaowool", "thickness": 5, "color": "#ffffcc"},
    {"name": "SiC Aerogel", "thickness": 55, "color": "#99ccff"},
    {"name": "SiC/SiC CMC", "thickness": 3, "color": "#E67979"},
]

# 总厚度（用于归一化坐标）
total_thickness = sum(layer["thickness"] for layer in layers)

# 画图
fig, ax = plt.subplots(figsize=(4, 8))
bottom = 0

for layer in layers:
    height = layer["thickness"]
    ax.bar(0, height, width=1, bottom=bottom, color=layer["color"], edgecolor='black')
    ax.text(0, bottom + height / 2, layer["name"] + f" {layer['thickness']} mm", ha='center', va='center', fontsize=10)
    bottom += height

# 设置图形参数
ax.set_xlim(-0.5, 0.5)
ax.set_ylim(0, total_thickness)
ax.set_xticks([])
ax.set_ylabel("相对厚度")
ax.set_title("月球基地顶棚多层材料结构示意图")

plt.tight_layout()
plt.show()
