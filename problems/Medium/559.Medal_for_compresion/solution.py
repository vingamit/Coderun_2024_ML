import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


n, m, p = map(float, input().split())
n, m = int(n), int(m)

X = []
y = []
for _ in range(n):
    row = list(map(float, input().split()))
    X.append(row[:-1])
    y.append(row[-1])

X = np.array(X)
y = np.array(y)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

target_components = int(2 / 3 * m)
pca = PCA(n_components=target_components)
X_pca = pca.fit_transform(X_scaled)

print(X_pca.shape[1])
for row in X_pca:
    print(" ".join(map(str, row)))