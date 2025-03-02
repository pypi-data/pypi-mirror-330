import base64
import io
from typing import Optional, List, Tuple, Union

import requests
from PIL import Image
from pydantic.main import BaseModel

from filedata.config import Config
from filedata.retry import retry_api
from filedata.utils import edit_distance

RegionBox = Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]

_session = requests.Session()


class OCRRegion(BaseModel):
    confidence: float = None
    text: str
    text_region: RegionBox


class OCRResult(BaseModel):
    angle: int
    img: bytes = None
    ocr_regions: List[OCRRegion]


def _bytes_to_img(img: bytes) -> Image.Image:
    img: Image.Image = Image.open(io.BytesIO(img))
    img = img.convert('RGB')
    return img


def _img_to_bytes(img: Image.Image) -> bytes:
    img_bytes_io = io.BytesIO()
    img.save(img_bytes_io, format='jpeg')
    return img_bytes_io.getvalue()


@retry_api
def ocr(img: Union[bytes, Image.Image], timeout: int = 20) -> List[OCRRegion]:
    if isinstance(img, Image.Image):
        img = _img_to_bytes(img)

    image = base64.b64encode(img).decode('utf8')
    data = {"images": [image]}
    resp = _session.post(
        url=f'http://{Config.PADDLE_OCR_HOST}/predict/ocr_system',
        json=data,
        timeout=timeout,
    )
    resp.raise_for_status()
    res = resp.json()['results'][0]
    return [OCRRegion(**i) for i in res]


def ocr_with_angle_correction(img: Union[bytes, Image.Image], timeout: int = 20) -> OCRResult:
    if isinstance(img, bytes):
        img = _bytes_to_img(img)

    regions = ocr(img, timeout=timeout)
    angle = detect_orientation(img, regions, timeout=timeout)
    if angle != 0:
        w = img.width
        h = img.height
        for r in regions:
            r.text_region = rotate_region_box(angle, r.text_region, w, h)
        img = img.rotate(angle, expand=True)

    # 对区域进行排序
    regions.sort(key=lambda k: (k.text_region[0][1], k.text_region[0][0]))

    return OCRResult(
        angle=angle,
        img=_img_to_bytes(img),
        ocr_regions=regions,
    )


def extract_content_by_ocr(
        img: Union[bytes, Image.Image],
        timeout: int = 20,
) -> str:
    """
    基于OCR获取文本内容
    :param img: 原始图片
    :param timeout: 超时时间
    :return: 文本内容
    """

    result = ocr_with_angle_correction(img, timeout=timeout)
    return ocr_result_to_text(result.ocr_regions)


def ocr_result_to_text(ocr_result: List[OCRRegion]) -> str:
    """
    将OCR结果输出为文本，默认已经经过方向矫正
    :param ocr_result:
    :return:
    """

    result = []
    for i, r in enumerate(ocr_result):
        if i > 0:
            _r = ocr_result[i - 1]
            if r.text_region[0][1] > _r.text_region[3][1] or r.text_region[1][0] < _r.text_region[0][0]:
                # 换行
                _d = r.text_region[0][1] - _r.text_region[3][1]
                if _d > 2 * (r.text_region[3][1] - r.text_region[0][1]) \
                        or _d > 2 * (_r.text_region[3][1] - _r.text_region[0][1]):
                    result.append('\n\n')
                else:
                    result.append('\n')
            else:
                # 同一行
                result.append('  ')
        result.append(r.text)
    return ''.join(result)


def select_longest_region(regions: List[OCRRegion]) -> Optional[OCRRegion]:
    """
    选择字数最多的区域
    """
    m = 0
    region = None
    for r in regions:
        _m = len(r.text)
        if _m > m:
            m = _m
            region = r
    return region


def crop_region(
        img: Union[bytes, Image.Image],
        box: RegionBox,
        margin: int = 0,
        angle: int = 0,
) -> bytes:
    if isinstance(img, bytes):
        img = _bytes_to_img(img)

    x1 = min(box[0][0], box[3][0])
    x2 = max(box[1][0], box[2][0])
    y1 = min(box[0][1], box[1][1])
    y2 = max(box[2][1], box[3][1])

    _crop = img.crop((
        max(x1 - margin, 0),
        max(y1 - margin, 0),
        min(x2 + margin, img.width),
        min(y2 + margin, img.height),
    ))

    if angle != 0:
        _crop = _crop.rotate(angle, expand=True)

    img_bytes_io = io.BytesIO()
    _crop.save(img_bytes_io, format='jpeg')
    return img_bytes_io.getvalue()


def detect_orientation(
        img: Union[bytes, Image.Image],
        ocr_result: List[OCRRegion],
        timeout: int = 20,
) -> int:
    """
    根据OCR结果判断图片方向

    :param img: 原始图片
    :param ocr_result: OCR结果
    :param timeout: 超时时间
    :return: 0, 90, 180, 270, 表示图片被顺时针旋转了多少度
    """

    if isinstance(img, bytes):
        img = _bytes_to_img(img)

    region = select_longest_region(ocr_result)
    if region is None or len(region.text) < 5:
        # 小于5个字符不做方向矫正
        return 0

    t = region.text_region
    if t[1][0] - t[0][0] > t[3][1] - t[0][1]:
        angle = 0
    else:
        angle = 90

    x1 = min(t[0][0], t[3][0])
    x2 = max(t[1][0], t[2][0])
    y1 = min(t[0][1], t[1][1])
    y2 = max(t[2][1], t[3][1])
    rw = (x2 - x1) // 2
    rh = (y2 - y1) // 2

    if angle == 0:
        r = (
            (x1, y1),
            (x1 + rw, y1),
            (x1 + rw, y2),
            (x1, y2),
        )
    else:
        r = (
            (x1, y1),
            (x2, y1),
            (x2, y1 + rh),
            (x1, y1 + rh),
        )
    crop_bytes = crop_region(img, r, margin=20, angle=angle)

    crop_result = ocr(crop_bytes, timeout=timeout)
    crop_text = ''.join([i.text for i in crop_result])

    mid = len(region.text) // 2
    if edit_distance(crop_text, region.text[:mid]) > edit_distance(crop_text, region.text[mid:]):
        angle += 180

    return angle


def rotate_region_box(angle: int, box: RegionBox, width: int, height: int) -> RegionBox:
    """
    逆时针旋转
    """
    if angle not in (0, 90, 180, 270):
        raise ValueError('angle must be one of 0, 90, 180 and 270')
    _times = angle // 90

    for _ in range(_times):
        box = (
            [box[1][1], width - box[1][0]],
            [box[2][1], width - box[2][0]],
            [box[3][1], width - box[3][0]],
            [box[0][1], width - box[0][0]],
        )
        width, height = height, width
    return box


def save_to_jpeg(img: Union[bytes, Image.Image]) -> bytes:
    """
    图片转为jpeg，具有去除EXIF方向信息的功能
    """
    if isinstance(img, bytes):
        img = _bytes_to_img(img)
    return _img_to_bytes(img)
