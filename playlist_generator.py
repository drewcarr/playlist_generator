import random
import generate_training_data

import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

test_ids = []

def plot_value_array(prediction):
    predictions_array = prediction[1:3]
    plt.grid(False)
    plt.xticks(np.arange(-1, 2, step=1))
    plt.yticks(np.arange(0, 1, step=.25))
    thisplot = plt.bar(range(2), predictions_array, color="#777777")
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('blue')
    if (predicted_label == 0):
        thisplot[0].set_color('red')

def show_song_info (subplot, id):
    song_data = generate_training_data.get_song_data(id)

    song_name = song_data['Name']
    if (len(song_name) > 14):
        song_name = song_name[0:14] + "..."

    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    subplot.text(0.05, 0.85, song_name, fontsize=10)
    subplot.text(0.05, 0.65, "Skips: " + str(song_data["Skip Count"]), fontsize=10)
    subplot.text(0.05, 0.45, "Genre: " + song_data["Genre"], fontsize=10)
    subplot.text(0.05, 0.25, "Plays: " + str(song_data["Play Count"]), fontsize=10)
    subplot.text(0.05, 0.05, "Year: " + str(song_data["Year"]), fontsize=10)

training_data = generate_training_data.get_training_data()
test_data = []
for data in training_data:
    if (data[1] == 0):
        print ("Adding to test: ", data[1])
        test_data.append(data)

# Holds the [year, plays, skips, genre]
train_variables = np.array([i[0] for i in training_data])
# Holds whether in playlist 0 or 1
train_labels = np.array([i[1] for i in training_data])
# Holds song id for identification
train_ids = np.array([i[2] for i in training_data])

# Holds the [year, plays, skips, genre]
test_variables = np.array([i[0] for i in test_data])
# Holds whether in playlist 0 or 1
test_labels = np.array([i[1] for i in test_data])
# Holds song id for identification
test_ids = np.array([i[2] for i in test_data])

model = keras.Sequential([
    keras.layers.Dense(4),
    keras.layers.Dense(10, activation=tf.nn.relu),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])

model.compile(optimizer=tf.train.AdamOptimizer(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(train_variables, train_labels, epochs=50)

# test_loss, test_acc = model.evaluate(test_variables, test_labels)

# print('Test accuracy:', test_acc)

predictions = model.predict(test_variables)
sorted_predictions = []
for i in range(len(predictions)):
    sorted_predictions.append((test_ids[i], predictions[i][0], predictions[i][1]))

sorted_predictions = sorted(sorted_predictions, key=lambda value: value[1])

num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(15):
    plt.subplot(num_rows, 2*num_cols, 2*i+1)
    plot_value_array(sorted_predictions[i])
    subplot = plt.subplot(num_rows, 2*num_cols, 2*i+2)
    show_song_info(subplot, sorted_predictions[i][0])

plt.tight_layout()
plt.show()
