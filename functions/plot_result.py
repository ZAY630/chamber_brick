# %%
import yaml
import matplotlib.pyplot as plt

# %%
def make_plot():
    with open('./readfiles/results/fan_test_result.yaml', 'r') as f:
        result_dict = yaml.safe_load(f)

    plt.figure(figsize=[10, 8])
    plt.plot(result_dict['Test_1']['step_1']['airflow_rate_value'], label = "before")
    plt.plot(result_dict['Test_1']['step_3']['airflow_rate_value'], label = "after")
    plt.title('Fan Test Result')
    plt.xlabel("Timestamp")
    plt.ylabel("Airflow rate (CFM)")
    plt.legend()
    plt.show()

    plt.savefig('../results/fan_test_result.png')

# %%
if __name__ == "__main__":
    make_plot()

