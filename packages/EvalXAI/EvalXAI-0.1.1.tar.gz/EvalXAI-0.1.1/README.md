# XAI Framework

This framework provides tools for generating and evaluating explanations for NLP models. It supports various explainers and evaluators, and includes caching mechanisms to optimize performance.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
  - [Loading the Dataset](#loading-the-dataset)
  - [Generating Explanations](#generating-explanations)
  - [Evaluating Explanations](#evaluating-explanations)
  - [Displaying Results](#displaying-results)
- [Configuration](#configuration)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This is an easy-to-use yet comprehensive toolbox for quantitative evaluation of explanations from different post-hoc explainers in NLP domain. 

## Explainers

This project supports several explanation methods to help understand the model’s predictions. Each method attributes importance to input features (tokens) in different ways:

-**Gradient** [https://arxiv.org/abs/1312.6034](Simonyan et al., 2014)
Uses plain gradients or gradients multiplied by input embeddings to measure feature influence on the model’s prediction.

-**Integrated Gradient** [https://arxiv.org/abs/1703.01365](Sundararajan et al., 2017)
Computes gradients from a baseline input to the actual input, aggregating them to measure each feature’s contribution.

-**Guided Backprop** [https://arxiv.org/abs/1412.6806](Springenberg et al.,2015)
Modifies backpropagation to mask negative gradients, highlighting features with positive contributions to the prediction.

-**DeepLift** [https://arxiv.org/abs/1704.02685](Shrikumar et al., 2019)
Compares model outputs relative to a baseline, propagating differences across the network to determine feature importance.

-**SHAP** [https://arxiv.org/abs/1705.07874](Lundberg & Lee, 2017)
Uses Shapley values from cooperative game theory to fairly distribute feature importance across all possible feature subsets.

-**SHAPIQ** [https://arxiv.org/abs/2410.01649](Muschalik et al., 2024)
A variant of SHAP designed for classification tasks, refining Shapley value approximations for better interpretation in classification problems.

-**LIME** [https://arxiv.org/abs/1602.04938](Ribeiro et al., 2016)
A model-agnostic method that explains predictions by approximating the model with a simpler surrogate model in the local neighborhood of the instance.

### Evaluation Metrics

This library aims to aggregate and implement evaluation metrics from the XAI literature to automate XAI quantification. These metrics generally fall into one of four main categories: faithfulness, robustness, plausibility, complexity. Our library provides implementations of the following evaluation metrics:

#### Faithfulness:
Measures how well the explanations reflect the model’s predictive behavior.

**Soft Comprehensiveness** [https://aclanthology.org/2023.acl-long.261/](Zhao and Aletras, 2023)

**Soft Sufficiency** [https://aclanthology.org/2023.acl-long.261/](Zhao and Aletras, 2023)

**FAD and N-AUC** [https://aclanthology.org/2022.bionlp-1.33/](Ngai and Rudzicz, 2022,)

**AUC-TP**
Computes the area under the curve where the x-axis is the proportion of features removed and the y-axis is the performance change

#### Plausibility:
Assesses how intuitively the explanations align with human understanding.

**Area-Under-Precision-Recall-Curve** (soft score) [https://aclanthology.org/2020.acl-main.408/](DeYoung et al., 2020)
Evaluates how well the explanation prioritizes truly important tokens based on precision-recall tradeoffs.

**Token F1** (hard score) [https://aclanthology.org/2020.acl-main.408/](DeYoung et al., 2020)
Measures the overlap between predicted important tokens and human-annotated tokens.

**Token Intersection Over Union** [https://aclanthology.org/2020.acl-main.408/](hard score) (DeYoung et al., 2020)
Assesses the similarity between explanation token sets and ground-truth annotations.

### Complexity
Evaluates the conciseness of explanations (fewer features imply higher clarity).

**Sparseness** [https://arxiv.org/abs/1810.06583](Chalasani et al., 2020): uses the Gini Index for measuring, if only highly attributed features are truly predictive of the model output

**Complexity** [https://arxiv.org/abs/2005.00631](Bhatt et al., 2020): computes the entropy of the fractional contribution of all features to the total magnitude of the attribution individually

## Installation

To install the necessary dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

### Explain and Evaluate

Below is the example of how you can use the library in a very simple way to generate explanations of a given input sentence for any explainers you want.

```python

model_name= "cardiffnlp/twitter-xlm-roberta-base-sentiment"
xai_framework = XAIFramework(model_name)
sentence = "I love your style!"
#Here you can define whatever explainers you want to generate scores for
explainer_names=["deepLift","lime","shapiq","shap","guidedbackprop","gradientxinput","integratedgradient"]
exp= xai_framework.explain(sentence,"positive",explainer_names)
```

You can also visualize the scores easily with a single line of code in form of a table.

```python
xai_framework.visualize(exp)
```

You can evaluate these explanations for the defined evaluation metrics as follows.
You have the flexibility to define the explainers and evaluators you want the results for.

```python
xai_framework.evaluate_single_sentence(sentence,
                       explainer_names=["deeplift","gradientxinput",
                                        "lime","shapiq","shap","guidedbackprop","integratedgradient"],
                       evaluator_names=["softcomprehensiveness","softsufficiency","fad","auprc","iou","complexity","sparseness"],
                        human_rationale=[0, 1, 0, 0, 0])
```

### Loading the Dataset

First, load your dataset using the [load_fields_from_dataset] function as follows. You can load a huggingface model or csv/excel file.

```python
from dataset_loaders.dataset_args import LoadDatasetArgs

dataset_args_ = LoadDatasetArgs( # Path to the dataset file
    # dataset_name= "csv",
    dataset_name="eraser-benchmark/movie_rationales",
    input_text_field="review",  # Assuming "text" column contains the text data
    label_field="label",  # Assuming "label" column contains the sentiment labels
    rationale_field="evidences",
    dataset_split="test",  # Assuming you want to load the test split
    # dataset_files=["healthFC_annotated.csv"]
)

# Load the dataset fields
input_texts, labels, rationale = xai_framework.load_fields_from_dataset(dataset_args_)
```

### Explain and Benchmark

With a single line of code, you can explain and evaluate an entire dataset or even sub-samples of it.

```python
xai_framework.generate_explainer_table_for_dataset(input_texts, labels,explainer_names=["deeplift"])
```

## Project Structure

```
.
├── data
│   └── ...
├── src
│   ├── __init__.py
│   ├── main.py
│   └── ...
├── tests
│   └── ...
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
