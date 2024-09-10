from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class SymbolCategory(Base):
    __tablename__ = "symbol_category"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(unique=True)

    symbols: Mapped[List["Symbol"]] = relationship(back_populates="category")


class Symbol(Base):
    __tablename__ = "symbol"
    # This ensures that every `Symbol` is linked to exactly one `SymbolCategory`
    category_id: Mapped[int] = mapped_column(ForeignKey("symbol_category.id"))

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    category: Mapped["SymbolCategory"] = relationship(back_populates="symbols")



