from typing import Optional

import cv2


def generate_thumbnail(vedio_link: str) -> Optional[bytes]:
    cam = cv2.VideoCapture(vedio_link)

    ret, frame = cam.read()
    if ret:
        b = cv2.imencode('.jpg', frame)[1].tobytes()
        return b
