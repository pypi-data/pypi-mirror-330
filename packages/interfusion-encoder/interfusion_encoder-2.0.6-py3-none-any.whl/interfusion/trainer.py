# interfusion/trainer.py

import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModel
import torch.optim as optim
import torch.nn as nn
from torch.cuda.amp import GradScaler
import os
import csv
import random
import numpy as np
from collections import defaultdict

from .models import CrossEncoderModel, compute_bi_encoder_embeddings
from .inference import InterFusionInference
from .data_utils import CrossEncoderDataset, set_seed
from .config import get_default_config


import time

'''
# Set environment variables and multiprocessing start method at the very beginning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import torch.multiprocessing as mp
try:
    mp.set_start_method('spawn', force=True)
except RuntimeError:
    # The start method has already been set
    pass
'''

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



def train_model(candidates, jobs, positive_matches, candidates_eval=None, jobs_eval=None, positive_matches_eval=None, user_config=None):
    """
    Train the InterFusion Encoder model.

    Parameters:
    - candidates: list of dictionaries representing candidates.
    - jobs: list of dictionaries representing jobs.
    - positive_matches: list of dictionaries representing positive matches.
    - candidates_eval: (optional) list of dictionaries representing evaluation candidates.
    - jobs_eval: (optional) list of dictionaries representing evaluation jobs.
    - positive_matches_eval: (optional) list of dictionaries representing evaluation positive matches.
    - user_config: (optional) dictionary to override default configurations.
    """
    
    
    start_epoch_bool = True
    
    # Merge user configuration with default configuration
    config = get_default_config()
    if user_config:
        config.update(user_config)
    
    if config.get('use_wandb', False):
        import wandb
        wandb.init(project=config.get('wandb_project', 'InterFusion'), config=config)
    elif config.get('use_mlflow', False):
        import mlflow
        mlflow.start_run()
        mlflow.log_params(config)


    set_seed(config['random_seed'])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Create directory to save models
    os.makedirs(config['save_dir'], exist_ok=True)

    # Load data
    # Candidates and jobs are passed directly as lists of dictionaries

    # Build mappings
    candidate_id_to_text = {candidate['candidate_id']: candidate['candidate_text'] for candidate in candidates}
    candidate_id_to_features = {candidate['candidate_id']: candidate.get('candidate_features', None) for candidate in candidates}
    job_id_to_text = {job['job_id']: job['job_text'] for job in jobs}
    job_id_to_features = {job['job_id']: job.get('job_features', None) for job in jobs}

    if candidates_eval is None:
        # If evaluation data is not provided, use the training data
        candidates_eval = candidates
        jobs_eval = jobs
        positive_matches_eval = positive_matches

    # Build data_samples
    # We will build data_samples per epoch, so no need to build it here

    # Initialize tokenizer
    tokenizer = AutoTokenizer.from_pretrained(config['cross_encoder_model_name'])

    # Initialize bi-encoder
    bi_encoder = AutoModel.from_pretrained(config['bi_encoder_model_name']).to(device)

    # Implement triangular learning rate scheduler with non-zero starting LR
    lr_start = config['initial_learning_rate']
    lr_max = config['learning_rate']
    num_epochs = config['num_epochs']
    start_mult = lr_start / lr_max  # Multiplier at epoch 0

    def lr_lambda(epoch):
        if epoch <= num_epochs / 2:
            return start_mult + (1.0 - start_mult) * (epoch / (num_epochs / 2))
        else:
            return start_mult + (1.0 - start_mult) * ((num_epochs - epoch) / (num_epochs / 2))

    # If using sparse features, set feature sizes
    candidate_feature_size = 0
    job_feature_size = 0
    if config['use_sparse']:
        # Verify that all candidates and jobs have 'candidate_features' and 'job_features'
        if all('candidate_features' in candidate for candidate in candidates) and all('job_features' in job for job in jobs):
            candidate_feature_lengths = [len(candidate['candidate_features']) for candidate in candidates]
            job_feature_lengths = [len(job['job_features']) for job in jobs]
            candidate_feature_size = max(candidate_feature_lengths)
            job_feature_size = max(job_feature_lengths)
            print(f"Candidate feature size detected and set to: {candidate_feature_size}")
            print(f"Job feature size detected and set to: {job_feature_size}")
        else:
            raise ValueError("All candidates and jobs must have 'candidate_features' and 'job_features' when 'use_sparse' is True.")

    # Load saved model if continue_training is True
    if config.get('continue_training', False):
        #saved_model_path = config.get('saved_model_path', None)
        saved_model_path = os.path.join(config.get('save_dir', None), config.get('saved_model_path', None))
        print("saved_model_path: ", saved_model_path)
        if saved_model_path and os.path.exists(saved_model_path):
            print(f"Loading saved model from {saved_model_path} for continued training...")
            checkpoint = torch.load(saved_model_path, map_location=device)

            # Initialize model
            model = CrossEncoderModel(config, candidate_feature_size, job_feature_size).to(device)

            # Load model state dict
            if 'model_state_dict' in checkpoint:
                model.load_state_dict(checkpoint['model_state_dict'])
                print("Model state dict loaded.")
            else:
                model.load_state_dict(checkpoint)
                print("Loaded model directly from checkpoint (no 'model_state_dict' key).")

            # Initialize optimizer, scheduler, and scaler
            optimizer = optim.AdamW(model.parameters(), lr=config['learning_rate'])
            scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)
            # scaler = torch.cuda.amp.GradScaler()  # REMOVED

            # Load optimizer and scheduler states if available
            if 'optimizer_state_dict' in checkpoint:
                optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
                print("Optimizer state dict loaded.")
            else:
                print("Optimizer state dict not found in checkpoint.")

            if 'scheduler_state_dict' in checkpoint:
                scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
                print("Scheduler state dict loaded.")
            else:
                print("Scheduler state dict not found in checkpoint.")

            # if 'scaler_state_dict' in checkpoint:
            #     scaler.load_state_dict(checkpoint['scaler_state_dict'])
            #     print("Scaler state dict loaded.")
            # else:
            #     print("Scaler state dict not found in checkpoint.")

            start_epoch = checkpoint.get('epoch', 1) + 1
            print(f"Resuming training from epoch {start_epoch}")
        else:
            print("Saved model path does not exist. Starting training from scratch.")
            start_epoch = 1
            # Initialize model, optimizer, scheduler, and scaler
            model = CrossEncoderModel(config, candidate_feature_size, job_feature_size).to(device)
            optimizer = optim.AdamW(model.parameters(), lr=config['learning_rate'])
            scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)
            # scaler = torch.cuda.amp.GradScaler()  # REMOVED
    else:
        print("Starting training from scratch.")
        start_epoch = 1
        # Initialize model, optimizer, scheduler, and scaler
        model = CrossEncoderModel(config, candidate_feature_size, job_feature_size).to(device)
        optimizer = optim.AdamW(model.parameters(), lr=config['learning_rate'])
        scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)
        # scaler = torch.cuda.amp.GradScaler()  # REMOVED

    # Build a list of all candidate IDs
    all_candidate_ids = list(candidate_id_to_text.keys())

    best_metric = 0.0  # Initialize best metric (e.g., Precision@5)
    
    evaluate(model, tokenizer, candidates_eval, jobs_eval, positive_matches_eval, config, bi_encoder, 0)
    
    for epoch in range(start_epoch, num_epochs):
    

        if (start_epoch_bool) or (epoch % config["hard_negative_sampling_frequency"] == 0):
            
            if (start_epoch_bool):
                start_epoch_bool = False
                
            sample_amount = config["random_candidate_sample_amount"]
            # Sample of candidates
            sampled_candidate_ids = random.sample(all_candidate_ids, k=int(len(all_candidate_ids)*sample_amount))
            sampled_candidate_set = set(sampled_candidate_ids)

            # Build data_samples for sampled candidates
            data_samples_epoch = []
            for match in positive_matches:
                candidate_id = match['candidate_id']
                if candidate_id in sampled_candidate_set:
                    job_id = match['job_id']
                    data_samples_epoch.append({
                        'candidate_id': candidate_id,
                        'candidate_text': candidate_id_to_text[candidate_id],
                        'positive_job_id': job_id,
                        'positive_job_text': job_id_to_text[job_id],
                        'candidate_features': candidate_id_to_features.get(candidate_id, None),
                        'positive_job_features': job_id_to_features.get(job_id, None)
                    })

            # Build positive_matches_epoch
            positive_matches_epoch = [match for match in positive_matches if match['candidate_id'] in sampled_candidate_set]

            # Build sampled_candidates
            sampled_candidates = [candidate for candidate in candidates if candidate['candidate_id'] in sampled_candidate_set]

            
            # Precompute negatives using bi-encoder
            print("Precomputing negatives using bi-encoder...")
            negatives = precompute_bi_encoder_negatives(bi_encoder, tokenizer, sampled_candidates, jobs, positive_matches_epoch, config)
            # Generate initial hard negatives
            print("Generating initial hard negatives...")
            hard_negatives = generate_hard_negatives(model, data_samples_epoch, tokenizer, negatives, config, candidate_feature_size, job_feature_size)

            # Precompute N random negatives per candidate
            print("Precomputing random negatives...")
            random_negatives = precompute_random_negatives(sampled_candidates, jobs, positive_matches_epoch, config)
            

        # Initialize dataset with initial hard negatives and random negatives
        train_dataset = CrossEncoderDataset(
            data_samples_epoch, tokenizer, config, negatives=negatives,
            hard_negatives=hard_negatives, random_negatives=random_negatives
        )
        train_dataset.update_hard_negatives(hard_negatives)
        train_dataset.update_random_negatives(random_negatives)

        # Train for one epoch (no scaler passed)
        train(model, train_dataset, optimizer, device, config, epoch, scheduler)

        # Evaluate the model
        if (epoch + 1) % config.get('eval_epoch', 1) == 0:
            avg_precisions = evaluate(model, tokenizer, candidates_eval, jobs_eval, positive_matches_eval, config, bi_encoder, epoch)
            
            path_tmp = os.path.join(config['save_dir'], "interfusion_tmp.pt")
            
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                 # 'scaler_state_dict': scaler.state_dict(),  # REMOVED
            }, path_tmp)
           
            
            # Check if Precision@5 improved
            if 5 in avg_precisions:
                current_metric = avg_precisions[5]  # Precision at 5
                if current_metric > best_metric:
                    best_metric = current_metric
                #if True:
                    # Save the model
                    model_save_path = os.path.join(config['save_dir'], f"interfusion_best_p5_{best_metric:.4f}.pt")
                    torch.save({
                        'epoch': epoch,
                        'model_state_dict': model.state_dict(),
                        'optimizer_state_dict': optimizer.state_dict(),
                        'scheduler_state_dict': scheduler.state_dict(),
                        # 'scaler_state_dict': scaler.state_dict(),  # REMOVED
                    }, model_save_path)
                    print(f"New best Precision@5: {best_metric:.4f}. Model saved to {model_save_path}")
                    # Log model checkpoint to W&B
            else:
                print("Precision@5 not available in evaluation results.")

    # Optionally, save the final model
    final_model_save_path = os.path.join(config['save_dir'], "interfusion_final.pt")
    torch.save({
        'epoch': num_epochs - 1,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'scheduler_state_dict': scheduler.state_dict(),
        # 'scaler_state_dict': scaler.state_dict(),  # REMOVED
    }, final_model_save_path)
    print(f"Final model saved to {final_model_save_path}")



import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
from tqdm import tqdm
import torch.nn as nn

class CandidatesDataset(Dataset):
    def __init__(self, candidates):
        self.candidates = candidates

    def __len__(self):
        return len(self.candidates)

    def __getitem__(self, idx):
        return self.candidates[idx]

def custom_collate_fn(batch):
    collated_batch = {}
    for key in batch[0]:
        collated_batch[key] = [item[key] for item in batch]
    return collated_batch



def precompute_bi_encoder_negatives(
    bi_encoder, tokenizer, candidates, jobs, positive_matches, config,
    batch_size=512, num_workers=12, debug=False
):
    """
    Precompute negative job samples for each candidate using DataLoader for efficient batching.

    Args:
        bi_encoder: The bi-encoder model used for computing embeddings.
        tokenizer: The tokenizer corresponding to the bi-encoder.
        candidates: List of candidate dictionaries with 'candidate_text' and 'candidate_id'.
        jobs: List of job dictionaries with 'job_text' and 'job_id'.
        positive_matches: List of dictionaries with 'candidate_id' and 'job_id' indicating positive matches.
        config: Dictionary containing configuration parameters like 'M', 'use_sparse', 'start_rank',
                and 'bi-encode_relevance_thresh' (the similarity threshold).
        batch_size: Batch size for processing candidates.
        num_workers: Number of worker processes for DataLoader.
        debug: If True, print timing and debug information.

    Returns:
        negatives: Dictionary mapping candidate IDs to negative job samples.
    """
    import time
    import numpy as np
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader

    # Assumed to be defined elsewhere:
    # - get_tqdm
    # - compute_bi_encoder_embeddings
    # - CandidatesDataset
    # - custom_collate_fn
    tqdm_fn = get_tqdm(config)

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    bi_encoder.to(device)

    # Extract candidate and job texts and IDs
    candidate_texts = [candidate['candidate_text'] for candidate in candidates]
    candidate_ids = [candidate['candidate_id'] for candidate in candidates]
    job_texts = [job['job_text'] for job in jobs]
    job_ids = [job['job_id'] for job in jobs]

    # Compute embeddings for candidates
    if debug:
        print("Computing candidate embeddings...")
        start_time = time.time()
    candidate_embeddings = compute_bi_encoder_embeddings(
        bi_encoder, tokenizer, candidate_texts, config
    )
    if debug:
        elapsed_time = time.time() - start_time
        print(f"Time taken to compute candidate embeddings: {elapsed_time:.2f} seconds")

    # Compute embeddings for jobs
    if debug:
        print("Computing job embeddings...")
        start_time = time.time()
    job_embeddings = compute_bi_encoder_embeddings(
        bi_encoder, tokenizer, job_texts, config
    )
    if debug:
        elapsed_time = time.time() - start_time
        print(f"Time taken to compute job embeddings: {elapsed_time:.2f} seconds")

    # Normalize embeddings
    candidate_embeddings = nn.functional.normalize(candidate_embeddings, p=2, dim=1).to(device)
    job_embeddings = nn.functional.normalize(job_embeddings, p=2, dim=1).to(device)

    # Build mappings from candidate/job IDs to their indices
    candidate_id_to_idx = {cid: idx for idx, cid in enumerate(candidate_ids)}
    job_id_to_idx = {jid: idx for idx, jid in enumerate(job_ids)}

    # Build a list of positive job indices per candidate
    positive_job_indices_per_candidate = [[] for _ in range(len(candidates))]
    for match in positive_matches:
        c_idx = candidate_id_to_idx.get(match['candidate_id'])
        j_idx = job_id_to_idx.get(match['job_id'])
        if c_idx is not None and j_idx is not None:
            positive_job_indices_per_candidate[c_idx].append(j_idx)

    # Retrieve configuration parameters
    M = config.get('M', 10)  # Number of negatives to sample per candidate
    use_sparse = config.get('use_sparse', False)
    start_rank = config.get('start_rank', 1000)  # Starting rank offset
    relevance_thresh = config.get('bi-encode_relevance_thresh', 0.7)  # Similarity threshold

    negatives = {}
    if use_sparse:
        negatives['negative_job_features'] = {}

    num_candidates = len(candidates)
    num_jobs = len(jobs)
    if num_jobs < start_rank + M:
        raise ValueError(f"Number of jobs ({num_jobs}) is less than start_rank ({start_rank}) + M ({M}).")

    # Ensure job embeddings are contiguous for efficient GPU operations
    job_embeddings = job_embeddings.contiguous()

    # Create Dataset and DataLoader for candidates
    dataset = CandidatesDataset(candidates)
    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
        collate_fn=custom_collate_fn
    )
    total_batches = len(dataloader)
    if debug:
        print(f"Total number of batches: {total_batches}")

    # Process candidate batches
    for batch_idx, batch_candidates in enumerate(tqdm_fn(dataloader, desc="Precomputing negatives in batches")):
        if debug:
            batch_start_time = time.time()

        # Get candidate IDs from the batch
        batch_candidate_ids = batch_candidates['candidate_id']
        batch_candidate_ids = [cid.item() if isinstance(cid, torch.Tensor) else cid for cid in batch_candidate_ids]

        try:
            batch_indices = [candidate_id_to_idx[cid] for cid in batch_candidate_ids]
        except KeyError as e:
            print(f"KeyError for candidate_id: {e}")
            raise

        # Retrieve embeddings for the current batch of candidates
        batch_embeddings = candidate_embeddings[batch_indices]  # Shape: [batch_size, embedding_dim]

        with torch.no_grad():
            # Compute similarities between batch candidates and all jobs
            similarities = torch.matmul(batch_embeddings, job_embeddings.t())  # Shape: [batch_size, num_jobs]

            # Exclude positive jobs by setting their similarities to -inf
            for i, c_idx in enumerate(batch_indices):
                pos_indices = positive_job_indices_per_candidate[c_idx]
                if pos_indices:
                    similarities[i, pos_indices] = -float('inf')

            # Sort similarities in descending order for each candidate
            sorted_similarities, sorted_indices = torch.sort(similarities, descending=True, dim=1)

        # Move sorted arrays to CPU for vectorized processing
        sorted_similarities_np = sorted_similarities.cpu().numpy()  # shape: [batch_size, num_jobs]
        sorted_indices_np = sorted_indices.cpu().numpy()  # shape: [batch_size, num_jobs]

        # Process negatives for each candidate using vectorized filtering
        for i, candidate_id in enumerate(batch_candidate_ids):
            # Consider jobs starting at start_rank onward
            sims_slice = sorted_similarities_np[i, start_rank:]
            indices_slice = sorted_indices_np[i, start_rank:]
            # Find positions where similarity is below the threshold
            valid_positions = np.where(sims_slice < relevance_thresh)[0]
            # Select up to M negatives
            if valid_positions.size > 0:
                selected_positions = valid_positions[:M]
                candidate_negatives = indices_slice[selected_positions]
            else:
                candidate_negatives = np.array([], dtype=np.int64)
            # Retrieve negative job IDs and texts
            negative_job_ids = [job_ids[j] for j in candidate_negatives]
            negative_job_texts = [job_texts[j] for j in candidate_negatives]
            negatives[candidate_id] = {
                'job_ids': negative_job_ids,
                'job_texts': negative_job_texts
            }
            if use_sparse:
                negative_job_features = [jobs[j].get('job_features', None) for j in candidate_negatives]
                negatives['negative_job_features'][candidate_id] = negative_job_features

        if debug:
            batch_elapsed_time = time.time() - batch_start_time
            print(f"Processed batch {batch_idx+1}/{total_batches} in {batch_elapsed_time:.2f} seconds")

        # Free memory for the batch variables
        del similarities, sorted_similarities, sorted_indices, sorted_similarities_np, sorted_indices_np
        torch.cuda.empty_cache()

    return negatives







def generate_hard_negatives(
    model, data_samples, tokenizer, negatives, config,
    candidate_feature_size, job_feature_size, debug=False
):
    """
    Generate hard negatives from precomputed negatives using a cross-encoder model.
    Optimized to process negatives per candidate to reduce redundant computations.
    Only computes hard negatives for candidates with more than a specified number of applies.
    """
    
    #return {}
    
    import time
    import numpy as np
    import torch
    from collections import defaultdict
    from torch.utils.data import DataLoader

    # Assume the following helper functions and classes are defined elsewhere:
    # - get_tqdm
    # - CrossEncoderDataset

    tqdm_fn = get_tqdm(config)

    # Set model to evaluation mode and get device
    model.eval()
    device = next(model.parameters()).device

    # Retrieve configuration parameters
    N = config['N']  # Number of hard negatives to select per candidate
    batch_size = config.get('negative_batch_size', 128)  # Default batch size
    use_sparse = config['use_sparse']  # Whether to use sparse features
    max_length = config.get('max_length', 512)  # Maximum sequence length for tokenizer

    # Get apply count threshold from config, default to 10
    apply_count_threshold = config.get('apply_count_threshold', 10)

    if debug:
        print("Preparing data for processing...")
        data_prep_start_time = time.time()

    # Compute apply counts per candidate
    candidate_apply_counts = defaultdict(int)
    for sample in data_samples:
        candidate_id = sample['candidate_id']
        candidate_apply_counts[candidate_id] += 1

    # Prepare data per candidate
    candidate_data = []
    processed_candidates = set()
    for sample in data_samples:
        candidate_id = sample['candidate_id']
        if (
            candidate_apply_counts[candidate_id] > apply_count_threshold
            and candidate_id not in processed_candidates
        ):
            processed_candidates.add(candidate_id)
            candidate_text = sample['candidate_text']
            candidate_features = sample.get('candidate_features', None)

            # Use precomputed negatives
            neg_job_texts = negatives[candidate_id]['job_texts']  # List of negative job texts
            neg_job_ids = negatives[candidate_id]['job_ids']      # List of negative job IDs
            if use_sparse:
                neg_features_list = negatives['negative_job_features'][candidate_id]
            else:
                neg_features_list = [None] * len(neg_job_texts)

            candidate_data.append({
                'candidate_id': candidate_id,
                'candidate_text': candidate_text,
                'candidate_features': candidate_features,
                'negative_job_texts': neg_job_texts,
                'negative_job_ids': neg_job_ids,
                'negative_job_features': neg_features_list
            })

    if debug:
        data_prep_elapsed_time = time.time() - data_prep_start_time
        print(f"Data preparation completed in {data_prep_elapsed_time:.2f} seconds")
        print(f"Total number of candidates to process: {len(candidate_data)} (Candidates with applies > {apply_count_threshold})")

    # Process data in batches
    hard_negatives = {}
    total_candidates = len(candidate_data)

    # Create DataLoader for candidates
    def collate_fn(batch):
        # Batch is a list of candidate_data dictionaries
        return batch

    dataloader = DataLoader(
        candidate_data,
        batch_size=batch_size,
        shuffle=False,
        num_workers=6,  # Adjust as needed
        collate_fn=collate_fn
    )

    if debug:
        print(f"Total number of batches: {len(dataloader)}")

    with torch.no_grad():
        for batch_idx, batch in enumerate(tqdm_fn(dataloader, desc="Generating hard negatives")):
            if debug:
                batch_start_time = time.time()

            # Process each candidate in the batch
            for candidate in batch:
            
                #if True:
                #    continue
            
                if debug:
                    candidate_start_time = time.time()

                candidate_id = candidate['candidate_id']
                candidate_text = candidate['candidate_text']
                candidate_features = candidate['candidate_features']
                neg_job_texts = candidate['negative_job_texts']
                neg_job_ids = candidate['negative_job_ids']
                neg_job_features_list = candidate['negative_job_features']

                # Tokenize candidate text once
                if debug:
                    tokenization_candidate_start_time = time.time()

                inputs_candidate = tokenizer(
                    candidate_text,
                    max_length=max_length,
                    truncation=True,
                    padding='max_length',
                    return_tensors='pt'
                )

                if debug:
                    tokenization_candidate_elapsed = time.time() - tokenization_candidate_start_time
                    print(f"Candidate {candidate_id}: Tokenized candidate text in {tokenization_candidate_elapsed:.2f} seconds")

                # Tokenize negative job texts
                if debug:
                    tokenization_negatives_start_time = time.time()

                inputs_negatives = tokenizer(
                    neg_job_texts,
                    max_length=max_length,
                    truncation=True,
                    padding='max_length',
                    return_tensors='pt'
                )

                if debug:
                    tokenization_negatives_elapsed = time.time() - tokenization_negatives_start_time
                    print(f"Candidate {candidate_id}: Tokenized negative job texts in {tokenization_negatives_elapsed:.2f} seconds")

                # Combine candidate and negative job tokens
                input_ids = torch.cat([inputs_candidate['input_ids'].repeat(len(neg_job_texts), 1), inputs_negatives['input_ids']], dim=1)
                attention_mask = torch.cat([inputs_candidate['attention_mask'].repeat(len(neg_job_texts), 1), inputs_negatives['attention_mask']], dim=1)

                input_ids = input_ids.to(device)
                attention_mask = attention_mask.to(device)

                if use_sparse:
                    if debug:
                        feature_prep_start_time = time.time()

                    # Prepare features
                    candidate_features_tensor = torch.tensor(candidate_features, dtype=torch.float).to(device).unsqueeze(0)
                    neg_job_features_tensor = torch.tensor(neg_job_features_list, dtype=torch.float).to(device)
                    features_tensor = torch.cat([candidate_features_tensor.repeat(len(neg_job_texts), 1), neg_job_features_tensor], dim=1)

                    if debug:
                        feature_prep_elapsed_time = time.time() - feature_prep_start_time
                        print(f"Candidate {candidate_id}: Prepared features in {feature_prep_elapsed_time:.2f} seconds")
                else:
                    features_tensor = None

                # Model inference
                if debug:
                    inference_start_time = time.time()

                if use_sparse and features_tensor is not None:
                    logits = model(input_ids=input_ids, attention_mask=attention_mask, features=features_tensor)
                else:
                    logits = model(input_ids=input_ids, attention_mask=attention_mask)

                if debug:
                    inference_elapsed_time = time.time() - inference_start_time
                    print(f"Candidate {candidate_id}: Model inference completed in {inference_elapsed_time:.2f} seconds")

                # Keep scores as tensors on GPU
                scores = logits.squeeze(-1)  # Assuming logits shape is [N, 1]

                # Select top negatives starting from the 10th hardest onward.
                if debug:
                    selection_start_time = time.time()

                num_to_skip = 10 # Number of hardest negatives to skip
                num_total = N + num_to_skip  # Total negatives to gather before skipping
                
                #print("num_total: ", scores.shape[0])

                # Make sure we don't request more negatives than available.
                if scores.shape[0] < num_total:
                    num_total = scores.shape[0]
                 

                top_scores, top_indices = torch.topk(scores, num_total, largest=True, sorted=False)

                # Convert indices to CPU and numpy.
                top_indices = top_indices.cpu().numpy()

                # Skip the hardest 'num_to_skip' negatives.
                selected_indices = top_indices[num_to_skip:]
                # In case there are more negatives than required, further trim to N negatives.
                if len(selected_indices) > N:
                    selected_indices = selected_indices[:N]

                # Use selected indices to select negative job IDs and texts
                hard_neg_ids = [neg_job_ids[i] for i in selected_indices]
                hard_neg_texts = [neg_job_texts[i] for i in selected_indices]
                if use_sparse:
                    hard_neg_features = [neg_job_features_list[i] for i in selected_indices]

                # Store hard negatives for this candidate
                hard_negatives[candidate_id] = {
                    'job_ids': hard_neg_ids,
                    'job_texts': hard_neg_texts
                }
                if use_sparse:
                    hard_negatives[candidate_id]['job_features'] = hard_neg_features

                if debug:
                    selection_elapsed_time = time.time() - selection_start_time
                    candidate_elapsed_time = time.time() - candidate_start_time
                    print(f"Candidate {candidate_id}: Selected top negatives in {selection_elapsed_time:.2f} seconds")
                    print(f"Candidate {candidate_id}: Processed in {candidate_elapsed_time:.2f} seconds")

            if debug:
                batch_elapsed_time = time.time() - batch_start_time
                print(f"Batch {batch_idx+1}/{len(dataloader)}: Processed in {batch_elapsed_time:.2f} seconds")

    return hard_negatives  # Return the hard negatives separately



def precompute_random_negatives(candidates, jobs, positive_matches, config, debug=False):
    """
    Function to precompute N random negatives per candidate.
    Optimized using NumPy for efficient sampling and includes bug fixes.
    """
    import time
    import numpy as np
    from collections import defaultdict

    tqdm_fn = get_tqdm(config)

    if debug:
        total_start_time = time.time()
        print("Starting precompute_random_negatives...")

    # Extract job IDs, texts, and features
    if debug:
        job_prep_start_time = time.time()

    job_ids = [job['job_id'] for job in jobs]
    job_texts = [job['job_text'] for job in jobs]
    job_id_to_text = {job['job_id']: job['job_text'] for job in jobs}
    job_id_to_features = {job['job_id']: job.get('job_features', None) for job in jobs}

    # Convert job IDs to a NumPy array for efficient operations
    np_job_ids = np.array(job_ids)
    
    # Convert job_ids (assumed to be a list or similar) to a NumPy array
    np_job_ids = np.array(job_ids)

    # Determine the number of samples that correspond to 10% of the array
    sample_size = max(1, int(0.1 * len(np_job_ids)))  # Ensures at least 1 element is selected

    # Randomly select 10% of the job IDs without replacement
    np_job_ids = np.random.choice(np_job_ids, size=sample_size, replace=False)

    if debug:
        job_prep_elapsed_time = time.time() - job_prep_start_time
        print(f"Prepared job IDs, texts, and features in {job_prep_elapsed_time:.2f} seconds")

    # Build positive job IDs per candidate
    if debug:
        positive_prep_start_time = time.time()

    positive_job_ids_per_candidate = defaultdict(set)
    for match in positive_matches:
        cid = match['candidate_id']
        jid = match['job_id']
        positive_job_ids_per_candidate[cid].add(jid)

    if debug:
        positive_prep_elapsed_time = time.time() - positive_prep_start_time
        print(f"Built positive job IDs per candidate in {positive_prep_elapsed_time:.2f} seconds")

    N = config['N']
    use_sparse = config['use_sparse']
    random_negatives = {}
    total_candidates = len(candidates)

    if debug:
        candidate_loop_start_time = time.time()
        print(f"Processing {total_candidates} candidates...")

    for idx, candidate in enumerate(tqdm_fn(candidates, desc="Random Sampling")):
    
        #if True:
        #    continue
    
        if debug and idx % 1000 == 0 and idx > 0:
            candidate_loop_elapsed = time.time() - candidate_loop_start_time
            print(f"Processed {idx}/{total_candidates} candidates in {candidate_loop_elapsed:.2f} seconds")

        cid = candidate['candidate_id']
        positive_jids = positive_job_ids_per_candidate.get(cid, set())
        
        
        if len(set(list(positive_jids))) <= config.get('apply_count_threshold', 10):
            continue
            
        #print("candidate applies: ", len(set(list(positive_jids))))
            
        # Use NumPy set difference to efficiently compute negative job IDs
        negative_jids = np.setdiff1d(np_job_ids, list(positive_jids), assume_unique=True)
        
        #negative_jids = np_job_ids
        

        if len(negative_jids) >= N:
            sampled_neg_jids = np.random.choice(negative_jids, N, replace=False)
        else:
            sampled_neg_jids = np.random.choice(negative_jids, N, replace=True)

        sampled_neg_jids = sampled_neg_jids.tolist()
        neg_job_texts = [job_id_to_text[jid] for jid in sampled_neg_jids]

        if use_sparse:
            neg_features_list = [job_id_to_features[jid] for jid in sampled_neg_jids]
        else:
            neg_features_list = [None] * len(sampled_neg_jids)

        random_negatives[cid] = {
            'job_ids': sampled_neg_jids,
            'job_texts': neg_job_texts,
            'job_features': neg_features_list  # Store features here under candidate_id
        }

    if debug:
        candidate_loop_elapsed_time = time.time() - candidate_loop_start_time
        total_elapsed_time = time.time() - total_start_time
        print(f"Processed all candidates in {candidate_loop_elapsed_time:.2f} seconds")
        print(f"Total time for precompute_random_negatives: {total_elapsed_time:.2f} seconds")

    return random_negatives


import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader

def train(model, train_dataset, optimizer, device, config, epoch, scheduler):
    """
    Train the CrossEncoderModel for one epoch with a listwise or pairwise ranking loss.
    
    This version removes mixed-precision calls and does *not* use GradScaler.
    All other lines remain unchanged.
    """

    tqdm = get_tqdm(config)

    # Initialize optimizer and accumulation steps
    optimizer.zero_grad()
    accumulation_steps = config['accumulation_steps']  # Update weights every N batches

    # Training function with listwise ranking loss
    model.train()
    train_dataloader = DataLoader(
        train_dataset,
        batch_size=config['train_batch_size'],
        shuffle=True,
        collate_fn=train_dataset.collate_fn,
        num_workers=config['num_workers'],
        pin_memory=True
    )
    total_loss = 0

    # This is still defined here (not used in the final loss),
    # kept so we're not skipping any line from the original code.
    criterion = nn.CrossEntropyLoss()

    for batch_idx, batch in enumerate(tqdm(train_dataloader, desc=f"Training Epoch {epoch+1}")):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels']
        candidate_to_indices = batch['candidate_to_indices']

        # No autocast context here
        if model.use_sparse:
            features = batch['features'].to(device)
            logits = model(input_ids=input_ids, attention_mask=attention_mask, features=features)
        else:
            logits = model(input_ids=input_ids, attention_mask=attention_mask)

        #print("logits: ", logits)
        #print("logits.shapes: ", logits.shape)

        # Make sure to start with a Tensor for loss
        loss = torch.zeros((), device=device, requires_grad=True)

        # If you'd like to configure margin for pairwise approach, you can keep it in config as well
        margin = 1.0  

        # Loop over each candidate group
        for candidate_id, indices in candidate_to_indices.items():
            candidate_logits = logits[indices]    # shape: (k,)
            candidate_labels = labels[indices]    # shape: (k,)

            positive_indices = (candidate_labels == 1).nonzero(as_tuple=True)[0]
            negative_indices = (candidate_labels == 0).nonzero(as_tuple=True)[0]

            # If no positives, skip
            if positive_indices.numel() == 0:
                continue
                
                
            # -------------------------
            # SAMPLING POSITIVES (NEW)
            # -------------------------
            max_positives = 30
            if positive_indices.numel() > max_positives:
                perm = torch.randperm(positive_indices.numel())
                positive_indices = positive_indices[perm[:max_positives]]

            # ---------------------------------------------------------
            # Check config for "ranking_loss_mode" to decide the approach
            # ---------------------------------------------------------
            if config.get("ranking_loss_mode", "listwise") == "listwise":
                # MULTI-POSITIVE LISTWISE CROSS-ENTROPY
                # -------------------------------------
                # 1. Compute log-softmax across candidate_logits
                # 2. Sum or average the log-prob for all positive items

                # candidate_logits shape: (k,)
                log_softmaxed = F.log_softmax(candidate_logits, dim=0)  # also shape: (k,)

                # Gather log-softmax values of the positives
                pos_log_probs = log_softmaxed[positive_indices]  # shape: (#positives,)

                # Option 1: sum of positives
                loss_candidate = -pos_log_probs.sum()

                # Optionally normalize by #positives if you prefer an average:
                num_positives = len(positive_indices)
                loss_candidate /= num_positives

            else:
                # print("PAIRWISE HINGE-STYLE RANKING (original code)")
                # PAIRWISE HINGE-STYLE RANKING (original code)
                # -------------------------------------------
                # We want logit[pos] - logit[neg] >= margin
                # => hinge loss = max(0, margin - (pos - neg))

              

                loss_candidate = torch.zeros((), device=device, requires_grad=True)
                for p in positive_indices:
                    for n in negative_indices:
                        diff = candidate_logits[p] - candidate_logits[n]
                        loss_pair = F.relu(margin - diff)  # shape: ()
                        loss_candidate = loss_candidate + loss_pair

                # Normalize by number of pairs (original logic)
                #num_pairs = len(positive_indices) * len(negative_indices)
                
                num_pairs = len(negative_indices)
                
                if num_pairs > 0:
                    loss_candidate = loss_candidate / num_pairs

            # Accumulate into total loss
            loss = loss + loss_candidate

        # Original code for per-candidate averaging:
        if len(candidate_to_indices) > 0:
            loss = loss / len(candidate_to_indices)
        else:
            # Keep it a Tensor
            loss = torch.zeros((), device=device, requires_grad=True)

        # Normalize loss for gradient accumulation
        loss = loss / accumulation_steps

        # Standard (full-precision) backward pass
        loss.backward()

        # Perform optimizer step every 'accumulation_steps' batches
        if (batch_idx + 1) % accumulation_steps == 0 or (batch_idx + 1 == len(train_dataloader)):
            optimizer.step()
            optimizer.zero_grad()

        # Accumulate total loss (multiply back to original scale)
        total_loss += loss.item() * accumulation_steps

    avg_loss = total_loss / len(train_dataloader)
    print(f"Average training loss: {avg_loss:.4f}")

    # Update learning rate
    scheduler.step()
    current_lr = scheduler.get_last_lr()[0]
    print(f"Current learning rate: {current_lr:.6f}")
    
eval_visual_fixed_candidate_ids = []



def evaluate(model, tokenizer, candidates_eval, jobs_eval, positive_matches_eval, config, bi_encoder, epoch):
    """
    Evaluate the model by computing Precision at N using both the bi-encoder and cross-encoder.
    Only evaluates candidates who have more than a specified number of applications.
    """
    import torch
    import numpy as np
    from collections import defaultdict

    # Use tqdm for progress bars
    tqdm_fn = get_tqdm(config)

    # Set model to evaluation mode and get device
    model.eval()
    device = next(model.parameters()).device

    # Retrieve evaluation parameters from config
    Ns = config['eval_Ns']
    K = config.get('eval_K', 50)  # Number of top jobs to retrieve using bi-encoder

    # Retrieve apply count threshold from config
    eval_apply_count_threshold = config.get('eval_apply_count_threshold', 10)

    # Build candidate and job texts and IDs
    candidate_texts_all = [candidate['candidate_text'] for candidate in candidates_eval]
    candidate_ids_all = [candidate['candidate_id'] for candidate in candidates_eval]
    job_texts = [job['job_text'] for job in jobs_eval]
    job_ids = [job['job_id'] for job in jobs_eval]

    # Create mappings from IDs to features
    candidate_id_to_features_all = {
        candidate['candidate_id']: candidate.get('candidate_features', None)
        for candidate in candidates_eval
    }
    job_id_to_features = {
        job['job_id']: job.get('job_features', None)
        for job in jobs_eval
    }

    # Create a mapping from candidate_id to ground truth job_ids
    candidate_to_jobs = defaultdict(set)
    for match in positive_matches_eval:
        cid = match['candidate_id']
        jid = match['job_id']
        candidate_to_jobs[cid].add(jid)

    # Compute application counts per candidate
    candidate_apply_counts = {cid: len(jobs) for cid, jobs in candidate_to_jobs.items()}

    # Filter candidates based on apply count threshold
    filtered_candidate_ids = [cid for cid in candidate_ids_all if candidate_apply_counts.get(cid, 0) > eval_apply_count_threshold]
    if not filtered_candidate_ids:
        print(f"No candidates have more than {eval_apply_count_threshold} applications.")
        return {}

    # Update candidate_texts, candidate_ids, candidate_id_to_features to only include filtered candidates
    candidate_ids = filtered_candidate_ids
    candidate_texts = [candidate_texts_all[candidate_ids_all.index(cid)] for cid in candidate_ids]
    candidate_id_to_features = {cid: candidate_id_to_features_all[cid] for cid in candidate_ids}

    # If using sparse features, set feature sizes
    if config['use_sparse']:
        # Verify that all evaluation candidates and jobs have 'candidate_features' and 'job_features'
        if all('candidate_features' in candidate for candidate in candidates_eval) and all('job_features' in job for job in jobs_eval):
            candidate_feature_lengths = [len(candidate['candidate_features']) for candidate in candidates_eval]
            job_feature_lengths = [len(job['job_features']) for job in jobs_eval]
            candidate_feature_size = max(candidate_feature_lengths)
            job_feature_size = max(job_feature_lengths)
            print(f"Candidate feature size detected and set to: {candidate_feature_size}")
            print(f"Job feature size detected and set to: {job_feature_size}")
        else:
            raise ValueError("All evaluation candidates and jobs must have 'candidate_features' and 'job_features' when 'use_sparse' is True.")
    else:
        candidate_feature_size = 0
        job_feature_size = 0

    # Compute embeddings using bi-encoder
    print("Computing candidate embeddings for evaluation...")
    candidate_embeddings = compute_bi_encoder_embeddings(
        bi_encoder, tokenizer, candidate_texts, config
    )
    print("Computing job embeddings for evaluation...")
    job_embeddings = compute_bi_encoder_embeddings(
        bi_encoder, tokenizer, job_texts, config
    )

    # Normalize embeddings
    candidate_embeddings = torch.nn.functional.normalize(candidate_embeddings, p=2, dim=1)
    job_embeddings = torch.nn.functional.normalize(job_embeddings, p=2, dim=1)

    # Move job_embeddings to the same device as batch_candidate_embeddings
    job_embeddings = job_embeddings.to(device)

    # Initialize per-candidate data structures
    num_candidates = len(candidate_ids)
    num_jobs = len(job_ids)

    # For storing top K job indices and similarities per candidate
    topk_similarities = np.zeros((num_candidates, K), dtype=np.float32)
    topk_indices = np.zeros((num_candidates, K), dtype=int)

    # Compute similarities in batches to handle memory constraints
    print("Computing top K similarities in batches...")
    eval_batch_size = config.get('eval_batch_size', 512)
    job_batch_size = config.get('eval_job_batch_size', 5000)  # New parameter to control job batch size

    for i in tqdm_fn(range(0, num_candidates, eval_batch_size), desc="Candidates"):
        batch_candidate_embeddings = candidate_embeddings[i:i+eval_batch_size].to(device)

        # Initialize per-batch top K similarities and indices
        batch_size = batch_candidate_embeddings.shape[0]
        batch_topk_similarities = np.full((batch_size, K), -np.inf, dtype=np.float32)
        batch_topk_indices = np.zeros((batch_size, K), dtype=int)

        for j in range(0, num_jobs, job_batch_size):
            job_embeddings_chunk = job_embeddings[j:j+job_batch_size].to(device)
            job_indices_chunk = np.arange(j, min(j+job_batch_size, num_jobs))

            # Compute similarities between batch candidates and job chunk
            with torch.no_grad():
                sim_chunk = torch.matmul(batch_candidate_embeddings, job_embeddings_chunk.t())  # [batch_size, job_chunk_size]
            sim_chunk = sim_chunk.cpu().numpy()  # [batch_size, job_chunk_size]

            # For each candidate in the batch, update top K similarities
            for bi in range(batch_size):
                # Combine current top K with new similarities
                candidate_similarities = np.concatenate([batch_topk_similarities[bi], sim_chunk[bi]])
                candidate_indices = np.concatenate([batch_topk_indices[bi], job_indices_chunk])
                # Get indices of top K similarities
                topk = np.argpartition(-candidate_similarities, K-1)[:K]
                # Update top K similarities and indices
                batch_topk_similarities[bi] = candidate_similarities[topk]
                batch_topk_indices[bi] = candidate_indices[topk]

        # After processing all job chunks, store the top K similarities and indices for this batch
        topk_similarities[i:i+batch_size] = batch_topk_similarities
        topk_indices[i:i+batch_size] = batch_topk_indices

    # Now, we have top K similarities and indices for all candidates
    # Proceed with evaluation

    ### Evaluation using bi-encoder similarities ###
    print("\nEvaluating using bi-encoder similarities...")
    precisions_at_N_bi = {N: [] for N in Ns}
    for idx, candidate_id in enumerate(candidate_ids):
        candidate_topk_indices = topk_indices[idx]
        candidate_topk_similarities = topk_similarities[idx]
        # Sort the top K similarities and indices
        sorted_order = np.argsort(-candidate_topk_similarities)
        sorted_indices = candidate_topk_indices[sorted_order]
        sorted_job_ids = [job_ids[i] for i in sorted_indices]
        ground_truth_job_ids = candidate_to_jobs.get(candidate_id, set())
        for N in Ns:
            top_N_job_ids = sorted_job_ids[:N]
            hits = ground_truth_job_ids.intersection(top_N_job_ids)
            precision = len(hits) / N
            precisions_at_N_bi[N].append(precision)

    # Compute average precision at each N for bi-encoder
    avg_precisions_bi = {}
    print("\nAverage Precision at N using bi-encoder:")
    for N in Ns:
        avg_precision = np.mean(precisions_at_N_bi[N]) if precisions_at_N_bi[N] else 0.0
        avg_precisions_bi[N] = avg_precision
        print(f"Precision at {N}: {avg_precision:.4f}")

    ### Proceed with cross-encoder evaluation ###
    # Prepare cross-encoder inputs
    print("\nEvaluating with cross-encoder...")
    all_candidate_texts = []
    all_job_texts = []
    all_candidate_ids = []
    all_job_ids_list = []  # Collect job_ids
    all_candidate_features = []
    all_job_features = []

    for idx, candidate_id in enumerate(candidate_ids):
        candidate_topk_indices = topk_indices[idx]
        candidate_topk_similarities = topk_similarities[idx]
        # Sort the top K similarities and indices
        sorted_order = np.argsort(-candidate_topk_similarities)
        sorted_indices = candidate_topk_indices[sorted_order]
        sorted_job_ids = [job_ids[i] for i in sorted_indices]
        sorted_job_texts = [job_texts[i] for i in sorted_indices]
        candidate_text = candidate_texts[idx]
        candidate_feature = candidate_id_to_features.get(candidate_id, None)
        num_jobs = len(sorted_job_texts)
        all_candidate_texts.extend([candidate_text] * num_jobs)
        all_candidate_features.extend([candidate_feature] * num_jobs)
        all_job_texts.extend(sorted_job_texts)
        all_job_ids_list.extend(sorted_job_ids)
        job_features = [
            job_id_to_features.get(job_id, None) for job_id in sorted_job_ids
        ]
        all_job_features.extend(job_features)
        all_candidate_ids.extend([candidate_id] * num_jobs)

    # Proceed with cross-encoder evaluation
    total_pairs = len(all_candidate_texts)
    scores = []
    negative_batch_size = config.get('negative_batch_size', 512)
    with torch.no_grad():
        for i in tqdm_fn(
            range(0, total_pairs, negative_batch_size), desc="Evaluating"
        ):
            batch_candidate_texts = all_candidate_texts[i:i+negative_batch_size]
            batch_job_texts = all_job_texts[i:i+negative_batch_size]
            batch_candidate_features = all_candidate_features[i:i+negative_batch_size]
            batch_job_features = all_job_features[i:i+negative_batch_size]
            inputs = tokenizer(
                batch_candidate_texts,
                batch_job_texts,
                max_length=config['max_length'],
                truncation=True,
                padding=True,
                return_tensors='pt'
            )
            input_ids = inputs['input_ids'].to(device)
            attention_mask = inputs['attention_mask'].to(device)
            if config['use_sparse']:
                # Prepare features
                features_list = []
                for cf, jf in zip(batch_candidate_features, batch_job_features):
                    if cf is not None and jf is not None:
                        features = np.concatenate([cf, jf])
                        features = torch.tensor(features, dtype=torch.float)
                    else:
                        # Use the calculated feature sizes
                        features = torch.zeros(candidate_feature_size + job_feature_size, dtype=torch.float)
                    features_list.append(features)
                features_tensor = torch.stack(features_list).to(device)
                logits = model(
                    input_ids=input_ids, attention_mask=attention_mask, features=features_tensor
                )
            else:
                logits = model(input_ids=input_ids, attention_mask=attention_mask)
            # Since logits is already the output, and it's a tensor of shape [batch_size], we can directly use it
            batch_scores = logits.cpu().tolist()
            scores.extend(batch_scores)

    # Collect scores per candidate
    candidate_job_scores = defaultdict(list)
    candidate_job_ids = defaultdict(list)
    idx = 0
    for cid, job_id in zip(all_candidate_ids, all_job_ids_list):
        candidate_job_scores[cid].append(scores[idx])
        candidate_job_ids[cid].append(job_id)
        idx += 1

    # Compute precision at N using cross-encoder
    precisions_at_N_cross = {N: [] for N in Ns}
    for candidate_id in candidate_ids:
        job_scores = candidate_job_scores[candidate_id]
        job_ids_list = candidate_job_ids[candidate_id]
        sorted_indices = np.argsort(-np.array(job_scores))
        sorted_job_ids = [job_ids_list[i] for i in sorted_indices]
        ground_truth_job_ids = candidate_to_jobs.get(candidate_id, set())
        for N in Ns:
            top_N_job_ids = sorted_job_ids[:N]
            hits = ground_truth_job_ids.intersection(top_N_job_ids)
            precision = len(hits) / N
            precisions_at_N_cross[N].append(precision)

    # Compute average precision at each N for cross-encoder
    avg_precisions = {}
    print("\nAverage Precision at N using cross-encoder:")
    for N in Ns:
        avg_precision = (
            np.mean(precisions_at_N_cross[N]) if precisions_at_N_cross[N] else 0.0
        )
        avg_precisions[N] = avg_precision
        print(f"Precision at {N}: {avg_precision:.4f}")

    # Log evaluation metrics to W&B or MLflow
    metrics = {f"Precision@{N}": avg_precisions[N] for N in Ns}
    metrics.update({f"BiEncoder Precision@{N}": avg_precisions_bi[N] for N in Ns})
    metrics["Epoch"] = epoch + 1

    if config.get('use_wandb', False):
        import wandb
        wandb.log(metrics)
    elif config.get('use_mlflow', False):
        import mlflow
        for key, value in metrics.items():
            mlflow.log_metric(key, value, step=epoch+1)
            
        
    #---------------------------------------
    # 5) SANITY CHECK: Print Top 10 and Bottom 10 Recommendations for 5 Candidates
    #---------------------------------------
    print("\n--- SANITY CHECK: Top 10 and Bottom 10 Recommendations for 5 Candidates ---\n")

    # Create mappings for candidate id -> candidate text and job id -> job text
    candidate_id_to_text = {cid: text for cid, text in zip(candidate_ids, candidate_texts)}
    job_id_to_text = {jid: text for jid, text in zip(job_ids, job_texts)}


    global eval_visual_fixed_candidate_ids
    
    if len(eval_visual_fixed_candidate_ids) == 0:
        # Choose 5 candidate IDs at random from candidate_ids
        eval_visual_fixed_candidate_ids = random.sample(candidate_ids, 5)

    for cid in eval_visual_fixed_candidate_ids:
        print(f"Candidate ID: {cid}")
        print(f"Candidate Text: {candidate_id_to_text[cid]}\n")
    
        scores_list = candidate_job_scores[cid]
        job_ids_list = candidate_job_ids[cid]
        scores_arr = np.array(scores_list)
    
        # === Sort indices in descending order by score ===
        sorted_indices = np.argsort(-scores_arr)

        # === Top 10 Unique Recommendations ===
        top10_unique_indices = []
        seen_texts = set()

        # Iterate over all sorted indices and pick jobs with unique text until we have 10.
        for idx in sorted_indices:
            jid = job_ids_list[idx]
            job_text = job_id_to_text.get(jid, "N/A")
            if job_text in seen_texts:
                continue  # Skip duplicates
            seen_texts.add(job_text)
            top10_unique_indices.append(idx)
            if len(top10_unique_indices) >= 10:
                break

        print("Top 10 Unique Recommendations:")
        for idx in top10_unique_indices:
            jid = job_ids_list[idx]
            score_val = scores_arr[idx]
            job_text = job_id_to_text.get(jid, "N/A")
            print(f"  Job ID: {jid}, Score: {score_val:.4f}")
            print(f"  Job Text: {job_text}\n")

        # === Mid 10 Recommendations ===
        # Calculate starting index for the middle 10 recommendations.
        total = len(sorted_indices)
        mid_start = total // 2 - 5  # Adjust if total is small
        mid10_indices = sorted_indices[mid_start:mid_start+10]

        print("Mid 10 Recommendations:")
        for idx in mid10_indices:
            jid = job_ids_list[idx]
            score_val = scores_arr[idx]
            job_text = job_id_to_text.get(jid, "N/A")
            print(f"  Job ID: {jid}, Score: {score_val:.4f}")
            print(f"  Job Text: {job_text}\n")

        # === Bottom 10 Recommendations ===
        bottom10_indices = np.argsort(scores_arr)[:10]

        print("Bottom 10 Recommendations:")
        for idx in bottom10_indices:
            jid = job_ids_list[idx]
            score_val = scores_arr[idx]
            job_text = job_id_to_text.get(jid, "N/A")
            print(f"  Job ID: {jid}, Score: {score_val:.4f}")
            print(f"  Job Text: {job_text}\n")

        print("=" * 10 + "\n")

    return avg_precisions
    
    

