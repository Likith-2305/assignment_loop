from starlette.responses import Response

class MultipartMixedResponse(Response):
    def __init__(self, json_data, file_path, filename):
        boundary = "boundary"
        json_part = (
            f'--{boundary}\r\n'
            f'Content-Disposition: inline\r\n'
            f'Content-Type: application/json\r\n\r\n'
            f'{json_data}\r\n'
        ).encode("utf-8")  
        file_part = (
            f'--{boundary}\r\n'
            f'Content-Disposition: attachment; filename="{filename}"\r\n'
            f'Content-Type: text/csv\r\n\r\n'
        ).encode("utf-8")  
        with open(file_path, "rb") as file:
            file_part += file.read()
        content = b''.join([json_part, file_part, f'\r\n--{boundary}--\r\n'.encode("utf-8")])
        
        super().__init__(content=content, media_type=f"multipart/mixed; boundary={boundary}")