import datetime
import time
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String, UniqueConstraint, select

from neurion_ganglion.db import with_db

Base = declarative_base()

class IonUsage(Base):
    __tablename__ = "ion_usage"

    id = Column(Integer, primary_key=True, index=True)
    ion_address = Column(String, unique=False, index=True)
    user_address = Column(String, unique=False, index=True)
    num_of_calls = Column(Integer)
    created_at = Column(DateTime)

    __table_args__ = (UniqueConstraint('ion_address', 'user_address', name='_ion_user_uc'),)


class IonUsageDAO:
    """Data Access Object for IonUsage model."""

    @staticmethod
    async def increment_usage(ion_address: str, user_address: str):
        """
        Increases num_of_calls by 1 for the given ion_address and user_address.
        If the entry does not exist, insert a new record with num_of_calls = 1.
        """

        async def _increment(db: AsyncSession):
            result = await db.execute(
                select(IonUsage).filter_by(ion_address=ion_address, user_address=user_address)
            )
            entry = result.scalars().first()

            if entry:
                entry.num_of_calls += 1
            else:
                entry = IonUsage(ion_address=ion_address, user_address=user_address, num_of_calls=1,created_at=datetime.datetime.now())
                db.add(entry)

            await db.commit()

            return entry

        return await with_db(_increment)

    @staticmethod
    async def get_num_of_calls(ion_address: str, user_address: str):
        """
        Retrieves the number of calls for the given ion_address and user_address.

        :param ion_address: The address of the ion.
        :param user_address: The address of the user.
        :return: The number of calls if found, else None.
        """

        async def _get_calls(db: AsyncSession):
            result = await db.execute(
                select(IonUsage.num_of_calls).filter_by(ion_address=ion_address, user_address=user_address)
            )
            return result.scalar()  # Returns num_of_calls or None if not found

        return await with_db(_get_calls)

