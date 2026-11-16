/**
 * LetzAI Image Generation & Editing Examples
 *
 * Public API: https://api.letz.ai  (Swagger: https://api.letz.ai/doc)
 *
 * Every generation endpoint is asynchronous: POST returns a job id, then you
 * poll the matching GET until the status is terminal.
 */

const API_BASE_URL = 'https://api.letz.ai';
const API_KEY = process.env.LETZAI_API_KEY || 'YOUR_API_KEY';

const headers = {
  'Content-Type': 'application/json',
  Authorization: `Bearer ${API_KEY}`,
};

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/** Statuses that mean the job will never produce a result. */
const FAILED_STATUSES = new Set(['failed', 'interrupted', 'not_allowed']);
/** Statuses that mean the job finished successfully. */
const READY_STATUSES = new Set(['ready', 'saved']);

/**
 * Poll any LetzAI job endpoint until it reaches a terminal state.
 *
 * @param {string} endpoint - 'images' | 'image-edits' | 'upscale' | 'videos'
 * @param {string} jobId
 * @param {{ intervalMs?: number, maxAttempts?: number }} [options]
 */
async function pollJob(endpoint, jobId, { intervalMs = 3000, maxAttempts = 120 } = {}) {
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    const response = await fetch(`${API_BASE_URL}/${endpoint}/${jobId}`, { headers });

    if (response.status === 429) {
      await sleep(Number(response.headers.get('Retry-After') || 30) * 1000);
      continue;
    }
    if (!response.ok) {
      throw new Error(`HTTP ${response.status} polling ${endpoint}/${jobId}`);
    }

    const data = await response.json();
    console.log(`  ${endpoint}/${jobId}: ${data.status} (${data.progress ?? 0}%)`);

    if (READY_STATUSES.has(data.status)) return data;
    if (FAILED_STATUSES.has(data.status)) {
      throw new Error(`Job ${data.status}: ${data.statusDetail || 'no detail'}`);
    }

    await sleep(intervalMs);
  }

  throw new Error(`Timed out waiting for ${endpoint}/${jobId}`);
}

/** POST a job and surface API errors with a readable message. */
async function createJob(path, body) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    const message = Array.isArray(detail.message)
      ? detail.message.join('; ')
      : detail.message || response.statusText;

    switch (response.status) {
      case 400:
        throw new Error(`Invalid parameters: ${message}`);
      case 401:
        throw new Error('Invalid API key — check the Authorization header.');
      case 402:
        throw new Error('Insufficient credits. Top up at letz.ai/subscription');
      case 429:
        throw new Error('Rate limited — back off and retry.');
      default:
        throw new Error(`API error ${response.status}: ${message}`);
    }
  }

  return response.json();
}

// =============================================================================
// Image generation
// =============================================================================

/**
 * Example 1: Nano Banana Pro at HD.
 *
 * `mode` is the resolution tier and its allowed values differ per model:
 * Nano Banana Pro accepts 'default' (1K), '2k' (HD) and '4k'.
 */
async function generateBasicImage() {
  console.log('=== Nano Banana Pro (HD) ===');

  const { id } = await createJob('/images', {
    prompt: 'A beautiful sunset over a calm ocean, vibrant orange and purple sky',
    baseModel: 'gemini-3-pro-image',
    mode: '2k',
  });

  const result = await pollJob('images', id);
  console.log(`Image: ${result.imageVersions.original}`);
  return result;
}

/**
 * Example 2: Explicit dimensions.
 *
 * Aspect ratio is expressed through width/height (480-2160 each). There is no
 * `aspectRatio`, `seed` or `negativePrompt` field — sending one returns 400.
 */
async function generateWidescreenImage() {
  console.log('=== Widescreen, 4K tier ===');

  const { id } = await createJob('/images', {
    prompt: 'A majestic eagle soaring through snow-capped mountains, dramatic lighting',
    baseModel: 'gemini-3-pro-image',
    mode: '4k',
    width: 2160,
    height: 1216,
    quality: 3,
    creativity: 2,
  });

  const result = await pollJob('images', id);
  console.log(`Image: ${result.imageVersions.original}`);
  return result;
}

/** Example 3: Flux 2 — the API identifier is `flux2`, not `flux2-max`. */
async function generateFlux2Image() {
  console.log('=== Flux 2 (HD) ===');

  const { id } = await createJob('/images', {
    prompt: 'Cyberpunk city street at night, neon reflecting on wet pavement',
    baseModel: 'flux2',
    mode: 'hd',
    width: 1920,
    height: 1080,
  });

  const result = await pollJob('images', id);
  console.log(`Image: ${result.imageVersions.original}`);
  return result;
}

/** Example 4: Seedream 5 Pro. */
async function generateSeedreamImage() {
  console.log('=== Seedream 5 Pro (HD) ===');

  const { id } = await createJob('/images', {
    prompt: 'A serene Japanese garden with cherry blossoms, koi pond and a wooden bridge',
    baseModel: 'seedream-5-0-pro',
    mode: '2k',
  });

  const result = await pollJob('images', id);
  console.log(`Image: ${result.imageVersions.original}`);
  return result;
}

/** Example 5: Same prompt across several models, generated in parallel. */
async function compareModels() {
  console.log('=== Model comparison ===');

  const configs = [
    { baseModel: 'gemini-3-pro-image', mode: '2k' },
    { baseModel: 'flux2', mode: 'hd' },
    { baseModel: 'seedream-5-0-pro', mode: '2k' },
    { baseModel: 'gpt-image-2', mode: 'hd' },
  ];

  const jobs = await Promise.all(
    configs.map(async (config) => {
      const job = await createJob('/images', {
        prompt: 'Abstract art with flowing colours',
        ...config,
      });
      return { ...job, baseModel: config.baseModel };
    }),
  );

  const results = await Promise.all(jobs.map((job) => pollJob('images', job.id)));

  results.forEach((result, i) => {
    console.log(`${jobs[i].baseModel}: ${result.imageVersions.original}`);
  });

  return results;
}

/** Example 6: Fire-and-forget with a webhook instead of polling. */
async function generateWithWebhook(callbackUrl) {
  const job = await createJob('/images', {
    prompt: 'A lighthouse in a storm, long exposure',
    baseModel: 'flux2',
    mode: 'hd',
    webhookUrl: callbackUrl,
  });

  console.log(`Job ${job.id} started; your server will be called at ${callbackUrl}`);
  return job;
}

// =============================================================================
// Context editing
// =============================================================================

/** Example 7: Edit a public image URL. */
async function contextEditFromUrl(imageUrl, editPrompt) {
  console.log('=== Context edit (single source) ===');

  const { id } = await createJob('/image-edits', {
    mode: 'context',
    prompt: editPrompt,
    imageUrl,
    baseModel: 'gemini-3-pro-image',
    settings: {
      resolution: '2k',
      aspect_ratio: '16:9',
      model: 'gemini-3-pro-image',
    },
  });

  const result = await pollJob('image-edits', id);
  console.log(`Edited: ${result.generatedImageCompletion.imageVersions.original}`);
  return result;
}

/** Example 8: Combine several reference images (up to 9). */
async function contextEditMultiReference(imageUrls, editPrompt) {
  console.log('=== Context edit (multi-reference) ===');

  if (imageUrls.length > 9) {
    throw new Error('Maximum 9 reference images');
  }

  const { id } = await createJob('/image-edits', {
    mode: 'context',
    prompt: editPrompt,
    inputImageUrls: imageUrls,
    baseModel: 'seedream-5-0-pro',
    settings: { resolution: '4k', model: 'seedream-5-0-pro' },
  });

  const result = await pollJob('image-edits', id);
  console.log(`Edited: ${result.generatedImageCompletion.imageVersions.original}`);
  return result;
}

/** Example 9: Edit an image previously generated on LetzAI. */
async function editLetzAIImage(imageCompletionId, editPrompt) {
  console.log('=== Edit an existing LetzAI image ===');

  const { id } = await createJob('/image-edits', {
    mode: 'context',
    prompt: editPrompt,
    originalImageCompletionId: imageCompletionId,
    baseModel: 'gemini-3-pro-image',
    settings: { resolution: '2k', model: 'gemini-3-pro-image' },
  });

  const result = await pollJob('image-edits', id);
  console.log(`Original: ${result.originalImageCompletion?.imageVersions?.original ?? 'n/a'}`);
  console.log(`Edited:   ${result.generatedImageCompletion.imageVersions.original}`);
  return result;
}

// =============================================================================
// Upscaling — note the singular /upscale path on the public API
// =============================================================================

/** Example 10: Upscale a LetzAI image to 2K with Nano Banana Pro. */
async function upscaleImage(imageCompletionId) {
  console.log('=== Upscale ===');

  const { id } = await createJob('/upscale', {
    imageId: imageCompletionId,
    mode: 'nano-banana-pro',
    size: 8, // 4 -> 1K, 8 -> 2K, 12 -> 4K
    strength: 2,
  });

  const result = await pollJob('upscale', id);
  console.log(`Upscaled: ${result.imageVersions.original}`);
  return result;
}

// =============================================================================
// Custom trained models
// =============================================================================

/** Example 11: List trained models, optionally filtered by class. */
async function listTrainedModels(modelClass = null) {
  console.log('=== Trained models ===');

  const params = new URLSearchParams({
    limit: '10',
    sortBy: 'usages',
    sortOrder: 'DESC',
  });
  if (modelClass) params.set('class', modelClass);

  const response = await fetch(`${API_BASE_URL}/models?${params}`, { headers });
  if (!response.ok) throw new Error(`Failed to list models: HTTP ${response.status}`);

  const body = await response.json();
  const models = Array.isArray(body) ? body : body.data ?? [];

  console.log(`Total: ${response.headers.get('X-Total-Count') ?? models.length}`);
  models.forEach((model) => {
    console.log(`  @${model.name} (${model.class}) — ${model.usages} uses`);
  });

  return models;
}

/** Example 12: Find a person model and generate with it. */
async function generateWithTrainedModel() {
  console.log('=== Generate with a trained model ===');

  const models = await listTrainedModels('person');
  if (models.length === 0) {
    console.log('No person models found. Train one at letz.ai or via POST /models.');
    return null;
  }

  const model = models[0];
  const { id } = await createJob('/images', {
    prompt: `@${model.name} in a modern office, professional headshot`,
    baseModel: 'gemini-3-pro-image',
    mode: '2k',
  });

  const result = await pollJob('images', id);
  console.log(`Image with @${model.name}: ${result.imageVersions.original}`);
  return result;
}

// =============================================================================

async function main() {
  await generateBasicImage();

  // Uncomment to run the others:
  // await generateWidescreenImage();
  // await generateFlux2Image();
  // await generateSeedreamImage();
  // await compareModels();
  // await contextEditFromUrl('https://example.com/photo.jpg', 'Change the background to a beach');
  // await listTrainedModels('person');
  // await generateWithTrainedModel();
}

if (require.main === module) {
  main().catch((error) => {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  });
}

module.exports = {
  pollJob,
  createJob,
  generateBasicImage,
  generateWidescreenImage,
  generateFlux2Image,
  generateSeedreamImage,
  compareModels,
  generateWithWebhook,
  contextEditFromUrl,
  contextEditMultiReference,
  editLetzAIImage,
  upscaleImage,
  listTrainedModels,
  generateWithTrainedModel,
};
