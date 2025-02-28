def guess_type_by_extension(filename):
    extension = filename.split('.')[-1].lower()

    # Extended mapping of file extensions to MIME types
    mime_mapping = {
        # Document types
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'pdf': 'application/pdf',
        'txt': 'text/plain',
        'doc': 'application/msword',
        'ppt': 'application/vnd.ms-powerpoint',
        'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'xls': 'application/vnd.ms-excel',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'odt': 'application/vnd.oasis.opendocument.text',
        'ods': 'application/vnd.oasis.opendocument.spreadsheet',
        'odp': 'application/vnd.oasis.opendocument.presentation',
        'rtf': 'application/rtf',
        'csv': 'text/csv',
        'html': 'text/html',
        'xml': 'application/xml',
        # Image types
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'bmp': 'image/bmp',
        'svg': 'image/svg+xml',
        'tiff': 'image/tiff',
        'webp': 'image/webp',
        # Video types
        'mp4': 'video/mp4',
        'avi': 'video/x-msvideo',
        'mkv': 'video/x-matroska',
        'mov': 'video/quicktime',
        'wmv': 'video/x-ms-wmv',
        'flv': 'video/x-flv',
        'webm': 'video/webm',
        # Audio types
        'mp3': 'audio/mpeg',
        'wav': 'audio/wav',
        'ogg': 'audio/ogg',
        'flac': 'audio/flac',
        'aac': 'audio/aac',
        'm4a': 'audio/mp4',
        'wma': 'audio/x-ms-wma',
        # Archive types
        'zip': 'application/zip',
        'rar': 'application/x-rar-compressed',
        '7z': 'application/x-7z-compressed',
        'tar': 'application/x-tar',
        'gz': 'application/gzip',
        'bz2': 'application/x-bzip2',
        # Executable and script types
        'exe': 'application/x-msdownload',
        'sh': 'application/x-sh',
        'bat': 'application/x-bat',
        'py': 'text/x-python',
        'jar': 'application/java-archive',
        # Font types
        'woff': 'font/woff',
        'woff2': 'font/woff2',
        'ttf': 'font/ttf',
        'otf': 'font/otf',
        # Other
        'json': 'application/json',
        'md': 'text/markdown',
    }

    # Lookup MIME type based on extension
    mime_type = mime_mapping.get(extension)
    return mime_type
