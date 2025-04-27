from sqlalchemy import MetaData, Column, Integer, String, ForeignKey, UniqueConstraint, Float
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False, unique=True)  # Имя файла
    file_path = Column(String, nullable=False)  # Путь к файлу
    words = relationship("DocumentWord", back_populates="document")

class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    documents = relationship("DocumentWord", back_populates="word")

class DocumentWord(Base):
    __tablename__ = 'document_words'
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey('documents.id'))
    word_id = Column(Integer, ForeignKey('words.id'))
    text = Column(String, index=True)
    tf = Column(Float, nullable=False)  # Сколько раз слово встречается в документе

    document = relationship("Document", back_populates="words")
    word = relationship("Word", back_populates="documents")

    __table_args__ = (UniqueConstraint('document_id', 'word_id', name='uc_document_word'),)