from sensorDataGenerator import RandomDataGenerator

if __name__ == '__main__':
    generator = RandomDataGenerator()
    generator.generator(1000)
    print('Produced test file.')