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
    category_name: Mapped[str] = mapped_column(unique=True, nullable=False)

    symbols: Mapped[List["Symbol"]] = relationship("Symbol", back_populates="category")


class Symbol(Base):
    __tablename__ = "symbol"
    # This ensures that every `Symbol` is linked to exactly one `SymbolCategory`
    category_id: Mapped[int] = mapped_column(ForeignKey("symbol_category.id"))

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    category: Mapped["SymbolCategory"] = relationship("SymbolCategory", back_populates="symbols")


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="commenter")


class Comment(Base):
    __tablename__ = "comment"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(nullable=False)

    commenter: Mapped["User"] = relationship("User", back_populates="comments")


