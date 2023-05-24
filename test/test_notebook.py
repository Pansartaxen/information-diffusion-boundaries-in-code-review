import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

def execute_notebook(notebook_path):
    with open(notebook_path) as f:
        notebook = nbformat.read(f, as_version=4)

    executor = ExecutePreprocessor(timeout=6000)  # Set an appropriate timeout value, this notebook takes forever to run *sigh*

    executor.preprocess(notebook, {'metadata': {'path': './'}})  # Provide the desired execution path

    return notebook

def extract_outputs(notebook):
    outputs = []
    for cell in notebook.cells:
        if cell.cell_type == 'code' and 'outputs' in cell:
            for output in cell.outputs:
                if output.output_type == 'execute_result':
                    outputs.append(output.data['text/plain'])

    return outputs

def test_notebook_outputs():
    notebook_path = 'notebooks/plot.ipynb'
    expected_outputs = ['expected_output_1', 'expected_output_2', ...]

    notebook = execute_notebook(notebook_path)
    outputs = extract_outputs(notebook)

    assert outputs == expected_outputs


if __name__ == '__main__':
    test_notebook_outputs()
