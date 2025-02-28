from hierarchical_mechanism_LDP import Private_TreeBary
import numpy as np

# test Quantile
B = 4000
b = 4
eps = 1
q = 0.4
protocol = 'unary_encoding'
tree = Private_TreeBary(B, b)
data = np.random.randint(0, B, 100000)
# get quantile of the data
true_quantile = np.quantile(data, q)
# get private quantile
tree.update_tree(data, eps, protocol, post_process=True)
private_quantile = tree.get_quantile(q)
print(f"DP quantile: {private_quantile}")
print(f"True quantile: {true_quantile}")

# test range query
left = 1000
right = 2000
true_range_query = np.sum(data >= left) - np.sum(data >= right)
private_range_query = tree.get_range_query(left, right, normalized=False)
print(f"True range query: {true_range_query}")
print(f"Private range query: {private_range_query}")

# test binning
quantiles = [0.25, 0.50, 0.75]
alpha = 0.1
bins = tree.get_bins(quantiles, alpha)
print("Bins:\n", bins)

# Test amplification by shuffling
delta = 1e-6
shuffle_numerical = tree.get_privacy(shuffle=True, delta=delta, numerical=True)
shuffle_theoretical = tree.get_privacy(shuffle=True, delta=delta, numerical=False)
print(f"For an initial {tree.eps}-DP mechanism, after shuffling {tree.N} users and considering delta = {delta} we obtain"
      f"a numerical upper bound of eps = : {shuffle_numerical} and a theoretical upper bound of eps = {shuffle_theoretical}")



