# Manim Code Generator

This script generates Manim visualization code for Python solutions using OpenAI. It follows a two-step process:

1. First, it generates a Python solution with explanation for a given problem
2. Then, it uses that solution to generate Manim visualization code

## Requirements

- Python 3.6+
- OpenAI API access

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:

```bash
python manim_code_generator.py
```

2. The script will:
   - Generate a Python solution for the problem specified in the `main()` function
   - Generate Manim visualization code based on that solution
   - Save the Manim code to `manim_visualization.py`

3. To render the visualization later (requires Manim installation):

```bash
pip install manim==0.17.3  # Install Manim if not already installed
manim -pql manim_visualization.py ConceptVisualization
```

Note: Rendering requires sufficient disk space and Manim to be installed. See the [Manim documentation](https://docs.manim.community/en/stable/installation.html) for installation details.

## Customization

You can customize the prompt in the `main()` function to generate visualizations for different problems:

```python
def main():
    prompt = "explain addition"  # Change this to any problem you want to visualize
    # ...
```

## Troubleshooting

If you encounter issues with rendering:

1. Make sure you have sufficient disk space (at least 1GB free)
2. Ensure Manim is installed correctly
3. Try running the render command manually:

```bash
manim -pql manim_visualization.py ConceptVisualization
```

4. Check the Manim documentation for troubleshooting tips 