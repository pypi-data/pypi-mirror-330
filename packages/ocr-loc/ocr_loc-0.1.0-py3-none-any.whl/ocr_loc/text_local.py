import cv2
import numpy as np

from ocr_loc.corp import crop_image


def order_point(coor):
    arr = np.array(coor).reshape([4, 2])
    sum_ = np.sum(arr, 0)
    centroid = sum_ / arr.shape[0]
    theta = np.arctan2(arr[:, 1] - centroid[1], arr[:, 0] - centroid[0])
    sort_points = arr[np.argsort(theta)]
    sort_points = sort_points.reshape([4, -1])
    if sort_points[0][0] > centroid[0]:
        sort_points = np.concatenate([sort_points[3:], sort_points[:3]])
    sort_points = sort_points.reshape([4, 2]).astype("float32")
    return sort_points


def ocr(image_path, ocr_detection, ocr_recognition):
    text_data = []
    coordinate = []

    image_full = cv2.imread(image_path)
    det_result = ocr_detection(image_full)
    det_result = det_result["polygons"]
    for i in range(det_result.shape[0]):
        pts = order_point(det_result[i])
        image_crop = crop_image(image_full, pts)

        try:
            result = ocr_recognition(image_crop)["text"][0]
        except Exception:
            continue

        box = [int(e) for e in list(pts.reshape(-1))]
        box = [box[0], box[1], box[4], box[5]]

        text_data.append(result)
        coordinate.append(box)

    else:
        return text_data, coordinate
