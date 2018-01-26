import pandas as pd

df = pd.read_csv(filepath_or_buffer='pandas.csv', sep=';')

#df.columns=['sepal_len', 'sepal_wid', 'petal_len', 'petal_wid', 'class']
df.dropna(how="all", inplace=True) # drops the empty line at file-end

df.tail()

X = df.ix[:, 0:16].values
y = df.ix[:,16].values


from sklearn.preprocessing import StandardScaler
X_std = StandardScaler().fit_transform(X)

import numpy as np
mean_vec = np.mean(X_std, axis=0)

cov_mat = np.cov(X_std.T)

eig_vals, eig_vecs = np.linalg.eig(cov_mat)

u,s,v = np.linalg.svd(X_std.T)

for ev in eig_vecs:
    np.testing.assert_array_almost_equal(1.0, np.linalg.norm(ev))
print('Everything ok!')

# Make a list of (eigenvalue, eigenvector) tuples
eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:,i]) for i in range(len(eig_vals))]

# Sort the (eigenvalue, eigenvector) tuples from high to low
eig_pairs.sort()
eig_pairs.reverse()

# Visually confirm that the list is correctly sorted by decreasing eigenvalues
print('Eigenvalues in descending order:')
for i in eig_pairs:
    print(i[0])


tot = sum(eig_vals)
var_exp = [(i / tot)*100 for i in sorted(eig_vals, reverse=True)]
cum_var_exp = np.cumsum(var_exp)

print(var_exp)
print(cum_var_exp)

import matplotlib.pyplot as plt
from matplotlib import style
from mpl_toolkits.mplot3d import axes3d

style.use("ggplot")

fig= plt.figure()

#
plot = fig.add_subplot(111 , projection='3d')
#
# plot.bar([i for i in range(1,17)], var_exp, color = "#e54e37", label="Explained variance in percent")
# plot.plot([i for i in range(1,17)], cum_var_exp, color = "#608edb", label="Cumulative explained variance")
# plot.set_title('Explained variance by different principal components')
# plot.legend(bbox_to_anchor=(.40, 0.7), loc=2, borderaxespad=0.)
# plt.show()

#
# matrix_w = np.hstack((eig_pairs[0][1].reshape(16, 1),
#                       eig_pairs[1][1].reshape(16, 1)))


matrix_w = np.hstack((eig_pairs[0][1].reshape(16, 1),
                      eig_pairs[1][1].reshape(16, 1),
                      eig_pairs[2][1].reshape(16, 1)))

Y = X_std.dot(matrix_w)


# traces = []
# for name in ["Background", "Cognitive", "Emotional", "Afterwards"]:
#     trace = plot.scatter(Y[y==name,0], Y[y==name,1], alpha=0.8, label = name)
#     traces.append(trace)



"""
111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111¶¶¶111111111111111111111
111111111111111111111111111111¶¶¶¶11111111111111111111111
1111111111111111111111111111¶¶¶¶1111111111111111111111111
11111111111111111111111111¶¶¶¶¶¶1111111111111111111111111
111111111111111111111111¶¶¶¶¶¶1111¶¶¶11¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶111
111111111111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶111111111
11111111111111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶111111111111
11111111111111111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1111
1111111111111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1111111111
111111111111111¶¶¶111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1111111
111111111111¶¶¶¶¶11¶¶¶¶¶¶¶¶¶¶¶11¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶111111
11111111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1¶¶1111¶¶¶¶¶¶¶¶¶¶¶¶¶11¶¶¶¶¶1111
1111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶111¶11111¶¶¶¶¶¶¶¶¶¶¶¶¶111¶¶¶¶111
11111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶111111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1111¶¶¶11
1111¶¶¶¶¶¶¶¶111111111111111111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶11111¶¶1
11111¶¶¶¶¶111111111111111111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶11111111
1111111¶1111111111111111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1111111
1111111111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1111111
111111111111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶11¶¶¶¶¶1111111
11111111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1111¶¶¶¶¶1111111
11111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶111111¶¶¶¶1111111
111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶111111111¶¶¶¶1111111
1111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶11111111111¶¶¶¶1111111
111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶111¶¶¶¶¶¶111111111111111¶¶¶11111111
11¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1111111111111111111111111111¶¶111111111
1¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶11111111111111111¶¶1111111111111111111111
¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶111111111111111111111¶¶¶¶11111111111111111
¶¶¶¶¶¶¶¶¶¶1¶¶¶111111111111111111111111¶¶¶¶¶11111111111111
¶¶¶¶¶¶¶¶¶¶11¶¶11111111111111111111111111¶¶¶¶¶¶¶1111111111
¶¶¶¶¶¶¶¶¶¶¶111¶111111111111¶¶¶11111¶¶¶¶111¶¶¶¶¶¶¶11111111
¶¶¶¶¶¶¶¶¶¶¶¶11111111111111111¶¶¶11111¶¶¶¶¶¶¶¶¶¶¶¶¶¶111111
¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶11111111111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1111
¶1¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶111111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶11
¶¶11¶¶¶¶¶¶¶¶¶¶¶¶111111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶111¶¶¶¶¶¶¶¶¶¶¶¶1
1¶11¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶11111111111¶¶¶¶¶¶¶¶
1111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶11111111111111¶¶¶¶¶¶
1111¶¶¶¶¶1¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶11¶¶¶¶¶¶¶¶11111111111111¶¶¶¶¶
11111¶¶¶11111¶¶¶¶¶¶¶¶¶¶¶¶¶11111¶¶¶¶¶¶¶¶¶¶11111111111111¶¶
1111¶¶¶11111111¶¶¶1¶¶¶¶¶¶¶¶¶11111¶¶¶¶¶11111111111111111¶¶
1111¶¶¶111111111111111¶¶¶¶¶¶¶1111111¶¶¶¶¶¶¶¶111111111111¶
11111¶¶1111111111111111111¶¶¶¶¶1111111111111111111111111¶
111111¶11111111111111111111¶¶¶¶11111111111111111111111111
1111111111111111111111111111¶¶¶11111111111111111111111111
11111111111111111111111111111¶¶11111111111111111111111111
111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111
"""



traces = []
for name in ["Background", "Cognitive", "Emotional", "Afterwards"]:
    trace = plot.scatter(Y[y==name,0], Y[y==name,1], Y[y==name,2], alpha=0.8, label = name)
    traces.append(trace)

plot.legend(bbox_to_anchor=(1.05, 0.8), loc=2, borderaxespad=0.)
plot.set_title('Distribution plot - 3D')
fig.subplots_adjust(left=0.07, bottom=0.05, right=0.750, top=0.95)
plt.show()

