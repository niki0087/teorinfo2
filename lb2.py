import tensorflow as tf
import matplotlib.pyplot as plt
import os

# Принудительно используем CPU (раскомментируйте при проблемах с GPU)
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Параметры
IMG_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 15
NOISE_FACTOR = 0.3

# Пути к данным
TRAIN_PATH = '/home/nikita/Институт/teorinf/teorinfo2/data/pets_4_classes/train'
TEST_PATH = '/home/nikita/Институт/teorinf/teorinfo2/data/pets_4_classes/test'

# Проверка существования путей
if not os.path.exists(TRAIN_PATH):
    raise FileNotFoundError(f"Train directory {TRAIN_PATH} not found!")
if not os.path.exists(TEST_PATH):
    raise FileNotFoundError(f"Test directory {TEST_PATH} not found!")

# Загрузка данных
def load_dataset(directory):
    # Проверка наличия файлов
    files = tf.io.gfile.glob(os.path.join(directory, '*/*.jpg'))
    if not files:
        raise FileNotFoundError(f"No JPG files found in {directory}")
    
    list_ds = tf.data.Dataset.list_files(files, shuffle=True)
    
    def process_path(file_path):
        img = tf.io.read_file(file_path)
        img = tf.image.decode_jpeg(img, channels=3)
        img = tf.image.convert_image_dtype(img, tf.float32)
        img = tf.image.resize(img, IMG_SIZE)
        return img
    
    return (list_ds.map(process_path, num_parallel_calls=tf.data.AUTOTUNE)
                  .batch(BATCH_SIZE)
                  .prefetch(tf.data.AUTOTUNE))

# Загрузка данных
try:
    train_ds = load_dataset(TRAIN_PATH)
    test_ds = load_dataset(TEST_PATH)
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit()

# Добавление шума
def add_noise(image):
    noise = tf.random.normal(shape=tf.shape(image), mean=0.0, stddev=NOISE_FACTOR)
    return tf.clip_by_value(image + noise, 0.0, 1.0)

# Подготовка данных
train_ds_noisy = train_ds.map(lambda x: (add_noise(x), x))
test_ds_noisy = test_ds.map(lambda x: (add_noise(x), x))

# Архитектуры моделей
def build_dense_ae(input_shape):
    inputs = tf.keras.Input(shape=input_shape)
    
    # Энкодер
    x = tf.keras.layers.Flatten()(inputs)
    x = tf.keras.layers.Dense(512, activation='relu')(x)
    x = tf.keras.layers.Dense(256, activation='relu')(x)
    encoded = tf.keras.layers.Dense(128, activation='relu')(x)
    
    # Декодер
    x = tf.keras.layers.Dense(256, activation='relu')(encoded)
    x = tf.keras.layers.Dense(512, activation='relu')(x)
    
    # Исправленный расчет размера
    flattened_size = input_shape[0] * input_shape[1] * input_shape[2]
    x = tf.keras.layers.Dense(flattened_size, activation='sigmoid')(x)
    decoded = tf.keras.layers.Reshape(input_shape)(x)
    
    return tf.keras.Model(inputs, decoded, name="Dense_AE")

def build_cnn_ae(input_shape):
    inputs = tf.keras.Input(shape=input_shape)
    
    # Энкодер
    x = tf.keras.layers.Conv2D(32, (3,3), activation='relu', padding='same')(inputs)
    x = tf.keras.layers.MaxPooling2D((2,2))(x)
    x = tf.keras.layers.Conv2D(64, (3,3), activation='relu', padding='same')(x)
    encoded = tf.keras.layers.MaxPooling2D((2,2))(x)
    
    # Декодер
    x = tf.keras.layers.Conv2D(64, (3,3), activation='relu', padding='same')(encoded)
    x = tf.keras.layers.UpSampling2D((2,2))(x)
    x = tf.keras.layers.Conv2D(32, (3,3), activation='relu', padding='same')(x)
    x = tf.keras.layers.UpSampling2D((2,2))(x)
    decoded = tf.keras.layers.Conv2D(3, (3,3), activation='sigmoid', padding='same')(x)
    
    return tf.keras.Model(inputs, decoded, name="CNN_AE")

# Создание моделей
input_shape = (IMG_SIZE[0], IMG_SIZE[1], 3)
dense_ae = build_dense_ae(input_shape)
cnn_ae = build_cnn_ae(input_shape)

# Компиляция моделей
dense_ae.compile(optimizer='adam', loss='mse')
cnn_ae.compile(optimizer='adam', loss='mse')

# Выбор модели
model = None
while model is None:
    print("\n" + "="*40)
    print("Выберите архитектуру автоэнкодера:")
    print("1 - Полносвязная сеть")
    print("2 - Сверточная сеть")
    choice = input("Ваш выбор (1/2): ").strip()
    
    if choice == '1':
        model = dense_ae
        print("\nВыбрана полносвязная архитектура")
    elif choice == '2':
        model = cnn_ae
        print("\nВыбрана сверточная архитектура")
    else:
        print("\nНекорректный ввод! Пожалуйста, введите 1 или 2")

# Обучение модели
print("\nНачало обучения...")
history = model.fit(
    train_ds_noisy,
    epochs=EPOCHS,
    validation_data=test_ds_noisy,
    verbose=1
)

# Визуализация результатов
def plot_results(test_data, model, num_images=5):
    test_images = next(iter(test_data))
    noisy_images = add_noise(test_images)
    reconstructed = model.predict(noisy_images)
    
    plt.figure(figsize=(15, 6))
    for i in range(num_images):
        # Оригинал
        plt.subplot(3, num_images, i+1)
        plt.imshow(test_images[i])
        plt.title("Original")
        plt.axis('off')
        
        # Зашумленный
        plt.subplot(3, num_images, num_images+i+1)
        plt.imshow(noisy_images[i])
        plt.title("Noisy")
        plt.axis('off')
        
        # Восстановленный
        plt.subplot(3, num_images, 2*num_images+i+1)
        plt.imshow(reconstructed[i])
        plt.title("Reconstructed")
        plt.axis('off')
    
    plt.tight_layout()
    plt.show()

# Отображение результатов
try:
    plot_results(test_ds, model)
except Exception as e:
    print(f"\nОшибка при визуализации: {e}")

# Вывод истории обучения
if history:
    plt.figure(figsize=(10, 5))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('График обучения')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()