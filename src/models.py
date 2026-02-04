from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


db = SQLAlchemy()

follower_table = Table(
    "followers",
    db.Model.metadata,
    Column("follower_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("followed_id", Integer, ForeignKey("user.id"), primary_key=True)
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)

    post: Mapped[list["Post"]] = relationship("Post", back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="author")

    following: Mapped[list["User"]] = relationship(
        "User",
        secondary=follower_table,
        primaryjoin=(follower_table.c.follower_id == id),
        secondaryjoin=(follower_table.c.followed_id == id),
        back_populates="followers")
    followers: Mapped[list["User"]] = relationship(
        "User",
        secondary=follower_table,
        primaryjoin=(follower_table.c.followed_id == id),
        secondaryjoin=(follower_table.c.follower_id == id),
        back_populates="following")


def serialize(self):
    return {
        "id": self.id,
        "email": self.email,
        "username": self.username,
        "firstname": self.firstname,
        "lastname": self.lastname
        # do not serialize the password, its a security breach
    }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    user: Mapped[User] = relationship("User", back_populates="post")

    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="post")
    media: Mapped[list["Media"]] = relationship("Media", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,

            # do not serialize the password, its a security breach
        }


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(120), nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    author: Mapped[User] = relationship("User", back_populates="comments")
    post: Mapped[Post] = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id

            # do not serialize the password, its a security breach
        }


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(120), nullable=False)
    url: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id

            # do not serialize the password, its a security breach
        }
