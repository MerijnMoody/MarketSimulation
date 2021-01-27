import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
from pylab import cm

# Reads the data from the data file.
diff_list = []  # Stores the difference between average buy and sell prices.
y_list = []     # Stores the raw average buy and sell price.
p_list = []     # Stores the p-values of the simulation.
with open('data.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    temp_list = []
    for row in csv_reader:
        data_list = [row[i] for i in range(3, int(row[2]))]
        n_iter = int(row[2])  # Number of times the simulation was run
        n_days = int(row[3])  # Number of days of the simulations

        # The original structure of the data is recovered.
        final_list = [[] for _ in range(n_days)]
        for i in range(n_days):
            for j in range(n_iter):
                final_list[i].append(float(row[4 + i * n_iter + j]))

        y_list.append(final_list)
        temp_list.append([sum(i) / n_iter for i in final_list])

        # We want to take the p-values and differences only for each
        # buyer/seller pair.
        if len(temp_list) == 2:
            p_list.append(float(row[0]))
            y_diff = [temp_list[0][i] - temp_list[1][i]
                      for i in range(len(temp_list[0]))]
            diff_list.append(y_diff)
            temp_list = []


# Helper function for setting the tick parameters of the plot.
def tick(ax):
    ax.xaxis.set_tick_params(which='major', size=10,
                             width=2, direction='in', top='on')
    ax.xaxis.set_tick_params(which='minor', size=7,
                             width=2, direction='in', top='on')
    ax.yaxis.set_tick_params(which='major', size=10,
                             width=2, direction='in', right='on')
    ax.yaxis.set_tick_params(which='minor', size=7,
                             width=2, direction='in', right='on')
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(100))
    ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(25))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(0.2))
    ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(0.05))


# Helper function that determines that standard deviation of a list.
def std(deviation_list):
    final_sum = 0
    average = sum(deviation_list) / len(deviation_list)
    for i in deviation_list:
        final_sum += (i - average) ** 2 / (len(deviation_list) - 1)
    return final_sum ** 0.5


# General plot parameters.
# Many of the plotting parameters were taken from the tutorial https://towardsdatascience.com/an-introduction-to-making-scientific-publication-plots-with-python-ea19dfa7f51e.
plt.rcParams['font.size'] = 22
plt.rcParams['axes.linewidth'] = 2
x = [i for i in range(500)]


# A graph of the price differences for different p-values.
fig = plt.figure(figsize=(11, 7))
i_list = [0, 2, 12, 10, 13, 11, 14]  # Plot a selection of p-values
assert(max(i_list) < len(p_list))    # Indices should be in range of the p_list
colors = cm.get_cmap('tab10', len(i_list))


# Main graph for plotting the price differences for different p-values.
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlabel('Time', labelpad=10)
ax.set_ylabel('Price difference', labelpad=10)
ax.set_xlim(0, 500)
ax.set_ylim(-0.03, 0.5)
ax.set_title("Difference between the average buying and selling prices")
tick(ax)

# Zoomed-in inset of the end of the graph.
ax2 = fig.add_axes([0.2, 0.5, 0.4, 0.4])
ax2.set_xlim(450, 500)
ax2.set_ylim(0, 0.04)
tick(ax)


# We plot the price differences for each p-value with an index in i_list.
std_bool = False  # Determines if we plot the std. Can reduce clarity
for j in range(len(i_list)):
    i = i_list[j]
    final_list_buyer = y_list[2 * i + 1]
    final_list_seller = y_list[2 * i]
    x = [i for i in range(500)]
    y_buyer = [sum(i)/n_iter for i in final_list_buyer]
    y_buyer_std = [std(i) for i in final_list_buyer]
    y_seller = [sum(i)/n_iter for i in final_list_seller]
    y_seller_std = [std(i) for i in final_list_seller]
    y_diff = [y_buyer[i] - y_seller[i] for i in range(len(y_buyer))]
    ax.plot(x, y_diff, label=r'$\rho = $' + str(p_list[i]), color=colors(j))
    ax2.plot(x, y_diff, label=r'$\rho = $' + str(p_list[i]), color=colors(j))
    lower_std = [y_diff[i] - (y_buyer_std[i] + y_seller_std[i])
                 for i in range(n_days)]
    upper_std = [y_diff[i] + (y_buyer_std[i] + y_seller_std[i])
                 for i in range(n_days)]
    if std_bool:
        ax.fill_between(x, lower_std, upper_std, alpha=0.2, color=colors(j))
ax.legend(bbox_to_anchor=(1, 1), loc=1, frameon=False, fontsize=16)


plt.savefig('PriceDifferenceP.png', dpi=300,
            transparent=False, bbox_inches='tight')


# A graph of the average buying and selling prices with standard deviations.
fig = plt.figure(figsize=(11, 7))
final_list_buyer = y_list[0]
final_list_seller = y_list[1]
x = [i for i in range(500)]
y_buyer = [sum(i)/n_iter for i in final_list_buyer]
y_buyer_std = [std(i) for i in final_list_buyer]
y_seller = [sum(i)/n_iter for i in final_list_seller]
y_seller_std = [std(i) for i in final_list_seller]


# Main graph.
ax = fig.add_axes([0, 0.3, 1, 0.7])
ax.set_ylabel('Price', labelpad=10)
ax.set_xlim(0, 300)
ax.set_ylim(0.17, 0.83)
tick(ax)


ax.plot(x, y_buyer, color='red', label='buyer')
ax.fill_between(x, [y_buyer[i] - y_buyer_std[i] for i in range(n_days)],
                [y_buyer[i] + y_buyer_std[i] for i in range(n_days)],
                alpha=0.2, color='red')
ax.plot(x, y_seller, color='blue', label='seller')
ax.fill_between(x, [y_seller[i] - y_seller_std[i] for i in range(n_days)],
                [y_seller[i] + y_seller_std[i] for i in range(n_days)],
                alpha=0.2, color='blue')
ax.legend(bbox_to_anchor=(1, 1), loc=1, frameon=False, fontsize=16)
ax.set_xticklabels([])
ax.set_title("Average buying and selling prices")


# Bottom part of graph with buying/selling price difference.
ax2 = fig.add_axes([0, 0, 1, 0.3])
ax2.set_xlabel('Time', labelpad=10)
ax2.set_ylabel('Price difference', labelpad=10)
ax2.set_xlim(0, 300)
ax2.set_ylim(-0.03, 0.5)
tick(ax2)
ax2.plot(x, diff_list[0], label=r'$\rho = $' + str(p_list[0]))
ax2.fill_between(x, [diff_list[0][i] - (y_buyer_std[i] + y_seller_std[i])
                     for i in range(n_days)],
                 [diff_list[0][i] + (y_buyer_std[i] + y_seller_std[i])
                  for i in range(n_days)],
                 alpha=0.2, color='green')


plt.savefig('AveragePrice.png', dpi=300,
            transparent=False, bbox_inches='tight')
