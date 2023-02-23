from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from services.backend.app.core.security import get_current_active_user
from services.backend.app.db.crud.crud_adventure import get_adventure_by_title, create_adventure, get_adventures
from services.backend.app.db.crud.crud_item import get_item_by_title
from services.backend.app.db.session import get_db
from services.backend.app.schemas import Adventure, AdventureCreate, User


router_adventure = APIRouter(
    prefix="/adventure",
    tags=["ADVENTURES"],
    responses={404: {"description": "Not found"}},
)


@router_adventure.post("/create", status_code=status.HTTP_201_CREATED, response_model=Adventure)
async def create_new_adventure(
        adventure: AdventureCreate,
        item_title: str,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    db_adventure = await get_adventure_by_title(db=db, adventure_title=adventure.title)
    if db_adventure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Adventure with this {db_adventure.title} title Already created",
        )

    db_item = await get_item_by_title(db=db, item_title=item_title)

    return await create_adventure(db=db, adventure=adventure, item_id=db_item.id, user_id=current_user.id)


@router_adventure.get("/all", response_model=list[Adventure])
async def read_adventures(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    adventures = await get_adventures(db=db, skip=skip, limit=limit)

    return adventures


@router_adventure.get("/{adventure_title}")
async def read_adventure(adventure_title: str, db: AsyncSession = Depends(get_db)):
    db_adventure = await get_adventure_by_title(db=db, adventure_title=adventure_title)

    if db_adventure is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return db_adventure


# adventure add item to current adventure

# adventure delete item from group
