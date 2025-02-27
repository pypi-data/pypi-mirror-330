# interfusion/inference.py

import torch
from transformers import AutoTokenizer
from .models import CrossEncoderModel
from .config import get_default_config

class InterFusionInference:
    def __init__(self, config=None, model_path=None):
        if config is None:
            config = get_default_config()
        self.config = config
        if model_path is None:
            model_path = config['saved_model_path']
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(config['cross_encoder_model_name'])
        # For inference, we need to know the feature sizes
        candidate_feature_size = config.get('candidate_feature_size', 0)
        job_feature_size = config.get('job_feature_size', 0)
        self.model = CrossEncoderModel(config, candidate_feature_size, job_feature_size).to(self.device)
        state_dict = torch.load(model_path, map_location=self.device)
        if 'model_state_dict' in state_dict:
            self.model.load_state_dict(state_dict['model_state_dict'])
        else:
            self.model.load_state_dict(state_dict)
        self.model.eval()

    def predict(self, candidate_texts, job_texts, candidate_features_list=None, job_features_list=None, batch_size=32):
        predictions = []
        if candidate_features_list is None:
            candidate_features_list = [None] * len(candidate_texts)
        if job_features_list is None:
            job_features_list = [None] * len(job_texts)
        with torch.no_grad():
            for i in range(0, len(candidate_texts), batch_size):
                batch_candidate_texts = candidate_texts[i:i+batch_size]
                batch_job_texts = job_texts[i:i+batch_size]
                inputs = self.tokenizer(batch_candidate_texts, batch_job_texts, max_length=self.config['max_length'],
                                        truncation=True, padding=True, return_tensors='pt')
                input_ids = inputs['input_ids'].to(self.device)
                attention_mask = inputs['attention_mask'].to(self.device)
                if self.config['use_sparse']:
                    batch_candidate_features = candidate_features_list[i:i+batch_size]
                    batch_job_features = job_features_list[i:i+batch_size]
                    features_list = []
                    for cf, jf in zip(batch_candidate_features, batch_job_features):
                        features = {
                            'candidate_features': torch.tensor(cf, dtype=torch.float) if cf is not None else torch.zeros(self.model.candidate_feature_size),
                            'job_features': torch.tensor(jf, dtype=torch.float) if jf is not None else torch.zeros(self.model.job_feature_size)
                        }
                        features_list.append(features)
                    # Prepare features
                    features_padded = CrossEncoderDataset.pad_features_static(features_list, self.model.candidate_feature_size, self.model.job_feature_size)
                    features_tensor = features_padded.to(self.device)
                    logits = self.model(input_ids=input_ids, attention_mask=attention_mask, features=features_tensor)
                else:
                    logits = self.model(input_ids=input_ids, attention_mask=attention_mask)
                #scores = torch.sigmoid(logits).cpu().tolist()
                raw_scores = logits.cpu().tolist()
                predictions.extend(raw_scores)
        return predictions

