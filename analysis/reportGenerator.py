'''
This functions use a LaTeX template to dynamically add data for the report and generate it for the given
period of time. There are three templates, one for each period option.

Take default images and take new graphs from the `images` directory.
Save the reports into the `reports` folder.
'''

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import shutil
import subprocess

def conditionStatistics(withStats:bool=True, testing:bool=False, show:bool=False, maskOutliers:bool=False) -> tuple:
    '''
    Reads the appropriate file, creates the plots for the report and gets the min/max of temperature,
    humidity and light.
    '''
    # ["ID", "batch_number", "device_number", "date", "temperature", "humidity", "light_percentage"]
    # Keep: ["date", "temperature", "humidity", "light_percentage"]
    if testing:
        path = '../test/data/sensor_data_train.csv'
        data = pd.read_csv(path)
        columns_drop = ["ID", "batch_number", "device_number", "state"]
        data = data.drop(columns=columns_drop, inplace=False)
        
    else: 
        path = './temp/tempData.csv'
        data = pd.read_csv(path)
        columns_drop = ["ID", "batch_number", "device_number"]
        data = data.drop(columns=columns_drop, inplace=False)
    
    windowSize = 1000
    data["date"] = pd.to_datetime(data["date"])
    
    if maskOutliers:
        # Remove outliers to be able to see the mean clearly
        # Create a boolean mask for rows within the specified range
        tempRange = (0, 6)
        humRange = (50, 70)
        lightRange = (0, 15)
        
        mask = (
            (data["temperature"] >= tempRange[0]) & (data["temperature"] <= tempRange[1]) &
            (data["humidity"] >= humRange[0]) & (data["humidity"] <= humRange[1]) &
            (data["light_percentage"] >= lightRange[0]) & (data["light_percentage"] <= lightRange[1])
        )
        data = data[mask]
    
    # Get the max and min for temperature, hum...
    minTemp = data["temperature"].min()
    maxTemp = data["temperature"].max()
    
    minHum = data["humidity"].min()
    maxHum = data["humidity"].max()
    
    minLight = data["light_percentage"].min()
    maxLight = data["light_percentage"].max()

    # Compute rolling mean statistics for all three variables    
    tempRollingMean = data['temperature'].rolling(window=windowSize, center=False).mean()
    humRollingMean = data['humidity'].rolling(window=windowSize, center=False).mean()
    lightRollingMean = data['light_percentage'].rolling(window=windowSize, center=False).mean()

    # Calculate the std deviation
    stdTemp = data["temperature"].std()
    stdHum = data["humidity"].std()
    stdLight = data["light_percentage"].std()
    
    if withStats:
        upperBand_temp = tempRollingMean + stdTemp
        lowerBand_temp = tempRollingMean - stdTemp

        upperBand_hum = humRollingMean + stdHum
        lowerBand_hum = humRollingMean - stdHum

        upperBand_light = lightRollingMean + stdLight
        lowerBand_light = lightRollingMean - stdLight
        
    ##### Produce the plots and save them to ./temp/
    sns.set_style("dark")
     
    ##### TEMPERATURE #####
    plt.figure(figsize=(10,6))
    sns.lineplot(data=tempRollingMean, label='Mean Temperature')
    z = np.polyfit(data.index, data["temperature"], 1)
    p = np.poly1d(z)
    plt.plot(data.index, p(data.index), "r--")    
    
    if withStats:
        sns.lineplot(data=upperBand_temp, label='Upper Band Temperature')
        sns.lineplot(data=lowerBand_temp, label='Lower Band Temperature')

    plt.title("Temperature over the day.")
    plt.xlabel("Temperature readings")
    plt.ylabel("Temperature °C")
    plt.legend(loc='upper left')
    if show: plt.show()
    else: plt.savefig("./temp/temperature_plot.png")
    plt.close()
    
    ##### HUMIDITY #####
    plt.figure(figsize=(10,6))
    hum = humRollingMean.plot(title="Humidity over the day.")
    z = np.polyfit(data.index, data["humidity"], 1)
    p = np.poly1d(z)
    plt.plot(data.index, p(data.index), "r--")
    
    if withStats:
        sns.lineplot(data=upperBand_hum, label='Upper Band Humidity', ax=hum)
        sns.lineplot(data=lowerBand_hum, label='Lower Band Humidity', ax=hum)

    hum.set_xlabel("Humidity readings")
    hum.set_ylabel("Humidity %")
    hum.legend(loc='upper left')
    if show: plt.show()
    else: plt.savefig("./temp/humidity_plot.png")
    plt.close()

    ##### LIGHT #####
    plt.figure(figsize=(10,6))
    light = lightRollingMean.plot(title="Light over the day.")
    z = np.polyfit(data.index, data["light_percentage"], 1)
    p = np.poly1d(z)
    plt.plot(data.index, p(data.index), "r--")
    
    if withStats:
        sns.lineplot(data=upperBand_light, label='Upper Band Light', ax=light)
        sns.lineplot(data=lowerBand_light, label='Lower Band Light', ax=light)

    light.set_xlabel("UV-Light readings")
    light.set_ylabel("Light %")
    light.legend(loc='upper left')
    if show: plt.show()
    else: plt.savefig("./temp/light_plot.png")
    plt.close()
    
    # Round the min/max values before return (2 decimals)
    minTemp = round(minTemp, 2)
    maxTemp = round(maxTemp, 2)
    minHum = round(minHum, 2)
    maxHum = round(maxHum, 2)
    minLight = round(minLight, 2)
    maxLight = round(maxLight, 2)
    
    return (minTemp, maxTemp, minHum, maxHum, minLight, maxLight)

def createStateTable(states:map) -> None:
    pass

def generatePDF(product:str, alertCount:int, numBatches:int, goodBatches:int, badBatches:int, minTemp:float, maxTemp:float, minHum:float, maxHum:float, minLight:float, maxLight:float) -> None:
    '''
    Takes the appropriate template, adds the dynamic data, compiles into a `.pdf` document.
    '''
    
    # Read the template
    with open('./templates/dailyReportTemplate.tex', 'r') as template_file:
        template_content = template_file.read()

    # Fill the template
    
    percGoodBatches = (goodBatches / numBatches) * 100
    percBadBatches = (badBatches / numBatches) * 100
    periodType = 'daily'
    
    template_content = template_content.replace("<<PRODUCT>>", str(product))
    template_content = template_content.replace("<<PERIOD_TYPE>>", str(periodType))
    template_content = template_content.replace("<<GOOD_BATCHES>>", str(goodBatches))
    template_content = template_content.replace("<<NUM_ALERTS>>", str(alertCount))
    template_content = template_content.replace("<<BAD_BATCHES>>", str(badBatches))
    template_content = template_content.replace("<<TOTAL_BATCHES>>", str(numBatches))
    template_content = template_content.replace("<<PERC_GOOD_BATCHES>>", str(percGoodBatches))
    template_content = template_content.replace("<<PERC_BAD_BATCHES>>", str(percBadBatches))
    template_content = template_content.replace("<<HIGHEST_TEMPERATURE>>", str(maxTemp))
    template_content = template_content.replace("<<LOWEST_TEMPERATURE>>", str(minTemp))
    template_content = template_content.replace("<<HIGHEST_HUMIDITY>>", str(maxHum))
    template_content = template_content.replace("<<LOWEST_HUMIDITY>>", str(minHum))
    template_content = template_content.replace("<<HIGHEST_UV_LIGHT>>", str(maxLight))
    template_content = template_content.replace("<<LOWEST_UV_LIGHT>>", str(minLight))

    # Write the filled template to a new file
    with open('./temp/dailyReport.tex', 'w') as filled_template_file:
        filled_template_file.write(template_content)

    # Compile LaTeX to PDF using pdflatex
    # -output-directory=./reports/dailyReport.pdf
    subprocess.run(['pdflatex', '-shell-escape', './temp/dailyReport.tex'])