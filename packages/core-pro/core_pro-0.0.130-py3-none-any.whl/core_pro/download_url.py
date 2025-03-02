from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path
from io import BytesIO
from typing import List, Tuple, Optional, Union
from functools import partial
from rich import print
from tqdm.auto import tqdm
from tenacity import retry, stop_after_attempt, wait_exponential
from PIL import Image, ImageFile
import httpx
from time import time
import certifi
import os
import traceback
import math

# Allow loading of truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry_error_callback=lambda retry_state: None,
)
def download_image(url: str, timeout: float = 30.0):
    """Download an image with retry logic"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "image/webp,image/*,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    try:
        with httpx.Client(
            verify=certifi.where(),
            headers=headers,
            follow_redirects=True,
            timeout=timeout,
        ) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.content
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return None


def process_image(
    data: Tuple[int, str],
    output_dir: Path,
    resize_size: Optional[Tuple[int, int]] = None,
    images_per_folder: int = 1000,
) -> bool:
    """Download and process a single image."""
    idx, url = data

    # Skip empty URLs
    if not url:
        return False

    try:
        # Determine folder based on index
        folder_index = idx // images_per_folder
        start_range = folder_index * images_per_folder
        end_range = start_range + images_per_folder - 1
        batch_folder = f"batch_{start_range}_to_{end_range}"

        # Create folder if needed
        folder_path = output_dir / batch_folder
        folder_path.mkdir(exist_ok=True, parents=True)

        # Output file path
        output_path = folder_path / f"{idx}.jpg"

        # Skip if already downloaded
        if output_path.exists():
            return True

        # Download image
        content = download_image(url)
        if content is None:
            return False

        # Process image
        img = Image.open(BytesIO(content))
        if img.mode != "RGB":
            img = img.convert("RGB")
        if resize_size:
            img = img.resize(resize_size, Image.Resampling.LANCZOS)

        # Save image
        img.save(output_path, "JPEG")
        return True

    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return False


def process_batch(batch_data: List[Tuple[int, str]], **kwargs) -> List[bool]:
    """Process a batch of images using threads"""
    try:
        results = []
        with ThreadPoolExecutor(max_workers=kwargs.get("threads", 4)) as executor:
            process_func = partial(
                process_image,
                output_dir=kwargs.get("output_dir"),
                resize_size=kwargs.get("resize_size"),
                images_per_folder=kwargs.get("images_per_folder", 1000),
            )

            futures = [
                executor.submit(process_func, url_data) for url_data in batch_data
            ]

            for future in tqdm(
                futures,
                total=len(futures),
                disable=os.environ.get("DISABLE_TQDM", False),
            ):
                try:
                    results.append(future.result())
                except Exception as e:
                    print(f"Thread error: {str(e)}")
                    results.append(False)

        return results
    except Exception as e:
        print(f"Batch processing error: {traceback.format_exc()}")
        return [False] * len(batch_data)


class ImageDownloader:
    def __init__(
        self,
        output_dir: Union[str, Path],
        num_processes: int = 1,
        threads_per_process: int = 4,
        resize_size: Optional[Tuple[int, int]] = None,
        batch_size: int = 100,
        images_per_folder: int = 1000,
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.num_processes = max(1, min(os.cpu_count() or 1, num_processes))
        self.threads_per_process = threads_per_process
        self.resize_size = resize_size
        self.batch_size = batch_size
        self.images_per_folder = images_per_folder

    def download_images(
        self, data: Union[List[str], List[Tuple[int, str]]]
    ) -> Tuple[int, int]:
        """Download images using multiple processes and threads, organized in batch folders."""
        start_time = time()

        # Transform data format if needed
        if data and not isinstance(data[0], tuple):
            data = [(i, url) for i, url in enumerate(data)]

        total_urls = len(data)
        print(
            f"[green]START[/] {total_urls} images {self.threads_per_process} threads, {self.num_processes} processes"
        )
        print(
            f"[green]ORGANIZATION[/] Images will be stored in folders with {self.images_per_folder} images each"
        )

        # Process in batches
        successful = 0
        for i in range(0, total_urls, self.batch_size):
            batch = data[i : i + self.batch_size]

            # Split batch for multiprocessing
            chunks = []
            chunk_size = math.ceil(len(batch) / self.num_processes)
            for j in range(0, len(batch), chunk_size):
                chunks.append(batch[j : j + chunk_size])

            # Process parameters
            process_kwargs = {
                "output_dir": self.output_dir,
                "threads": self.threads_per_process,
                "resize_size": self.resize_size,
                "images_per_folder": self.images_per_folder,
            }

            # Process URLs
            if self.num_processes > 1 and len(chunks) > 1:
                # Use process pool for parallel processing
                try:
                    with ProcessPoolExecutor(
                        max_workers=self.num_processes
                    ) as executor:
                        results = list(
                            executor.map(
                                partial(process_batch, **process_kwargs), chunks
                            )
                        )
                except Exception as e:
                    print(f"Process pool error: {str(e)}")
                    # Fall back to single process
                    results = [
                        process_batch(chunk, **process_kwargs) for chunk in chunks
                    ]
            else:
                # Single process mode
                results = [process_batch(chunk, **process_kwargs) for chunk in chunks]

            # Count successes
            batch_successful = sum(item for sublist in results for item in sublist)
            successful += batch_successful

            print(f"[green]BATCH COMPLETE[/] {batch_successful}/{len(batch)} images")

        elapsed_time = time() - start_time
        print(
            f"[green]DOWNLOADED[/] {successful}/{total_urls} images in {elapsed_time:.2f} seconds"
        )

        return successful, total_urls


# Example usage
# if __name__ == "__main__":
#     multiprocessing.freeze_support()
#
#     import polars as pl
#     from core_pro.ultilities import make_sync_folder
#
#     path = make_sync_folder("item_match/scs")
#     path_image = path / "img"
#     shp = pl.read_parquet(path / "shp.parquet")
#     sample_urls = shp["image_url_1"].to_list()[:100]
#     # Initialize downloader
#     downloader = ImageDownloader(
#         output_dir=path_image,
#         num_processes=4,
#         threads_per_process=4,
#         resize_size=(224, 224),
#         batch_size=10,
#         images_per_folder=10,
#     )
#
#     # Download images
#     successful, total = downloader.download_images(sample_urls)
