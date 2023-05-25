import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from time import time

def execute_notebook(notebook_path):
    with open(notebook_path) as f:
        notebook = nbformat.read(f, as_version=4)

    executor = ExecutePreprocessor(timeout=6000)  # Set an appropriate timeout value, this notebook takes forever to run *sigh*

    executor.preprocess(notebook, {'metadata': {'path': './'}})  # Provide the desired execution path

    return notebook

def extract_outputs(notebook):
    outputs = []
    for cell in notebook.cells:
        print('cell', cell, '\ncell type', cell.cell_type, '\ncell outputs', cell.outputs)
        if cell.cell_type == 'code' and 'outputs' in cell:
            for output in cell.outputs:
                print('Output', output, '\noutput type', output.output_type, '\nOutput data', output.data)
                if output.output_type == 'execute_result':
                    if 'data' in output and 'image/png' in output.data:
                        print(output.data['image/png'])
                        outputs.append(output.data['image/png'])

    return outputs

def compare_images(image_1, image_2):
    image1 = Image.open(image_1)
    image2 = Image.open(image_2)

    # Convert images to numpy arrays
    array1 = np.array(image1)
    array2 = np.array(image2)

    # Calculate the mean squared error (MSE) between the two images
    mse = np.mean((array1 - array2) ** 2)

    # Define a threshold for similarity
    threshold = 100  # Adjust this value based on your specific requirements

    # Compare MSE with the threshold
    return mse < threshold

def test_notebook_outputs():
    notebook_path = 'notebooks/plot.ipynb'

    notebook = execute_notebook(notebook_path)
    #outputs = extract_outputs(notebook)

    last_cell = notebook.cells[-1]

    if last_cell.outputs:
        first_output = last_cell.outputs[0]
        output_type = type(first_output)
        output_keys = first_output.keys()

        print("Output Type:", output_type)
        print("Output Keys:", output_keys)

        for key in output_keys:
            print(key, ":", first_output[key])
    else:
        print("No outputs in the last cell.")

    #generated_plot = last_cell.outputs[0]['data']['image/png']

    #reference_plot_path = 'test/Reference_pictures/output.png'

    #comparison = compare_images(generated_plot, reference_plot_path)

    #assert comparison, 'The generated plot does not match the reference plot.'


if __name__ == '__main__':
    test_notebook_outputs()