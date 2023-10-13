from typing import List

from bson import json_util
from fastapi import APIRouter
from starlette.responses import JSONResponse

from database import currencies_collection

from schemas.currency import Currency

router = APIRouter(prefix="/currencies", tags=["currencies"])


@router.get("", responses={400: {"description": "Bad request"}},
            response_model=List[Currency],
            description="Get list of all currency",
            )
async def get_all_currency():
    currencies_cursor = currencies_collection.find()
    currencies = await currencies_cursor.to_list(None)
    serialized_currencies = json_util.dumps(currencies, default=str)

    return JSONResponse(content=serialized_currencies)
