from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from model import MenuItem
from schemas import MenuItemCreate, MenuItemUpdate

def create_menu_item(menu_item: MenuItemCreate, db: Session):
    try:
        existed = db.query(MenuItem).filter(MenuItem.dish_code == menu_item.dish_code).first()

        if existed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dish code already exists"
            )

        new_item = MenuItem(
            dish_code=menu_item.dish_code,
            dish_name=menu_item.dish_name,
            calorie_count=menu_item.calorie_count,
            price=menu_item.price,
            status=menu_item.status
        )

        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        return new_item

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

def get_all_menu_items(db: Session):
    return db.query(MenuItem).all()

def get_menu_item(item_id: int, db: Session):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )

    return item


def update_menu_item(item_id: int,menu_item: MenuItemUpdate,db: Session):
    try:
        item = db.query(MenuItem).filter(MenuItem.id == item_id).first()

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found"
            )

        update_data = menu_item.model_dump(exclude_unset=True)

        if "dish_code" in update_data:
            existed = db.query(MenuItem).filter(
                MenuItem.dish_code == update_data["dish_code"],
                MenuItem.id != item_id
            ).first()

            if existed:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Dish code already exists"
                )

        for key, value in update_data.items():
            setattr(item, key, value)

        db.commit()
        db.refresh(item)

        return item

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

def delete_menu_item(item_id: int, db: Session):
    try:
        item = db.query(MenuItem).filter(MenuItem.id == item_id).first()

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found"
            )

        db.delete(item)
        db.commit()

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )