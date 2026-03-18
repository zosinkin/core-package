from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from typing import List


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, session: AsyncSession,  **data):
        new_instance = cls.model(**data)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            raise e
        return new_instance 
    
    @classmethod
    async def get_object_by_id(cls, session: AsyncSession, obj_id: int):
        stmt = select(cls.model).filter(cls.model.id == obj_id)
        obj = await session.execute(stmt)
        res = obj.scalar_one_or_none()
        return res
    

    @classmethod
    async def get_all_objects(cls, session: AsyncSession):
        stmt = select(cls.model).filter(cls.model.is_active == True)
        result = await session.execute(stmt)
        all_obj = result.scalars()
        return all_obj
    

    @classmethod
    async def update_data(cls, obj_id: int, data: dict, session: AsyncSession):
        stmt = select(cls.model).where(cls.model.id == obj_id)
        result = await session.execute(stmt)
        obj = result.scalar_one_or_none()
        for field, value in data.items():
            setattr(obj, field, value)
        
        try:
            await session.commit()
            await session.refresh(obj)
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return obj


    @classmethod
    async def get_object_list(cls, session: AsyncSession, data: dict) -> List:
        product_list = []
        for item in data.items:
            stmt = select(cls.model).where(cls.model.id == item.product_id)
            result = await session.execute(stmt)
            product = result.scalar_one_or_none()
            product_list.append(product)
        
        return product_list
    
    @classmethod
    async def get_one_by_filter(cls, session: AsyncSession, **filters):
        stmt = select(cls.model).filter_by(**filters)
        object = await session.execute(stmt)
        result = object.scalar_one_or_none()


    
    

    

   
