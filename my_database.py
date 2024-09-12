from sqlalchemy import ForeignKey, UniqueConstraint
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

    symbols: Mapped[List["Symbol"]] = relationship(
        "Symbol",
        back_populates="category"
    )


class Symbol(Base):
    __tablename__ = "symbol"

    # This ensures that every `Symbol` is linked to exactly one `SymbolCategory`
    category_id: Mapped[int] = mapped_column(ForeignKey("symbol_category.id"))

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    category: Mapped["SymbolCategory"] = relationship(
        "SymbolCategory",
        back_populates="symbols"
    )


class User(Base):
    # TODO: Add activate or deactivate user feature.
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    comments: Mapped[List["Comment"]] = relationship(
        "Comment",
        back_populates="commenter",
        cascade="all, delete-orphan"
    )
    liked_comments: Mapped[List["Like"]] = relationship(
        "Like",
        back_populates="by",
        cascade="all, delete-orphan"
    )
    disliked_comments: Mapped[List["Dislike"]] = relationship(
        "Dislike",
        back_populates="by",
        cascade="all, delete-orphan"
    )


class Comment(Base):
    __tablename__ = "comment"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(nullable=False)

    commenter: Mapped["User"] = relationship(
        "User",
        back_populates="comments"
    )
    likes: Mapped[List["Like"]] = relationship(
        "Like",
        back_populates="on_comment",
        cascade="all, delete-orphan"
    )
    dislikes: Mapped[List["Dislike"]] = relationship(
        "Dislike",
        back_populates="on_comment",
        cascade="all, delete-orphan"
    )


# record of each time a user likes a comment
class Like(Base):
    __tablename__ = "like"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    comment_id: Mapped[int] = mapped_column(ForeignKey("comment.id"))

    id: Mapped[int] = mapped_column(primary_key=True)

    by: Mapped["User"] = relationship(
        "User",
        back_populates="liked_comments"
    )
    on_comment: Mapped["Comment"] = relationship(
        "Comment",
        back_populates="likes"
    )

    # Provide additional configurations for `like` table (table-level settings).
    # We don't want the same user to be able to like the same comment more than once
    # So, we set a unique constraint on the combination of user_id and comment_id to prevent this.
    __table_args__ = (UniqueConstraint("user_id", "comment_id", name="unique_like"),)


class Dislike(Base):
    __tablename__ = "dislike"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    comment_id: Mapped[int] = mapped_column(ForeignKey("comment.id"))

    id: Mapped[int] = mapped_column(primary_key=True)

    by: Mapped["User"] = relationship(
        "User",
        back_populates="disliked_comments"
    )
    on_comment: Mapped["Comment"] = relationship(
        "Comment",
        back_populates="dislikes"
    )

    __table_args__ = (UniqueConstraint("user_id", "comment_id", name="unique_dislike"),)


