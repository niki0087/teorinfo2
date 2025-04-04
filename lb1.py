import collections
import glob
import numpy as np
import pathlib
import pandas as pd
import pretty_midi
import seaborn as sns
import tensorflow as tf
import os
import datetime
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Tuple

seed = 42
tf.random.set_seed(seed)
np.random.seed(seed)

_SEQUENCE_LENGTH = 32
_BATCH_SIZE = 256

physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    print("Используется GPU:", physical_devices[0])
else:
    print("GPU не найден, используется CPU")

data_dir = pathlib.Path('data/maestro-v2.0.0')
if not data_dir.exists():
    tf.keras.utils.get_file(
        'maestro-v2.0.0-midi.zip',
        origin='https://storage.googleapis.com/magentadata/datasets/maestro/v2.0.0/maestro-v2.0.0-midi.zip',
        extract=True,
        cache_dir='.', cache_subdir='data',
    )

filenames = glob.glob(str(data_dir / '**/*.mid*'))
print(f'Найдено MIDI-файлов: {len(filenames)}')

if not filenames:
    raise ValueError("MIDI файлы не найдены")

def midi_to_notes(midi_file: str) -> pd.DataFrame:
    try:
        pm = pretty_midi.PrettyMIDI(midi_file)
        instrument = pm.instruments[0]
        notes = collections.defaultdict(list)

        sorted_notes = sorted(instrument.notes, key=lambda note: note.start)
        prev_start = sorted_notes[0].start if sorted_notes else 0.0

        for note in sorted_notes:
            start = note.start
            end = note.end
            notes['pitch'].append(note.pitch)
            notes['start'].append(start)
            notes['end'].append(end)
            notes['step'].append(start - prev_start)
            notes['duration'].append(end - start)
            prev_start = start

        return pd.DataFrame({name: np.array(value) for name, value in notes.items()})
    except Exception as e:
        print(f"Ошибка обработки файла {midi_file}: {e}")
        return pd.DataFrame()

def augment_notes(notes_df: pd.DataFrame) -> pd.DataFrame:
    notes_df = notes_df.copy()
    
    if np.random.rand() > 0.5:
        pitch_shift = np.random.randint(-3, 4)
        notes_df['pitch'] = np.clip(notes_df['pitch'] + pitch_shift, 0, 127)
    
    time_stretch = np.random.uniform(0.9, 1.1)
    notes_df['start'] *= time_stretch
    notes_df['end'] *= time_stretch
    
    return notes_df

def plot_notes(notes: pd.DataFrame, title: str = "Нотная последовательность", count: int = None):
    if count:
        notes = notes.head(count)
        title = f"{title} (первые {count} нот)"
    
    plt.figure(figsize=(14, 5))
    plt.title(title)
    plt.plot(notes['start'], notes['pitch'], "bo", markersize=3)
    plt.xlabel('Время (сек)')
    plt.ylabel('Высота ноты')
    plt.grid(True)
    plt.show()

def plot_note_distribution(notes: List[str], title: str = "Распределение нот"):
    plt.figure(figsize=(14, 6))
    note_numbers = [int(note) for note in notes]
    sorted_notes = sorted(note_numbers)
    plt.xticks(rotation=90)
    sns.histplot(sorted_notes, bins=128, kde=False)
    plt.title(title)
    plt.xlabel('MIDI Pitch')
    plt.ylabel('Количество')
    plt.grid(True)
    plt.show()

def notes_to_midi(
    notes: pd.DataFrame,
    out_file: str,
    instrument_name: str,
    velocity: int = 100
) -> pretty_midi.PrettyMIDI:
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    
    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(
        program=pretty_midi.instrument_name_to_program(instrument_name)
    )

    for _, row in notes.iterrows():
        note = pretty_midi.Note(
            velocity=velocity,
            pitch=int(row['pitch']),
            start=float(row['start']),
            end=float(row['end'])
        )
        instrument.notes.append(note)

    pm.instruments.append(instrument)
    pm.write(out_file)
    print(f'Файл сохранен: {os.path.abspath(out_file)}')
    return pm

def create_model(model_type: str, input_shape: Tuple[int, int], n_vocab: int) -> tf.keras.Model:
    l2_reg = tf.keras.regularizers.l2(0.001)
    
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.InputLayer(input_shape=input_shape))
    
    if model_type == 'basic':
        model.add(tf.keras.layers.SimpleRNN(128, activation='tanh', kernel_regularizer=l2_reg, return_sequences=True))
        model.add(tf.keras.layers.BatchNormalization())
        model.add(tf.keras.layers.Dropout(0.3))
        model.add(tf.keras.layers.SimpleRNN(64, activation='tanh', kernel_regularizer=l2_reg))
        model.add(tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=l2_reg))
    
    elif model_type == 'deep':
        model.add(tf.keras.layers.SimpleRNN(128, activation='tanh', kernel_regularizer=l2_reg, return_sequences=True))
        model.add(tf.keras.layers.BatchNormalization())
        model.add(tf.keras.layers.Dropout(0.3))
        model.add(tf.keras.layers.SimpleRNN(64, activation='tanh', kernel_regularizer=l2_reg, return_sequences=True))
        model.add(tf.keras.layers.BatchNormalization())
        model.add(tf.keras.layers.Dropout(0.3))
        model.add(tf.keras.layers.SimpleRNN(32, activation='tanh', kernel_regularizer=l2_reg))
        model.add(tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=l2_reg))
    
    elif model_type == 'bidirectional':
        model.add(tf.keras.layers.Bidirectional(tf.keras.layers.SimpleRNN(64, activation='tanh', kernel_regularizer=l2_reg, return_sequences=True)))
        model.add(tf.keras.layers.BatchNormalization())
        model.add(tf.keras.layers.Dropout(0.3))
        model.add(tf.keras.layers.Bidirectional(tf.keras.layers.SimpleRNN(32, activation='tanh', kernel_regularizer=l2_reg)))
        model.add(tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=l2_reg))
    
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(n_vocab, activation='softmax'))
    
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model

def train_model(model: tf.keras.Model, X: np.ndarray, y: np.ndarray, model_type: str):
    split = int(0.8 * len(X))
    X_train, X_val = X[:split], X[split:]
    y_train, y_val = y[:split], y[split:]
    
    train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))
    train_dataset = train_dataset.shuffle(buffer_size=1024)
    train_dataset = train_dataset.batch(_BATCH_SIZE)
    train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)
    
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            f'{model_type}_best.weights.h5',
            save_best_only=True,
            monitor='val_accuracy',
            mode='max',
            save_weights_only=True),
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=15,
            restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=5,
            min_lr=1e-6),
        tf.keras.callbacks.TerminateOnNaN()
    ]
    
    history = model.fit(
        train_dataset,
        epochs=10,
        validation_data=(X_val, y_val),
        callbacks=callbacks,
        verbose=1)
    
    plot_history(history)
    return history

def plot_history(history):
    plt.figure(figsize=(12, 6))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('История обучения модели')
    plt.xlabel('Эпохи')
    plt.ylabel('Потери')
    plt.legend()
    plt.grid(True)
    plt.show()

def generate_music(
    model: tf.keras.Model, 
    start_sequence: List[int], 
    note_to_int: Dict[str, int], 
    length: int, 
    temperature: float = 0.7
) -> List[str]:
    pitchnames = list(note_to_int.keys())
    int_to_note = {num: note for note, num in note_to_int.items()}
    n_vocab = len(pitchnames)
    
    pattern = start_sequence.copy()
    prediction_output = []
    
    for _ in range(length):
        input_seq = np.reshape(pattern, (1, len(pattern), 1))
        input_seq = input_seq / float(n_vocab)
        
        prediction = model.predict(input_seq, verbose=0)[0]
        prediction = np.log(prediction) / temperature
        exp_preds = np.exp(prediction)
        probabilities = exp_preds / np.sum(exp_preds)
        
        index = np.random.choice(range(n_vocab), p=probabilities)
        result = int_to_note[index]
        prediction_output.append(result)
        
        pattern.append(index)
        pattern = pattern[1:]
    
    return prediction_output

def main():
    print("\nВыберите тип модели:")
    print("1. Базовая RNN (128-64 нейронов)")
    print("2. Глубокая RNN (128-64-32 нейронов)")
    print("3. Двунаправленная RNN (64-32 нейронов)")
    
    while True:
        choice = input("Введите номер (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            break
        print("Неверный ввод! Пожалуйста, введите 1, 2 или 3")
    
    model_types = {"1": "basic", "2": "deep", "3": "bidirectional"}
    model_type = model_types[choice]
    
    print("\nЗагрузка и обработка MIDI файлов...")
    all_notes = []
    for file in filenames[:30]:
        try:
            notes_df = midi_to_notes(file)
            if not notes_df.empty:
                augmented_df = augment_notes(notes_df)
                all_notes.extend(augmented_df['pitch'].astype(str).tolist())
                all_notes.extend(notes_df['pitch'].astype(str).tolist())
        except Exception as e:
            print(f"Ошибка обработки файла {file}: {e}")
    
    if not all_notes:
        raise ValueError("Не удалось загрузить нотные данные")
    
    plot_note_distribution(all_notes[:2000], "Распределение нот (первые 2000)")
    
    note_counts = collections.Counter(all_notes)
    pitchnames = sorted(note_counts.keys())
    note_to_int = {note: num for num, note in enumerate(pitchnames)}
    n_vocab = len(pitchnames)
    print(f"Уникальных нот: {n_vocab}")
    
    network_input = []
    network_output = []
    
    for i in range(0, len(all_notes) - _SEQUENCE_LENGTH, 1):
        sequence_in = all_notes[i:i + _SEQUENCE_LENGTH]
        sequence_out = all_notes[i + _SEQUENCE_LENGTH]
        network_input.append([note_to_int[note] for note in sequence_in])
        network_output.append(note_to_int[sequence_out])
    
    X = np.reshape(network_input, (len(network_input), _SEQUENCE_LENGTH, 1))
    X = X / float(n_vocab)
    y = tf.keras.utils.to_categorical(network_output)
    
    print(f"\nСоздание и обучение {model_type} модели...")
    model = create_model(model_type, (X.shape[1], X.shape[2]), n_vocab)
    history = train_model(model, X, y, model_type)
    
    print("\nГенерация музыкальной последовательности...")
    start_idx = np.random.randint(0, len(all_notes) - _SEQUENCE_LENGTH)
    start_sequence = [note_to_int[note] for note in all_notes[start_idx:start_idx + _SEQUENCE_LENGTH]]
    
    generated_notes = generate_music(
        model, 
        start_sequence, 
        note_to_int, 
        length=300,
        temperature=0.7
    )
    
    generated_df = pd.DataFrame({
        'pitch': [int(note) for note in generated_notes],
        'start': np.arange(len(generated_notes)) * 0.5,
        'end': (np.arange(len(generated_notes)) + 1) * 0.5
    })
    plot_notes(generated_df, "Сгенерированная нотная последовательность", 100)
    
    output_dir = 'generated_music'
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f'generated_{model_type}_{timestamp}.mid')
    
    notes_to_midi(generated_df, output_file, 'Acoustic Grand Piano')
    print(f'\nГенерация завершена. MIDI файл сохранен:\n{os.path.abspath(output_file)}')

if __name__ == "__main__":
    plt.rcParams['figure.figsize'] = [14, 5]
    plt.rcParams['figure.dpi'] = 100
    main()