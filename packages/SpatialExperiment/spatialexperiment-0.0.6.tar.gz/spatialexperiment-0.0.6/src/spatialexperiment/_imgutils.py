from typing import Union

import os
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse
from PIL import Image
from biocframe import BiocFrame
from .SpatialImage import construct_spatial_image_class

__author__ = "keviny2"
__copyright__ = "keviny2"
__license__ = "MIT"



def read_image(input_image):
    """Read image from PIL Image, file path, or URL.

    Args:
        input_image: PIL Image, string path to local file, or URL string.

    Returns:
        The loaded image.

    Raises:
        TypeError: If input is not PIL Image, path string, or URL string.
    """
    import requests

    if isinstance(input_image, Image.Image):
        return input_image
    
    if isinstance(input_image, (str, Path)):
        is_url = urlparse(str(input_image)).scheme in ("http", "https", "ftp")
        if is_url:
            response = requests.get(input_image)
            return Image.open(BytesIO(response.content))
        else:
            return Image.open(input_image)
            
    raise TypeError(f"Expected PIL Image, path, or URL. Got {type(input_image)}")


def get_img_data(
    img: Union[str, os.PathLike],
    scale_factor: str,
    sample_id: str,
    image_id: str,
    load: bool = True
) -> BiocFrame:
    """
    Construct an image data dataframe.

    Args:
        img:
            A path or url to the image file.

        scale_factor:
            The scale factor associated with the image.

        sample_id:
            A unique identifier for the sample to which the image belongs.

        image_id:
            A unique identifier for the image itself.

        load:
            A boolean specifying whether the image(s) should be loaded into memory? If False, will store the path/URL instead.
            Defaults to `True`.

    Returns:
        The image data.
    """
    if load:
        img = read_image(img)

    spi = construct_spatial_image_class(img)
    return BiocFrame(
        {
            "sample_id": [sample_id],
            "image_id": [image_id],
            "data": [spi],
            "scale_factor": [scale_factor]
        }
    )


def retrieve_rows_by_id(
    img_data: BiocFrame,
    sample_id: Union[str, bool, None] = None,
    image_id: Union[str, bool, None] = None,
) -> Union[BiocFrame, None]:
    """
    Retrieve rows from `img_data` based on specified `sample_id` and `image_id`.

    Args:
        img_data:
            The data from which to retrieve rows.

        sample_id:
            - `sample_id=True`: Matches all samples.
            - `sample_id=None`: Matches the first sample.
            - `sample_id="<str>"`: Matches a sample by its id.

        image_id:
            - `image_id=True`: Matches all images for the specified sample(s).
            - `image_id=None`: Matches the first image for the sample(s).
            - `image_id="<str>"`: Matches image(s) by its(their) id.

    Returns:
        The filtered `img_data` based on the specified ids, or `None` if `img_data` is empty.
    """

    if img_data is None:
        return None

    if img_data.shape[0] == 0:
        return None

    if sample_id is True:
        if image_id is True:
            return img_data

        elif image_id is None:
            unique_sample_ids = list(set(img_data["sample_id"]))
            sample_id_groups = img_data.split("sample_id")
            subset = None

            for sample_id in unique_sample_ids:
                row = sample_id_groups[sample_id][0, :]
                if subset is None:
                    subset = row
                else:
                    subset = subset.combine_rows(row)
        else:
            subset = img_data[
                [_image_id == image_id for _image_id in img_data["image_id"]], :
            ]

    elif sample_id is None:
        first_sample_id = img_data["sample_id"][0]
        first_sample = img_data[
            [_sample_id == first_sample_id for _sample_id in img_data["sample_id"]], :
        ]

        if image_id is True:
            subset = first_sample

        elif image_id is None:
            subset = first_sample[0, :]
        else:
            subset = first_sample[
                [_image_id == image_id for _image_id in img_data["image_id"]], :
            ]

    else:
        selected_sample = img_data[
            [_sample_id == sample_id for _sample_id in img_data["sample_id"]], :
        ]

        if selected_sample.shape[0] == 0:
            subset = selected_sample
        elif image_id is True:
            subset = selected_sample
        elif image_id is None:
            subset = selected_sample[0, :]
        else:
            subset = selected_sample[
                [_image_id == image_id for _image_id in selected_sample["image_id"]]
            ]

    return subset
