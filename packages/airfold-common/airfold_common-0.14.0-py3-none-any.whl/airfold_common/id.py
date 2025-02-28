import re

from airfold_common.utils import uuid

OBJ_RESOLVABLE_ID_RE = re.compile(r"^(af[0-9a-f]{32})\.(.+)$")


def resolve_id(target_id: str) -> str:
    if is_resolvable_id(target_id):
        _, parts = parse_resolvable_id(target_id)
        if len(parts) == 1:
            return parts[0]
        quoted_parts = [f'"{p}"' for p in parts]
        return ".".join(quoted_parts)
    else:
        return target_id


def resolvable_id(*args) -> str:
    return f'{uuid()}.{".".join(args)}'


def is_resolvable_id(obj_id: str) -> bool:
    if obj_id:
        if OBJ_RESOLVABLE_ID_RE.match(obj_id):
            return True
    return False


def parse_resolvable_id(obj_id: str) -> tuple[str, list[str]]:
    m = OBJ_RESOLVABLE_ID_RE.match(obj_id)
    if m:
        return m.group(1), m.group(2).split(".")
    return obj_id, []
