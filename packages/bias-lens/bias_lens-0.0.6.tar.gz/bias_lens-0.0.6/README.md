# Bias Lens

**Bias Lens** is a Python library designed for bias detection and explainable AI (XAI) methods for NLP models. It provides a unified interface to perform token-level bias analysis using multiple state-of-the-art explanation techniques including Integrated Gradients, DeepLIFT, LIME, SHAP, attention-based methods, counterfactual explanations, LRP, and occlusion methods.

## Features

-   **Bias NER Classification:**  
    Leverage a token classification model (e.g., BERT) to identify bias-related tokens with customizable label mappings.

-   **Explainability Methods:**  
    Integrated support for various XAI techniques:

    -   **LIME:** Local, interpretable model-agnostic explanations.
    -   **SHAP:** Shapley values for fair attribution of input tokens.
    -   **Integrated Gradients:** Gradient-based attributions for deep models.
    -   **DeepLIFT:** Explains predictions by comparing against a baseline.
    -   **Attention Explanations:** Visualize attention scores.
    -   **Counterfactual Explanations:** Generate alternative input versions to understand model decisions.
    -   **Layer-wise Relevance Propagation (LRP):** Propagate relevance scores back to input features.
    -   **Occlusion:** Identify important tokens by systematically masking parts of the input.

-   **Modular Design:**  
    Easily extendable code structure to add new explanation methods or integrate with custom models.

-   **Factory Pattern:**  
    Use a unified factory to access various explanation methods effortlessly.

## Installation

You can install **Bias Lens** from PyPI (after publishing) with:

```bash
pip install bias-lens
```

Or install directly from the repository:

```bash
pip install git+https://github.com/bhavaniit24/bias-lens.git
```

## Quick Start

Below is a simple example demonstrating how to use Bias Lens with your own model, tokenizer, and label mapping.

```python
from transformers import BertForTokenClassification, BertTokenizerFast
from bias_lens import BiasNERClassifier, BiasModelExplainerFactory, ExplainerMethod

# User-defined model, tokenizer, and id2label mapping
model = BertForTokenClassification.from_pretrained("your_model_path")
tokenizer = BertTokenizerFast.from_pretrained("your_model_path")
id2label = {
    0: "O",
    1: "B-STEREO",
    2: "I-STEREO",
    3: "B-GEN",
    4: "I-GEN",
    5: "B-UNFAIR",
    6: "I-UNFAIR",
    7: "B-EXCL",
    8: "I-EXCL",
    9: "B-FRAME",
    10: "I-FRAME",
    11: "B-ASSUMP",
    12: "I-ASSUMP",
}

# Create a bias NER classifier instance
ner_classifier = BiasNERClassifier(model, tokenizer, id2label)
result = ner_classifier.predict("Women are bad drivers")
print("NER Prediction:", result)

# Create an explainer factory
explainer_factory = BiasModelExplainerFactory(model, tokenizer, id2label)

# Example: Get LIME explainer and generate explanation
lime_explainer = explainer_factory.get_explainer(ExplainerMethod.LIME)
lime_explanation = lime_explainer.explain("Women are bad drivers")
print("LIME Explanation:", lime_explanation)
```

## Documentation

### Modules and Classes

-   **BiasNERClassifier:**
    Provides a method to perform token-level bias prediction using a pre-trained token classification model.

-   **BaseExplainer & ProbabilityExplainerMixin:**
    Base classes that offer common functionality such as input preparation and probability prediction.

-   **Explainer Implementations:**
    Classes like `LimeExplainer`, `ShapExplainer`, `IntegratedGradientsExplainer`, `DeepLiftExplainer`, `AttentionExplainer`, `CounterfactualExplainer`, `LRPExplainer`, and `OcclusionExplainer` each encapsulate a different XAI method.

-   **BiasModelExplainerFactory:**
    A factory class to easily retrieve the desired explainer based on a string key.

-   **ExplainerMethod:**
    An enum class that defines the available explanation methods.

### Explanation Methods

The available methods in the enum are:

-   LIME
-   SHAP
-   INTEGRATED_GRADIENTS
-   INTEGRATED_GAP_GRADIENTS
-   DEEPLIFT
-   ATTENTION
-   COUNTERFACTUAL
-   LRP
-   OCCLUSION
-   SALIENCY

### Contributing

Contributions are welcome! Please open an issue or submit a pull request on [GitHub](https://github.com/bhavaniit24/bias-lens) with your ideas and improvements.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Contact

For any questions or feedback, please contact [bhavaniit24](mailto:loganthan.20201212@iit.ac.lk).

---

_Bias Lens_ is designed to make bias detection and model interpretability more accessible and flexible. Whether you are researching fairness in NLP or developing production models, this library aims to provide robust tools to explain and mitigate biases.
