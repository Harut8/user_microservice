
def create_token_for_email_verify(subject_id: str):
    from jose import jwt
    from service.parser import ParseEnv
    from datetime import datetime, timedelta
    to_encode = {"sub": subject_id, "exp": datetime.utcnow() + timedelta(minutes=60)}
    encoded_jwt = jwt.encode(to_encode, ParseEnv.JWT_SECRET_KEY, ParseEnv.ALGORITHM)
    return encoded_jwt


def generate_url_for_email_verify(*, id_: str):
    """ GENERATE URL FOR VERIFYING ACCOUNT"""
    from service.parser import ParseEnv
    import urllib.parse
    url = ParseEnv.API_HOST+ParseEnv.API_PORT+'/api/v1/user/verify-email?'
    params = {'token_verify': id_, 'data': 'JbbfghGVEVGEJKIJCVBEJGHEBEKKEHBHNKVIRH'}
    return url + urllib.parse.urlencode(params)