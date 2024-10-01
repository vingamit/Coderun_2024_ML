import numpy as np
import matplotlib.pyplot as plt

# Загрузка данных из файла
with open('answers.npy', 'rb') as file:
    images = np.load(file)

# Функция для отображения изображений
def show_images(images):
    num_images = images.shape[0]
    
    plt.figure(figsize=(30, 20))
    
    for i in range(num_images):
        plt.subplot(1, num_images, i + 1)
        plt.imshow(images[i], cmap='gray')
        plt.title(f'Image {i + 1}')
        plt.axis('off')  # Скрыть оси

    plt.show()

# Вызов функции для отображения изображений
show_images(images)
