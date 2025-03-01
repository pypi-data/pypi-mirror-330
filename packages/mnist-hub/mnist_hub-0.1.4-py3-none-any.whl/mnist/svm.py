"""
Support Vector Machine implementation for MNIST digit recognition.
"""
# Third-party libraries
from sklearn import svm
from itertools import *

from mnist.lib import timing_decorator, log

class SimpleSVM:
    """"""

    def __init__(self):
        log(f"initializing class: {self.__class__.__name__}")  
        self.model = svm.SVC()

    @timing_decorator
    def train(self, data, test_data=None):
        """Train the SVM model"""
        self.model.fit(data[0], data[1])
        if test_data:
            preds = self.model.predict(test_data[0])
            correct = sum(map(lambda x, y: x == y, test_data[1], preds))
            print (f"# accuracy: {correct} / {len(test_data[0])} ({correct / len(test_data[0]) * 100:.1f}%)")

    @timing_decorator
    def predict(self, data):
        """
        Run predictions on the data.
        """
        preds = self.model.predict(data)
        return preds

def test(fname='tmp.bin'):
    """
    Test the model when run from command line
    """
    from mnist import lib

    # Initialize the model
    mod = SimpleSVM()

    # Load the data
    train_data, validation_data, test_data = lib.load_data()

    # Reduce the size of the training and test data for speed
    shift, train_data = lib.random_slice(train_data, limit=100)
    shift, test_data = lib.random_slice(test_data, limit=100)

    # Test training the model
    mod.train(train_data)

    # Save the model
    lib.save_model(mod, fname=fname)

    # Loading the model from a file.
    mod = lib.load_model(fname=fname)

    # Predict the test data
    preds = mod.predict(test_data[0])
    
    # Print the accuracy of the model
    correct = sum(map(lambda x, y: x == y, test_data[1], preds))
    print (f"# accuracy: {correct} / {len(test_data[0])} ({correct / len(test_data[0]) * 100:.1f}%)")
    return 

if __name__ == "__main__":
    test()