import logging
from typing import Dict, List, Optional, Tuple

import phy_credit
from spb_label import sdk as spb_label_sdk
from spb_label.exceptions import NotFoundException

from spb_apps.apps import SuperbApps

from .label.annotation_operations import (
    make_bbox_annotation,
    upload_annotation,
)
from .label.image_operations import (
    download_image,
    download_image_by_filter,
    get_width_height,
    upload_binary_image,
    upload_image,
    upload_images,
)
from .label.project_management import (
    add_object_classes_to_project,
    build_label_interface,
    download_export,
    get_labels,
    update_tags,
)
from .label.video_operations import upload_video

logger = logging.getLogger("superb_label")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

formatter_debug = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
handler_debug = logging.FileHandler("log_event.log")
handler_debug.setLevel(logging.DEBUG)
handler_debug.setFormatter(formatter_debug)

logger.addHandler(handler)
logger.addHandler(handler_debug)


class SuperbLabel(SuperbApps):
    def __init__(
        self,
        team_name: str,
        access_key: str,
        project_id: str = "",
        project_name: str = "",
        data_type: str = "image",
    ):
        """
        Initializes the SuperbLabel class with necessary details for operation.

        Parameters:
        - team_name (str): The name of the team.
        - access_key (str): The access key for authentication.
        - project_id (str, optional): The ID of the project to be set for the client. Defaults to an empty string.
        - project_name (str, optional): The name of the project. Defaults to an empty string.
        """
        self.team_name: str = team_name
        self.access_key: str = access_key
        super().__init__(team_name, access_key)
        try:
            self.client = spb_label_sdk.Client(
                team_name=team_name,
                access_key=access_key,
                project_id=project_id if project_id else None,
                project_name=project_name if project_name else None,
            )
        except NotFoundException:
            print("[INFO]: Project not found, creating a new Image project")
            self.client = spb_label_sdk.Client(
                team_name=team_name,
                access_key=access_key,
            )
            if data_type == "image":
                new_label_interface = (
                    phy_credit.imageV2.LabelInterface.get_default()
                )
            elif data_type == "video":
                new_label_interface = (
                    phy_credit.video.LabelInterface.get_default()
                )
            else:  # data_type == "pointclouds"
                new_label_interface = (
                    phy_credit.pointclouds.LabelInterface.get_default()
                )
            self.client.create_project(
                name=project_name,
                label_interface=new_label_interface.to_dict(),
                description="Created from Superb Apps",
            )
            self.client.set_project(name=project_name)
        self.project = self.client.project
        self.project_id = self.client.project.id
        self.project_type = self.client._project.get_project_type()

    def get_project_list(self, max_attempts=10):
        """
        Retrieves the list of all projects available for the current team.

        Args:
            max_attempts (int): Maximum number of attempts to fetch all projects.

        Returns:
            List[Dict]: A list of dictionaries, each containing project details.
        """
        manager = spb_label_sdk.ProjectManager(self.team_name, self.access_key)
        all_projects = []
        page = 1
        page_size = 10  # Maximum allowed page size
        attempts = 0

        while attempts < max_attempts:
            try:
                projects = manager.get_project_list(
                    page=page, page_size=page_size
                )
                all_projects.extend(projects[1])

                if len(projects[1]) < page_size:
                    break  # We've reached the last page

                page += 1
                attempts = 0  # Reset attempts on successful fetch
            except Exception as e:
                print(f"Error fetching page {page}: {str(e)}")
                attempts += 1
                if attempts >= max_attempts:
                    print(
                        "Max attempts reached. Some projects may be missing."
                    )
                    break

        projects = []
        for project in all_projects:
            hold = {
                "id": project.id,
                "name": project.name,
                "workapp": project.workapp,
                "label_interface": project.label_interface,
                "label_count": project.label_count,
                "progress": project.progress,
            }
            projects.append(hold)
        print(f"Total projects fetched: {len(all_projects)}")
        return projects

    # Image Operations
    def download_image(
        self,
        label: spb_label_sdk.DataHandle = None,
        data_key: str = None,
        path: str = "",
    ):
        """
        Download an image associated with a label to a specified path.
        """
        download_image(self, label, data_key, path)

    def download_image_by_filter(
        self,
        tags: list = [],
        data_key: str = "",
        status: list = [],
        path: str = None,
    ):
        """
        Downloads images by applying filters such as tags, data key, and status.
        """
        download_image_by_filter(self, tags, data_key, status, path)

    def upload_image(
        self,
        image_path: str,
        dataset_name: str,
        data_key: str = None,
        ignore: bool = False,
    ):
        """
        Upload an image to a specified dataset.
        """
        upload_image(self, image_path, dataset_name, data_key, ignore)

    def upload_binary_image(
        self,
        binary_data: bytes,
        file_type: str,
        data_key: str,
        dataset_name: str,
    ):
        """
        Upload a binary image to a specified dataset.
        """
        upload_binary_image(
            self, binary_data, file_type, data_key, dataset_name
        )

    def upload_images(
        self, image_paths: list, dataset_name: str, ignore: bool = False
    ):
        """
        Upload multiple images to a specified dataset.
        """
        upload_images(self, image_paths, dataset_name, ignore)

    # Video Operations
    def upload_video(
        self, video_path: str, dataset_name: str, num_threads: int = 3
    ):
        """
        Uploads video data to a specified dataset.
        """
        upload_video(self, video_path, dataset_name, num_threads)

    def get_width_height(
        self, label: spb_label_sdk.DataHandle = None, data_key: str = None
    ) -> Tuple[int, int]:
        """
        Download an image associated with a label, return its width and height, and delete the image.
        """
        return get_width_height(self, label, data_key)

    # Project Management
    def build_label_interface(
        self,
        new_class_list: List[str],
        existing_label_interface: Optional[dict] = None,
    ):
        """
        Builds a label interface for a project.
        """
        build_label_interface(self, new_class_list, existing_label_interface)

    def add_object_classes_to_project(
        self,
        class_name: str,
        class_type: str,
        data_type: str = "image",
        properties: list = [],
    ):
        """
        Adds a specific type of object class to the label interface of the project based on the specified class type.
        """
        add_object_classes_to_project(
            self, class_name, class_type, data_type, properties
        )

    def update_tags(self, data_key: str, tags: list):
        """
        Updates the tags for a specific data key.
        """
        update_tags(self, data_key, tags)

    def get_labels(
        self,
        data_key: str = None,
        tags: list = None,
        assignees: list = None,
        status: list = None,
        all: bool = False,
    ) -> Tuple[int, List]:
        """
        Retrieve labels based on provided filters or all labels if specified.
        """
        get_labels(self, data_key, tags, assignees, status, all)

    def download_export(self, input_path: str, export_id: str):
        """
        Downloads an export of the project.
        """
        download_export(self, input_path, export_id)

    def change_project(self, project_name: str):
        """
        Changes the project context for the label client.

        Parameters:
            project_name (str): The name of the project to switch to.
        """
        self.client.set_project(name=project_name)

    def get_label_interface(self) -> Dict:
        """
        Retrieves the label interface configuration for the 'label' platform.

        Returns:
            Dict: The label interface configuration.
        """
        lb_interface = self.client.project.label_interface
        return lb_interface

    # Annotation Operations
    def upload_annotation(
        self,
        label: spb_label_sdk.DataHandle,
        annotations: list,
        overwrite: bool = False,
        data_type: str = "image",
    ):
        """
        Upload annotations to a specified label.
        """
        upload_annotation(self, label, annotations, overwrite, data_type)

    def make_bbox_annotation(
        self,
        data_key: str,
        class_name: str,
        annotation: list,
    ):
        """
        Make a bounding box annotation.
        """
        bbox = make_bbox_annotation(self, data_key, class_name, annotation)
        return bbox
