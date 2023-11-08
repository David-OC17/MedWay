import pandas as pd
import matplotlib.pyplot as plt

# Read the data from a CSV file
df = pd.read_csv('test_data.csv')

# Extract data for temperature, humidity, and light
temperature = df['temperature']
humidity = df['humidity']
light = df['light_percentage']

# Create subplots for each type of data
fig, axs = plt.subplots(3, 1, figsize=(10, 10))

# Plot temperature data
axs[0].plot(df['ID'], temperature, marker='o', color='blue')
axs[0].set_title('Temperature')
axs[0].set_xlabel('ID')
axs[0].set_ylabel('Temperature')

# Plot humidity data
axs[1].plot(df['ID'], humidity, marker='o', color='green')
axs[1].set_title('Humidity')
axs[1].set_xlabel('ID')
axs[1].set_ylabel('Humidity')

# Plot light data
axs[2].plot(df['ID'], light, marker='o', color='orange')
axs[2].set_title('Light')
axs[2].set_xlabel('ID')
axs[2].set_ylabel('Light Percentage')

# Adjust the layout
plt.tight_layout()

# Show the plots
plt.show()
