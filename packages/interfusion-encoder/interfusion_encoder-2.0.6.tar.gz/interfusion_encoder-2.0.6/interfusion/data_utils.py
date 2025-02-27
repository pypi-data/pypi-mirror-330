# interfusion/data_utils.py

import random
import torch
from torch.utils.data import Dataset
import numpy as np

def set_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)

# Dataset class for the cross-encoder
class CrossEncoderDataset(Dataset):
    def __init__(self, data_samples, tokenizer, config, negatives=None, hard_negatives=None, random_negatives=None):
        """
        data_samples: list of dicts, each dict contains 'candidate_text', 'positive_job_text', 'candidate_id', etc.
        tokenizer: tokenizer to use
        config: configuration dictionary
        negatives: dict mapping candidate_id to list of M negative job_texts and ids (from bi-encoder)
        hard_negatives: dict mapping candidate_id to list of N hard negative job_texts and ids (from cross-encoder)
        random_negatives: dict mapping candidate_id to list of N random negative job_texts and ids
        """
        self.data_samples = data_samples
        self.tokenizer = tokenizer
        self.max_length = config['max_length']
        self.negatives = negatives  # M negatives per candidate
        self.hard_negatives = hard_negatives  # N hard negatives per candidate
        self.random_negatives = random_negatives  # N random negatives per candidate
        self.use_sparse = config['use_sparse']

    def __len__(self):
        return len(self.data_samples)

    def __getitem__(self, idx):
        sample = self.data_samples[idx]
        candidate_text = sample['candidate_text']
        positive_job_text = sample['positive_job_text']
        candidate_id = sample['candidate_id']
        candidate_features = sample.get('candidate_features', None)
        positive_job_features = sample.get('positive_job_features', None)
        items = []

        # Positive sample
        inputs = self.tokenizer(candidate_text, positive_job_text, max_length=self.max_length, truncation=True,
                                padding='max_length', return_tensors='pt')
        label = 1  # Positive class
        if self.use_sparse:
            features = self._prepare_features(candidate_features, positive_job_features)
        else:
            features = None
        items.append((inputs, features, label, candidate_id))

        # Negative samples (N hard negatives per candidate)
        if self.hard_negatives and candidate_id in self.hard_negatives:
            negative_job_texts = self.hard_negatives[candidate_id]['job_texts']
            negative_job_ids = self.hard_negatives[candidate_id]['job_ids']
            if self.use_sparse:
                negative_job_features_list = self.hard_negatives[candidate_id]['job_features']
            else:
                negative_job_features_list = [None] * len(negative_job_texts)

            for idx_neg, neg_job_text in enumerate(negative_job_texts):
                inputs_neg = self.tokenizer(candidate_text, neg_job_text, max_length=self.max_length, truncation=True,
                                            padding='max_length', return_tensors='pt')
                label_neg = 0  # Negative class
                if self.use_sparse:
                    neg_job_features = negative_job_features_list[idx_neg]
                    features_neg = self._prepare_features(candidate_features, neg_job_features)
                else:
                    features_neg = None
                items.append((inputs_neg, features_neg, label_neg, candidate_id))

        # Negative samples (N random negatives per candidate)
        if self.random_negatives and candidate_id in self.random_negatives:
            rand_neg_job_texts = self.random_negatives[candidate_id]['job_texts']
            rand_neg_job_ids = self.random_negatives[candidate_id]['job_ids']
            if self.use_sparse:
                rand_neg_features_list = self.random_negatives[candidate_id]['job_features']
            else:
                rand_neg_features_list = [None] * len(rand_neg_job_texts)
            for idx_neg, neg_job_text in enumerate(rand_neg_job_texts):
                inputs_neg = self.tokenizer(candidate_text, neg_job_text, max_length=self.max_length, truncation=True,
                                            padding='max_length', return_tensors='pt')
                label_neg = 0  # Negative class
                if self.use_sparse:
                    neg_job_features = rand_neg_features_list[idx_neg]
                    features_neg = self._prepare_features(candidate_features, neg_job_features)
                else:
                    features_neg = None
                items.append((inputs_neg, features_neg, label_neg, candidate_id))

        return items  # Return list of (inputs, features, label, candidate_id) tuples
        
    def collate_fn(self, batch):
        # batch is a list of lists of (inputs, features, label, candidate_id) tuples
        input_ids = []
        attention_masks = []
        labels = []
        features_list = []
        candidate_ids = []
        candidate_to_indices = {}
        idx = 0
        for items in batch:
            for inputs, features, label, candidate_id in items:
                input_ids.append(inputs['input_ids'].squeeze(0))
                attention_masks.append(inputs['attention_mask'].squeeze(0))
                labels.append(label)
                candidate_ids.append(candidate_id)
                if candidate_id not in candidate_to_indices:
                    candidate_to_indices[candidate_id] = []
                candidate_to_indices[candidate_id].append(idx)
                idx += 1
                if self.use_sparse:
                    features_list.append(features)
        input_ids = torch.stack(input_ids)
        attention_masks = torch.stack(attention_masks)
        labels = torch.tensor(labels)
        batch_data = {
            'input_ids': input_ids,
            'attention_mask': attention_masks,
            'labels': labels,
            'candidate_ids': candidate_ids,
            'candidate_to_indices': candidate_to_indices,
        }
        if self.use_sparse:
            features_padded = self._pad_features(features_list)
            batch_data['features'] = features_padded
        return batch_data

    def _prepare_features(self, candidate_features, job_features):
        if candidate_features is not None and job_features is not None:
            features = {
                'candidate_features': torch.tensor(candidate_features, dtype=torch.float),
                'job_features': torch.tensor(job_features, dtype=torch.float)
            }
        else:
            features = None
        return features

    def _pad_features(self, features_list):
        # Features_list is a list of dicts with 'candidate_features' and 'job_features'
        candidate_feature_lengths = [f['candidate_features'].size(0) for f in features_list if f is not None]
        job_feature_lengths = [f['job_features'].size(0) for f in features_list if f is not None]

        max_candidate_length = max(candidate_feature_lengths) if candidate_feature_lengths else 0
        max_job_length = max(job_feature_lengths) if job_feature_lengths else 0

        padded_candidate_features = []
        padded_job_features = []

        for features in features_list:
            if features is not None:
                candidate_feat = features['candidate_features']
                job_feat = features['job_features']

                # Pad candidate features
                pad_size_candidate = max_candidate_length - candidate_feat.size(0)
                if pad_size_candidate > 0:
                    candidate_feat = torch.cat([candidate_feat, torch.zeros(pad_size_candidate)], dim=0)

                # Pad job features
                pad_size_job = max_job_length - job_feat.size(0)
                if pad_size_job > 0:
                    job_feat = torch.cat([job_feat, torch.zeros(pad_size_job)], dim=0)
            else:
                candidate_feat = torch.zeros(max_candidate_length)
                job_feat = torch.zeros(max_job_length)

            padded_candidate_features.append(candidate_feat)
            padded_job_features.append(job_feat)

        # Stack features
        candidate_features_tensor = torch.stack(padded_candidate_features)
        job_features_tensor = torch.stack(padded_job_features)

        # Concatenate candidate and job features
        features_tensor = torch.cat([candidate_features_tensor, job_features_tensor], dim=1)  # Shape: [batch_size, total_feature_size]
        return features_tensor

    @staticmethod
    def pad_features_static(features_list, candidate_feature_size, job_feature_size):
        # Static method to pad features when feature sizes are known
        padded_candidate_features = []
        padded_job_features = []

        for features in features_list:
            if features is not None:
                candidate_feat = features['candidate_features']
                job_feat = features['job_features']

                # Pad candidate features
                pad_size_candidate = candidate_feature_size - candidate_feat.size(0)
                if pad_size_candidate > 0:
                    candidate_feat = torch.cat([candidate_feat, torch.zeros(pad_size_candidate)], dim=0)

                # Pad job features
                pad_size_job = job_feature_size - job_feat.size(0)
                if pad_size_job > 0:
                    job_feat = torch.cat([job_feat, torch.zeros(pad_size_job)], dim=0)
            else:
                candidate_feat = torch.zeros(candidate_feature_size)
                job_feat = torch.zeros(job_feature_size)

            padded_candidate_features.append(candidate_feat)
            padded_job_features.append(job_feat)

        # Stack features
        candidate_features_tensor = torch.stack(padded_candidate_features)
        job_features_tensor = torch.stack(padded_job_features)

        # Concatenate candidate and job features
        features_tensor = torch.cat([candidate_features_tensor, job_features_tensor], dim=1)  # Shape: [batch_size, total_feature_size]
        return features_tensor

    def update_hard_negatives(self, hard_negatives):
        self.hard_negatives = hard_negatives

    def update_random_negatives(self, random_negatives):
        self.random_negatives = random_negatives

