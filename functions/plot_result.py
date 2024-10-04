# %%
import yaml
import matplotlib.pyplot as plt

# %%
def make_plot(test, name, xlab, ylab, title, subtitle):
    with open('./results/{}.yaml'.format(name), 'r') as f:
        result_dict = yaml.safe_load(f)

    plt.figure(figsize=[10, 6])
    plt.plot(result_dict[test]['step_1']['airflow_rate_value'], label = "before")
    plt.plot(result_dict[test]['step_3']['airflow_rate_value'], label = "after")
    plt.title(title)
    plt.suptitle(subtitle)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.legend()
    plt.grid(axis = 'y')

    plt.savefig('./results/{}.png'.format(name))
    plt.show()

# %%
if __name__ == "__main__":
    make_plot()

