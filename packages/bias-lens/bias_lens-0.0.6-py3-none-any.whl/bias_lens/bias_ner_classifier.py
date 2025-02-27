import torch


import torch


class BiasNERClassifier:
    def __init__(self, model, tokenizer, id2label, max_length=128, sensitivity=0.5):
        """
        Initializes the bias NER classifier.

        Args:
            model: A token classification model.
            tokenizer: The tokenizer corresponding to the model.
            id2label (dict): Mapping from label indices to string labels.
            max_length (int): Maximum token sequence length.
            sensitivity (float): Threshold for classification.
        """
        self.model = model
        self.tokenizer = tokenizer
        self.id2label = id2label
        self.max_length = max_length
        self.sensitivity = sensitivity
        self.device = next(model.parameters()).device

    def predict(self, sentence):
        """Predicts bias NER tags for a given sentence."""
        inputs = self.tokenizer(
            sentence,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=self.max_length,
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = torch.sigmoid(logits)
            predicted_labels = (probabilities > self.sensitivity).int()

        tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
        result = []
        for i, token in enumerate(tokens):
            if token not in self.tokenizer.all_special_tokens:
                label_indices = (
                    (predicted_labels[0][i] == 1).nonzero(as_tuple=False).squeeze(-1)
                )
                labels = (
                    [self.id2label[idx.item()] for idx in label_indices]
                    if label_indices.numel() > 0
                    else ["O"]
                )
                result.append({"token": token, "labels": labels})
        return result

    def predict_with_interpretation(self, sentence):
        """
        Predicts NER tags and retrieves attention weights for interpretability.

        Args:
            sentence (str): The input sentence to analyze.

        Returns:
            tuple:
                tokens (list of str): List of tokens from the tokenizer.
                attentions (tuple): Attention weights from all layers and heads.
                token_labels (list of dict): List of dictionaries containing tokens and their predicted labels.
        """
        inputs = self.tokenizer(
            sentence,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=self.max_length,
        )
        input_ids = inputs["input_ids"].to(self.device)
        attention_mask = inputs["attention_mask"].to(self.device)

        with torch.no_grad():
            outputs = self.model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                output_attentions=True,
            )
            logits = outputs.logits
            attentions = outputs.attentions
            probabilities = torch.sigmoid(logits)
            predicted_labels = (probabilities > self.sensitivity).int()

        tokens = self.tokenizer.convert_ids_to_tokens(input_ids[0])
        token_labels = []
        for i, token in enumerate(tokens):
            if token not in self.tokenizer.all_special_tokens:
                label_indices = (
                    (predicted_labels[0][i] == 1).nonzero(as_tuple=False).squeeze(-1)
                )
                labels = (
                    [self.id2label[idx.item()] for idx in label_indices]
                    if label_indices.numel() > 0
                    else ["O"]
                )
                token_labels.append({"token": token, "labels": labels})

        return tokens, attentions, token_labels
