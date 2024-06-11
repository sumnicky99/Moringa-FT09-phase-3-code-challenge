# Import the get_db_connection function from the database.connection module
from database.connection import get_db_connection

# Define the Author class
class Author:
    # Define the constructor (__init__) method to initialize Author instances
    def __init__(self, id, name):
        # Assign the id and name attributes
        self._id = id
        self.name = name

    # Define a property for the id attribute
    @property
    def id(self):
        return self._id
    
    # Define a property for the name attribute
    @property
    def name(self):
        # Check if the name attribute has been set
        if not hasattr(self, '_name'):
            # Establish a database connection
            conn = get_db_connection()
            # Create a cursor object to execute SQL queries
            cursor = conn.cursor()
            # Execute an SQL SELECT query to fetch the name from the database using the id
            cursor.execute('SELECT name FROM authors WHERE id = ?', (self._id,))
            # Fetch the result of the query
            result = cursor.fetchone()
            # Close the database connection
            conn.close()
            # If a result is found, set the name attribute
            if result:
                self._name = result[0]
            else:
                # Raise a ValueError if the name is not found in the database
                raise ValueError("Name not found in database")
        # Return the name attribute
        return self._name
    
    # Define a setter method for the name property
    @name.setter
    def name(self, value):
        # Check if the value is a string
        if not isinstance(value, str):
            # Raise a ValueError if the value is not a string
            raise ValueError("Name must be a string")
        # Check if the length of the name is greater than 0
        if len(value) == 0:
            # Raise a ValueError if the length of the name is 0
            raise ValueError("Name must be longer than 0 characters")
        # Set the name attribute
        self._name = value
    
    # Define a method to fetch articles associated with the author
    def articles(self):
        # Import the Article class
        from models.article import Article
        # Establish a database connection
        conn = get_db_connection()
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()
        # Execute an SQL SELECT query to fetch articles written by the author
        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self.id,))
        # Fetch all rows returned by the query
        articles = cursor.fetchall()
        # Close the database connection
        conn.close()
        # Return a list of Article instances created from the fetched articles
        return [Article(article['id'], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in articles]
    
    # Define a method to fetch magazines associated with the author
    def magazines(self):
        # Import the Magazine class
        from models.magazine import Magazine
        # Establish a database connection
        conn = get_db_connection()
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()
        # Execute an SQL SELECT query to fetch distinct magazines where the author has published articles
        cursor.execute('''
            SELECT DISTINCT magazines. * FROM magazines
            INNER JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self._id,))
        # Fetch all rows returned by the query
        magazines = cursor.fetchall()
        # Close the database connection
        conn.close()
        # Return a list of Magazine instances created from the fetched magazines
        return [Magazine(magazine['id'], magazine['name'], magazine['category']) for magazine in magazines]

    # Define the string representation (__repr__) method for Author instances
    def __repr__(self):
        # Return a string representation of the Author object
        return f'<Author {self.name}>'
