from fastapi import APIRouter, status, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from services.backend.app.db.session import get_db
from ..core.security import get_current_active_user
from ..schemas import ItemCreate, Item, User, Image, ItemUpdate
from ..db.crud.crud_item import item
from ..db.crud.crud_image import get_image_by_item, create_image

router_item = APIRouter(
    prefix="/item",
    tags=["ITEMS"],
    responses={404: {"description": "Not found"}},
)


@router_item.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=Item

)
async def create_new_item(
        item_in: ItemCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    db_item = await item.get_by_title(db=db, title=item_in.title)
    if db_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Item with this {db_item.title} title Already created",
        )

    return await item.create(db=db, obj_in=item_in, user_id=current_user.id)


@router_item.get("/all", response_model=list[Item])
async def read_items(
        db: AsyncSession = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    items = await item.get_multi(db=db, skip=skip, limit=limit)

    return items


@router_item.get("/{item_title}")
async def read_item(item_title: str, db: AsyncSession = Depends(get_db)):
    db_item = await item.get_by_title(sdb=db, title=item_title)

    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return db_item


@router_item.patch("/{item_title}")
async def update_item(
        item_in: ItemUpdate,
        item_title: str,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_active_user),
):
    db_item = await item.get_by_title(db=db, title=item_title)
    if db_item and db_item.user_id == current_user.id:
        return await item.update(db=db, db_obj=db_item, obj_in=item_in)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router_item.delete("/{item_title}")
async def delete_item(item_title: str,
                      db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
    db_item = await item.get_by_title(db=db, title=item_title)
    if db_item and db_item.user_id == current_user.id:
        return await item.remove_by_title(db=db, title=item_title)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router_item.post(
    "/create/{item_id}/image", status_code=status.HTTP_201_CREATED, response_model=Image

)
async def create_image_item(item_title: str,
                            file: UploadFile = File(None),
                            db: AsyncSession = Depends(get_db),
                            current_user: User = Depends(get_current_active_user)
                            ):
    db_item = await item.get_by_title(db=db, title=item_title)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Item with this {item_title} item already created",
        )

    db_image = await get_image_by_item(db=db, item_id=db_item.id)

    if db_image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Item om this {db_item.title} item already created",
        )

    file_name = file.filename
    extension = file_name.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return {"error": "Invalid image format. Only JPG, JPEG and PNG are allowed."}
    image = await file.read()

    return await create_image(db=db, file=image, file_name=file_name, item_id=db_item.id)
