import time
from typing import List

import spb_curate

from spb_apps.utils.utils import separate_batches

SLEEP_INTERVAL = 5  # Time in seconds to wait between loop iterations.


def curate_prep_annotations(
    self, annotation: list
) -> List[spb_curate.Annotation]:
    """
    Prepares annotations for upload by creating a list of spb_curate.Annotation objects.

    Args:
        annotation (list): List of dictionaries containing annotation details.

    Returns:
        List[spb_curate.Annotation]: List of prepared annotations for upload.
    """
    curate_annotations: List[spb_curate.Annotation] = []
    for anno in annotation:
        meta = anno.get("metadata", {"iscrowd": 0})
        curate_annotations.append(
            spb_curate.Annotation(
                image_key=anno["data_key"],
                annotation_class=anno["class_name"],
                annotation_type=anno["annotation_type"],
                annotation_value=anno["annotation"],
                metadata=meta,
            )
        )

    return curate_annotations


def curate_upload_annotations(self, annotation_list: list):
    """
    Uploads annotations in batches to the dataset.

    Args:
        annotation_list (list): List of annotations to upload.
    """
    separated_annotations = separate_batches(
        image_batch_size=500, to_batch_list=annotation_list
    )
    for idx, sep_annotations in enumerate(separated_annotations, start=1):
        annotation_import_job = spb_curate.Annotation.create_bulk(
            dataset_id=self.dataset["id"], annotations=sep_annotations
        )

        while True:
            annotation_import_job = spb_curate.Job.fetch(
                id=annotation_import_job["id"]
            )
            print(
                f"[INFO] {(idx-1) * 500 + annotation_import_job['progress']} / {len(annotation_list)} annotations updated"
            )

            if annotation_import_job["status"] == "COMPLETE":
                if annotation_import_job["result"]["fail_detail"]:
                    print(
                        "[INFO] Fail detail: ",
                        annotation_import_job["result"]["fail_detail"],
                    )
                    print(
                        "[INFO] Fail reason: ",
                        annotation_import_job["fail_reason"],
                    )
                break

            if annotation_import_job["status"] == "FAILED":
                if annotation_import_job["result"]["fail_detail"]:
                    print(
                        "[INFO] Fail detail: ",
                        annotation_import_job["result"]["fail_detail"],
                    )
                    print(
                        "[INFO] Fail reason: ",
                        annotation_import_job["fail_reason"],
                    )
                break
            time.sleep(SLEEP_INTERVAL)


def make_bbox_annotation(
    self, data_key: str, class_name: str, annotation: list
) -> spb_curate.Annotation:
    """
    Creates a bounding box annotation for a given image.

    Args:
        data_key (str): The unique identifier for the image.
        class_name (str): The class name associated with the bounding box.
        annotation (list): A list containing the x, y coordinates, width, and height of the bounding box.

    Returns:
        spb_curate.Annotation: An Annotation object representing the bounding box.
    """
    bounding_box = spb_curate.BoundingBox(
        raw_data={
            "x": annotation[0],
            "y": annotation[1],
            "width": annotation[2],
            "height": annotation[3],
        }
    )
    bbox_annotation = spb_curate.Annotation(
        image_key=data_key,
        annotation_class=class_name,
        annotation_type="box",
        annotation_value=bounding_box,
        metadata={},
    )

    return bbox_annotation
