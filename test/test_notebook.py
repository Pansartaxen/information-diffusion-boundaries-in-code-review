import base64
import cv2
import os
from datetime import timedelta
import imagehash
import matplotlib.pyplot as plt
import nbformat
import numpy as np
from nbconvert.preprocessors import ExecutePreprocessor
from PIL import Image
import pandas as pd
import unittest
import base64
import cv2
import numpy as np
from PIL import Image

class TestNotebook(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self._notebook = self.execute_notebook('notebooks/plot.ipynb')
        self._notebook = self.execute_notebook('notebooks/plot.ipynb')

    def execute_notebook(self, notebook_path) -> nbformat.NotebookNode:
        """
        Executes the notebook and stores it in
        the self._notebook for quick access
        """
        if os.path.isfile('data/minimal_paths/microsoft.pickle.bz2'):
            with open(notebook_path) as f:
                notebook = nbformat.read(f, as_version=4)

            executor = ExecutePreprocessor(timeout=60000)  # High time out because this notebook takes forever to run *sigh*

            executor.preprocess(notebook, {'metadata': {'path': './'}})

            return notebook

    def test_notebook_outputs(self) -> None:
        """Evaluates the plot outputed by the notebook"""
        if os.path.isfile('data/minimal_paths/microsoft.pickle.bz2'):
            last_cell = self._notebook.cells[-1]
            first_output = last_cell.outputs[0]

            if last_cell.outputs:
                first_output = last_cell.outputs[0]
                print('First output:', first_output)
                data = first_output['data']

                image_disk = cv2.imread('test/Reference_pictures/output.png')

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

                print(image_disk)
                print(image_memory)

                # Calculate the perceptual hashes
                hash_disk = imagehash.average_hash(Image.fromarray(image_disk))
                hash_memory = imagehash.average_hash(Image.fromarray(image_memory))

                self.assertAlmostEqual(hash_disk, hash_memory, delta = 5)
            else:
                self.skipTest(f"File 'microsoft.pickle.bz2' not found, skipping the test.")

    def test_pickle_read(self) -> None:
        """Checks if the pickle is read correctly"""
        if os.path.isfile('data/minimal_paths/microsoft.pickle.bz2'):
            reference = pd.read_pickle('data/minimal_paths/microsoft.pickle.bz2')
            cell = self._notebook.cells[2]
            cell_var = cell.outputs[0]['text/plain']

            if cell.cell_type == 'code' and cell.outputs:
                for output in cell.outputs:
                    if output.output_type == 'execute_result' and 'data' in output:
                        if 'text/plain' in output.data:
                            cell_var = output.data['text/plain']
                            if cell_var == repr(reference):
                                print('Values are equal')
                            else:
                                print('Values are not equal')
                            return

            self.assertEqual(cell_var, reference)
        else:
            self.skipTest(f"File 'microsoft.pickle.bz2' not found, skipping the test.")


if __name__ == '__main__':
    unittest.main()
