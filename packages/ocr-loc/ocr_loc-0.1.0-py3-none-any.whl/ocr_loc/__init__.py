from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

from ocr_loc.text_local import ocr


def merge_text_blocks(text_list, coordinates_list):
    sorted_text_list = text_list
    sorted_coordinates_list = coordinates_list

    num_blocks = len(sorted_text_list)
    merge = [False] * num_blocks

    results = {}
    for i in range(num_blocks):
        if merge[i]:
            continue

        anchor = i

        group_text = [sorted_text_list[anchor]]
        group_coordinates = [sorted_coordinates_list[anchor]]

        for j in range(i + 1, num_blocks):
            if merge[j]:
                continue

            if (
                abs(sorted_coordinates_list[anchor][0] - sorted_coordinates_list[j][0])
                < 10
                and sorted_coordinates_list[j][1] - sorted_coordinates_list[anchor][3]
                >= -10
                and sorted_coordinates_list[j][1] - sorted_coordinates_list[anchor][3]
                < 30
                and abs(
                    sorted_coordinates_list[anchor][3]
                    - sorted_coordinates_list[anchor][1]
                    - (sorted_coordinates_list[j][3] - sorted_coordinates_list[j][1])
                )
                < 10
            ):
                group_text.append(sorted_text_list[j])
                group_coordinates.append(sorted_coordinates_list[j])
                merge[anchor] = True
                anchor = j
                merge[anchor] = True

        merged_text = "\n".join(group_text)
        min_x1 = min(group_coordinates, key=lambda x: x[0])[0]
        min_y1 = min(group_coordinates, key=lambda x: x[1])[1]
        max_x2 = max(group_coordinates, key=lambda x: x[2])[2]
        max_y2 = max(group_coordinates, key=lambda x: x[3])[3]

        center = ((min_x1 + max_x2) / 2, (min_y1 + max_y2) / 2)

        if merged_text in results:
            results[merged_text].append(center)
        else:
            results[merged_text] = [center]

    return results


class OCR:
    def __init__(
        self,
        # 一个基于 ResNet18 的 OCR 文字检测模型，主要用于从图像中检测文字行的边界框坐标。
        ocr_detection_model="iic/cv_resnet18_ocr-detection-db-line-level_damo",
        # 一个基于 ConvNeXt 架构的 OCR 文字识别模型，专门用于文档场景中的文字识别任务。
        ocr_recognition_model="iic/cv_convnextTiny_ocr-recognition-document_damo",
    ):
        self.ocr_detection = pipeline(
            Tasks.ocr_detection,
            model=ocr_detection_model,
        )  # dbnet (no tensorflow)

        self.ocr_recognition = pipeline(
            Tasks.ocr_recognition,
            model=ocr_recognition_model,
        )

    def ocr(self, image_path: str) -> dict[str, list]:
        text, coordinates = ocr(image_path, self.ocr_detection, self.ocr_recognition)
        return merge_text_blocks(text, coordinates)
