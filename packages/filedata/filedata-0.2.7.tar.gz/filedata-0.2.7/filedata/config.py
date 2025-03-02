class Config:
    RETRY_API_TIMES = 1

    PADDLE_OCR_HOST = 'paddle-ocr.app.kdsec.org'
    TIKA_HOST = 'tika.app.kdsec.org'
    PDF_CONVERTER_HOST = 'pdf-converter.app.kdsec.org'
    IP_SEARCH_HOST = 'ip-search.app.kdsec.org'


def configure(
        retry_api_times: int = None,
        paddle_ocr_host: str = None,
        tika_host: str = None,
        pdf_converter_host: str = None,
        ip_search_host: str = None,
):
    if retry_api_times is not None:
        Config.RETRY_API_TIMES = retry_api_times
    if paddle_ocr_host is not None:
        Config.PADDLE_OCR_HOST = paddle_ocr_host
    if tika_host is not None:
        Config.TIKA_HOST = tika_host
    if pdf_converter_host is not None:
        Config.PDF_CONVERTER_HOST = pdf_converter_host
    if ip_search_host is not None:
        Config.IP_SEARCH_HOST = ip_search_host
