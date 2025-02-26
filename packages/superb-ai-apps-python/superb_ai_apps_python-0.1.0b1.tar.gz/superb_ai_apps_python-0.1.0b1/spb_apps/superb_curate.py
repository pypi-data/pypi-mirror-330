from typing import List, Tuple

import spb_curate

from spb_apps.apps import SuperbApps

from .curate.annotation_operations import (
    curate_prep_annotations,
    curate_upload_annotations,
    make_bbox_annotation,
)
from .curate.image_operations import (
    download_image,
    download_images_by_slice,
    get_width_height,
    upload_binary_images,
    upload_images,
)

SLEEP_INTERVAL = 5  # Time in seconds to wait between loop iterations.


class SuperbCurate(SuperbApps):
    """
    A class to handle dataset curation tasks including image and annotation uploads for Superb AI.

    Attributes:
        team_name (str): Name of the team.
        access_key (str): Access key for authentication.
        dataset_name (str): Name of the dataset.
        is_dev (bool): Flag to set the environment to development mode.
    """

    def __init__(
        self,
        team_name: str,
        access_key: str,
        dataset_name: str = "",
        is_dev: bool = False,
    ):
        """
        Initializes the SuperbCurate class with team, dataset, and slice details.
        Optionally sets the environment to development mode.

        Args:
            team_name (str): Name of the team.
            access_key (str): Access key for authentication.
            dataset_name (str, optional): Name of the dataset.
            is_dev (bool, optional): Flag to set the environment to development mode.
        """
        super().__init__(team_name, access_key)
        self.team_name: str = team_name
        self.access_key: str = access_key
        self.dataset_name: str = dataset_name
        spb_curate.team_name = self.team_name
        spb_curate.access_key = self.access_key
        if is_dev:
            spb_curate.api_base = "https://api.dev.superb-ai.com"

        if dataset_name:
            try:
                self.dataset = spb_curate.fetch_dataset(name=dataset_name)
            except:
                print(
                    f"Dataset does not exist, Creating Dataset {dataset_name}"
                )
                self.dataset = spb_curate.create_dataset(
                    name=dataset_name, description="Demo dataset."
                )

    def get_slice(self, slice_name: str):
        """
        Fetches a slice from the dataset using its name.

        Args:
            slice_name (str): Name of the slice to fetch.

        Returns:
            The fetched slice object.
        """
        if slice_name:
            slice = self.dataset.fetch_slice(name=slice_name)
        return slice

    # Image Operations
    def upload_images(self, image_path: list):
        """
        Uploads images in batches to the dataset.

        Args:
            image_path (list): List of image paths to upload.
        """
        upload_images(self, image_path)

    def upload_binary_images(self, images: list[Tuple[str, bytes]]) -> List:
        """
        Uploads a list of binary image data to the dataset.

        Args:
            images (list): A list of image data to be uploaded. Each element in the list should be a list containing:
                        - [0] str: The file name of the image (used as the key).
                        - [1] bytes: The binary data of the image.

        Returns:
            List: A list of the results from the image upload job.
        """
        upload_binary_images(self, images)

    def get_width_height(self, data_key: str) -> Tuple[int, int]:
        """
        Fetches the width and height of an image using its data key.
        """
        return get_width_height(self, data_key)

    def download_image(self, data_key: str, path: str = ""):
        """
        Downloads an image from the dataset using its data key.
        """
        download_image(self, data_key, path)

    def download_images_by_slice(self, slice_name: str, download_path: str):
        """
        Downloads all images within a specified slice of the dataset.
        """
        download_images_by_slice(self, slice_name, download_path)

    # Annotation Operation
    def curate_prep_annotations(self, annotations: list):
        """
        Prepares annotations for upload to the dataset.
        """
        return curate_prep_annotations(self, annotations)

    def curate_upload_annotations(self, annotations: list):
        """
        Uploads annotations to the dataset.
        """
        curate_upload_annotations(self, annotations)

    def make_bbox_annotation(
        self, data_key: str, class_name: str, annotation: list
    ):
        """
        Creates a bounding box annotation for a given image.
        """
        return make_bbox_annotation(self, data_key, class_name, annotation)
