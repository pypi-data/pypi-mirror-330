import torch
import torch.nn as nn
from transformers import BertModel, BertForSequenceClassification
from huggingface_hub import hf_hub_download

class SentimentModel(nn.Module):
    """For general sentiment classification"""
    def __init__(self, pretrained_model_name='bert-base-cased', num_labels=3):
        super(SentimentModel, self).__init__()
        self.bert = BertForSequenceClassification.from_pretrained(pretrained_model_name, num_labels=num_labels)
    
    def forward(self, input_ids, attention_mask, token_type_ids=None):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        return outputs  # Returns full model output object

class SentimentBERT(nn.Module):
    """For query intent classification"""
    def __init__(self, output_dim):
        super(SentimentBERT, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.fc = nn.Linear(self.bert.config.hidden_size, output_dim)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.pooler_output
        return self.fc(pooled_output)

def load_sentiment_model(model_filename, repo_id="Vaish1906/FYP-weights-model"):
    """
    Downloads and loads the appropriate sentiment/query intent model from Hugging Face.

    Args:
        model_filename (str): The filename of the model weights on Hugging Face.
        repo_id (str): The Hugging Face repo where the model is stored.

    Returns:
        nn.Module: The loaded PyTorch model.
    """
    try:
        # Download model weights from Hugging Face
        model_path = hf_hub_download(repo_id=repo_id, filename=model_filename)

        # Select the correct model architecture based on the filename
        if "query" in model_filename:
            model = SentimentBERT(output_dim=10)  # Output dimension is 10 for intent classification
        else:
            model = SentimentModel(num_labels=3)  # Default sentiment classification model

        # Load the model weights
        model.load_state_dict(torch.load(model_path, map_location="cpu"))  # Loads on CPU by default

        # Set model to evaluation mode
        model.eval()

        return model

    except Exception as e:
        print(f"Error loading model {model_filename}: {e}")
        return None
