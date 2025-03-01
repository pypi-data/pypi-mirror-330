
import random

class Toy:

    def train(self, training_data, test_data=None):
        print(f"# Toy training data size: {len(training_data[0])}")

    def predict(self, data):
        # Data is list of numpy array of shape (784,)
        print(f"# Toy predict size: {len(data)}")
        values = map(lambda x: random.randint(0, 9), data)
        values = list(values)
        return values