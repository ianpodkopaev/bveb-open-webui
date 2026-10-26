import logging
import os
from typing import Optional

import aiohttp
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from starlette.responses import Response

from open_webui.constants import ERROR_MESSAGES
from open_webui.utils.access_control import has_permission
from open_webui.utils.auth import get_verified_user

log = logging.getLogger(__name__)

router = APIRouter()


class DigUpConfigForm(BaseModel):
    # Folders to search. `code_roots` are indexed/searched as code; the others
    # keep images, pdfs, audio, video and text.
    roots: Optional[list] = None
    code_roots: Optional[list] = None


class DigUpSearchForm(BaseModel):
    q: str
    code: bool = False
    kinds: Optional[list] = None
    limit: int = 8
    meaning: bool = True


class DigUpTextForm(BaseModel):
    segment: int
    code: bool = False


class DigUpRenderForm(BaseModel):
    path: str
    kind: str = 'image'
    loc: Optional[float] = None
    pixels: int = 720


def bridge(url: str) -> str:
    host = os.environ.get('DIGUP_BRIDGE_HOST', 'host.docker.internal')
    port = os.environ.get('DIGUP_BRIDGE_PORT', '8199')
    return f'http://{host}:{port}{url}'


async def check(request: Request, user) -> None:
    if user.role == 'admin':
        return
    if await has_permission(user.id, 'workspace.knowledge', request.app.state.config.USER_PERMISSIONS):
        return
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ERROR_MESSAGES.UNAUTHORIZED)


async def call(url: str, body: Optional[dict] = None, timeout_s: int = 120):
    """One round trip to the digup bridge on the host; its answer is the response."""
    timeout = aiohttp.ClientTimeout(total=timeout_s)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.request('POST' if body is not None else 'GET', bridge(url), json=body) as resp:
            data = await resp.json(content_type=None)
            if resp.status >= 400:
                raise HTTPException(status_code=resp.status, detail=data.get('error') or 'digup bridge error')
            return data


@router.get('/status')
async def get_status(request: Request, user=Depends(get_verified_user)):
    await check(request, user)
    return await call('/status')


@router.post('/config', response_model=bool)
async def set_config(
    request: Request,
    form_data: DigUpConfigForm,
    user=Depends(get_verified_user),
):
    await check(request, user)
    await call('/config', form_data.model_dump(exclude_none=True))
    return True


@router.post('/search')
async def search(
    request: Request,
    form_data: DigUpSearchForm,
    user=Depends(get_verified_user),
):
    await check(request, user)
    return await call('/search', form_data.model_dump(exclude_none=False))


@router.post('/text')
async def get_text(
    request: Request,
    form_data: DigUpTextForm,
    user=Depends(get_verified_user),
):
    await check(request, user)
    return await call('/text', form_data.model_dump(exclude_none=False))


@router.post('/render')
async def render(
    request: Request,
    form_data: DigUpRenderForm,
    user=Depends(get_verified_user),
):
    await check(request, user)
    return await call('/render', form_data.model_dump(exclude_none=False))


@router.get('/media/{path:path}')
async def media(request: Request, path: str, user=Depends(get_verified_user)):
    """A search result image (original or rendered preview), streamed from the bridge."""
    from urllib.parse import quote

    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(bridge(f'/media?path=/{quote(path, safe="/")}')) as resp:
            if resp.status >= 400:
                raise HTTPException(status_code=resp.status, detail='no media')
            await check(request, user)
            data = await resp.read()
            return Response(content=data, media_type=resp.headers.get('Content-Type', 'application/octet-stream'))
