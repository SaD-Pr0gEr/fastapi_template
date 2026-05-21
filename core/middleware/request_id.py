import uuid

from core.context import request_id_ctx, user_id_ctx


async def request_identify_middleware(request, call_next):
    request_id = str(uuid.uuid4())
    request_id_ctx.set(request_id)
    user_id_ctx.set(None)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
