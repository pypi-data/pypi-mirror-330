from larigira.fsutils import download_http


def generate(spec):
    """
    resolves audiospec-static

    Recognized argument is  "paths" (list of static paths)
    """
    if "urls" not in spec:
        raise ValueError("Malformed audiospec: missing 'urls'")

    for url in spec["urls"]:
        ret = download_http(url, copy=True, prefix="http")
        if ret is None:
            continue
        yield ret


generate.description = "Fetch audio from an URL"
