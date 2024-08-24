import numpy as np
from scipy.interpolate import griddata

def restore_image(image):
    h, w, c = image.shape
    restored_image = np.zeros((h, w, c), dtype=np.float32)

    for channel in range(c):
        channel_data = image[:, :, channel]
        known_mask = channel_data > 0

        # Координаты известных точек
        coords = np.array(np.nonzero(known_mask)).T
        values = channel_data[known_mask]

        # Координаты всех точек
        grid_coords = np.array(np.meshgrid(np.arange(h), np.arange(w))).T.reshape(-1, 2)
        
        # Интерполяция с использованием метода 'nearest'
        restored_channel = griddata(coords, values, grid_coords, method='nearest').reshape(h, w)

        # Замена нулевых значений восстановленными
        restored_image[:, :, channel] = restored_channel

    # Нормализация и приведение к типу uint8
    restored_image = np.clip(restored_image, 0, 255).astype(np.uint8)
    
    return restored_image

def main():
    # Загрузка данных
    with open('data.npy', 'rb') as file:
        images = np.load(file)

    restored_images = np.zeros_like(images, dtype=np.uint8)

    # Восстановление каждого изображения
    for i in range(images.shape[0]):
        restored_images[i] = restore_image(images[i])

    # Сохранение восстановленных изображений
    with open('answers.npy', 'wb') as file:
        np.save(file, restored_images, allow_pickle=False, fix_imports=False)

if __name__ == "__main__":
    main()
