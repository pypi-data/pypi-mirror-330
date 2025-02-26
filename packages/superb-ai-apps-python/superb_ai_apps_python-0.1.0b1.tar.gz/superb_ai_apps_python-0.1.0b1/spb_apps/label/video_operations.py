import glob
import json
import os
import threading

import requests
import spb_label
from natsort import natsorted


def upload_video(
    self, video_path: str, dataset_name: str, num_threads: int = 3
):
    """
    Uploads video data to a specified dataset. This method handles the upload of multiple video frames concurrently.

    Parameters:
    - video_path (str): The directory path containing video frames.
    - dataset_name (str): The name of the dataset to which the video will be uploaded.
    - num_threads (int, optional): The number of threads to use for concurrent uploads. Defaults to 3.

    Raises:
    - Exception: If the project type does not support video uploads.
    """
    if self.project_type == "image":
        raise Exception("Cannot upload image to a video project")

    file_names = [
        os.path.basename(file_path)
        for file_path in glob.glob(os.path.join(video_path, "*.jpg"))
    ]
    key = os.path.basename(video_path)

    if len(file_names) > 1000:
        print(
            "[INFO] Large video detected, splitting into chunks of 1000 frames"
        )
        self.upload_large_video(
            file_names, video_path, dataset_name, key, num_threads
        )
    else:
        self.upload_small_video(
            file_names, video_path, dataset_name, key, num_threads
        )


def upload_large_video(
    self, file_names, video_path, dataset_name, key, num_threads
):
    chunks = [
        file_names[i : i + 1000] for i in range(0, len(file_names), 1000)
    ]
    for index, chunk in enumerate(chunks):
        folder_key = f"{key}_{index + 1}"
        self.process_video_chunk(
            chunk, video_path, dataset_name, folder_key, num_threads
        )


def upload_small_video(
    self, file_names, video_path, dataset_name, key, num_threads
):
    self.process_video_chunk(
        file_names, video_path, dataset_name, key, num_threads
    )


def process_video_chunk(
    self, file_names, video_path, dataset_name, key, num_threads
):
    asset_video = {
        "dataset": dataset_name,
        "data_key": key,
        "files": {
            "path": video_path,
            "file_names": natsorted(file_names),
        },
    }
    project_id = self.project_id
    command = spb_label.Command(type="create_videodata")
    result = spb_label.run(
        command=command,
        option=asset_video,
        optional={"projectId": project_id},
    )
    file_infos = json.loads(result.file_infos)
    self.upload_files_concurrently(
        file_infos, file_names, num_threads, video_path
    )


def upload_files_concurrently(
    self, file_infos, file_names, num_threads, video_path
):
    print(f"[INFO] Uploading video to dataset")
    threads = []
    for tid in range(num_threads):
        start_index = tid * len(file_infos) // num_threads
        end_index = (tid + 1) * len(file_infos) // num_threads
        thread = threading.Thread(
            target=self.video_upload_worker,
            args=(file_infos[start_index:end_index], tid, video_path),
        )
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


def video_upload_worker(self, file_infos, tid, path):
    """
    Worker function for uploading video files. This function is intended to be run in a separate thread.

    Parameters:
    - file_infos (list): List of file information dictionaries containing presigned URLs and file names.
    - tid (int): Thread identifier.
    - path (str): Base path for the video files.
    """
    for file_info in file_infos:
        file_name = file_info["file_name"]
        file_path = os.path.join(path, file_name)
        with open(file_path, "rb") as file_data:
            response = requests.Session().put(
                file_info["presigned_url"], data=file_data.read()
            )
        if response.status_code != 200:
            with open("error.txt", "a") as error_file:
                error_file.write(f"Upload failed for {file_path}\n")
