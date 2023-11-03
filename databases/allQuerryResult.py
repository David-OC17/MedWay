'''
This a class used for the return value of an 'all' querry to the cloud database.
It contains numpy arrays for the different data matrices that the querries produce.
These arrays may be later used for easy data analysis.
'''

import numpy as np

class QuerryResult:
    def __init__(self, querryType: str) -> None:
        '''
        Provide a querry type to create attributes for the corresponding querries.
        Options:
            'a' - all querries (sensor data, batch alerts and batch positions)
            's' - only sensor data
            'sba' - sensor data and batch alerts
            'ba' - batch alerts only
            'bp' - batch positions only
        '''
        
        # Save in order to give acces to some methods as needed and appropiate for the selected type
        self.querryType = querryType
        
        self.sensor_data_dtype =  np.dtype([
            ('ID', np.int64),
            ('batch_number', np.int64),
            ('device_number', np.int64),
            ('date', 'datetime64[D]'),  # Using datetime64[D] for date
            ('temperature', np.float64),
            ('humidity', np.float64),
            ('light_percentage', np.float64)
        ])
        
        self.batch_alerts_dtype = np.dtype([
            ('alert_number', np.int64),
            ('batch_number', np.int64),
            ('temperature_alert', np.bool_),
            ('humidity_alert', np.bool_),
            ('light_alert', np.bool_)
        ])
        
        self.batch_position_dtype = np.dtype([
            ('batch_number', np.int64),
            ('date', 'datetime64[D]'),
            ('time', 'timedelta64[s]'),  # Using timedelta64[s] for time
            ('x_coordinate', np.float64),
            ('y_coordinate', np.float64)
        ])
        
        

        if querryType == 'a':
            self.sensor_data = np.array([], dtype=self.sensor_data_dtype)
            self.batch_alerts = np.array([], dtype=self.sensor_data_dtype)
            self.batch_positions = np.array([], dtype=self.sensor_data_dtype)
            
        elif querryType == 's':
            self.sensor_data = np.array([], dtype=self.sensor_data_dtype)
            
        elif querryType == 'sba':
            self.sensor_data = np.array([], dtype=self.sensor_data_dtype)
            self.batch_alerts = np.array([], dtype=self.sensor_data_dtype)
            
        elif querryType == 'ba':
            self.batch_alerts = np.array([], dtype=self.sensor_data_dtype)
            
        elif querryType == 'bp':
            self.batch_positions = np.array([], dtype=self.sensor_data_dtype)
            
        else:
            raise ValueError('Not a valid type for QuerryResult.')
            
        