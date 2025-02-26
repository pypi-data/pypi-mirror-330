from io import BytesIO
from typing import Tuple

import requests
from PIL import Image
from spb_label import sdk as spb_label_sdk
from spb_label.exceptions import APIException, ParameterException

from spb_apps.utils.graphql_api import upload_to_platform
from spb_apps.utils.utils import call_with_retry


def download_image(
    self,
    label: spb_label_sdk.DataHandle = None,
    data_key: str = None,
    path: str = "",
):
    """
    Download an image associated with a label to a specified path.

    Parameters:
    - label (spb_label.DataHandle, optional): The label data handle containing the image to download. If None, the label is retrieved using the data_key.
    - data_key (str, optional): The unique identifier for the image. Used if label is None.
    - path (str): The local file path where the image will be saved. Defaults to "/".
    """
    if label is None:
        label = self.get_label(data_key=data_key)
    label.download_image(download_to=path)


def download_image_by_filter(
    self,
    tags: list = [],
    data_key: str = "",
    status: list = [],
    path: str = None,
):
    """
    Downloads images by applying filters such as tags, data key, and status.

    Parameters:
        tags (list, optional): A list of tags to filter images. Defaults to [].
        data_key (str, optional): A specific data key to filter images. Defaults to "".
        status (list, optional): A list of statuses to filter images. Defaults to [].
        path (str, optional): The local file path to save the downloaded images. Defaults to None.
    """
    from concurrent.futures import ThreadPoolExecutor

    def download(label):
        self.download_image(label=label, path=path)

    count, labels = self.client.get_labels(
        tags=tags, data_key=data_key, status=status
    )
    print(f"Downloading {count} data to {path}")
    if count > 50:
        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(download, labels)
    else:
        for label in labels:
            download(label)


def upload_image(
    self,
    image_path: str,
    dataset_name: str,
    data_key: str = None,
    ignore: bool = False,
):
    """
    Upload an image to a specified dataset. If the 'ignore' flag is set to True, the image will be uploaded without checking for existing entries.
    If 'ignore' is False, it checks if the image already exists using the provided 'data_key' or derives a key from the image path.

    Parameters:
    - image_path (str): The path to the image to be uploaded.
    - dataset_name (str): The name of the dataset to upload the image to.
    - data_key (str, optional): The unique identifier for the image. If not provided, it is derived from the image path.
    - ignore (bool, optional): If set to True, the image will be uploaded without checking for existing entries. Defaults to False.

    Raises:
    - ParameterException: If the upload fails due to incorrect parameters.
    """
    if ignore:
        try:
            self.client.upload_image(
                path=image_path,
                dataset_name=dataset_name,
            )
        except ParameterException as e:
            print(f"[ERROR]: Uploading went wrong: {e}")
    else:
        if data_key is None:
            key = image_path.split("/")[-1]
            count, labels = self.get_labels(data_key=key)
        else:
            count, labels = self.get_labels(data_key=data_key)
            key = data_key

        if count == 0:
            # try:
            call_with_retry(
                fn=self.client.upload_image,
                path=image_path,
                dataset_name=dataset_name,
                key=data_key,
            )
            # except ParameterException as e:
            #     print(f"[ERROR]: Uploading went wrong: {e}")

        else:
            print(
                f"[INFO]: Image already exists, skipping upload for data key {key}"
            )


def upload_binary_image(
    self,
    binary_data: bytes,
    file_type: str,
    data_key: str,
    dataset_name: str,
):
    """
    Upload a binary image to a specified dataset.

    Parameters:
    - binary_data (bytes): The binary data of the image to be uploaded.
    - file_type (str): The file type of the image (e.g., 'jpg', 'png').
    - data_key (str): The unique identifier for the image.
    - dataset_name (str): The name of the dataset to upload the image to.

    Raises:
    - KeyError: If a required key is missing in the parameters.
    - ValueError: If the file size or type is incorrect.
    - Exception: For any other unexpected errors.
    """
    try:
        team_name = self.team_name
        access_key = self.access_key
        project_id = self.project_id
        file_size = len(binary_data)

        params = {}
        params["team_name"] = team_name
        params["access_key"] = access_key
        params["project_id"] = project_id
        params["binary_data"] = binary_data
        params["file_type"] = file_type
        params["file_size"] = file_size
        params["data_key"] = data_key
        params["dataset_name"] = dataset_name

        response = upload_to_platform(params)
        if "success" in response:
            return response
        else:
            return response

    except KeyError as e:
        print(f"Missing key in params: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def upload_images(
    self, image_paths: list, dataset_name: str, ignore: bool = False
):
    """
    Upload multiple images to a specified dataset. This function iterates over a list of image paths and uploads each using the 'upload_image' method.

    Parameters:
    - image_paths (list): A list of paths to the images to be uploaded.
    - dataset_name (str): The name of the dataset to upload the images to.
    - ignore (bool, optional): If set to True, the images will be uploaded without checking for existing entries. Defaults to False.

    Raises:
    - ParameterException: If the upload fails due to incorrect parameters.
    """
    if self.project_type == "video":
        raise Exception("Cannot upload video to an image project")
    for path in image_paths:
        try:
            self.upload_image(
                image_path=path, dataset_name=dataset_name, ignore=ignore
            )
        except ParameterException as e:
            print(f"[ERROR]: Uploading went wrong: {e}")


def get_width_height(
    self, label: spb_label_sdk.DataHandle = None, data_key: str = None
) -> Tuple[int, int]:
    """
    Download an image associated with a label, return its width and height, and delete the image.

    Parameters:
    - label (spb_label.DataHandle, optional): The label data handle containing the image to download. If None, the label is retrieved using the data_key.
    - data_key (str, optional): The unique identifier for the image. Used if label is None.

    Returns:
    Tuple[int, int]: A tuple containing the width and height of the downloaded image.
    """
    if label is None:
        label = self.get_label(data_key=data_key)
    image_url = label.get_image_url()
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    width, height = img.size

    return width, height
