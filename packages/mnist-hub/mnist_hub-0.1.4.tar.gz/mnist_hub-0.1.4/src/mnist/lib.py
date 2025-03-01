"""
Main library for MNIST SVM classifier
"""
# Third-party libraries
from sklearn import svm
import joblib
import os, time, gzip, pickle, random
import functools
from itertools import count
import sys, json
from PIL import Image
import importlib
import pkg_resources

__DIR__ = os.path.dirname(os.path.abspath(__file__))

# A few defaults.
DATA_DIR = os.path.join(__DIR__, 'data')
DEFAULT_DATA_PATH = pkg_resources.resource_filename('mnist', 'data/mnist.pkl.gz')
DEFAULT_MODEL_PATH = pkg_resources.resource_filename('mnist', 'data/mnist_net_model.gz')
DEFAULT_REPORT_PATH = pkg_resources.resource_filename('mnist', 'data/report.json.gz')

def log(message):
    """Print log messages to stderr with # prefix"""
    print(f"# {message}", file=sys.stderr)

def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        #log(f"{func.__name__} started")
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        log(f"{func.__name__} completed in {duration:.2f} seconds")
        return result
    return wrapper

# Third-party libraries
import numpy as np

@timing_decorator
def load_data(fname=DEFAULT_DATA_PATH):
    """
    Return the MNIST data as a tuple containing the training data,
    the validation data, and the test data.
        print(load_data_wrapper()[0])
    The ``training_data`` is returned as a tuple with two entries.
    The first entry contains the actual training images.  This is a
    numpy ndarray with 50,000 entries.  Each entry is, in turn, a
    numpy ndarray with 784 values, representing the 28 * 28 = 784
    pixels in a single MNIST image.

    The second entry in the ``training_data`` tuple is a numpy ndarray
    containing 50,000 entries.  Those entries are just the digit
    values (0...9) for the corresponding images contained in the first
    entry of the tuple.

    The ``validation_data`` and ``test_data`` are similar, except
    each contains only 10,000 images.

    This is a nice data format, but for use in neural networks it's
    helpful to modify the format of the ``training_data`` a little.
    That's done in the wrapper function ``load_data_wrapper()``, see
    below.
    """
    f = gzip.open(fname, 'rb')
    u = pickle._Unpickler(f)
    u.encoding = 'latin1'
    training_data, validation_data, test_data = u.load()
    f.close()
    return (training_data, validation_data, test_data)


def mnist_matrix_text(m):
    """
    Return a string representation of the matrix in a readable format.
    Displays a 28x28 MNIST image using ASCII characters to represent different intensity levels:
    ' ' (0.0-0.2) -> completely white
    '.' (0.2-0.4) -> light gray
    'o' (0.4-0.6) -> medium gray
    'O' (0.6-0.8) -> dark gray
    '@' (0.8-1.0) -> completely black
    """
    def pixel_to_char(pixel):
        if pixel < 0.2: return ' '
        if pixel < 0.4: return '.'
        if pixel < 0.6: return 'o'
        if pixel < 0.8: return 'O'
        return '*'

    m = m.reshape(28, 28)  # Reshape the 784-length array to 28x28
    lines = []
    for row in m:
        lines.append(''.join(map(pixel_to_char, row)))
    
    output = '\n'.join(lines) + '\n'  # Add newline after the matrix
 
    return output

def digitize_image(image_data, threshold=0.3):
    """
    Convert grayscale image data to more binary-like values.
    Values above threshold will be set to 1.0, below to 0.0.
    
    Args:
        image_data: numpy array of shape (784,) with values between 0 and 1
        threshold: float between 0 and 1, values above this will be set to 1.0
    
    Returns:
        numpy array of same shape with more binary-like values
    """
    return np.where(image_data > threshold, 1.0, 0.0)

def show_image(index):
    """
    Show the image at the given index
    """
    training_data, validation_data, test_data = load_data()
    print(mnist_matrix_text(test_data[0][index]))
    log(f"Expected digit: {test_data[1][index]}")

def get_model_class(mod_name="mnist_svm.SVM"):
    """
    Get the class from a module name.
    """
    
    try:
        # Dynamically import the mnist_svm module.
        module_path, class_name = mod_name.rsplit('.', 1)
    except Exception as e:
        log(f"Unable to split the name: {mod_name} as module.class")
        sys.exit()

    try:
        # Import the module
        module = importlib.import_module(module_path)
    except Exception as e:
        # Restore original sys.path even if import fails
        log(f"Unable to import the module: {module_path}")
        log(f"Error: {e}")
        log(f"Troubleshoot with: python -m {module_path}")
        sys.exit()

    # Instantiate the class from the module.
    mod = getattr(module, class_name)()

    return mod

def random_slice(data, limit):

     # Get a random slice of the test data.
    if limit:
        start = random.randint(0, len(data[0]) - limit)
        end = start + limit
        elem1 = data[0][start:end]
        elem2 = data[1][start:end]      
        log(f"random subset of size {len(elem1)} out of {len(data[0])}")
        data = (elem1, elem2)
    else:
        start = 0
        end = len(data[0])
        log(f"data size {len(data[0])}")
    return start, data

def load_model(fname):
    """
    Load model from a gzipped file
    """
    # Store original sys.path
    sys_path = sys.path.copy()
    
    try:
        # Add current directory to sys.path if it's not already there
        current_dir = os.path.abspath(os.getcwd())
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
            
        # Load the model
        with gzip.open(fname, 'rb') as f:
            obj = pickle.load(f)
            log(f"class {obj.__class__.__name__} loaded from {fname}") 
            
        # Restore original sys.path
        sys.path = sys_path
        return obj
    except Exception as e:
        # Restore original sys.path even if loading fails
        sys.path = sys_path
        raise e

def save_model(model, fname):
    """
    Save model to a gzipped file
    """
    with gzip.open(fname, 'wb') as f:
        pickle.dump(model, f)
    log(f"model saved to {fname}") 
            

def mnist_to_image(matrix_data, scale=1, invert=False):
    """
    Convert MNIST matrix data to a PIL Image.
    Input should be a 784-length array of values between 0 and 1.
    
    Args:
        matrix_data: 784-length array of values between 0 and 1
        scale: Integer scaling factor for the output image size (default=1)
        invert: If True, inverts the colors (white digits on black background)
               If False, keeps original colors (black digits on white background)
    
    Returns:
        PIL Image object
    """
    # Reshape the 784-length array to 28x28
    matrix = matrix_data.reshape(28, 28)
    
    # Convert from 0-1 float values to 0-255 uint8, optionally inverting colors
    if invert:
        image_data = ((1 - matrix) * 255).astype('uint8')
    else:
        image_data = (matrix * 255).astype('uint8')
    
    # Create PIL Image
    image = Image.fromarray(image_data)
    
    # Scale the image if requested
    if scale > 1:
        new_size = (28 * scale, 28 * scale)
        image = image.resize(new_size, Image.Resampling.NEAREST)
    
    return image

def test():
   pass
    

if __name__ == "__main__":
    test()