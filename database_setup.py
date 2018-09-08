from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Store(Base):
    __tablename__ = 'store'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref=backref("store", cascade="all,delete"))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class FashionItem(Base):
    __tablename__ = 'fashion_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    price = Column(String(8))
    category = Column(String(250))
    store_id = Column(Integer, ForeignKey('store.id'))
    store = relationship(Store, backref=backref("fashion_item",
                                                cascade="all,delete"))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref=backref("fashion_item",
                                              cascade="all,delete"))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'price': self.price,
            'category': self.category,
        }

database = 'sqlite:///onlineshopping.db'
engine = create_engine(database, connect_args={'check_same_thread': False})

Base.metadata.create_all(engine)
