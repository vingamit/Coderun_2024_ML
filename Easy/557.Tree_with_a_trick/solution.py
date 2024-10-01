import sys

def generate_dataset(f, c, n, tree):
    dataset = []
    visited = set()

    def traverse(node, features):
        if node == -1:
            return
        
        if tree[node][0] == -1 and tree[node][1] == -1:
            # Лист
            if node not in visited:
                dataset.append(features)
                visited.add(node)
        else:
            # Внутренний узел
            s, t = tree[node][2], tree[node][3]
            
            # Проверка корректности индекса признака
            if s < 1 or s > f:
                print(f"Ошибка: некорректный индекс признака {s} для узла {node}")
                return
            
            # Идем влево
            left_features = features.copy()
            left_features[s-1] = t - 1.0
            traverse(tree[node][0], left_features)
            
            # Идем вправо
            right_features = features.copy()
            right_features[s-1] = t + 1.0
            traverse(tree[node][1], right_features)

    # Начинаем с корня (узел 1)
    traverse(1, [-1000.0] * f)

    return dataset

# Чтение входных данных
f, c, n = map(int, input().split())
tree = [None] * (n + 1)  # Индексация с 1

for i in range(1, n + 1):
    p, q = map(int, input().split())
    if p == -1 and q == -1:
        # Лист
        k = int(input())
        tree[i] = [-1, -1, k, None]
    else:
        # Внутренний узел
        s, t = map(float, input().split())
        tree[i] = [p, q, int(s), t]  # s - это индекс признака, t - порог

# Генерация датасета
dataset = generate_dataset(f, c, n, tree)

# Вывод результата
print(len(dataset))
for features in dataset:
    print(' '.join(f"{x:.1f}" for x in features))