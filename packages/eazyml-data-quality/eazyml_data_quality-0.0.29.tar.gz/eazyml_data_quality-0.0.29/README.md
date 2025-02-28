## EazyML Responsible-AI: Data Quality Assessment
![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)  ![PyPI package](https://img.shields.io/badge/pypi%20package-0.0.29-brightgreen) ![Code Style](https://img.shields.io/badge/code%20style-black-black)

![EazyML](https://github.com/EazyML/eazyml-docs/raw/refs/heads/master/EazyML_logo.png)

## Overview
`eazyml-data-quality` is a python utility designed to evaluate the quality of datasets by performing various checks such as data shape, emptiness, outlier detection, balance, and correlation. It helps users identify potential issues in their datasets and provides detailed feedback to ensure data readiness for downstream processes.
It offers APIs for data quality assessment across multiple dimensions, including:

## Features
- **Missing Value Analysis**: Detect and impute missing values.
- **Bias Detection**: Uncover and mitigate bias in datasets.
- **Data Drift and Model Drift Analysis**: Monitor changes in data distributions over time.
- **Data Shape Quality**: Validates dataset dimensions and checks if the number of rows is sufficient relative to the number of columns.
- **Data Emptiness Check**: Identifies and reports missing values in the dataset.
- **Outlier Detection**: Detects and removes outliers based on statistical analysis.
- **Data Balance Check**: Analyzes the balance of the dataset and computes a balance score.
- **Correlation Analysis**: Identify multicollinearity, relationships between features and provides alerts for highly correlated features.
- **Summary Alerts**: Consolidates key quality issues into a single summary for quick review.
With eazyml-data-quality, you can ensure that your training data is clean, balanced, and ready for machine learning.

## Installation
To use the Data Quality Checker, ensure you have Python installed on your system.
### User installation
The easiest way to install data quality is using pip:
```bash
pip install -U eazyml-data-quality
```
### Dependencies
This package requires:
- pandas,
- scikit-learn,
- numpy,
- openpyxl,
flask

## Usage
Here's an example of how you can use the APIs from this package.
```python
from eazyml_data_quality import ez_init, ez_data_quality

# initialize: setup book-keeping, access_key if required 
_ = ez_init()

# Perform data quality checks
response = ez_data_quality(
                train_data(`DataFrame/str`) = 'train_dataframe/train_data_path',
                outcome(`str`) = 'target',
                options(`dict`) = {
                    "data_shape"(`str`): "yes"/"no",
                    "data_balance"(`str`): "yes"/"no",
                    "data_emptiness"(`str`): "yes"/"no",
                    "impute"(`str`): "yes"/"no",
                    "data_outliers"(`str`): "yes"/"no",
                    "remove_outliers"(`str`): "yes"/"no",
                    "outcome_correlation"(`str`): "yes"/"no",
                    "data_drift"(`str`): "yes"/"no",
                    "model_drift"(`str`): "yes"/"no",
                    "test_data"(`DataFrame/str`) = 'test_dataframe/test_data_path',
                    "data_completeness"(`str`): "yes"/"no",
                    "data_correctness"(`str`): "yes"/"no",
            }
        )

# Access specific quality metrics
if response["success"]:
    print("Data Shape Quality:", response["data_shape_quality"])
    print("Outlier Quality:", response["data_outliers_quality"])
    print("Bad Quality Alerts:", response["data_bad_quality_alerts"])
else:
    print("Error:", response["message"])
```
You can find more information in the [documentation](https://eazyml.readthedocs.io/en/latest/packages/eazyml_data_quality.html).


## Useful links, other packages from EazyML family
- [Documentation](https://docs.eazyml.com)
- [Homepage](https://eazyml.com)
- If you have questions or would like to discuss a use case, please contact us [here](https://eazyml.com/trust-in-ai)
- Here are the other packages from EazyML suite:

    - [eazyml-automl](https://pypi.org/project/eazyml-automl/): eazyml-automl provides a suite of APIs for training, optimizing and validating machine learning models with built-in AutoML capabilities, hyperparameter tuning, and cross-validation.
    - [eazyml-data-quality](https://pypi.org/project/eazyml-data-quality/): eazyml-data-quality provides APIs for comprehensive data quality assessment, including bias detection, outlier identification, and drift analysis for both data and models.
    - [eazyml-counterfactual](https://pypi.org/project/eazyml-counterfactual/): eazyml-counterfactual provides APIs for optimal prescriptive analytics, counterfactual explanations, and actionable insights to optimize predictive outcomes to align with your objectives.
    - [eazyml-insight](https://pypi.org/project/eazyml-insight/): eazyml-insight provides APIs to discover patterns, generate insights, and mine rules from your datasets.
    - [eazyml-xai](https://pypi.org/project/eazyml-xai/): eazyml-xai provides APIs for explainable AI (XAI), offering human-readable explanations, feature importance, and predictive reasoning.
    - [eazyml-xai-image](https://pypi.org/project/eazyml-xai-image/): eazyml-xai-image provides APIs for image explainable AI (XAI).

## License
This project is licensed under the [Proprietary License](https://github.com/EazyML/eazyml-docs/blob/master/LICENSE).

---

Maintained by [EazyML](https://eazyml.com)  
© 2025 EazyML. All rights reserved.
