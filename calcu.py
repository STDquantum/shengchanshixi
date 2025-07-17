import numpy as np
import pandas as pd

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

young_pu = 0.05e9
young_kao = 3e9
young_aero = 5e9

# 总厚度
total_thickness = 10  # cm
thickness_range = np.arange(0.5, total_thickness + 0.5, 0.5)  # 从0.5到10的步长

# 初始化存储结果
results = []
max_k = -1000000
max_rho = -1000000
max_cost = -1000000
max_young = 0

# 枚举三种材料的厚度
for pu_thickness in thickness_range:
    for kao_thickness in thickness_range:
        for aero_thickness in thickness_range:
            if pu_thickness + kao_thickness + aero_thickness == total_thickness:
                # 计算总热阻
                R_total = pu_thickness / k_pu + kao_thickness / k_kao + aero_thickness / k_aero
                k_total = total_thickness / R_total
                
                # 计算总密度
                rho_total = (pu_thickness * rho_pu + kao_thickness * rho_kao + aero_thickness * rho_aero) / total_thickness
                
                # 计算总成本
                cost_total = (pu_thickness * cost_pu + kao_thickness * cost_kao + aero_thickness * cost_aero) / total_thickness
                
                # 计算总杨氏模量
                young_total = (pu_thickness * young_pu + kao_thickness * young_kao + aero_thickness * young_aero) / total_thickness
                
                # 计算最大值
                max_k = max(max_k, k_total)
                max_rho = max(max_rho, rho_total)
                max_cost = max(max_cost, cost_total)
                max_young = max(max_young, young_total)
                
# 枚举三种材料的厚度
for pu_thickness in thickness_range:
    for kao_thickness in thickness_range:
        for aero_thickness in thickness_range:
            if pu_thickness + kao_thickness + aero_thickness == total_thickness:
                # 计算总热阻
                R_total = pu_thickness / k_pu + kao_thickness / k_kao + aero_thickness / k_aero
                k_total = total_thickness / R_total
                
                # 计算总密度
                rho_total = (pu_thickness * rho_pu + kao_thickness * rho_kao + aero_thickness * rho_aero) / total_thickness
                
                # 计算总成本
                cost_total = (pu_thickness * cost_pu + kao_thickness * cost_kao + aero_thickness * cost_aero) / total_thickness
                
                # 计算总杨氏模量
                young_total = (pu_thickness * young_pu + kao_thickness * young_kao + aero_thickness * young_aero) / total_thickness
                
                # 计算总价值
                value = (k_total / max_k * 0.6) - (young_total / max_young * 0.1) + (rho_total / max_rho * 0.2) + (cost_total / max_cost * 0.1)
                
                # 保存结果
                results.append([pu_thickness, kao_thickness, aero_thickness, k_total, rho_total, cost_total, young_total/1e9, value])

# 转换为 DataFrame 并排序
df = pd.DataFrame(results, columns=['PU', 'Kaowool', 'Aerogel', 
                                    '总热导率', '总密度', '总成本', '总杨氏模量', '价值'])
df_sorted = df.sort_values(by='价值', ascending=True).head(5)

# 输出为 Markdown 格式的表格
def df_to_markdown_table(df):
    headers = "| " + " | ".join(df.columns) + " |"
    separator = "| " + " | ".join(["---"] * len(df.columns)) + " |"
    rows = ["| " + " | ".join(f"{v:.3f}" if isinstance(v, float) else str(v) for v in row) + " |"
            for row in df.values]
    markdown_table = "\n".join([headers, separator] + rows)
    return markdown_table

# 打印 Markdown 表格
print(df_to_markdown_table(df_sorted))