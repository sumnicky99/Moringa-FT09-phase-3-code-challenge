# Import the get_db_connection function from the database.connection module
from database.connection import get_db_connection

# Define the Article class
class Article:
    # Define the constructor (__init__) method to initialize Article instances
    def __init__(self, id, title, content, author_id, magazine_id):
        # Assign the id, title, content, author_id, and magazine_id attributes
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    # Define a method to save the article to the database
    def save(self):
        # Establish a database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        # Execute an SQL INSERT query to insert the article into the articles table
        cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)', 
                    (self.title, self.content, self.author_id, self.magazine_id))
        # Get the last inserted row ID and assign it to the id attribute
        self.id = cursor.lastrowid
        # Commit the transaction and close the database connection
        conn.commit()
        conn.close()

    # Define a property for the title attribute
    @property
    def title(self):
        # Check if the title has been fetched from the database
        if not hasattr(self, '_title'):
            # If not fetched, establish a database connection
            conn = get_db_connection()
            cursor = conn.cursor()
            # Execute an SQL SELECT query to fetch the title from the articles table
            cursor.execute("SELECT title FROM articles WHERE id = ?", (self.id,))
            result = cursor.fetchone()
            # Close the database connection
            conn.close()
            # If title is found, assign it to the _title attribute, otherwise raise an exception
            if result:
                self._title = result[0]
            else:
                raise ValueError("Title not found in database")
        return self._title

    # Define a setter method for the title property
    @title.setter
    def title(self, value):
        # Check if the title has not been set previously
        if not hasattr(self, '_title'):
            # If not set, check if the value is a string and within the specified length range
            if isinstance(value, str) and 5 <= len(value) <= 50:
                self._title = value
            else:
                raise ValueError("Title must be a string and between 5 and 50 characters")
        else:
            raise ValueError("Title cannot be changed after it is set")

    # Define a property for the content attribute
    @property
    def content(self):
        # Similar logic as the title property to fetch content from the database
        if not hasattr(self, '_content'):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT content FROM articles WHERE id = ?", (self.id,))
            result = cursor.fetchone()
            conn.close()
            if result:
                self._content = result[0]
            else:
                raise ValueError("Content not found in database")
        return self._content

    # Define a setter method for the content property
    @content.setter
    def content(self, value):
        # Similar validation as the title setter method
        if not hasattr(self, '_content'):
            if isinstance(value, str):
                self._content = value
            else:
                raise ValueError("Content must be a string")
        else:
            raise ValueError("Content cannot be changed after it is set")

    # Define a property for the author attribute
    @property
    def author(self):
        # Similar logic as the title property to fetch author information from the database
        if not hasattr(self, '_author'):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT authors.name
                FROM articles
                INNER JOIN authors ON articles.author_id = authors.id
                WHERE articles.id = ?
            ''', (self.id,))
            result = cursor.fetchone()
            conn.close()
            if result:
                self._author = result[0]
            else:
                raise ValueError("Author not found in database")
        return self._author

    # Define a property for the magazine attribute
    @property
    def magazine(self):
        # Similar logic as the author property to fetch magazine information from the database
        if not hasattr(self, '_magazine'):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT magazines.name
                FROM articles
                INNER JOIN magazines ON articles.magazine_id = magazines.id
                WHERE articles.id = ?
            ''', (self.id,))
            result = cursor.fetchone()
            conn.close()
            if result:
                self._magazine = result[0]
            else:
                raise ValueError("Magazine not found in database")
        return self._magazine
    
    # Define the string representation (__repr__) method for Article instances
    def __repr__(self):
        # Return a string representation of the Article object
        return f'<Article {self.title}>'
