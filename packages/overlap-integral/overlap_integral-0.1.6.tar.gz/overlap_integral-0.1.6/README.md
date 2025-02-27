# Overlap Integral Package

[![PyPI version](https://img.shields.io/pypi/v/overlap-integral)](https://pypi.org/project/overlap-integral/)

This project focuses on calculating the overlap integral between two probability density functions (PDFs):

![Overlap Integral](https://latex.codecogs.com/svg.image?\theta=\int_{a}^{b}min[f(x),g(x)]dx)

The overlap integral is a measure of similarity between two distributions (f(x) and g(x)) and is used in various fields such as statistics, data science, etc. The package provides efficient methods for estimating PDFs using kernel density estimation (KDE) or Gaussian distributions.

## Project Structure

- `src/overlap_integral/`: Contains the core Python code for calculating the overlap integral.
- `tests/`: Includes the test scripts to validate the functionality of the code.
- `README.md`: Provides an overview and instructions for the project.
- `pyproject.toml`: Configuration file for the project dependencies and metadata.


## Installation

To install the package using `pip`, run the following command:

```bash
pip install overlap-integral
```

**Importing the Class**: Import the `OverlapIntegral` class in your Python script.

    ```python
    from overlap_integral.overlap_integral import OverlapIntegral
    ```

**Usage Example**: Provide a simple example to demonstrate how to use the `OverlapIntegral` class.

    ```python
               
            import numpy as np
            from overlap_integral.overlap_integral import OverlapIntegral

            import plotly.io as pio
            pio.kaleido.scope.default_format = "png"


            def main():
                np.random.seed(3)  # Set random seed for reproducibility

                overlap_integral_instance = OverlapIntegral()

                # Generate or load data
                data1 = np.random.normal(loc=10, scale=1, size=1000)
                data2 = np.random.normal(loc=10, scale=2, size=1000)

                # Choose PDF method: 'kde' or 'gaussian'
                function_type = 'kde'

                # Get PDFs
                pdf_1 = overlap_integral_instance.get_pdf(data1, pdf_type=function_type)
                pdf_2 = overlap_integral_instance.get_pdf(data2, pdf_type=function_type)

                # Calculate overlap integral
                lower_limit = min(np.min(data1), np.min(data2)) - 12 * max(np.std(data1), np.std(data2))
                upper_limit = max(np.max(data1), np.max(data2)) + 12 * max(np.std(data1), np.std(data2))
                integral, error = overlap_integral_instance.overlap_integral(pdf_1, pdf_2, lower_limit, upper_limit)

                print(f"Overlap integral: {integral}")
                print(f"Estimated error: {error}")

                # Plot distributions
                fig = overlap_integral_instance.plot_distributions(pdf_1, pdf_2, integral, error, x_range=(lower_limit, upper_limit))
                fig.write_image("overlap_plot.png")
                #fig.show()

                print(f"Everything worked!")

            if __name__ == '__main__':
                main()

    ```

## Dependencies

- python >= 3.11
- numpy>=1.21
- scipy>=1.7
- plotly>=5.3
- kaleido==0.2.0

## License

This project is licensed under the MIT License.

## Contribution 

Feel free to submit issues or pull requests. Your contributions are welcome!

## Contact 

For questions or suggestions, please contact kiatakimatheus@gmail.com