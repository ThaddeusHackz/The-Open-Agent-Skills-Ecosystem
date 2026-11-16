---
name: tinker-api
description: Guide for using the Tinker API for LLM training. Use when working with Tinker training workflows, RL environments, supervised fine-tuning, model sampling, rendering, or any Tinker API operations.
metadata:
  author: Tinker Cookbook
  version: 1.0.0
  argument-hint: (optional) Specify training type (supervised, rl, dpo) or operation (sample, render, save-load)
---

# Tinker API Training Skill

Expert guidance for using the Tinker API - a training platform for fine-tuning large language models with supervised learning, reinforcement learning, and preference optimization.

## How It Works

1. **Detect Tinker API usage** - When user mentions Tinker training, RL environments, sampling, or references Tinker API operations
2. **Identify the workflow** - Determine if it's supervised learning, RL training, sampling, rendering, or infrastructure setup
3. **Provide comprehensive guidance** - Use scripts and examples to implement complete training recipes
4. **Emphasize best practices** - Async patterns, overlapping requests, proper data preparation, checkpoint management

## Quick Reference: Common Workflows

| Workflow | Script | Key APIs |
|----------|--------|----------|
| Setup & Test Connection | `scripts/setup-check.py` | `ServiceClient`, `get_server_capabilities` |
| Supervised Fine-tuning | `scripts/supervised-training.py` | `forward_backward`, `cross_entropy`, rendering |
| RL Training Loop | `scripts/rl-training.py` | `sample`, policy gradients, advantage estimation |
| Sampling & Inference | `scripts/sampling-demo.py` | `SamplingClient`, `sample`, `compute_logprobs` |
| Vision Model Training | `scripts/vision-training.py` | `ImageChunk`, `Qwen3VLRenderer` |
| Save/Load Checkpoints | `scripts/checkpoint-management.py` | `save_state`, `load_state`, `save_weights_for_sampler` |

## Core Concepts

### 1. Client Types

**ServiceClient** - Entry point for all operations
```python
import tinker
service_client = tinker.ServiceClient()
```

**TrainingClient** - For training operations (forward/backward, optim_step)
```python
training_client = service_client.create_lora_training_client(
    base_model="Qwen/Qwen3-30B-A3B",
    rank=32  # LoRA rank
)
```

**SamplingClient** - For inference and generation
```python
sampling_client = service_client.create_sampling_client(
    base_model="Qwen/Qwen3-30B-A3B"
)
# Or from saved weights:
sampling_client = training_client.save_weights_and_get_sampling_client(name="checkpoint-001")
```

### 2. Training Data Structure

All training uses `Datum` objects:
```python
from tinker import types

datum = types.Datum(
    model_input=types.ModelInput.from_ints(input_tokens),
    loss_fn_inputs={
        "target_tokens": target_tokens,  # For cross_entropy
        "weights": weights,              # Loss weights per token
        "advantages": advantages,        # For RL
        "logprobs": sampling_logprobs   # For importance sampling
    }
)
```

### 3. Loss Functions

**Supervised Learning:**
- `cross_entropy` - Standard NLL loss for supervised fine-tuning

**Reinforcement Learning:**
- `importance_sampling` - Corrects for sampling/learner policy mismatch
- `ppo` - Proximal Policy Optimization with clipping
- `cispo` - Clipped Importance Sampling Policy Optimization
- `dro` - Direct Reward Optimization (offline RL)

**Custom Losses:**
- `forward_backward_custom` - Define arbitrary differentiable loss functions

### 4. Async Patterns (Critical for Performance!)

**Always overlap requests to avoid missing clock cycles (~10 seconds each):**

```python
# GOOD - Submit both operations before waiting
fwd_bwd_future = await client.forward_backward_async(batch, "cross_entropy")
optim_future = await client.optim_step_async(adam_params)

# Now wait for results
fwd_bwd_result = await fwd_bwd_future
optim_result = await optim_future

# BAD - Sequential waiting misses clock cycles
fwd_bwd_result = await (await client.forward_backward_async(batch, "cross_entropy"))
optim_result = await (await client.optim_step_async(adam_params))  # May miss cycle!
```

### 5. Rendering (Messages to Tokens)

Use renderers to convert conversations to tokens:

```python
from tinker_cookbook import renderers, tokenizer_utils

tokenizer = tokenizer_utils.get_tokenizer('Qwen/Qwen3-30B-A3B')
renderer = renderers.get_renderer('qwen3', tokenizer)

# For generation (inference/RL)
prompt = renderer.build_generation_prompt(messages)
stop_sequences = renderer.get_stop_sequences()

# For supervised learning
model_input, weights = renderer.build_supervised_example(messages)
```

**Available renderers:**
- `qwen3` - Qwen3 models with thinking enabled (default)
- `qwen3_disable_thinking` - Qwen3 without thinking tokens
- `llama3` - Llama 3 models
- `deepseekv3` - DeepSeek V3 models

### 6. Vision Models

For vision-language models (Qwen3-VL):

```python
from tinker_cookbook.renderers import Message, ImagePart, TextPart

messages = [
    Message(role='user', content=[
        ImagePart(type='image', image='https://example.com/image.png'),
        TextPart(type='text', text='What is in this image?')
    ])
]

# Use Qwen3VL renderer
from tinker_cookbook.image_processing_utils import get_image_processor
image_processor = get_image_processor("Qwen/Qwen3-VL-235B-A22B-Instruct")
renderer = renderers.Qwen3VLInstructRenderer(tokenizer, image_processor)
```

## Training Recipes

### Recipe 1: Supervised Fine-tuning

**Use Case:** Train model on instruction-following data with known correct responses

**Script:** `scripts/supervised-training.py`

**Key Steps:**
1. Prepare conversation data with renderer
2. Forward-backward with `cross_entropy` loss
3. Optimizer step with Adam
4. Save checkpoints periodically
5. Sample to evaluate progress

**Critical Details:**
- Use `renderer.build_supervised_example()` to get proper loss weights
- Only assistant turns get weight=1, context gets weight=0
- Monitor loss per token: `-np.dot(logprobs, weights) / weights.sum()`

### Recipe 2: Reinforcement Learning

**Use Case:** Train with rewards/preferences, handle multi-turn interactions

**Script:** `scripts/rl-training.py`

**Key Steps:**
1. Sample multiple completions per query
2. Compute rewards (external evaluator, rule-based, or human feedback)
3. Estimate advantages (per-group centering recommended)
4. Forward-backward with policy gradient loss (`ppo`, `importance_sampling`)
5. Optional: Incorporate KL penalty into rewards

**Critical Details:**
- Save `sampling_logprobs` during generation for importance sampling
- Use group-based advantage estimation (GRPO-style)
- For PPO: clip ratios prevent large policy updates
- Monitor KL divergence to reference policy

### Recipe 3: Vision Model Training

**Use Case:** Fine-tune vision-language models on multimodal data

**Script:** `scripts/vision-training.py`

**Key Steps:**
1. Use Qwen3-VL models (30B or 235B)
2. Prepare messages with `ImagePart` and `TextPart`
3. Use `Qwen3VLRenderer` or `Qwen3VLInstructRenderer`
4. Train with supervised or RL approaches
5. Handle special vision tokens automatically

**Critical Details:**
- Images must specify format (png, jpg, etc.)
- Vision models require `image_processor`
- Special tokens `<|vision_start|>` and `<|vision_end|>` handled by renderer

### Recipe 4: Checkpoint Management

**Use Case:** Save progress, resume training, create sampling clients

**Script:** `scripts/checkpoint-management.py`

**Key Operations:**
```python
# Save for sampling only (faster, less storage)
sampling_path = training_client.save_weights_for_sampler(name="step-100").result().path

# Save full state (weights + optimizer) for resuming
resume_path = training_client.save_state(name="checkpoint-100").result().path

# Resume training
training_client.load_state(resume_path)

# Create sampling client from checkpoint
sampling_client = service_client.create_sampling_client(model_path=sampling_path)
```

## Common Patterns & Best Practices

### Pattern 1: Training Loop Structure

```python
import asyncio
import tinker
from tinker import types

async def training_loop():
    service_client = tinker.ServiceClient()
    training_client = await service_client.create_lora_training_client_async(
        base_model="Qwen/Qwen3-30B-A3B",
        rank=32
    )

    for step in range(num_steps):
        # Prepare batch
        batch = prepare_training_batch()  # Your data preparation

        # Overlap forward_backward and optim_step
        fwd_bwd_future = await training_client.forward_backward_async(
            batch, "cross_entropy"
        )
        optim_future = await training_client.optim_step_async(
            types.AdamParams(learning_rate=1e-4)
        )

        # Wait for results
        fwd_bwd_result = await fwd_bwd_future
        optim_result = await optim_future

        # Log metrics
        logprobs = [output['logprobs'] for output in fwd_bwd_result.loss_fn_outputs]
        # ... compute and log loss

        # Periodic checkpointing
        if step % checkpoint_interval == 0:
            await training_client.save_state_async(name=f"step-{step}")

asyncio.run(training_loop())
```

### Pattern 2: RL with Group-Based Advantage Estimation

```python
# Sample multiple completions per query
queries = ["Query 1", "Query 2", ...]
samples_per_query = 8

all_sequences = []
for query in queries:
    prompt = renderer.build_generation_prompt([{"role": "user", "content": query}])
    result = await sampling_client.sample_async(
        prompt=prompt,
        num_samples=samples_per_query,
        sampling_params=types.SamplingParams(
            max_tokens=100,
            temperature=0.8,
            stop=renderer.get_stop_sequences()
        )
    )
    all_sequences.extend(result.sequences)

# Compute rewards
rewards = compute_rewards(all_sequences)  # Your reward function

# Per-group advantage centering (GRPO-style)
advantages = []
for i in range(len(queries)):
    group_rewards = rewards[i*samples_per_query:(i+1)*samples_per_query]
    group_mean = np.mean(group_rewards)
    group_std = np.std(group_rewards) + 1e-8
    group_advantages = [(r - group_mean) / group_std for r in group_rewards]
    advantages.extend(group_advantages)

# Prepare training data
training_data = [
    types.Datum(
        model_input=types.ModelInput.from_ints(seq.tokens[:-1]),
        loss_fn_inputs={
            "target_tokens": seq.tokens[1:],
            "logprobs": seq.logprobs,  # From sampling
            "advantages": advantages[i]
        }
    )
    for i, seq in enumerate(all_sequences)
]

# Train with PPO
fwd_bwd_future = await training_client.forward_backward_async(
    training_data,
    loss_fn="ppo",
    loss_fn_config={"clip_low_threshold": 0.9, "clip_high_threshold": 1.1}
)
```

### Pattern 3: Multi-Turn Conversations

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."},
    {"role": "user", "content": "What's the population?"}
]

# Generate next assistant response
prompt = renderer.build_generation_prompt(messages)
result = await sampling_client.sample_async(
    prompt=prompt,
    num_samples=1,
    sampling_params=types.SamplingParams(
        max_tokens=100,
        stop=renderer.get_stop_sequences()
    )
)

# Parse response back to message
sampled_message, success = renderer.parse_response(result.sequences[0].tokens)
if success:
    messages.append(sampled_message)
```

## Common Pitfalls & Solutions

### Pitfall 1: Missing Clock Cycles
**Problem:** Sequential async calls waste time
**Solution:** Always overlap independent operations:
```python
# Submit both before waiting
future1 = await client.op1_async()
future2 = await client.op2_async()
result1 = await future1
result2 = await future2
```

### Pitfall 2: Incorrect Target Tokens
**Problem:** Forgetting to shift tokens for autoregressive prediction
**Solution:** Input tokens = `tokens[:-1]`, target tokens = `tokens[1:]`

### Pitfall 3: Loss Weights Misconfiguration
**Problem:** Training on prompt tokens or missing completion tokens
**Solution:** Use renderer's `build_supervised_example()` which sets weights correctly

### Pitfall 4: Not Saving Sampling Logprobs
**Problem:** Can't use importance sampling correction in RL
**Solution:** Always include `logprobs` in returned sequences during sampling

### Pitfall 5: Renderer Compatibility Issues
**Problem:** Training with non-HF-compatible renderer breaks OpenAI endpoint
**Solution:** Use default renderers (`qwen3`, `llama3`, etc.) for deployment compatibility

## Environment Variables

Set your API key:
```bash
export TINKER_API_KEY=<your-key>
```

## Supported Models

**Text Models:**
- `meta-llama/Llama-3.1-70B`
- `meta-llama/Llama-3.1-8B`
- `Qwen/Qwen3-30B-A3B`
- `Qwen/Qwen3-8B`
- `deepseek-ai/DeepSeek-V3`

**Vision-Language Models:**
- `Qwen/Qwen3-VL-30B-A3B-Instruct`
- `Qwen/Qwen3-VL-235B-A22B-Instruct`

## Usage Instructions for AI Agents

When a user requests help with Tinker API:

1. **Identify the task type:**
   - Setup/connection testing → Use `scripts/setup-check.py`
   - Supervised fine-tuning → Use `scripts/supervised-training.py`
   - RL training → Use `scripts/rl-training.py`
   - Sampling/inference → Use `scripts/sampling-demo.py`
   - Vision tasks → Use `scripts/vision-training.py`
   - Checkpoint operations → Use `scripts/checkpoint-management.py`

2. **Provide the appropriate script** and explain how to customize it for their use case

3. **Emphasize critical patterns:**
   - Always use async and overlap operations
   - Use renderers for message-to-token conversion
   - Save sampling logprobs for RL
   - Monitor metrics during training

4. **Reference documentation:**
   - Full docs: https://github.com/thinking-machines-lab/tinker-cookbook
   - Cookbook examples in `tinker-cookbook/` repo

5. **Help debug issues:**
   - Check async patterns
   - Verify tensor shapes and types
   - Confirm renderer compatibility
   - Review loss function configuration

## Additional Resources

- Tinker Cookbook: https://github.com/thinking-machines-lab/tinker-cookbook
- Tinker Docs: https://raw.githubusercontent.com/thinking-machines-lab/tinker-cookbook/refs/heads/main/docs/
- Blog: https://thinkingmachines.ai/blog/
- OpenAI-Compatible API: `/chat/completions` endpoint available
