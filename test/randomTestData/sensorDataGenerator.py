
from time import strftime
import numpy as np
import csv

class RandomDataGenerator:
    """
    Generates random data for testing the database.
    """
    def __init__(self):
        print('Data generator created.')
        
    def replaceSome(self, light:list[np.float64], humidity: list[np.float64], temperature: list[np.float64], percentageReplace:float) -> tuple[list[np.float64], list[np.float64], list[np.float64], list[bool]]:
        '''
        Receives a data list for light percentage and replaces a percentage of the values for values that are outside the original range,
        generating some data that represents the medicine going out of the recommended state for preservation.
        At the end of each line, add another column that is if the batch suffered any irregularity, which will be all true for
        the altered rows.
        Returns all the lists that it got plus the status, contained in a tuple.
        '''
        
        '''
        Steps of the operation:
        1. Define new ranges for the values
        2. Define which values to change from what is available
        3. Do the replacement
        4. Add the appropriate value to the state column (used for training the model)
        5. Return all the modified parameters
        '''
        
        # Verify that the length of the lists is the same for all 
        assert(len(light) == len(humidity))
        assert(len(light) == len(temperature))

        numData = len(light)
        
        # Define the original range and the new range
        new_light_range = (70, 90)
        new_humidity_range = (70, 100)
        new_temperature_range = (6, 10)

        # Choose <percentage>% of the indices randomly
        # Use the same indexes for temperature and humidity, but different for light
        randomIncrease_light = np.random.uniform(low=0.05, high=0.3)
        randomIncrease_humidity = np.random.uniform(low=0.05, high=0.3)
        randomIncrease_temperature = np.random.uniform(low=0.05, high=0.3)
        
        num_elements_to_change_light = int((percentageReplace + randomIncrease_light)* numData)
        num_elements_to_change_humidity = int((percentageReplace + randomIncrease_humidity) * numData)
        num_elements_to_change_temperature = int((percentageReplace + randomIncrease_temperature) * numData)
        
        indices_to_change_light = np.random.choice(numData, num_elements_to_change_light, replace=False)
        indices_to_change_humidity = np.random.choice(numData, num_elements_to_change_light, replace=False)
        indices_to_change_temperature = np.random.choice(numData, num_elements_to_change_light, replace=False)
        
        
        # Print for debugging
        # print('Elements to change: ', num_elements_to_change_humidity)
        # print('Indices to change: ', indices_to_change_humidity)
        # print('Num indices: ', len(indices_to_change_humidity))
        
        
        # Add to the batch_alerts.csv file
        # Adjust the values at the selected indices to the new range
        for idx in indices_to_change_light:
            light[idx] = np.random.uniform(low=new_light_range[0], high=new_light_range[1])
        
        for idx in indices_to_change_light:
            humidity[idx] = np.random.uniform(low=new_humidity_range[0], high=new_humidity_range[1])
            
        for idx in indices_to_change_light:
            temperature[idx] = np.random.uniform(low=new_temperature_range[0], high=new_temperature_range[1])

        # Create the 'state' of the medicine list and populate it accordingly
        # The list is of the same size as any of the other lists, and will have a value of true if the index is inside modifiedIndexes
        
        allModifiedIndexes = set(indices_to_change_light + indices_to_change_humidity + indices_to_change_temperature)
        modifiedIndexes = list(allModifiedIndexes)
        
        state = [idx in modifiedIndexes for idx in range(numData)]
        
        # Return the tuple of all the modified lists and the new state for the row
        return light, humidity, temperature, state
    
    def generator(self, numData:int, numBatches:int, withLabels:bool = False) -> None:
        """
        Generates random data for humidity and returns it in a .csv file.
        Generates numData * numBatches rows of information.
        Select if to generate the data with or without labels via the withLabels parameter (true -> include labels).
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
        
        # Select the appropriate values for including labels or not (default to false)
        if withLabels:
            header = ["ID", "batch_number", "device_number", "date", "temperature", "humidity", "light_percentage", "state"]
            pathToFile = "../data/sensor_data_train.csv"
        else:
            header = ["ID", "batch_number", "device_number", "date", "temperature", "humidity", "light_percentage"]
            pathToFile = "../data/sensor_data.csv"
            
        
        # Create some batch numbers at random
        this_batch_numbers: list[int] = np.random.randint(1000, 100000 + 1, numBatches).tolist()
        
        with open(pathToFile, "a") as file:
            # Create writer object
            writer = csv.writer(file, lineterminator='\n')

            # Get last ID, if file is empty, set last ID to 0
            with open(pathToFile, "r") as file:
                try:
                    last_line: str = file.readlines()[-2]
                    last_id: int = int(last_line[0:last_line.find(",")])
                except IndexError:
                    #Add title to the .csv file
                    writer.writerow(header)
                    last_id: int = 0


            # Write several data rows for each batch number
            for this_batch_number in this_batch_numbers:
                # Generate random data
                batch_number: list[np.int64] = np.full((1, numData), this_batch_number).tolist()[0]
                device_number: list[np.int64] = np.full((1, numData), 729864).tolist()[0]
                temperature: list[np.float64] = (6 * np.random.random_sample((1, numData))).tolist()[0]
                humidity: list[np.float64] = ((70 - 50) * np.random.random((1, numData)) + 50).tolist()[0]
                light_percentage: list[np.float64] = (15 * np.random.random_sample((1, numData))).tolist()[0]
                
                # Check which values in the temperature, humidity or light percentage are over the accepted 
                #   limit and generate a line for the batch alerts if so
                # light --> 0, humidity --> 1, temperature --> 2, list[bool] --> 3
                if withLabels:
                    modified = self.replaceSome(light=light_percentage, temperature=temperature, humidity=humidity, percentageReplace=0.05)
                
                    # Write data to file
                    for idx in range(numData):
                        date: str = strftime("%d/%b/%Y %H:%M:%S")
                        row: tuple = (
                            last_id + 1,
                            batch_number[idx],
                            device_number[idx],
                            date,
                            modified[2][idx],
                            modified[1][idx],
                            modified[0][idx],
                            not modified[3][idx]
                        )
                        writer.writerow(row)
                        last_id += 1
                
                else:                
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