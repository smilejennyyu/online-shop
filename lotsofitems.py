from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Store, Base, FashionItem
 
engine = create_engine('sqlite:///onlineshopping.db', connect_args={'check_same_thread': False})
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()



#American Eagle Store
fashionStore1 = Store(name = "American Eagle")

session.add(fashionStore1)
session.commit()


FashionItem1 = FashionItem(name = "SHOULDER TOP", price = "$2.99", category = "Tops", store = fashionStore1)

session.add(FashionItem1)
session.commit()

FashionItem2 = FashionItem(name = "OVERSIZED T-SHIRT", price = "$5.50", category = "Tops", store = fashionStore1)

session.add(FashionItem2)
session.commit()

FashionItem3 = FashionItem(name = "SWEETHEART T-SHIRT", price = "$3.99", category = "Tops", store = fashionStore1)

session.add(FashionItem3)
session.commit()

FashionItem4 = FashionItem(name = "JEAN SHORTS", price = "$7.99", category = "Bottoms", store = fashionStore1)

session.add(FashionItem4)
session.commit()

FashionItem5 = FashionItem(name = "JEGGING", price = "$1.99", category = "Bottoms", store = fashionStore1)

session.add(FashionItem5)
session.commit()

FashionItem6 = FashionItem(name = "SNEAKER", price = "$.99", category = "Shoes", store = fashionStore1)

session.add(FashionItem6)
session.commit()

FashionItem7 = FashionItem(name = "POINTY TOE FLAT", price = "$3.49", category = "Shoes", store = fashionStore1)

session.add(FashionItem7)
session.commit()

FashionItem8 = FashionItem(name = "LOVE NECKLACE", price = "$5.99", category = "Jewellery", store = fashionStore1)

session.add(FashionItem8)
session.commit()


print "added fashion items!"

