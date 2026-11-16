"""
LetzAI Video Generation Examples

Public API: https://api.letz.ai  (Swagger: https://api.letz.ai/doc)

Videos are asynchronous: POST /videos returns a job id, then poll
GET /videos/{id} until the status is terminal. The finished file is at
`videoVersions["original"]`.
"""

import os
import time
from typing import Any, Dict, List, Optional

import requests

API_BASE_URL = "https://api.letz.ai"
API_KEY = os.environ.get("LETZAI_API_KEY", "YOUR_API_KEY")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}

READY_STATUSES = {"ready", "saved"}
FAILED_STATUSES = {"failed", "interrupted", "not_allowed"}


def create_job(path: str, body: Dict[str, Any]) -> Dict[str, Any]:
    """POST a job and raise a readable error when the API rejects it."""
    response = requests.post(f"{API_BASE_URL}{path}", headers=HEADERS, json=body)

    if not response.ok:
        try:
            detail = response.json()
        except ValueError:
            detail = {}
        message = detail.get("message", response.reason)
        if isinstance(message, list):
            message = "; ".join(message)

        if response.status_code == 400:
            raise ValueError(f"Invalid parameters: {message}")
        if response.status_code == 401:
            raise ValueError("Invalid API key — check the Authorization header.")
        if response.status_code == 402:
            raise ValueError("Insufficient credits. Top up at letz.ai/subscription")
        if response.status_code == 429:
            raise ValueError("Rate limited — back off and retry.")
        raise RuntimeError(f"API error {response.status_code}: {message}")

    return response.json()


def poll_job(
    endpoint: str,
    job_id: str,
    interval_seconds: float = 3.0,
    max_attempts: int = 200,
) -> Dict[str, Any]:
    """
    Poll a LetzAI job until it reaches a terminal state.

    Args:
        endpoint: 'images', 'videos', 'image-edits' or 'upscale'
        job_id: id returned by the create call
        interval_seconds: 3s for images/edits/upscales, 2-3s for videos
        max_attempts: give up after this many polls
    """
    url = f"{API_BASE_URL}/{endpoint}/{job_id}"

    for _ in range(max_attempts):
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 429:
            time.sleep(float(response.headers.get("Retry-After", 30)))
            continue

        response.raise_for_status()
        data = response.json()
        status = data.get("status", "")
        print(f"  {endpoint}/{job_id}: {status} ({data.get('progress', 0)}%)")

        if status in READY_STATUSES:
            return data
        if status in FAILED_STATUSES:
            raise RuntimeError(f"Job {status}: {data.get('statusDetail') or 'no detail'}")

        time.sleep(interval_seconds)

    raise TimeoutError(f"Timed out waiting for {endpoint}/{job_id}")


# =============================================================================
# Source image (optional — LetzAI also does text-to-video)
# =============================================================================


def generate_source_image(prompt: str) -> Dict[str, Any]:
    """Generate an image to animate."""
    print("=== Source image ===")

    job = create_job(
        "/images",
        {
            "prompt": prompt,
            "baseModel": "gemini-3-pro-image",
            "mode": "2k",
            "width": 1920,
            "height": 1080,
        },
    )
    result = poll_job("images", job["id"], interval_seconds=3.0)
    print(f"Image: {result['imageVersions']['original']}")
    return result


# =============================================================================
# Video generation
# =============================================================================


def text_to_video(prompt: str, mode: str = "video-kling26", duration: int = 5) -> Dict[str, Any]:
    """
    Example 1: Text-to-video.

    No image input is required — omit originalImageCompletionId / imageUrl /
    imageUrls and the model generates from the prompt alone.
    """
    print(f"=== Text-to-video ({mode}) ===")

    job = create_job(
        "/videos",
        {
            "prompt": prompt,
            "settings": {"mode": mode, "duration": duration},
        },
    )
    result = poll_job("videos", job["id"], interval_seconds=2.5)
    print(f"Video: {result['videoVersions']['original']}")
    return result


def video_from_url(
    prompt: str,
    image_url: str,
    mode: str = "video-kling26",
    duration: int = 5,
) -> Dict[str, Any]:
    """Example 2: Animate a public image URL."""
    print(f"=== Image-to-video from URL ({mode}) ===")

    job = create_job(
        "/videos",
        {
            "prompt": prompt,
            "imageUrl": image_url,
            "settings": {"mode": mode, "duration": duration},
        },
    )
    result = poll_job("videos", job["id"], interval_seconds=2.5)
    print(f"Video: {result['videoVersions']['original']}")
    return result


def video_from_image_id(
    prompt: str,
    image_completion_id: str,
    mode: str = "video-kling26",
    duration: int = 5,
) -> Dict[str, Any]:
    """Example 3: Animate an image you already generated on LetzAI."""
    print(f"=== Image-to-video from completion id ({mode}) ===")

    job = create_job(
        "/videos",
        {
            "prompt": prompt,
            "originalImageCompletionId": image_completion_id,
            "settings": {"mode": mode, "duration": duration},
        },
    )
    result = poll_job("videos", job["id"], interval_seconds=2.5)
    print(f"Video: {result['videoVersions']['original']}")
    return result


def video_veo31(prompt: str, image_url: str, with_sound: bool = True) -> Dict[str, Any]:
    """
    Example 4: Google Veo 3.1 with native audio.

    Veo 3.1 is fixed at 8 seconds. Base cost is 1500 credits, doubled with
    audio and doubled again at 1080p, so this call is expensive.
    """
    print("=== Veo 3.1 ===")

    job = create_job(
        "/videos",
        {
            "prompt": prompt,
            "imageUrl": image_url,
            "settings": {"mode": "video-veo31", "withSound": with_sound},
        },
    )
    # Veo takes noticeably longer than the Kling models.
    result = poll_job("videos", job["id"], interval_seconds=5.0)
    print(f"Video: {result['videoVersions']['original']}")
    return result


def video_kling3_multishot(shots: List[Dict[str, Any]], image_url: str) -> Dict[str, Any]:
    """
    Example 5: Kling V3 multi-shot storyboard.

    `prompts` is a top-level array of {prompt, duration} objects. Each shot
    needs at least 3 seconds and the total must stay within 15.
    """
    print("=== Kling V3 multi-shot ===")

    total = sum(shot["duration"] for shot in shots)
    if total > 15:
        raise ValueError(f"Total duration {total}s exceeds the 15s limit")

    job = create_job(
        "/videos",
        {
            "prompt": " ".join(shot["prompt"] for shot in shots),
            "prompts": shots,
            "imageUrl": image_url,
            "settings": {"mode": "video-kling3", "duration": total, "withSound": True},
        },
    )
    result = poll_job("videos", job["id"], interval_seconds=3.0)
    print(f"Video: {result['videoVersions']['original']}")
    return result


def video_first_last_frame(prompt: str, first_frame: str, last_frame: str) -> Dict[str, Any]:
    """
    Example 6: First/last-frame interpolation.

    `imageUrls[0]` is the first frame and `imageUrls[1]` the last. Supported by
    video-veo31, video-kling3 and the Seedance models.
    """
    print("=== First/last frame ===")

    job = create_job(
        "/videos",
        {
            "prompt": prompt,
            "imageUrls": [first_frame, last_frame],
            "settings": {"mode": "video-kling3", "duration": 5},
        },
    )
    result = poll_job("videos", job["id"], interval_seconds=3.0)
    print(f"Video: {result['videoVersions']['original']}")
    return result


def video_seedance(prompt: str, image_url: str, duration: int = 5) -> Dict[str, Any]:
    """
    Example 7: Seedance 2.0 — cinematic, always with audio.

    Priced per second and per resolution: 105/s at 480p, 210/s at 720p,
    500/s at 1080p and 1000/s at 4K. Set `resolution` deliberately.
    """
    print("=== Seedance 2.0 ===")

    job = create_job(
        "/videos",
        {
            "prompt": prompt,
            "imageUrl": image_url,
            "settings": {
                "mode": "video-seedance2",
                "duration": duration,
                "resolution": "720p",
            },
        },
    )
    result = poll_job("videos", job["id"], interval_seconds=3.0)
    print(f"Video: {result['videoVersions']['original']}")
    return result


def video_with_webhook(prompt: str, image_url: str, callback_url: str) -> Dict[str, Any]:
    """Example 8: Fire-and-forget with a webhook instead of polling."""
    job = create_job(
        "/videos",
        {
            "prompt": prompt,
            "imageUrl": image_url,
            "settings": {"mode": "video-kling26", "duration": 5},
            "webhookUrl": callback_url,
        },
    )
    print(f"Job {job['id']} started; your server will be called at {callback_url}")
    return job


# =============================================================================
# Complete workflow
# =============================================================================


def image_to_video_workflow() -> Dict[str, Any]:
    """Example 9: Generate an image, then animate it."""
    print("=" * 60)
    print("IMAGE-TO-VIDEO WORKFLOW")
    print("=" * 60)

    image = generate_source_image(
        "A majestic lion standing on a rock at sunset, golden savanna behind"
    )
    video = video_from_image_id(
        prompt="The lion slowly turns its head towards the camera, wind in its mane",
        image_completion_id=image["id"],
        mode="video-kling26",
        duration=5,
    )

    print("-" * 60)
    print(f"Image: {image['imageVersions']['original']}")
    print(f"Video: {video['videoVersions']['original']}")

    return {"image": image, "video": video}


def compare_video_models(image_url: str) -> Dict[str, Any]:
    """
    Example 10: Same source, several models.

    Veo 3.1 is deliberately left out — at 1500+ credits per clip it is far more
    expensive than the others.
    """
    print("=" * 60)
    print("VIDEO MODEL COMPARISON")
    print("=" * 60)

    prompt = "Gentle camera pan with subtle motion, cinematic"
    configs = [
        {"mode": "video-kling26", "duration": 5},
        {"mode": "video-wan25", "duration": 5},
        {"mode": "video-gemini-omni", "duration": 5},
    ]

    results: Dict[str, Any] = {}

    for config in configs:
        mode = config["mode"]
        print(f"--- {mode} ---")
        try:
            job = create_job(
                "/videos",
                {"prompt": prompt, "imageUrl": image_url, "settings": config},
            )
            result = poll_job("videos", job["id"], interval_seconds=3.0)
            results[mode] = result["videoVersions"]["original"]
        except (ValueError, RuntimeError, TimeoutError) as error:
            print(f"  {mode} failed: {error}")
            results[mode] = None

    print("-" * 60)
    for mode, url in results.items():
        print(f"{mode}: {url or 'failed'}")

    return results


def main() -> int:
    try:
        image = generate_source_image(
            "A serene mountain lake at dawn with mist rising from the water"
        )
        video_from_image_id(
            prompt="Gentle ripples spread across the lake as morning light intensifies",
            image_completion_id=image["id"],
            mode="video-kling26",
            duration=5,
        )

        # Uncomment to run the others:
        # text_to_video("A timelapse of clouds over a desert canyon")
        # video_veo31("...", image["imageVersions"]["original"])
        # compare_video_models(image["imageVersions"]["original"])

    except Exception as error:  # noqa: BLE001 - example script
        print(f"Error: {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
