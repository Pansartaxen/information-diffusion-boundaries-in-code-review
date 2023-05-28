import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import cv2
import imagehash
import base64

def execute_notebook(notebook_path):
    with open(notebook_path) as f:
        notebook = nbformat.read(f, as_version=4)

    executor = ExecutePreprocessor(timeout=6000)  # Set an appropriate timeout value, this notebook takes forever to run *sigh*

    executor.preprocess(notebook, {'metadata': {'path': './'}})  # Provide the desired execution path

    return notebook

def test_notebook_outputs():
    notebook_path = 'notebooks/plot.ipynb'

    notebook = execute_notebook(notebook_path)

    last_cell = notebook.cells[-1]  # Assuming `notebook` is the notebook object

    if last_cell.outputs:
        first_output = last_cell.outputs[0]
        data = first_output['data']

        image_disk = cv2.imread('test/Reference_pictures/output.png')

        # Assume you already have the image in memory as a variable
        # Here, image_memory represents the image data stored in memory
        # Replace this with your actual variable containing the image data
        image_memory_base64 = data['image/png']

        # Decode the base64 string into bytes
        image_memory_bytes = base64.b64decode(image_memory_base64)

        # Convert the bytes to a NumPy array
        image_memory = np.frombuffer(image_memory_bytes, dtype=np.uint8)

        # Decode the NumPy array as an image
        image_memory = cv2.imdecode(image_memory, cv2.IMREAD_COLOR)

        # Convert the image in memory to a NumPy array and ensure RGB color space
        image_memory = cv2.cvtColor(image_memory, cv2.COLOR_BGR2RGB)

        # Ensure that both images are of the same data type (np.uint8)
        image_disk = np.array(image_disk, dtype=np.uint8)
        image_memory = np.array(image_memory, dtype=np.uint8)

        # Calculate the perceptual hashes
        hash_disk = imagehash.average_hash(Image.fromarray(image_disk))
        hash_memory = imagehash.average_hash(Image.fromarray(image_memory))

        # Compare the hash values
        threshold = 5  # Adjust this value based on your requirements

        # Calculate the hamming distance between the hashes
        hamming_distance = hash_disk - hash_memory

        # Compare the hamming distance with the threshold
        return hamming_distance <= threshold


if __name__ == '__main__':
    test_notebook_outputs()
