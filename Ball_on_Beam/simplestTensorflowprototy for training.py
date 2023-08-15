import tensorflow as tf
import numpy as np
import pandas as pd


excel_file = "C:/Users/knn/OneDrive - EFIF/AI/tensor with beam data/measurement_distance_vinkel2.xlsx" #vinkel.xlsx"
df = pd.read_excel(excel_file)

# Convert DataFrame to a NumPy array
numpy_array = df.to_numpy()

print(numpy_array)

#print("selected : ",numpy_array[:,1])

# Create some example input data
#input_data = np.array([[0.1], [0.4], [0.7]])
input_data = numpy_array[:,2]   # afstand til bold

# Create some example target output data
target_output = numpy_array[:,1]

# Define the neural network model
#model = tf.keras.models.Sequential([
#    tf.keras.layers.Dense(units=1, activation='linear', input_shape=(1,))
#])

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(units=10, activation='relu', input_shape=(1,)),
    tf.keras.layers.Dense(units=1, activation='linear')
])

# Compile the model
model.compile(optimizer='sgd', loss='mean_squared_error')

# Print the initial weights of the model
print("Initial Weights:")
print(model.layers[0].get_weights())

# Train the model on the input data and target output
model.fit(input_data, target_output, epochs=1000, verbose=1)

# Print the final weights of the model
print("\nFinal Weights:")
print(model.layers[0].get_weights())

input_data = np.array([[-0.8],[-0.6],[-0.4],[-0.2],[0.0],[0.2],[0.4],[0.6],[0.8]])


print (model.predict(input_data))
