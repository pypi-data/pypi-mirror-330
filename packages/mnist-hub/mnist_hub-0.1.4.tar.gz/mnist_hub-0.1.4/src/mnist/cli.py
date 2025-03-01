"""Command line interface for MNIST Hub."""

import click
import sys, gzip, json
from itertools import count
from pathlib import Path
from mnist import lib, __version__
from mnist.lib import log
from io import TextIOWrapper

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

class OrderedGroup(click.Group):
    def __init__(self, name=None, commands=None, **attrs):
        super(OrderedGroup, self).__init__(name, commands, **attrs)
        # Commands in the order we want them to appear
        self.command_order = ['train', 'eval', 'show', 'gui', 'contest']

    def list_commands(self, ctx):
        """Return commands in specified order"""
        return self.command_order

@click.group(context_settings=CONTEXT_SETTINGS, cls=OrderedGroup, help=f"MNIST Hub v{__version__} - A collection of MNIST classifiers and tools")
def cli():
    pass


@cli.command()
@click.argument('name', default="mnist.svm.SimpleSVM")
@click.option('-f', '--fname', required=True, help='The file to save the fitted data into')
@click.option('-l', '--limit', default=None, type=int,
              help='Limit the number of training samples')
def train(name, fname, limit):
    """Train a model and save the fitted model to a file"""
    log(f"training model: {name}")
    
    # Get the model class
    model = lib.get_model_class(name)

    # Load the data
    training_data, validation_data, test_data = lib.load_data()

    # Random slice the training data
    shift, training_data = lib.random_slice(training_data, limit=limit)

    # Train the model
    model.train(training_data, test_data=test_data)

    # Save the model
    lib.save_model(model, fname=fname)
    
@cli.command()
@click.option('-f','--fname', default=lib.DEFAULT_MODEL_PATH, help='The saved model file')
@click.option('-l', '--limit', default=None, type=int,
              help='Limit the number of test samples to evaluate')
@click.option('-o', '--output', default='report.json.gz',
              help='Output file for the evaluation report (default: report.json)')
def eval(fname, limit, output):
    """Load a model stored in a file and evaluate it"""
    
    # Load the model
    mod = lib.load_model(fname)

    # Load the data
    train_data, validation_data, test_data = lib.load_data()

    # Random slice the test data
    shift, test_data = lib.random_slice(test_data, limit=limit)

    # Evaluate the model
    inp_data = test_data[0]
    inp_true = test_data[1]
    
    # Get the predictions
    values  = list(map(int, mod.predict(inp_data)))

    # Initialize the report data.
    report = dict(model=mod.__class__.__name__, limit=limit, accuracy=0, total=0,
                  correct=0, incorrect=0, errors=[]
    )

    # Fill in the report data.
    correct = incorrect = 0
    for i, e, p in zip(count(0), inp_true, values):
        valid = int(e == p)
        if not valid:
            report['errors'].append(dict(index=i+shift, expected=int(e), predicted=int(p)))
            incorrect += 1
        else:
            correct += 1

    total = correct + incorrect
    acc = round(correct / total,4)
    
    report['correct'] = correct
    report['incorrect'] = incorrect
    report['total'] = total

    report['accuracy'] = acc
    log(f"accuracy: {correct}/{total} ({acc*100:.2f}%)")
    log(f"report saved to {output}")

    # Save the report to the output file.
    stream = gzip.open(output, 'wb') if output.endswith('.gz') else open(output, 'wb')

    with TextIOWrapper(stream) as stream:
        json.dump(report, stream, indent=4)

@cli.command()
def gui():
    """Launch the MNIST GUI application."""
    from mnist.gui import main
    main()

@cli.command()
def contest():
    """Run the MNIST contest evaluation."""
    from mnist.contest import main
    sys.argv = [sys.argv[0]]  # Reset argv to avoid conflicts
    main()

@cli.command()
@click.argument('index', type=int)
def show(index):
    """Show the MNIST image at the given index"""
    lib.show_image(index)


if __name__ == '__main__':
    cli.__doc__ = "HEY"
    cli()