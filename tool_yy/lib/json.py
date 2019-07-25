import codecs
from itsdangerous import json as _json


def loads(s, **kwargs):
    """Deserialize an object from a JSON-formatted string ``s``. If
    there is an app context pushed, use the current app's configured
    decoder (:attr:`~flask.Flask.json_decoder`), or fall back to the
    default :class:`JSONDecoder`.

    Takes the same arguments as the built-in :func:`json.loads`, and
    does some extra configuration based on the application. If the
    simplejson package is installed, it is preferred.

    :param s: JSON string to deserialize.
    :param app: App instance to use to configure the JSON decoder.
        Uses ``current_app`` if not given, and falls back to the default
        encoder when not in an app context.
    :param kwargs: Extra arguments passed to :func:`json.dumps`.

    .. versionchanged:: 1.0.3

        ``app`` can be passed directly, rather than requiring an app
        context for configuration.
    """
    if isinstance(s, bytes):
        encoding = kwargs.pop('encoding', None)
        if encoding is None:
            encoding = detect_encoding(s)
        s = s.decode(encoding)
    return _json.loads(s, **kwargs)


def detect_encoding(data):
    """Detect which UTF codec was used to encode the given bytes.

    The latest JSON standard (:rfc:`8259`) suggests that only UTF-8 is
    accepted. Older documents allowed 8, 16, or 32. 16 and 32 can be big
    or little endian. Some editors or libraries may prepend a BOM.

    :param data: Bytes in unknown UTF encoding.
    :return: UTF encoding name
    """
    head = data[:4]

    if head[:3] == codecs.BOM_UTF8:
        return 'utf-8-sig'

    if b'\x00' not in head:
        return 'utf-8'

    if head in (codecs.BOM_UTF32_BE, codecs.BOM_UTF32_LE):
        return 'utf-32'

    if head[:2] in (codecs.BOM_UTF16_BE, codecs.BOM_UTF16_LE):
        return 'utf-16'

    if len(head) == 4:
        if head[:3] == b'\x00\x00\x00':
            return 'utf-32-be'

        if head[::2] == b'\x00\x00':
            return 'utf-16-be'

        if head[1:] == b'\x00\x00\x00':
            return 'utf-32-le'

        if head[1::2] == b'\x00\x00':
            return 'utf-16-le'

    if len(head) == 2:
        return 'utf-16-be' if head.startswith(b'\x00') else 'utf-16-le'

    return 'utf-8'
