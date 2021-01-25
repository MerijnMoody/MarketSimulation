import random
import itertools
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
import numpy as np

# Model parameters.
n_buyers = 10000  # Number of buyers.
n_sellers = 500   # Number of sellers.
starting_stock = 20                    # Starting stocks of the sellers.
starting_capital = starting_stock / 2  # Starting capital of the sellers.
rent = starting_capital / 10           # Rent for the sellers.
price_var = 0.05  # Price variability parameter.
max_hunger = 20   # Hunger parameter of the buyer.


# The Buyer class handles each buyer entity.
class Buyer:
    global n_sellers

    # Each buyer is initialized with a random hunger, salary, buy price
    # and random connections to the sellers.
    def __init__(self, p, sellers):
        self.hunger = random.randint(0, max_hunger - 1)
        self.salary = random.random()
        self.buy_price = self.salary - random.random() * self.salary
        self.connections = [sellers[i] for i in range(n_sellers)
                            if random.random() < p]

    # A connection to a new seller can be made in the case that a new seller
    # is added to the model.
    def new_seller(self, p, seller):
        if random.random() < p:
            self.connections.append(seller)

    # Update fuction that is called at each iteration of the simulation.
    def update_buyer(self, sellers):
        cheapest = 2
        best = -1

        # Determines the connected seller with the lowest selling price.
        for seller in self.connections:
            if not seller.alive:
                del seller   # Remove bankrupt sellers from the model
            elif seller.sell_price < cheapest and seller.stock > 0:
                cheapest = seller.sell_price
                best = seller

        # Adjusts the buyer and seller parameters according to the
        # potential purchase made.
        if best != -1 and self.buy_price > cheapest:
            self.hunger = 0
            self.buy_price -= random.random() * price_var
            best.stock -= 1
            best.capital += best.sell_price
            best.buy += 1
        else:
            self.hunger += 1
            self.buy_price = min(self.salary,
                                 self.buy_price
                                 + price_var * random.random())


# The Seller class handles each seller entity.
class Seller:
    global n_sellers, n_buyers, starting_stock

    # Each sellers is initialized with a random production cost and a
    # random selling price.
    def __init__(self):
        self.production_cost = random.random()
        self.sell_price = (self.production_cost
                           + random.random()
                           * (1 - self.production_cost))
        self.stock = starting_stock
        self.capital = starting_capital
        self.buy = 0       # Keeps track of the purchases made in an iteration
        self.alive = True  # False if the seller is no longer part of the model

    # Updates the capital, stock and selling price of the seller.
    def update_seller(self):
        while self.stock < starting_stock:
            self.stock += 1
            self.capital -= self.production_cost
        self.sell_price = max(self.production_cost,
                              (self.sell_price
                               + (self.buy/starting_stock - 0.5)
                               * 2 * random.random() * price_var))
        self.buy = 0
        self.capital -= rent


# Update function for each iteration of the simulation.
def update():
    global sellers, buyers, n_buyers

    # Shuffles the order in which the buyers can pick a seller to buy from for
    # each iteration.
    order = [i for i in range(n_buyers)]
    random.shuffle(order)

    for i in order:
        buyers[i].update_buyer(sellers)

    # Removes inactive buyers from the simulation and replaces them with new
    # buyers.
    buyers = [buyer for buyer in buyers if buyer.hunger < max_hunger]
    while len(buyers) < n_buyers:
        buyers.append(Buyer(p, sellers))

    # Sellers with negative capital are removed from the simulation and
    # replaced with new sellers.
    for seller in sellers:
        seller.alive = True if seller.capital >= 0 else False
        seller.update_seller()

    sellers = [seller for seller in sellers if seller.alive]
    while len(sellers) < n_sellers:
        new_seller = Seller()
        for buyer in buyers:
            buyer.new_seller(p, new_seller)
        sellers.append(new_seller)


# Function that runs a number of iterations of the whole simulation consisting
# of a number of days for a list of p-values. The data is then saved to a file.
def generate_data(p_list, n_iter, n_days):
    global sellers, buyers, p

    for k in range(len(p_list)):
        p = p_list[k]
        print("P: " + str(p))
        final_list_seller = [[] for _ in range(n_days)]
        final_list_buyer = [[] for _ in range(n_days)]
        for i in range(n_iter):
            sellers = [Seller() for _ in range(n_sellers)]
            buyers = [Buyer(p, sellers) for _ in range(n_buyers)]
            print("Iter: " + str(i))
            for j in range(n_days):
                sell_prices = [seller.sell_price for seller in sellers]
                buy_prices = [buyer.buy_price for buyer in buyers]
                seller_average = sum(sell_prices) / len(sell_prices)
                buyer_average = sum(buy_prices) / len(buy_prices)
                final_list_seller[j].append(seller_average)
                final_list_buyer[j].append(buyer_average)
                update()

        # Write the data to the file.
        with open('data.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')

            # Parse the data to one list to write to the data file.
            sell_data = list(itertools.chain.from_iterable(final_list_seller))
            buy_data = list(itertools.chain.from_iterable(final_list_buyer))
            writer.writerow([p, "Sell", n_iter, n_days] + sell_data)
            writer.writerow([p, "Buy", n_iter, n_days] + buy_data)


# Generates the data used for the results. This takes a long time.
p_list = [0.5, 0.1, 0.05, 0.04, 0.03, 0.02, 0.01, 0.005, 0.004,
          0.003, 0.002, 0.001, 0.0025, 0.0015, 0.0005]
generate_data(p_list, 100, 500)


# Plots the buy/selling prices and the salaries/production costs in a bar plot.
buyer_prices = sorted([(b.buy_price, b.salary) for b in buyers], reverse=True)
seller_prices = sorted([(s.sell_price, s.production_cost) for s in sellers])
heights = buyer_prices + seller_prices
height_price = [i[0] for i in heights]
height_bound = [i[1] for i in heights]
y_pos = np.arange(n_buyers + n_sellers)
colors = ['red' for _ in range(n_buyers)] + ['blue' for _ in range(n_sellers)]
plt.bar(y_pos[0:n_buyers],
        height_price[0:n_buyers],
        color=colors[0:n_buyers])
plt.bar(y_pos[n_buyers:n_buyers+n_sellers],
        height_price[n_buyers:n_buyers+n_sellers],
        color=colors[n_buyers:n_buyers+n_sellers],
        alpha=0.2)
plt.bar(y_pos[0:n_buyers],
        height_bound[0:n_buyers],
        color=colors[0:n_buyers],
        alpha=0.2)
plt.bar(y_pos[n_buyers:n_buyers+n_sellers],
        height_bound[n_buyers:n_buyers+n_sellers],
        color=colors[n_buyers:n_buyers+n_sellers])
plt.ylabel('Price')
plt.title('Market convergence')
plt.xticks([])
plt.show()
