Setup your DB first
===================

SQLBatis provides the ability to interact with the database through command-line base on the alembic.
There is `sqlbatis` command is available once the sqlbatis is installed, you can use it directly.

Four common commands will be mentioned here, we will take a quick tour about them, also
create a database for your app from scratch step by step, and you can run the command::

    sqlbatis --help

to get more details about `sqlbatis`


Define a Model
--------------
SQLBatis also can mapping the model to the table in the database, but there are some rules that we need to follow,
Let's define a Model first::

    from sqlalchemy import Column, Integer, String
    from sqlbatis import Model

    class User(Model):

        id = Column(Integer, primary_key=True)
        name = Column(String)
        full_name = Column(String)    

All the Models should inherit from sqlbatis.Model, so we can find all the models that you defined
in the app. When we mapping the class to the table, we will convert the class name to camel case, 
and use it as table name.But if `__tablename__` is specified we will use it instead of the camel case::

    from sqlalchemy import Column, Integer, String
    from sqlbatis import Model

    class User(Model):

        # will use 'customized_table_name' instead of 'user'
        __tablename__ = 'customized_table_name'

        id = Column(Integer, primary_key=True)
        name = Column(String)
        full_name = Column(String) 


**tips:** Column, Integer, String etc. are imported from the sqlalchemy

Scan all the models
-------------------
You can use the command::

    sqlbatis scan

to check the models that you defined in the app, the useage of this command::

    Usage: sqlbatis scan [OPTIONS]

    Show all the models that searched in the directory

    Options:
    -d, --directory TEXT  The main folder that you want to search the models,
                            default is current work directory
    -i, --ignore TEXT     Ignore the folder or files through defined regrex
                            expression, List[regrex]
    --help                Show this message and exit.

now the default ignore directories are::
    
    ['tests', 'build', 'vscode','dist', 'egg', 'migrations', 'sqlbatis']


Initialize the tools
--------------------
Once you confirmed the models that you defined, just use the command::

    sqlbatis init

to generate the initial configuration file which will be used in migrate and upgrade stage. the usage of this::

    Usage: sqlbatis init [OPTIONS]

    Init the db tools

    Options:
    -d, --directory TEXT  The main folder that you want to search the models,
                            default is current work directory
    -i, --ignore TEXT     Ignore the folder or files through defined regrex
                            expression, List[regrex]
    -db, --db_url TEXT    The database url config
    --help                Show this message and exit.

This command will generate several configuration files in the migrations folder automatically, the migrate scripts
will be generated according to the configuration defined here.

**Caution:** We need to specify the **-db** when we execute this command, will remove that in the near future.


Generate the scripts
--------------------
Here we will generate the scripts for upgrade, the command::

    Usage: sqlbatis migrate [OPTIONS]

    Generate the migrate script

    Options:
    --help  Show this message and exit.

The upgrade script will be generated in the migrations/versions/ folder, and you can find the script name from
the console. Before you go to next step, you still have the opportunity to modify the scripts in the versions 
folder utils you think it's make sense.

Sync the DB
-----------
We have not mapping the models to our database table util the upgrade command is executed::

    Usage: sqlbatis upgrade [OPTIONS]

    Upgrade the db to the version specified, if not sepecified will update to
    the latest version

    Options:
    -v, --version TEXT  The version that you want to upgrade to.
    --help              Show this message and exit.

Now, the table will be created in your DB.
