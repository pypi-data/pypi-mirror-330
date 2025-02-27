# interfusion/models.py

import torch
import torch.nn as nn
from transformers import AutoModel
import numpy as np


class DummyTqdm:
    def __init__(self, iterable=None, **kwargs):
        self.iterable = iterable if iterable is not None else []
        self.iterator = iter(self.iterable)
        self.desc = kwargs.get('desc', '')
        self.start_time = None
        self.end_time = None

    def __iter__(self):
        self.start_time = time.time()
        return self

    def __next__(self):
        try:
            return next(self.iterator)
        except StopIteration:
            self.end_time = time.time()
            total_time = self.end_time - self.start_time
            if self.desc:
                print(f"{self.desc} completed in {total_time:.2f} seconds")
            else:
                print(f"Iteration completed in {total_time:.2f} seconds")
            raise

    def __getattr__(self, attr):
        # Return a dummy function for any other attributes
        return lambda *args, **kwargs: None

    def update(self, n=1):
        pass

    def set_description(self, desc=None, refresh=True):
        pass

    def close(self):
        pass


def get_tqdm(config):
    if not config.get('use_tqdm', True):
        return DummyTqdm
    else:
        tqdm_type = config.get('tqdm_type', 'standard')
        try:
            if tqdm_type == 'notebook':
                from tqdm.notebook import tqdm
            else:
                from tqdm import tqdm
        except ImportError:
            print("tqdm is not installed. Progress bars will be disabled.")
            return DummyTqdm
        return tqdm
        
        
import sys
import torch
import torch.nn as nn
from transformers import AutoModel, AutoModelForSequenceClassification

class CrossEncoderModel(nn.Module):
    def __init__(self, config, candidate_feature_size=0, job_feature_size=0):
        super().__init__()
        self.use_sparse = config.get('use_sparse', False)

        if not self.use_sparse:
            # Use the simple version with AutoModelForSequenceClassification
            self.model = AutoModelForSequenceClassification.from_pretrained(
                config['cross_encoder_model_name']
            )
        else:
            # Use the extended version with additional sparse features and layers
            self.model = AutoModel.from_pretrained(config['cross_encoder_model_name'])
            # Freeze the transformer model parameters
            for param in self.model.parameters():
                param.requires_grad = False

            hidden_size = self.model.config.hidden_size
            self.candidate_feature_size = candidate_feature_size
            self.job_feature_size = job_feature_size
            total_feature_size = candidate_feature_size + job_feature_size
            classifier_input_size = hidden_size * 3 + total_feature_size

            self.dropout = nn.Dropout(0.2)

            # Attention mechanism to weigh token embeddings
            self.attention = nn.Sequential(
                nn.Linear(hidden_size, hidden_size),
                nn.Tanh(),
                nn.Linear(hidden_size, 1)
            )

            # Interaction layer to capture token interactions
            self.interaction = nn.Sequential(
                nn.Linear(hidden_size, hidden_size),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(hidden_size, hidden_size),
                nn.ReLU()
            )

            # Classifier network
            self.classifier = nn.Sequential(
                nn.Linear(classifier_input_size, classifier_input_size // 2),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(classifier_input_size // 2, classifier_input_size // 4),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(classifier_input_size // 4, 1)
            )

    def forward(self, input_ids, attention_mask, features=None):
        if not self.use_sparse:
            # Forward pass for simple version
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits  # shape could be [batch_size, 2] for binary classification

            if logits.size(-1) == 2:
                # Convert two logits into a single ranking score
                logits = logits[:, 1] - logits[:, 0]
            else:
                logits = logits.squeeze(-1)
            return logits
        else:
            # Forward pass for extended version with additional layers and sparse features
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            last_hidden_state = outputs.last_hidden_state  # [batch_size, seq_length, hidden_size]

            # Apply attention mechanism
            attention_weights = self.attention(last_hidden_state).squeeze(-1)  # [batch_size, seq_length]
            attention_weights = torch.softmax(attention_weights, dim=1).unsqueeze(-1)  # [batch_size, seq_length, 1]
            weighted_embeddings = last_hidden_state * attention_weights
            attended_output = weighted_embeddings.sum(dim=1)  # [batch_size, hidden_size]

            # Apply interaction layer
            interacted = self.interaction(last_hidden_state)  # [batch_size, seq_length, hidden_size]
            interacted = torch.mean(interacted, dim=1)  # [batch_size, hidden_size]

            # Extract [CLS] token representation
            cls_output = last_hidden_state[:, 0, :]  # [batch_size, hidden_size]

            # Combine representations
            combined_representation = torch.cat([cls_output, attended_output, interacted], dim=1)
            if features is not None:
                combined_representation = torch.cat((combined_representation, features), dim=1)

            combined = self.dropout(combined_representation)
            logits = self.classifier(combined)
            return logits.squeeze(-1)




def compute_bi_encoder_embeddings(model, tokenizer, texts, config):
    
    tqdm = get_tqdm(config)

    model.eval()
    device = next(model.parameters()).device
    embeddings = []
    batch_size = config['bi_encoder_batch_size']
    max_length = config['max_length']
    with torch.no_grad():
        for i in tqdm(range(0, len(texts), batch_size), desc="Computing embeddings"):
            batch_texts = texts[i:i+batch_size]
            inputs = tokenizer(batch_texts, max_length=max_length, padding=True, truncation=True, return_tensors='pt')
            input_ids = inputs['input_ids'].to(device)
            attention_mask = inputs['attention_mask'].to(device)
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            cls_embeddings = outputs.last_hidden_state[:, 0]  # CLS token
            embeddings.append(cls_embeddings.cpu())
    embeddings = torch.cat(embeddings, dim=0)
    return embeddings

