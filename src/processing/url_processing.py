def extract_uri(url):
    if url is None:
        return None
    removed_http = url.replace("http://","")
    removed_https = removed_http.replace("https://","")
    *_ , uri = removed_https.split("/",maxsplit=1)
    return uri