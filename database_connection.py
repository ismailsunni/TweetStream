"""Database Connection
For handling database connection.
"""

__author__ = 'ismailsunni'
__project_name = 'TweetStream'
__filename = 'database_connection.py'
__date__ = '28/02/13'
__copyright__ = 'imajimatika@gmail.com'

import MySQLdb

class db_conn:
    # database variable
    db_host = 'localhost'
    db_user = 'root'
    db_password = ''
    db_name = 'tweet_data'

    def __init__(self):
        """Init db class
        """
        self.conn = MySQLdb.connect(self.db_host, self.db_user,
                                    self.db_password, self.db_name)
        self.cursor = self.conn.cursor()

    def read(self, query):
        """Read database.
        """

        try:
            self.cursor.execute(query)
            retval = self.cursor.fetchall()
            return retval

        except MySQLdb.MySQLError, e:
            self.conn.rollback()
            return None

    def insert(self, query):
        """Insert to database.
        """

        try:
            print query
            self.cursor.execute(query)
            print 'a'
            self.conn.commit()
            return True

        except MySQLdb.MySQLError, e:
            self.conn.rollback()
            return False

    def delete(self, query):
        """Delete row(s) in database.
        """

        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True

        except MySQLdb.MySQLError, e:
            self.conn.rollback()
            return False

    def update(self, query):
        """Update database.
        """
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True

        except MySQLdb.MySQLError, e:
            self.conn.rollback()
            return False

    def insert_tweet(self, my_tweet_id, my_text, my_timestamp, my_category,
                    my_sentiment, my_user_id, my_user_name, my_categorized,
                    my_sentimented):
        my_query = 'INSERT INTO `tweets` (`tweet_id`, `text`, `time_stamp`, '
        my_query += '`category`, `sentiment`, `user_id`, `user_name`, '
        my_query += '`categorized`, `sentimented`)'

        my_query += ' VALUES '

        my_query += '("' + my_tweet_id + '","' + my_text + '","' + str(my_timestamp) + '","' + my_category + '","'
        my_query += str(my_sentiment) + '","' + my_user_id + '","' + my_user_name + '","' + str(my_categorized) + '","'
        my_query += str(my_sentimented) + '")'

        return self.insert(my_query)