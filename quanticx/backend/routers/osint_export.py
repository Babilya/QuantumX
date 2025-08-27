from __future__ import annotations

import io
import csv
from fastapi import APIRouter, Response, HTTPException
from reportlab.pdfgen import canvas
from backend.redis_client import get_redis

router = APIRouter()


@router.get('/csv')
async def export_csv(key: str):
    r = get_redis()
    data = r.hgetall(key)
    if not data:
        raise HTTPException(status_code=404, detail='not found')
    buf = io.StringIO()
    w = csv.writer(buf)
    for k,v in data.items():
        w.writerow([k, v])
    return Response(content=buf.getvalue(), media_type='text/csv')


@router.get('/pdf')
async def export_pdf(key: str):
    r = get_redis()
    data = r.hgetall(key)
    if not data:
        raise HTTPException(status_code=404, detail='not found')
    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    y = 800
    for k, v in data.items():
        c.drawString(40, y, f"{k}: {v[:80]}")
        y -= 20
    c.save()
    return Response(content=buf.getvalue(), media_type='application/pdf')
