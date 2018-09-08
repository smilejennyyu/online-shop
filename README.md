# Udacity Project 4: Item Catalog (Online Shops)

This site is used to display fashion items in predefined categories. Also, users can login through google account and create, read, update, and delete items in their own store.

#### Prerequirements
This project requires Python 2.X (2.7.x is expected).
[Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads) are required to run the site. 

#### Setup
When you enter the virtual machine, go to the directory that you just cloned.
To initially setup the database, run the following commands:

    python database_setup.py
    python lotsofitems.py

The database_setup.py script constructs an empty database that will be used for the online shops site. The logsofitems.py script populates the database that already exists with various items. You can always to add or modify the lotsofitem.py in order to add or modify things.

Then, run the following command to start the site:

    python project.py

Now, go to http://localhost:5000/ to view the site.

#### Usage

To create, edit, or delete items and stores, you must be logged in to the site with your Google account. To login, click the Login link in the upper left to access the login page.

To logout of the page, click Logout in the upper left.