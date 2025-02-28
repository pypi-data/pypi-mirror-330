from verse.core.exceptions import BadRequestError


def get_client_and_lib(
    url: str | None,
    host: str | None,
    port: int | None,
    username: str | None,
    password: str | None,
    options: dict | None,
    decode_responses: bool = True,
):
    import redis

    lib = redis
    roptions: dict = options if options is not None else {}
    if url is not None:
        client = redis.from_url(
            url, decode_responses=decode_responses, **roptions
        )
    elif host is not None and port is not None:
        client = redis.Redis(
            host=host,
            port=port,
            username=username,
            password=password,
            decode_responses=decode_responses,
            **roptions,
        )
    else:
        raise BadRequestError(
            "Redis initialization needs url or host and port"
        )
    return client, lib


def get_aclient_and_lib(
    url: str | None,
    host: str | None,
    port: int | None,
    username: str | None,
    password: str | None,
    options: dict | None,
    decode_responses: bool = True,
):
    import redis.asyncio as redis

    lib = redis
    roptions: dict = options if options is not None else {}
    if url is not None:
        client = redis.from_url(
            url, decode_responses=decode_responses, **roptions
        )
    elif host is not None and port is not None:
        client = redis.Redis(
            host=host,
            port=port,
            username=username,
            password=password,
            decode_responses=decode_responses,
            **roptions,
        )
    else:
        raise BadRequestError(
            "Redis initialization needs url or host and port"
        )
    return client, lib
