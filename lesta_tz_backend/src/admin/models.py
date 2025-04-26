from typing import Union
import os
from pydantic import Field

from src.db import Base
from src.models import Words
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_file import FileField, ImageField, File
from sqlalchemy_file.storage import StorageManager
from libcloud.storage.drivers.local import LocalStorageDriver



os.makedirs("./static/server", 0o777, exist_ok=True)
container = LocalStorageDriver("./static").get_container("server")
StorageManager.add_storage("default", container)

class Word(Base):
    __table__ = Words
