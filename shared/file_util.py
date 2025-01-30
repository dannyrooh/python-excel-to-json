import pandas as pd
import zlib

def get_file_crc32(file):
    """
    Calculate the CRC32 checksum of the uploaded file.
    
    :param file: File object from request.files
    :return: CRC32 checksum as a hexadecimal string
    """
    file_content = file.read()
    crc32_checksum = zlib.crc32(file_content)
    return format(crc32_checksum & 0xFFFFFFFF, '08x')