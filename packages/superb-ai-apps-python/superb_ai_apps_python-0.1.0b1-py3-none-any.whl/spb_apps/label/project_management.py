from pathlib import Path
from typing import List, Optional, Tuple
from uuid import uuid4

import phy_credit
import requests
from spb_label.utils import SearchFilter

from spb_apps.utils.utils import call_with_retry


def build_label_interface(
    new_class_list: List[str],
    existing_label_interface: Optional[dict] = None,
):
    if existing_label_interface:
        label_interface = phy_credit.imageV2.LabelInterface.from_dict(
            existing_label_interface
        )
        object_detection = phy_credit.imageV2.ObjectDetectionDef.from_dict(
            existing_label_interface.get("object_detection")
        )
    else:
        # get default label_interface and object_detection (json)
        label_interface = phy_credit.imageV2.LabelInterface.get_default()
        object_detection = phy_credit.imageV2.ObjectDetectionDef.get_default()

    hold = label_interface.to_dict()
    if len(hold["object_detection"]["object_classes"]) == 0:
        existing_classes = []
    else:
        existing_classes = [
            obj["name"] for obj in hold["object_detection"]["object_classes"]
        ]

    for class_name in new_class_list:
        if class_name not in existing_classes:
            bbox_suite_class_id = str(uuid4())
            bbox_suite_class_name = class_name[0]
            object_detection.add_box(
                name=bbox_suite_class_name, id=bbox_suite_class_id
            )

    label_interface.set_object_detection(object_detection=object_detection)

    return label_interface


def add_object_classes_to_project(
    self,
    class_name: str,
    class_type: str,
    data_type: str = "image",
    properties: list = [],
):
    """
    Adds a specific type of object class to the label interface of the project based on the specified class type.

    Parameters:
    - class_name (str): The name of the class to be added to the label interface.
    - class_type (str): The type of class to be added. Supported types include 'bbox' (bounding box), 'polygon', 'polyline', 'rbox' (rotated bounding box), and '2dcuboid'.

    Returns:
    A tuple containing the updated label interface.
    """
    existing_label_interface = self.client.project.label_interface
    if data_type == "image":
        if existing_label_interface:
            label_interface = phy_credit.imageV2.LabelInterface.from_dict(
                existing_label_interface
            )
            object_detection = phy_credit.imageV2.ObjectDetectionDef.from_dict(
                existing_label_interface.get("object_detection")
            )
        else:
            label_interface = phy_credit.imageV2.LabelInterface.get_default()
            object_detection = (
                phy_credit.imageV2.ObjectDetectionDef.get_default()
            )
    elif data_type == "video":
        if existing_label_interface:
            label_interface = phy_credit.video.LabelInterface.from_dict(
                existing_label_interface
            )
            object_tracking = phy_credit.video.ObjectTrackingDef.from_dict(
                existing_label_interface.get("object_tracking")
            )
        else:
            label_interface = phy_credit.video.LabelInterface.get_default()
            object_tracking = phy_credit.video.ObjectTrackingDef.get_default()
    else:  # data_type == "pointclouds"
        if existing_label_interface:
            label_interface = phy_credit.pointclouds.LabelInterface.from_dict(
                existing_label_interface
            )
            object_tracking = (
                phy_credit.pointclouds.ObjectTrackingDef.from_dict(
                    existing_label_interface.get("object_tracking")
                )
            )
        else:
            label_interface = (
                phy_credit.pointclouds.LabelInterface.get_default()
            )
            object_tracking = (
                phy_credit.pointclouds.ObjectTrackingDef.get_default()
            )

    if class_type == "bbox":
        bbox_suite_class_id = str(uuid4())
        bbox_suite_class_name = class_name

        if data_type == "image":
            object_detection.add_box(
                name=bbox_suite_class_name,
                id=bbox_suite_class_id,
                properties=properties,
            )
        else:
            object_tracking.add_box(
                name=bbox_suite_class_name,
                id=bbox_suite_class_id,
                properties=properties,
            )

    if class_type == "polygon":
        seg_suite_class_id = str(uuid4())
        seg_suite_class_name = class_name

        object_detection.add_polygon(
            name=seg_suite_class_name,
            id=seg_suite_class_id,
            properties=properties,
        )

    if class_type == "polyline":
        seg_suite_class_id = str(uuid4())
        seg_suite_class_name = class_name

        if data_type == "image":
            object_detection.add_polyline(
                name=seg_suite_class_name,
                id=seg_suite_class_id,
                properties=properties,
            )
        else:
            object_tracking.add_polyline(
                name=seg_suite_class_name,
                id=seg_suite_class_id,
                properties=properties,
            )

    if class_type == "rbox":
        seg_suite_class_id = str(uuid4())
        seg_suite_class_name = class_name

        if data_type == "image":
            object_detection.add_rbox(
                name=seg_suite_class_name,
                id=seg_suite_class_id,
                properties=properties,
            )
        else:
            object_tracking.add_rbox(
                name=seg_suite_class_name,
                id=seg_suite_class_id,
                properties=properties,
            )

    if class_type == "2dcuboid":
        seg_suite_class_id = str(uuid4())
        seg_suite_class_name = class_name

        if data_type == "image":
            object_detection.add_2dcuboid(
                name=seg_suite_class_name,
                id=seg_suite_class_id,
                properties=properties,
            )
        else:
            object_tracking.add_2dcuboid(
                name=seg_suite_class_name,
                id=seg_suite_class_id,
                properties=properties,
            )

    if data_type == "image":
        label_interface.set_object_detection(object_detection=object_detection)
    else:
        label_interface.set_object_tracking(object_tracking=object_tracking)

    call_with_retry(
        fn=self.client.update_project,
        id=self.client.project.id,
        label_interface=label_interface.to_dict(),
    )
    return label_interface


def update_tags(self, data_key: str, tags: list):
    filter = SearchFilter(project=self.project)
    try:
        filter.data_key_matches = data_key
        data_handler = self.client.get_labels(filter=filter, page_size=1)[1][0]
        data_handler.update_tags(tags=tags)
        data_handler.update_info()
    except Exception as e:
        print(f"Failed update tags {data_key}: {e}")


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

    Parameters:
    - data_key (str, optional): Filter for a specific data key. Defaults to an empty string.
    - tags (list, optional): Filter for specific tags. Defaults to an empty list.
    - assignees (list, optional): Filter for specific assignees. Defaults to an empty list.
    - status (list, optional): Filter for specific status. Defaults to an empty list.
    - all (bool, optional): If True, ignores other filters and retrieves all labels. Defaults to False.

    Returns:
    Tuple[int, List]: A tuple containing the count of labels and a list of labels.
    """
    count, labels = 0, []
    next_cursor = None

    if all:
        # Retrieve all labels without filters
        while True:
            count, new_labels, next_cursor = call_with_retry(
                fn=self.client.get_labels, cursor=next_cursor
            )
            labels.extend(new_labels)

            if next_cursor is None:
                break
    else:
        # Retrieve labels with filters
        filter = SearchFilter(project=self.project)
        if data_key:
            filter.data_key_matches = data_key
        if tags:
            filter.tag_name_all = tags
        if assignees:
            filter.assignee_is_any_one_of = assignees
        if status:
            filter.status_is_any_one_of = status

        while True:
            count, new_labels, next_cursor = call_with_retry(
                fn=self.client.get_labels,
                filter=filter,
                cursor=next_cursor,
            )
            labels.extend(new_labels)

            if next_cursor is None:
                break

    if count == 0:
        return count, None

    return count, labels


def download_export(
    self,
    input_path: str,
    export_id: str,
):
    """
    Download an export from the server to a local path.

    Parameters:
    - input_path (str): The local file path where the export will be saved.
    - export_id (str): The ID of the export to download.
    """
    print("[INFO] Checking for the export to be downloaded...")
    download_url = self.client.get_export(id=export_id).download_url
    r = requests.get(download_url)
    if r.status_code == 200:
        print("Saving export to local path")
        Path(input_path).parents[0].mkdir(parents=True, exist_ok=True)
        with open(input_path, "wb") as f:
            f.write(r.content)
    else:
        print(f"Failed to download the file. Status code: {r.status_code}")
