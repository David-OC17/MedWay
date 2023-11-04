
from time import strftime
import numpy as np
import csv

class RandomDataGenerator:
    """
    Generates random data for testing the database
    """

    def generator() -> None:
        """
        Generates random data for humidity and returns it in a .csv file
        """

        """
        ID -> Constant
        batch_number -> Constant
        device_number -> Constant
        date -> Use datetime in real-time
        temperature -> 1000 random readings (0°C - 6°C)
        humidity -> 1000 random readings (70% - 95%)
        light_percentage -> (0% - 15%)
        """

        with open("test_data.csv", "a") as file:
            # Create writer object
            writer = csv.writer(file)

            # Get last ID, if file is empty, set last ID to 0
            with open("test_data.csv", "r") as file:
                try:
                    last_line: str = file.readlines()[-2]
                    last_id: int = int(last_line[0:last_line.find(",")])
                except IndexError:
                    last_id: int = 0

            # Generate random data
            batch_number: list[np.int64] = np.full((1, 1000), 195251).tolist()[0]
            device_number: list[np.int64] = np.full((1, 1000), 729864).tolist()[0]
            temperature: list[np.float64] = (6 * np.random.random_sample((1, 1000))).tolist()[0]
            humidity: list[np.float64] = ((95 - 70) * np.random.random((1, 1000)) + 70).tolist()[0]
            light_percentage: list[np.float64] = (15 * np.random.random_sample((1, 1000))).tolist()[0]

            # Write data to file
            for idx in range(1000):
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
