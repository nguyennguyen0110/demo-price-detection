class Const:
    # REST request content_type & response mimetype, content_type, parameters
    FORM = 'multipart/form-data'
    NOT_FORM = 'Content type must be multipart/form-data'
    RES_PARAM = {
        'status': 200, 'mimetype': 'application/json',
        'content_type': 'application/json'
    }
