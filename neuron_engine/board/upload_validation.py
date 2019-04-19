import os
import magic


def validate_uploaded_file(filename):

    result = None

    m = magic.open(magic.MAGIC_MIME)
    m.load()

    mimetype = m.file(filename)
    file_type = str((mimetype.split('/')[:1])[0])

    if file_type == 'image':
        result = mimetype
    else:
        print('files with mimetype [%s] are not supported' % (mimetype))
        os.remove(filename)

    return result
