from sensorDataGenerator import RandomDataGenerator

if __name__ == '__main__':
    generator = RandomDataGenerator()
    
    # Generate training data
    generator.generator(1000, 100, withLabels=True)
    print('Produced training file.')
    
    # Generate evaluation data/testing build reports
    generator.generator(1000, 100, withLabels=False)
    print('Produced evaluation file.')