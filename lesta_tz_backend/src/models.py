from sqlalchemy import MetaData, Column, Integer, String, ForeignKey, UniqueConstraint, Float, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.declarative import declarative_base


metadata = MetaData()
Base = declarative_base(metadata=metadata)

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)

    documents = relationship("Document", back_populates="owner", cascade="all, delete-orphan")
    collections = relationship("Collection", back_populates="owner", cascade="all, delete-orphan")

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
    content_hash = Column(String, nullable=True) 
    
    owner = relationship("Users", back_populates="documents")
    words = relationship("DocumentWord", back_populates="document", cascade="all, delete-orphan")
    collections = relationship("CollectionDocument", back_populates="document", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint('filename', 'owner_id', name='uc_filename_owner'),)

class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True, unique=True)

    documents = relationship("DocumentWord", back_populates="word", cascade="all, delete-orphan")

class DocumentWord(Base):
    __tablename__ = 'document_words'
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey('documents.id'))
    word_id = Column(Integer, ForeignKey('words.id'))
    text = Column(String, index=True)
    tf = Column(Float, nullable=False)

    document = relationship("Document", back_populates="words")
    word = relationship("Word", back_populates="documents")

    __table_args__ = (UniqueConstraint('document_id', 'word_id', name='uc_document_word'),)

class Collection(Base):
    __tablename__ = 'collections'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("Users", back_populates="collections")
    documents = relationship("CollectionDocument", back_populates="collection", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint('name', 'owner_id', name='uc_collection_owner'),)

class CollectionDocument(Base):
    __tablename__ = 'collection_documents'
    id = Column(Integer, primary_key=True, index=True)
    collection_id = Column(Integer, ForeignKey('collections.id'))
    document_id = Column(Integer, ForeignKey('documents.id'))

    collection = relationship("Collection", back_populates="documents")
    document = relationship("Document", back_populates="collections")

    __table_args__ = (UniqueConstraint('collection_id', 'document_id', name='uc_collection_document'),)


class AppMetrics(Base):
    __tablename__ = "app_metrics"

    id = Column(Integer, primary_key=True, index=True)
    files_processed = Column(Integer, default=0)
    min_time_processed = Column(Float, default=0.0)
    avg_time_processed = Column(Float, default=0.0)
    max_time_processed = Column(Float, default=0.0)

    latest_file_processed_timestamp = Column(DateTime, nullable=True)
    last_user_id = Column(Integer, nullable=True)
    last_user_name = Column(String, nullable=True) # имя пользователя загрузиший последний файл
    last_file_size = Column(Integer, nullable=True)  # в байтах
    last_file_name = Column(String, nullable=True)
    last_file_path = Column(String, nullable=True)