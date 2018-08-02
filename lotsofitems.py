from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Store, Base, FashionItem
 
engine = create_engine('sqlite:///onlineshopping.db', connect_args={'check_same_thread': False})
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



#Menu for UrbanBurger
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




#Menu for Super Stir Fry
# FashionStore2 = FashionStore(name = "Super Stir Fry")

# session.add(FashionStore2)
# session.commit()


# FashionItem1 = FashionItem(name = "Chicken Stir Fry", description = "with your choice of noodles vegetables and sauces", price = "$7.99", category = "Entree", FashionStore = FashionStore2)

# session.add(FashionItem1)
# session.commit()

# FashionItem2 = FashionItem(name = "Peking Duck", description = " a famous duck dish from Beijing[1] that has been prepared since the imperial era. The meat is prized for its thin, crisp skin, with authentic versions of the dish serving mostly the skin and little meat, sliced in front of the diners by the cook", price = "$25", category = "Entree", FashionStore = FashionStore2)

# session.add(FashionItem2)
# session.commit()

# FashionItem3 = FashionItem(name = "Spicy Tuna Roll", description = "", price = "", category = "", FashionStore = FashionStore2)

# session.add(FashionItem3)
# session.commit()

# FashionItem4 = FashionItem(name = "Nepali Momo ", description = "", price = "", category = "", FashionStore = FashionStore2)

# session.add(FashionItem4)
# session.commit()

# FashionItem5 = FashionItem(name = "Beef Noodle Soup", description = "", price = "", category = "", FashionStore = FashionStore2)

# session.add(FashionItem5)
# session.commit()

# FashionItem6 = FashionItem(name = "Ramen", description = "", price = "", category = "", FashionStore = FashionStore2)

# session.add(FashionItem6)
# session.commit()




# #Menu for Panda Garden
# FashionStore1 = FashionStore(name = "Panda Garden")

# session.add(FashionStore1)
# session.commit()


# FashionItem1 = FashionItem(name = "Pho", description = "a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem1)
# session.commit()

# FashionItem2 = FashionItem(name = "Chinese Dumplings", description = "a common Chinese dumpling which generally consists of minced meat and finely chopped vegetables wrapped into a piece of dough skin. The skin can be either thin and elastic or thicker.", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem2)
# session.commit()

# FashionItem3 = FashionItem(name = "Gyoza", description = "The most prominent differences between Japanese-style gyoza and Chinese-style jiaozi are the rich garlic flavor, which is less noticeable in the Chinese version, the light seasoning of Japanese gyoza with salt and soy sauce, and the fact that gyoza wrappers are much thinner", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem3)
# session.commit()

# FashionItem4 = FashionItem(name = "Stinky Tofu", description = "Taiwanese dish, deep fried fermented tofu served with pickled cabbage.", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem4)
# session.commit()



# #Menu for Thyme for that
# FashionStore1 = FashionStore(name = "Thyme for That Vegetarian Cuisine ")

# session.add(FashionStore1)
# session.commit()


# FashionItem1 = FashionItem(name = "Tres Leches Cake", description = "Rich, luscious sponge cake soaked in sweet milk and topped with vanilla bean whipped cream and strawberries.", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem1)
# session.commit()

# FashionItem2 = FashionItem(name = "Mushroom risotto", description = "Portabello mushrooms in a creamy risotto", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem2)
# session.commit()

# FashionItem3 = FashionItem(name = "Honey Boba Shaved Snow", description = "Milk snow layered with honey boba, jasmine tea jelly, grass jelly, caramel, cream, and freshly made mochi", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem3)
# session.commit()

# FashionItem4 = FashionItem(name = "Cauliflower Manchurian", description = "Golden fried cauliflower florets in a midly spiced soya,garlic sauce cooked with fresh cilantro, celery, chilies,ginger & green onions", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem4)
# session.commit()

# FashionItem5 = FashionItem(name = "Aloo Gobi Burrito", description = "Vegan goodness. Burrito filled with rice, garbanzo beans, curry sauce, potatoes (aloo), fried cauliflower (gobi) and chutney. Nom Nom", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem5)
# session.commit()




# #Menu for Tony's Bistro
# FashionStore1 = FashionStore(name = "Tony\'s Bistro ")

# session.add(FashionStore1)
# session.commit()


# FashionItem1 = FashionItem(name = "Shellfish Tower", description = "", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem1)
# session.commit()

# FashionItem2 = FashionItem(name = "Chicken and Rice", description = "", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem2)
# session.commit()

# FashionItem3 = FashionItem(name = "Mom's Spaghetti", description = "", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem3)
# session.commit()

# FashionItem4 = FashionItem(name = "Choc Full O\' Mint (Smitten\'s Fresh Mint Chip ice cream)", description = "", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem4)
# session.commit()

# FashionItem5 = FashionItem(name = "Tonkatsu Ramen", description = "Noodles in a delicious pork-based broth with a soft-boiled egg", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem5)
# session.commit()




# #Menu for Andala's 
# FashionStore1 = FashionStore(name = "Andala\'s")

# session.add(FashionStore1)
# session.commit()


# FashionItem1 = FashionItem(name = "Lamb Curry", description = "Slow cook that thang in a pool of tomatoes, onions and alllll those tasty Indian spices. Mmmm.", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem1)
# session.commit()

# FashionItem2 = FashionItem(name = "Chicken Marsala", description = "Chicken cooked in Marsala wine sauce with mushrooms", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem2)
# session.commit()

# FashionItem3 = FashionItem(name = "Potstickers", description = "Delicious chicken and veggies encapsulated in fried dough.", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem3)
# session.commit()

# FashionItem4 = FashionItem(name = "Nigiri SamplerMaguro, Sake, Hamachi, Unagi, Uni, TORO!", description = "", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem4)
# session.commit()




# #Menu for Auntie Ann's
# FashionStore1 = FashionStore(name = "Auntie Ann\'s Diner ")

# session.add(FashionStore1)
# session.commit()

# FashionItem9 = FashionItem(name = "Chicken Fried Steak", description = "Fresh battered sirloin steak fried and smothered with cream gravy", price = "$8.99", category = "Entree", FashionStore = FashionStore1)

# session.add(FashionItem9)
# session.commit()



# FashionItem1 = FashionItem(name = "Boysenberry Sorbet", description = "An unsettlingly huge amount of ripe berries turned into frozen (and seedless) awesomeness", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem1)
# session.commit()

# FashionItem2 = FashionItem(name = "Broiled salmon", description = "Salmon fillet marinated with fresh herbs and broiled hot & fast", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem2)
# session.commit()

# FashionItem3 = FashionItem(name = "Morels on toast (seasonal)", description = "Wild morel mushrooms fried in butter, served on herbed toast slices", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem3)
# session.commit()

# FashionItem4 = FashionItem(name = "Tandoori Chicken", description = "Chicken marinated in yoghurt and seasoned with a spicy mix(chilli, tamarind among others) and slow cooked in a cylindrical clay or metal oven which gets its heat from burning charcoal.", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem4)
# session.commit()




# #Menu for Cocina Y Amor
# FashionStore1 = FashionStore(name = "Cocina Y Amor ")

# session.add(FashionStore1)
# session.commit()


# FashionItem1 = FashionItem(name = "Super Burrito Al Pastor", description = "Marinated Pork, Rice, Beans, Avocado, Cilantro, Salsa, Tortilla", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem1)
# session.commit()

# FashionItem2 = FashionItem(name = "Cachapa", description = "Golden brown, corn-based venezuelan pancake; usually stuffed with queso telita or queso de mano, and possibly lechon. ", price = "", category = "", FashionStore = FashionStore1)

# session.add(FashionItem2)
# session.commit()

print "added menu items!"

