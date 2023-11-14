
from time import strftime
import numpy as np
import csv

class RandomDataGenerator:
    """
    Generates random data for testing the database.
    """
    def __init__(self):
        print('Data generator created.')
        
    def replaceSome(numData:int, light:list[np.float64], humidity: list[np.float64], temperature: list[np.float64], percentageReplace:float) -> list[np.float64]:
        '''
        Receives a data list for light percentage and replaces a percentage of the values for values that are outside the original range,
        generating some data that triggers the 
        '''

        # Define the original range and the new range
        new_light_range = (20, 30)
        new_humidity_range = (70, 100)
        new_temperature_range = (6, 10)

        # Choose <percentage>% of the indices randomly
        # Use the same indexes for temperature and humidty, but different for light
        num_elements_to_change_light = int(percentageReplace * numData)
        indices_to_change = np.random.choice(numData, num_elements_to_change_light, replace=False)
        
        
        
        # Add to the batch_alerts.csv file

        # Adjust the values at the selected indices to the new range
        light[indices_to_change] = np.random.uniform(new_light_range[0], new_light_range[1], num_elements_to_change)
        humidity[indices_to_change] = np.random.uniform(new_light_range[0], new_light_range[1], num_elements_to_change)
        temperature[indices_to_change] = np.random.uniform(new_light_range[0], new_light_range[1], num_elements_to_change)
    

    def generator(self, numData:int) -> None:
        """
        Generates random data for humidity and returns it in a .csv file
        """

        """
        ID -> Constant
        batch_number -> Constant
        device_number -> Constant
        date -> Use datetime in real-time
        temperature -> 1000 random readings (0°C - 6°C)(sometimes going to 10°C)
        humidity -> 1000 random readings (50% - 70%)(sometimes going to 100%)
        light_percentage -> (0% - 15%)(sometimes going over and to 20%)
        """

        with open("../data/sensor_data.csv", "a") as file:
            # Create writer object
            writer = csv.writer(file)

            # Get last ID, if file is empty, set last ID to 0
            with open("../data/sensor_data.csv", "r") as file:
                try:
                    last_line: str = file.readlines()[-2]
                    last_id: int = int(last_line[0:last_line.find(",")])
                except IndexError:
                    #Add title to the .csv file
                    header = ["ID", "batch_number", "device_number", "date", "temperature", "humidity", "light_percentage"]
                    writer.writerow(header)
                    last_id: int = 0

            # Generate random data
            batch_number: list[np.int64] = np.full((1, numData), 195251).tolist()[0]
            device_number: list[np.int64] = np.full((1, numData), 729864).tolist()[0]
            temperature: list[np.float64] = (6 * np.random.random_sample((1, numData))).tolist()[0]
            humidity: list[np.float64] = ((70 - 50) * np.random.random((1, numData)) + 50).tolist()[0]
            light_percentage: list[np.float64] = (15 * np.random.random_sample((1, numData))).tolist()[0]
            
            # Check which values in the temperature, humity or light percentage are over the accepted 
            #   limit and generate a line for the batch alerts if so
            self.replaceSome(temperature, humidity, light_percentage)
            
            # Write data to file
            for idx in range(numData):
                date: str = strftime("%d/%b/%Y %H:%M:%S")
                row: tuple = (
                    last_id + 1,
                    batch_number[idx],
                    device_number[idx],
                    date,
                    temperature[idx],
                    humidity[idx],
                    light_percentage[idx]
                )
                writer.writerow(row)
                last_id += 1

        file.close()
