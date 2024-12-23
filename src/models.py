import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    User_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String, nullable=False)
    Password= Column(String(30), nullable=False)
    posts = relationship("Post", back_populates="owner") #Relacion: Un usuario puede tener/ser creador de muchos posts
    likes = relationship("Like", back_populates="owner") #Relacion: Un usuario puede tener/ser owner de muchos likes
    comments = relationship("Comment", back_populates="owner")  # Un usuario puede hacer muchos comentarios

class Post(Base):
    __tablename__ = 'post'
    Post_id = Column(Integer, primary_key=True)
    Date = Column(String, nullable=False)
    Content =Column(String)
    Owner_ID =Column(Integer,ForeignKey('user.User_id')) #Esta es la llave foranea que lleva al creador (que esta en la tabla User)
    owner = relationship("User", back_populates="posts") #Un post solo puede tener un usuario como creador/owner
    likes = relationship("Like", back_populates="post")   # Relación con Like (un post puede tener muchos likes)
    comments = relationship("Comment", back_populates="post")  # Un post puede tener muchos comentarios
    def to_dict(self):
        return {}
    
class Like(Base):
    __tablename__ = 'like'
    Like_id = Column(Integer, primary_key=True)
    Date = Column(String, nullable=False)
    Owner_ID =Column(Integer, ForeignKey('user.User_id'))# Aca se muestra el usuario que da el like
    Post_ID =Column(Integer, ForeignKey('post.Post_id')) # Aca se muestra el post en donde se hizo el like 
    post = relationship("Post", back_populates="likes")   # Relación con Post
    owner = relationship("User", back_populates="likes") # Relación con User

class Comment(Base):
    __tablename__ = 'comment'
    Comment_id = Column(Integer, primary_key=True)
    Date = Column(String, nullable=False)
    Content = Column(String, nullable=False)
    
    Owner_ID = Column(Integer, ForeignKey('user.User_id'))  # Usuario que hace el comentario
    Post_ID = Column(Integer, ForeignKey('post.Post_id'))  # Post comentado
    
    owner = relationship("User", back_populates="comments")  # Relación con User
    post = relationship("Post", back_populates="comments")   # Relación con Post



## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
