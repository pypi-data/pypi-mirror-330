import os
import time
from timeit import default_timer as timer
from typing import List, Tuple

import requests
import spb_curate
from spb_curate import Image, ImageSourceLocal

from spb_apps.utils.utils import separate_batches

SLEEP_INTERVAL = 5  # Time in seconds to wait between loop iterations.


def curate_prep_images(images_path: list) -> List[spb_curate.Image]:
    """
    Prepares local images for Superb Curate by creating a list of Superb Curate images.

    Args:
        images_path (list): List of paths to images to be uploaded.

    Returns:
        List[spb_curate.Image]: List of prepared images for upload.
    """
    curate_images: List[spb_curate.Image] = []
    for image in images_path:
        curate_images.append(
            spb_curate.Image(
                key=image.split("/")[-1],
                source=spb_curate.ImageSourceLocal(asset=image),
                metadata={},
            )
        )

        return curate_images


def upload_images(self, image_path: list):
    """
    Uploads images in batches to the dataset.

    Args:
        image_path (list): List of image paths to upload.
    """
    separated_images = separate_batches(
        image_batch_size=500, to_batch_list=image_path
    )
    for idx, sep_images in enumerate(separated_images, start=1):
        curate_images = curate_prep_images(images_path=sep_images)
        image_import_job = spb_curate.Image.create_bulk(
            dataset_id=self.dataset["id"], images=curate_images
        )

        while True:
            image_import_job = spb_curate.Job.fetch(id=image_import_job["id"])
            print(f"job progress: {image_import_job['progress']}", end="\r")

            if image_import_job["status"] == "COMPLETE":
                if image_import_job["result"]["fail_detail"]:
                    print(image_import_job["result"]["fail_detail"])
                    print(image_import_job["fail_reason"])
                break

            if image_import_job["status"] == "FAILED":
                if image_import_job["result"]["fail_detail"]:
                    print(
                        "[INFO] Fail detail: ",
                        image_import_job["result"]["fail_detail"],
                    )
                    print(
                        "[INFO] Fail reason: ",
                        image_import_job["fail_reason"],
                    )
                break
            time.sleep(SLEEP_INTERVAL)


def upload_binary_images(self, images: List[Tuple[str, bytes]]) -> List:
    """
    Uploads a list of binary image data to the dataset.

    Args:
        images (list): A list of image data to be uploaded. Each element in the list should be a list containing:
                    - [0] str: The file name of the image (used as the key).
                    - [1] bytes: The binary data of the image.

    Returns:
        List: A list of the results from the image upload job.

    Example:
        images = [
            ["image1.jpg", b'binary_data_of_image1'],
            ["image2.png", b'binary_data_of_image2']
        ]
        upload_result = upload_binary_images(images)
    """
    start_time = timer()

    image_objects = []
    for img_data in images:
        img_object = Image(
            key=img_data[0],
            source=ImageSourceLocal(asset=img_data[1]),
            metadata={
                "misc-key": "new-value",
            },
        )
        image_objects.append(img_object)

    job = self.dataset.add_images(images=image_objects)
    job.wait_until_complete()

    print(f"{len(images)} images uploaded")
    print(f"total time: {timer() - start_time}")


def get_width_height(self, data_key: str) -> Tuple[int, int]:
    """
    Fetches the width and height of an image using its data key.

    Args:
        data_key (str): The unique identifier for the image.

    Returns:
        Tuple[int, int]: A tuple containing the width and height of the image.
    """
    image = self.dataset.fetch_images(key=data_key)[0]
    meta = image["metadata"]
    width, height = meta["_width"], meta["_height"]
    return width, height


def download_image(self, data_key: str, path: str = ""):
    """
    Downloads an image from the dataset using its data key.

    Args:
        data_key (str): The unique identifier for the image.
        path (str): The path where the image will be downloaded.
    """
    image_url = self.dataset.fetch_images(
        key=data_key, include_image_url=True
    )[0]["image_url"]
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        os.makedirs(
            os.path.dirname(os.path.join(path, data_key)),
            exist_ok=True,
        )
        with open(os.path.join(path, data_key), "wb") as f:
            f.write(response.content)
        print(
            f"[INFO] Image downloaded successfully: {os.path.join(path, data_key)}"
        )
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to download image: {e}")


def download_images_by_slice(self, slice_name: str, download_path: str):
    """
    Downloads all images within a specified slice of the dataset.

    This method fetches all image keys within a given slice and iteratively
    downloads each image to the specified download path.

    Args:
        slice_name (str): The name of the slice from which to download images.
        download_path (str): The local file path where the images will be saved.
    """
    slice = self.dataset.fetch_images(slice=slice_name, include_image_url=True)
    for image in slice:
        self.download_image(data_key=image["key"], path=download_path)
