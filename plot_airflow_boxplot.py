import yaml
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

YAML_PATH = "./results/Test_1/fan_test_result.yaml"

with open(YAML_PATH, "r") as f:
    data = yaml.safe_load(f)

step1_airflow = data["Test_1"]["step_1"]["airflow_rate_value"]
step3_airflow = data["Test_1"]["step_3"]["airflow_rate_value"]

step1_mean = data["Test_1"]["step_1"]["mean_airflow_rate"]
step3_mean = data["Test_1"]["step_3"]["mean_airflow_rate"]

fig, ax = plt.subplots(figsize=(7, 6))

bp = ax.boxplot(
    [step1_airflow, step3_airflow],
    labels=["Step 1", "Step 3"],
    patch_artist=True,
    widths=0.4,
    medianprops=dict(color="black", linewidth=2),
)

colors = ["#4C72B0", "#DD8452"]
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_title("Airflow Rate Distribution — Test 1", fontsize=14, fontweight="bold")
ax.set_ylabel("Airflow Rate (CFM)", fontsize=12)
ax.set_xlabel("Test Step", fontsize=12)
y_min = min(step1_airflow + step3_airflow)
y_max = max(step1_airflow + step3_airflow)
margin = (y_max - y_min) * 0.1
ax.set_ylim(145, 210)

ax.set_yticks([150, 175, 200])
ax.grid(axis="y", linestyle="--", alpha=0.5)
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.savefig("./results/Test_1/airflow_boxplot.svg", format="svg")
plt.show()
