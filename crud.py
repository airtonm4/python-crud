from sqlalchemy.orm import Session

import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def remove_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter_by(id=item_id).first()
    db.delete(db_item)
    db.commit()
    return db_item


def remove_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter_by(id=user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user


def update_item(db: Session, item: schemas.ItemUpdate, item_id: int):
    # Essa foi a forma que encontrei para conseguir alterar ambos os valores de objeto,
    # Como o método update retorna um valor, db_item, acaba tendo seu valor alterado,
    # Assim utilizamos um query auxiliar para o return

    db_item_query = db.query(models.Item).filter(
        models.Item.id == item_id).first()
    db_item = db.query(models.Item).filter(models.Item.id == item_id).update({"title": item.dict()[
        "title"], "description": item.dict()["description"]}, synchronize_session=False)

    db.commit()

    return db_item_query
