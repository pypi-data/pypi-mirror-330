# interfusion/inference.py

import torch
from transformers import AutoTokenizer
from .models import CrossEncoderModel
from .config import get_default_config
from .data_utils import CrossEncoderDataset

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
        user_feature_size = config.get('user_feature_size', 0)
        item_feature_size = config.get('item_feature_size', 0)
        self.model = CrossEncoderModel(config, user_feature_size, item_feature_size).to(self.device)
        state_dict = torch.load(model_path, map_location=self.device)
        if 'model_state_dict' in state_dict:
            self.model.load_state_dict(state_dict['model_state_dict'])
        else:
            self.model.load_state_dict(state_dict)
        self.model.eval()

    def predict(self, user_texts, item_texts, user_features_list=None, item_features_list=None, batch_size=32):
        predictions = []
        if user_features_list is None:
            user_features_list = [None] * len(user_texts)
        if item_features_list is None:
            item_features_list = [None] * len(item_texts)
        with torch.no_grad():
            for i in range(0, len(user_texts), batch_size):
                batch_user_texts = user_texts[i:i+batch_size]
                batch_item_texts = item_texts[i:i+batch_size]
                inputs = self.tokenizer(batch_user_texts, batch_item_texts, max_length=self.config['max_length'],
                                        truncation=True, padding=True, return_tensors='pt')
                input_ids = inputs['input_ids'].to(self.device)
                attention_mask = inputs['attention_mask'].to(self.device)
                if self.config['use_sparse']:
                    batch_user_features = user_features_list[i:i+batch_size]
                    batch_item_features = item_features_list[i:i+batch_size]
                    features_list = []
                    for cf, jf in zip(batch_user_features, batch_item_features):
                        features = {
                            'user_features': torch.tensor(cf, dtype=torch.float) if cf is not None else torch.zeros(self.model.user_feature_size),
                            'item_features': torch.tensor(jf, dtype=torch.float) if jf is not None else torch.zeros(self.model.item_feature_size)
                        }
                        features_list.append(features)
                    # Prepare features
                    features_padded = CrossEncoderDataset.pad_features_static(features_list, self.model.user_feature_size, self.model.item_feature_size)
                    features_tensor = features_padded.to(self.device)
                    logits = self.model(input_ids=input_ids, attention_mask=attention_mask, features=features_tensor)
                else:
                    logits = self.model(input_ids=input_ids, attention_mask=attention_mask)
                #scores = torch.sigmoid(logits).cpu().tolist()
                raw_scores = logits.cpu().tolist()
                predictions.extend(raw_scores)
        return predictions

