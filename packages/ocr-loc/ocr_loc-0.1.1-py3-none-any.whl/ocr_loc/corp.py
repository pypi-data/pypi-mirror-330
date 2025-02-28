import math

import cv2
import numpy as np


def crop_image(img, position):
    def distance(x1, y1, x2, y2):
        return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))

    position = position.tolist()
    for i in range(4):
        for j in range(i + 1, 4):
            if position[i][0] > position[j][0]:
                tmp = position[j]
                position[j] = position[i]
                position[i] = tmp
    if position[0][1] > position[1][1]:
        tmp = position[0]
        position[0] = position[1]
        position[1] = tmp

    if position[2][1] > position[3][1]:
        tmp = position[2]
        position[2] = position[3]
        position[3] = tmp

    x1, y1 = position[0][0], position[0][1]
    x2, y2 = position[2][0], position[2][1]
    x3, y3 = position[3][0], position[3][1]
    x4, y4 = position[1][0], position[1][1]

    corners = np.zeros((4, 2), np.float32)
    corners[0] = [x1, y1]
    corners[1] = [x2, y2]
    corners[2] = [x4, y4]
    corners[3] = [x3, y3]

    img_width = distance((x1 + x4) / 2, (y1 + y4) / 2, (x2 + x3) / 2, (y2 + y3) / 2)
    img_height = distance((x1 + x2) / 2, (y1 + y2) / 2, (x4 + x3) / 2, (y4 + y3) / 2)

    corners_trans = np.zeros((4, 2), np.float32)
    corners_trans[0] = [0, 0]
    corners_trans[1] = [img_width - 1, 0]
    corners_trans[2] = [0, img_height - 1]
    corners_trans[3] = [img_width - 1, img_height - 1]

    transform = cv2.getPerspectiveTransform(corners, corners_trans)
    dst = cv2.warpPerspective(img, transform, (int(img_width), int(img_height)))
    return dst


# def calculate_size(box):
#     return (box[2] - box[0]) * (box[3] - box[1])


# def calculate_iou(box1, box2):
#     xA = max(box1[0], box2[0])
#     yA = max(box1[1], box2[1])
#     xB = min(box1[2], box2[2])
#     yB = min(box1[3], box2[3])
#
#     interArea = max(0, xB - xA) * max(0, yB - yA)
#     box1Area = (box1[2] - box1[0]) * (box1[3] - box1[1])
#     box2Area = (box2[2] - box2[0]) * (box2[3] - box2[1])
#     unionArea = box1Area + box2Area - interArea
#     iou = interArea / unionArea
#
#     return iou


# def crop(image, box, i, text_data=None):
#     image = Image.open(image)
#
#     if text_data:
#         draw = ImageDraw.Draw(image)
#         draw.rectangle(
#             ((text_data[0], text_data[1]), (text_data[2], text_data[3])),
#             outline="red",
#             width=5,
#         )
#
#     cropped_image = image.crop(box)
#     cropped_image.save(f"./temp/{i}.jpg")


# def in_box(box, target):
#     if (
#         (box[0] > target[0])
#         and (box[1] > target[1])
#         and (box[2] < target[2])
#         and (box[3] < target[3])
#     ):
#         return True
#     else:
#         return False
