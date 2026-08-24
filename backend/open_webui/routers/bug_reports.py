import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from open_webui.models.feedbacks import Feedbacks, FeedbackForm, FeedbackModel
from open_webui.utils.auth import get_admin_user, get_verified_user
from open_webui.internal.db import get_async_session

log = logging.getLogger(__name__)

router = APIRouter()

MAX_PHOTO_SIZE = 5 * 1024 * 1024  # 5MB


class BugReportForm(BaseModel):
    name: str
    email: str
    category: str
    message: str
    photo: Optional[str] = None
    bug_time: Optional[str] = None


@router.post('/bug-reports', response_model=FeedbackModel)
async def submit_bug_report(
    form_data: BugReportForm,
    user=Depends(get_verified_user),
    db: AsyncSession = Depends(get_async_session),
):
    if form_data.photo:
        if len(form_data.photo) > MAX_PHOTO_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Photo exceeds maximum size of 5MB',
            )

    data = {
        'name': form_data.name,
        'email': form_data.email,
        'category': form_data.category,
        'message': form_data.message,
    }
    if form_data.photo:
        data['photo'] = form_data.photo
    if form_data.bug_time:
        data['bug_time'] = form_data.bug_time

    feedback_form = FeedbackForm(type='bug_report', data=data)
    feedback = await Feedbacks.insert_new_feedback(user_id=user.id, form_data=feedback_form, db=db)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Failed to submit bug report',
        )
    return feedback


@router.get('/bug-reports', response_model=list[FeedbackModel])
async def get_bug_reports(
    user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_async_session),
):
    return await Feedbacks.get_feedbacks_by_type(type='bug_report', db=db)
