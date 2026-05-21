from typing import Annotated

from fastapi.params import Depends

from core.context import user_id_ctx


async def get_auth_user():
    return "GET USER LOGIC"


async def auth_user(user: Annotated[str, Depends(get_auth_user)]):
    user_id_ctx.set("user_id")
    return user
