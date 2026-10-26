"""
search_project_images
---
Chat tool that returns the project images most connected to the user's question
as Markdown `<img>` links. The chat renderer already turns Markdown images into
displayed pictures (MarkdownInlineTokens -> <Image>), so no frontend changes are
needed.

The LLM passes `query` (a short phrase describing what image is wanted). Image
files whose filename/meta best match it are returned. On an empty match it still
returns the project's available images so "show me the pictures" works out of the
box.
"""

import re

from typing import Any, Dict, List
from pydantic import BaseModel

IMAGE_EXT = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')


class Valves(BaseModel):
    # Maximum number of images returned per call.
    max_images: int = 3


class Tools:
    valves = Valves()

    async def search_project_images(
        self,
        query: str = '',
        __user__: Dict[str, Any] = None,
        __messages__: List[Dict[str, Any]] = None,
        __id__: str = None,
    ) -> str:
        """
        Find project images (PNG/JPG/GIF/WebP/SVG) connected to the user's
        question and return them as Markdown image links.

        Call this when the user asks for a picture / diagram / scheme /
        screenshot / figure (e.g. "покажи схему", "какая диаграмма по X",
        "нужны картинки по Y").

        `query`: a short phrase describing the image you want. Leave it empty to
        return the project's available images.

        :param query: short description of the desired image
        :param __user__: user context (injected)
        :param __messages__: chat history (injected)
        :param __id__: tool id (injected)
        """
        from open_webui.models.files import Files

        user = __user__ or {}
        uid, role = user.get('id', ''), user.get('role', '')

        if not query or not str(query).strip():
            query = self._last_user_message(__messages__ or [])
        query = (query or '').strip()

        files = await Files.get_files()
        imgs = [
            f
            for f in files
            if (f.filename or '').lower().endswith(IMAGE_EXT)
            and (role == 'admin' or f.user_id == uid)
        ]
        if not imgs:
            return 'В проекте пока нет доступных изображений.'

        tokens = set(re.findall(r'\w{3,}', query.lower()))
        scored = sorted(((self._score(tokens, f), f) for f in imgs), key=lambda x: -x[0])
        hits = [f for s, f in scored[: self.valves.max_images] if s > 0] or imgs[: self.valves.max_images]

        md = '\n\n'.join(f"![{self._alt(f)}]({self._src(f)})" for f in hits)
        if not query:
            return f'Вот доступные изображения проекта:\n\n{md}'
        return f'Изображения, связанные с «{query}»:\n\n{md}'

    # ------------------------------------------------------------------
    @staticmethod
    def _last_user_message(messages: List[Dict[str, Any]]) -> str:
        for m in reversed(messages or []):
            if isinstance(m, dict) and m.get('role') == 'user':
                c = m.get('content')
                return c if isinstance(c, str) else ''
        return ''

    @staticmethod
    def _score(tokens: set, f) -> int:
        hay = ' '.join(
            [
                f.filename or '',
                str((f.meta or {}).get('name', '')),
                str(((f.meta or {}).get('data') or {}).get('caption', '')),
            ]
        ).lower()
        return sum(1 for t in tokens if t in hay)

    @staticmethod
    def _alt(f) -> str:
        return (f.meta or {}).get('name') or f.filename

    @staticmethod
    def _src(f) -> str:
        return f'/api/v1/files/{f.id}/content/{f.filename}'
