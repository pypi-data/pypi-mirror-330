import datetime
import time
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String, UniqueConstraint, select

from neurion_ganglion.db import with_db
from neurion_ganglion.db.ion_usage import Base


class PathwayUsage(Base):
    __tablename__ = "pathway_usage"

    id = Column(Integer, primary_key=True, index=True)
    pathway_id = Column(Integer, unique=False, index=True)
    user_address = Column(String, unique=False, index=True)
    num_of_calls_settled = Column(Integer)
    num_of_calls_pending = Column(Integer)
    created_at = Column(DateTime)


class PathwayUsageDAO:
    """Data Access Object for PathwayUsage model."""

    @staticmethod
    async def get_num_of_calls_pending(pathway_id: int, user_address: str):
        """
        Retrieves the number of pending calls for the given pathway_id and user_address.

        :param pathway_id: The ID of the pathway.
        :param user_address: The address of the user.
        :return: The number of pending calls if found, else None.
        """

        async def _get_calls_pending(db: AsyncSession):
            result = await db.execute(
                select(PathwayUsage.num_of_calls_pending).filter_by(pathway_id=pathway_id, user_address=user_address)
            )
            return result.scalar()  # Returns num_of_calls_pending or None if not found

        return await with_db(_get_calls_pending)

    @staticmethod
    async def increment_calls_pending(pathway_id: int, user_address: str):
        """
        Increases num_of_calls_pending by 1 for the given pathway_id and user_address.
        If the entry does not exist, insert a new record with num_of_calls_pending = 1.
        """

        async def _increment_pending(db: AsyncSession):
            result = await db.execute(
                select(PathwayUsage).filter_by(pathway_id=pathway_id, user_address=user_address)
            )
            entry = result.scalars().first()

            if entry:
                entry.num_of_calls_pending += 1
            else:
                entry = PathwayUsage(
                    pathway_id=pathway_id,
                    user_address=user_address,
                    num_of_calls_settled=0,
                    num_of_calls_pending=1,
                    created_at=datetime.datetime.now()
                )
                db.add(entry)

            await db.commit()
            return entry

        return await with_db(_increment_pending)

    @staticmethod
    async def clear_calls_pending(pathway_id: int, user_address: str):
        """
        Moves all num_of_calls_pending to num_of_calls_settled and resets num_of_calls_pending to 0.

        :param pathway_id: The ID of the pathway.
        :param user_address: The address of the user.
        """

        async def _clear_pending(db: AsyncSession):
            result = await db.execute(
                select(PathwayUsage).filter_by(pathway_id=pathway_id, user_address=user_address)
            )
            entry = result.scalars().first()

            if entry and entry.num_of_calls_pending > 0:
                entry.num_of_calls_settled += entry.num_of_calls_pending
                entry.num_of_calls_pending = 0
                await db.commit()

            return entry

        return await with_db(_clear_pending)