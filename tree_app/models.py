import nanoid
from sqlalchemy import Column, String, func, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, remote, foreign
from sqlalchemy_utils import LtreeType, Ltree

Base = declarative_base()


class Node(Base):
    __tablename__ = "nodes"

    id = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    path = Column(LtreeType, nullable=False)

    parent = relationship(
        "Node",
        primaryjoin=(remote(path) == foreign(func.subpath(path, 0, -1))),
        backref="children",
        viewonly=True,
    )

    def __init__(self, name, parent=None):
        _id = nanoid.generate('1234567890abcdef', 16)
        self.id = _id
        self.name = name
        ltree_id = Ltree(str(_id))
        self.path = ltree_id if parent is None else parent.path + ltree_id

    __table_args__ = (Index("ix_nodes_path", path, postgresql_using="gist"),)

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Node({})'.format(self.name)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'path': list(map(str, self.path)),
        }
