---
name: ml-knowledge-index
description: >
  Routes ML/DL questions to specialized skills. Use FIRST when unsure which
  skill applies, when user asks broad ML questions, or when multiple topics
  might be relevant. Maps: regression/classification → ml-fundamentals,
  ensembles/clustering → ml-advanced, TF-IDF/Word2Vec → nlp-classical,
  training/backprop → deep-learning-core, PyTorch → pytorch-mastery,
  CNNs/images → cnn-vision, LSTM/time-series → sequence-models,
  BERT/HuggingFace → transformers-llm, RAG/embeddings → rag-retrieval,
  APIs/PDF-parsing → data-pipeline, LoRA/QLoRA/PEFT → fine-tuning-peft,
  MLflow/W&B/Optuna → mlops-experiment, SHAP/Grad-CAM → model-interpretability,
  Q-learning/PPO/DQN → reinforcement-learning, GAN/VAE/diffusion →
  generative-models, explanations → ml-teaching-assistant.
---

# ML/DL Knowledge Index

מדריך ניווט למערכת הסקילים של ML/DL מקורס Hebrew University.

## Quick Reference: Which Skill to Use

| If the task involves... | Use this skill |
|------------------------|----------------|
| Regression, classification, evaluation metrics | `ml-fundamentals` |
| Random Forest, XGBoost, clustering, PCA, recommender systems | `ml-advanced` |
| TF-IDF, Word2Vec, topic modeling, text similarity | `nlp-classical` |
| Training loops, loss functions, backpropagation | `deep-learning-core` |
| PyTorch tensors, DataLoader, GPU memory | `pytorch-mastery` |
| CNNs, image classification, transfer learning | `cnn-vision` |
| RNN, LSTM, time series, text generation | `sequence-models` |
| Transformers, BERT, HuggingFace, LLMs | `transformers-llm` |
| RAG, embeddings, vector stores, semantic search | `rag-retrieval` |
| LLM APIs, PDF parsing, chunking, function calling | `data-pipeline` |
| LoRA, QLoRA, PEFT, quantization, instruction tuning, RLHF/DPO | `fine-tuning-peft` |
| MLflow, W&B, experiment tracking, hyperparameter tuning, Optuna | `mlops-experiment` |
| SHAP, feature importance, Grad-CAM, error analysis, explainability | `model-interpretability` |
| Reinforcement learning, Q-learning, DQN, PPO, Gymnasium | `reinforcement-learning` |
| GANs, VAE, diffusion models, Stable Diffusion, image generation | `generative-models` |
| Need explanation, "how does X work", teaching | `ml-teaching-assistant` |

## Skill Summaries

### ml-fundamentals
**Topics**: Linear/Logistic Regression, Decision Trees, Ridge/Lasso, train/test split, cross-validation, Precision/Recall/F1, ROC-AUC, feature engineering, encoding, scaling

### ml-advanced
**Topics**: Random Forest, XGBoost, CatBoost, Stacking, K-Means, DBSCAN, Hierarchical clustering, PCA, t-SNE, UMAP, geospatial analysis, **Matrix Factorization**, **NeuMF**, **recommender systems**

### nlp-classical
**Topics**: Bag-of-Words, TF-IDF, Word2Vec, FastText, GloVe, Doc2Vec, LDA topic modeling, Jaccard/Cosine similarity, FuzzyWuzzy, record linkage

### deep-learning-core
**Topics**: Three Pillars (Model, Loss, Optimizer), gradient descent, backpropagation, Adam/SGD, learning rate, Dropout, BatchNorm, MLP architecture, **Autoencoders**, Denoising AE, latent space

### pytorch-mastery
**Topics**: Tensor creation, broadcasting, NCHW format, Dataset/DataLoader, training loop patterns, CUDA, GPU memory, `.to(device)`, debugging shapes, **environment setup**, nvidia-smi

### cnn-vision
**Topics**: Convolution, pooling, feature maps, LeNet/ResNet/VGG, transfer learning, fine-tuning, data augmentation, image preprocessing, MNIST, **multi-modal networks**, **image captioning**

### sequence-models
**Topics**: RNN formula, hidden state, vanishing gradients, LSTM/GRU, time series forecasting, text generation, language models, sequence classification

### transformers-llm
**Topics**: Self-attention, Transformer architecture, BERT, MLM/NSP, HuggingFace Tokenizer/Trainer/Pipeline, GPT, Claude, Gemini, prompt engineering

### rag-retrieval
**Topics**: Embedding APIs (OpenAI, Gemini, Sentence-Transformers), FAISS, ChromaDB, Pinecone, RAG variants, query rewriting, RAGAS evaluation, hybrid search

### data-pipeline
**Topics**: OpenAI/Gemini/Ollama setup, LiteLLM, pdfplumber, PyMuPDF, OCR, chunking strategies, function calling, LangChain agents, Pydantic validation

### fine-tuning-peft
**Topics**: LoRA, QLoRA, PEFT library, adapter tuning, instruction tuning, quantization (GPTQ, AWQ, GGUF, bitsandbytes), DPO/RLHF alignment, SFTTrainer, TRL, Unsloth, Axolotl, model merging

### mlops-experiment
**Topics**: MLflow, Weights & Biases, TensorBoard, Optuna hyperparameter tuning, model registry, experiment versioning, learning rate schedulers, early stopping, reproducibility

### model-interpretability
**Topics**: SHAP (TreeExplainer, DeepExplainer, KernelExplainer), feature importance (MDI, Permutation), Grad-CAM, LIME, attention visualization, confusion matrix analysis, error analysis pipeline

### reinforcement-learning
**Topics**: MDP, Q-Learning, DQN (experience replay, target network), Policy Gradient (REINFORCE), PPO, Actor-Critic, Stable-Baselines3, Gymnasium environments, reward shaping

### generative-models
**Topics**: GANs (DCGAN, WGAN), VAE (reparameterization trick, KL divergence), Diffusion Models (DDPM), Stable Diffusion, text-to-image, latent space interpolation, conditional generation

### ml-teaching-assistant
**Topics**: Concept explanations with analogies, visual ASCII diagrams, common misconceptions, progressive complexity, "why" questions

## Common Cross-Skill Workflows

### "I want to build an image classifier"
```
1. cnn-vision          → Architecture selection, augmentation
2. pytorch-mastery     → Training loop, DataLoader
3. deep-learning-core  → Loss functions, regularization
4. ml-teaching-assistant → If needs explanation
```

### "I want to build a RAG system"
```
1. rag-retrieval       → Architecture, vector stores
2. data-pipeline       → PDF parsing, chunking
3. transformers-llm    → Embedding models, LLM selection
```

### "I want to do customer segmentation"
```
1. ml-advanced         → Clustering algorithms (K-Means, DBSCAN)
2. ml-fundamentals     → Feature engineering, evaluation
3. data-pipeline       → Data preprocessing
```

### "I want to classify text"
```
Option A (Classical): nlp-classical → TF-IDF + sklearn
Option B (Deep): sequence-models → LSTM embeddings
Option C (Modern): transformers-llm → BERT fine-tuning
```

### "I want to build a recommender system"
```
1. ml-advanced           → Matrix Factorization, NeuMF architecture
2. pytorch-mastery       → Training loop, DataLoader, GPU
3. deep-learning-core    → Loss functions (MSELoss), embedding layers
```

### "I want to fine-tune an LLM"
```
1. fine-tuning-peft      → LoRA/QLoRA setup, dataset preparation
2. transformers-llm      → HuggingFace Trainer, tokenization
3. mlops-experiment      → Experiment tracking, hyperparameter tuning
```

### "I want to understand why my model predicts X"
```
1. model-interpretability → SHAP, Grad-CAM, error analysis
2. ml-fundamentals        → Evaluation metrics, confusion matrix
```

### "I want to train an RL agent"
```
1. reinforcement-learning → Algorithm selection, environment setup
2. pytorch-mastery        → Neural network for policy/value
3. mlops-experiment       → Tracking RL experiments
```

### "I want to generate images"
```
1. generative-models      → GAN/VAE/Diffusion architecture
2. cnn-vision             → CNN layers, image processing
3. pytorch-mastery        → Training loop, GPU optimization
```

## Custom Models vs LLMs Decision Framework

| Scenario | Use Custom Models | Use LLMs |
|----------|------------------|----------|
| Narrow tasks (classification, ranking) | Small models can beat LLMs | - |
| Domain-specific jargon, frequent updates | Private data, specialized | - |
| Large corpus analysis | LLMs can't comprehend many docs | - |
| Tabular / Time-series data | LLMs not suited | - |
| Recommender systems | Specialized architectures (MF, NeuMF) | - |
| Cost / Privacy concerns | LLMs expensive, external APIs | - |
| Flexible NL understanding | - | Quick prototyping |
| Document generation / summarization | - | Natural strength |
| Question answering with RAG | - | With retrieval pipeline |
| Function calling / AI agents | - | Tool-augmented LLMs |

**Rule of thumb:** Start with the simplest model that meets your needs.

## Learning Paths

- **New to ML?** Start with `ml-fundamentals` → `ml-advanced` → `deep-learning-core`
- **Deep Learning Track:** `deep-learning-core` → `pytorch-mastery` → `cnn-vision` or `sequence-models`
- **NLP Track:** `nlp-classical` → `transformers-llm` → `rag-retrieval`
- **LLM Engineering:** `transformers-llm` → `fine-tuning-peft` → `mlops-experiment`
- **Generative AI:** `deep-learning-core` → `generative-models` → `fine-tuning-peft`
- **RL Track:** `deep-learning-core` → `reinforcement-learning`
- **Production ML:** `mlops-experiment` → `model-interpretability` → `fine-tuning-peft`

## Reference
- `reference/full_topic_index.md` - Complete searchable index of all topics
