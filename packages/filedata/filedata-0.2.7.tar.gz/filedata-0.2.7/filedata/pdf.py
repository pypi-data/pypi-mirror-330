import io
from typing import List

import fitz
from PIL import Image
from fitz import Pixmap


def pdf_to_image(
        source: bytes,
        format: str = 'jpeg',
        dpi: int = 220,
        limit: int = None,
) -> List[bytes]:
    result = []
    pdf = fitz.Document(stream=io.BytesIO(source), filetype='pdf')
    for i, page in enumerate(pdf):
        # 将每一页pdf读取为图片
        img: Pixmap = page.get_pixmap(dpi=dpi)
        img_bytes = img.tobytes()
        if format == 'png':
            result.append(img_bytes)
        else:
            t = Image.open(io.BytesIO(img_bytes))
            o = io.BytesIO()
            t.save(o, format=format)
            result.append(o.getvalue())
        if limit is not None and len(result) >= limit:
            break
    return result
