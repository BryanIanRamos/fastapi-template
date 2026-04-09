from typing import Any


def success_response(message: str, data: Any, meta: dict[str, Any] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "success": True,
        "message": message,
        "data": data,
    }
    if meta is not None:
        payload["meta"] = meta
    return payload


def pagination_meta(page: int, page_size: int, total: int) -> dict[str, int]:
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    return {
        "page": page,
        "pageSize": page_size,
        "total": total,
        "totalPages": total_pages,
    }
