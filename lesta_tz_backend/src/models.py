from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, Text, DateTime, CheckConstraint, UniqueConstraint, Float, JSON, Boolean

metadata = MetaData()

Words = Table(
    "words",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("word", String, nullable=True),
    Column("tf", Integer, nullable=True),
    Column("idf", Integer, nullable=True),
)