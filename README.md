# BudgetApp
Processes bank statement information cross-referencing with category databases and goals set by user to determine goal success and expenses.

# Building A Database
To create a database using the DatabaseManager, you will need to instantiate a database object: The Database constructor actually returns a connection to the database object. This makes the internal class infrastructure simpler for code design.
```python
db_connection = Database("path_to_new_db.db") # creates an object that returns the database connection
```

Once you have a database object, you may call any one of the associated commands.
For example:
```python
db_connection.create_table(table_name, [field_names])
```
More information on creating tables and managing database data can be found here: 

http://www.sqlitetutorial.net/sqlite-python/


The below link will direct you to the download for the DB Browser for SQLite. You may create your databases within this application or use the DatabaseManager.py utilities

https://sqlitebrowser.org/
