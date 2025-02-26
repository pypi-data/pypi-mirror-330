class StatusKeys:
    CLEAN_UP = "digitizer_clean_up"
    ELASTICSEARCH_UPLOAD = "digitizer_elasticsearch_upload"
    UPLOAD = "s3_upload"
    DOWNLOAD = "digitizer_s3_download"
    OCR = "digitizer_ocr"


class Queue:
    IO = "io"
    DOWNLOAD = "download"
    FINISH = "finish"
    OCR = "ocr"
