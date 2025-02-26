from spb_label import sdk as spb_label_sdk

from spb_apps.utils.utils import call_with_retry


def make_bbox_annotation(
    self,
    class_name: str,
    annotation: list,
    data_type: str = "image",
):
    """
    Create a bounding box setting for a given class name and annotation coordinates.

    Parameters:
    - class_name (str): The class name associated with the bounding box.
    - annotation (list)
        - image: A list containing the coordinates of the bounding box in the order
          [x, y, width, height].
        - video: A list containing the tracking_id and a list of coordinates for each frame,
          like [tracking_id, [[x, y, width, height, frame_num],...]].

    Returns:
    A tuple containing the class name and a dictionary with the bounding box coordinates.
    """
    if data_type == "image":
        bbox = {
            "class_name": class_name,
            "annotation": {
                "coord": {
                    "x": annotation[0],
                    "y": annotation[1],
                    "width": annotation[2],
                    "height": annotation[3],
                }
            },
        }

    elif data_type == "video":
        if len(annotation) != 2 or not isinstance(annotation[1], list):
            raise ValueError(
                "Annotation for video must be in the format [tracking_id, [[x, y, width, height, frame_num],...]]"
            )

        tracking_id = annotation[0]
        frame_annotations = annotation[1]

        if not all(len(anno) == 5 for anno in frame_annotations):
            raise ValueError(
                "Each annotation must have 5 elements: [x, y, width, height, frame_num]"
            )

        bbox = {
            "class_name": class_name,
            "annotation_type": "box",
            "tracking_id": tracking_id,
            "annotations": [],
        }

        # annotations 리스트에서 각 프레임의 바운딩 박스 정보를 추가
        for anno in sorted(
            frame_annotations, key=lambda x: x[4]
        ):  # 프레임 번호 기준으로 정렬
            bbox["annotations"].append(
                {
                    "coord": {
                        "x": anno[0],
                        "y": anno[1],
                        "width": anno[2],
                        "height": anno[3],
                    },
                    "frame_num": anno[4],
                    "properties": [],
                }
            )

    else:  # data_type == "pointclouds"
        print(
            "The SDK does not yet support making bbox for point clouds data types."
        )
        return

    return bbox


def build_seg_pieces(self, seg: list) -> list:
    """
    Constructs a list of dictionaries representing points from a segmentation list.

    Parameters:
    - seg (list): A list of integers representing x and y coordinates alternately.

    Returns:
    list: A list of dictionaries, each containing an 'x' and 'y' coordinate.
    """
    poly = []
    x, y = 0, 0
    for index, p in enumerate(seg):
        if index % 2:  # odd -> y
            y = p
            poly.append({"x": x, "y": y})
        else:  # even -> x
            x = p
    if poly:
        poly.append({"x": seg[0], "y": seg[1]})
    return poly


def parse_segmentation(self, segmentation: list) -> dict:
    """
    Parses a list of segmentations into a structured dictionary format suitable for annotations.

    Parameters:
    - segmentation (list): A list of lists, each sublist contains integers representing x and y coordinates alternately.

    Returns:
    dict: A dictionary with coordinates of points and a flag indicating multiple segmentations.
    """
    points = []
    for seg in segmentation:
        add_poly = self.build_seg_pieces(seg)
        points.append([add_poly])
    annotation = {
        "coord": {"points": points},
        "multiple": True,
    }
    return annotation


def upload_annotation(
    self,
    label: spb_label_sdk.DataHandle,
    annotations: list,
    overwrite: bool = False,
    data_type: str = "image",
):
    """
    Upload annotations for a given label.

    Parameters:
    - label (DataHandle): The label to which the annotations will be added.
    - annotations (list): A list of annotations to be added to the label.
    - overwrite (bool, optional): A flag indicating whether existing annotations should be overwritten. Defaults to False.
    """
    if data_type == "image":
        if overwrite:
            labels = []
            for anno in annotations:
                try:
                    bbox = self.make_bbox_annotation(
                        class_name=anno[0], annotation=anno[1]
                    )
                except Exception:
                    raise Exception(
                        f"[ERROR]: Error occurred while making bbox, check the annotation format || {anno}"
                    )
                labels.append(bbox)
            if len(labels) == 0:
                raise Exception(f"[ERROR]: No annotations found for the label")
            call_with_retry(fn=label.set_object_labels, labels=labels)
        else:
            for anno in annotations:
                try:
                    bbox = self.make_bbox_annotation(
                        class_name=anno[0], annotation=anno[1]
                    )
                except Exception:
                    raise Exception(
                        f"[ERROR]: Error occurred while making bbox, check the annotation format || {anno}"
                    )
                if "class_name" not in bbox or "annotation" not in bbox:
                    raise Exception(
                        "[ERROR]: No annotations found for the label"
                    )
                call_with_retry(
                    fn=label.add_object_label,
                    class_name=bbox["class_name"],
                    annotation=bbox["annotation"],
                )

    elif data_type == "video":
        overwrite = True  # The current SDK does not support the add_object_label function for video data types.
        labels = []
        for anno in annotations:
            try:
                bbox = self.make_bbox_annotation(
                    class_name=anno[0],
                    annotation=anno[1],
                    data_type="video",
                )  # annotation=anno[1] -> [tracking_id, [[x, y, width, height, frame_num],...]]
            except Exception:
                raise Exception(
                    f"[ERROR]: Error occurred while making bbox, check the annotation format || {anno}"
                )
            labels.append(bbox)
        if len(labels) == 0:
            raise Exception(f"[ERROR]: No annotations found for the label")
        call_with_retry(fn=label.set_object_labels, labels=labels)

    else:  # data_type == "pointclouds":
        raise Exception(
            f"[ERROR]: Apps SDK does not yet support uploading annotations for pointclouds."
        )

    call_with_retry(fn=label.update_info)
