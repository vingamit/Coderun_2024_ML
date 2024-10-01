import numpy as np
from sklearn.ensemble import IsolationForest


def detect_anomalies(data, threshold=3):
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    z_scores = np.abs((data - mean) / std)
    return np.where(np.any(z_scores > threshold, axis=1))[0]


def main():
    with open('attention_to_emission_input.txt', 'r') as file:
        n, m = map(int, file.readline().strip().split())
        data = []
        for _ in range(n):
            row = list(map(float, file.readline().strip().split()))
            data.append(row)
    
    
    X = np.array(data)
    
    clf = IsolationForest(contamination=0.1, random_state=42)
    y_pred = clf.fit_predict(X)
    
    anomalies = np.where(y_pred == -1)[0]
    
    with open('answer.txt', 'w') as file:
        file.write(f"{len(anomalies)}\n")
        for idx in anomalies:
            file.write(str(idx + 1) + '\n')
    print(len(anomalies))
    for idx in anomalies:
        print(idx + 1)


if __name__ == "__main__":
    main()