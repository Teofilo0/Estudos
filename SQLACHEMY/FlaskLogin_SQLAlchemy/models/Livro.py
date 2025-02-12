from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import db


class Livro(db.Model):
    __tablename__ = 'livros'
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(db.String(150), nullable=False)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='livros')
