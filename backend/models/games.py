from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.db import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String)
    status = Column(Boolean)
    corrlett = Column(String)
    incorrlett = Column(String)
    error_count = Column(Integer)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    gamer = relationship("Account", back_populates="games")
