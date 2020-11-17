import sqlite3

class SQLighter:
    def __init__(self, database_file):
        """Connection to database and save the cursor"""
        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()

    def get_subscriptions(self, status=False):
        """Get all active subscribers"""
        with self.conn:
            return self.cursor.execute("SELECT * FROM `cities` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        """Check out if subscriber is in database"""
        with self.conn:
            result = self.cursor.execute("SELECT * FROM `cities` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_subcriber(self, user_id, town="Moscow"):
        """Add new subscriber"""
        with self.conn:
            return self.cursor.execute("INSERT INTO `cities` (`user_id`, `city`) VALUES (?, ?)", (user_id, town))

    def update_town(self, user_id, town):
        """Close connection"""
        with self.conn:
            return self.cursor.execute("UPDATE `cities` SET `city` = ? WHERE `user_id` = ?", (town, user_id))

    def update_status(self, user_id, status=True):
        """Close connection"""
        with self.conn:
            return self.cursor.execute("UPDATE `cities` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def get_town(self, user_id):
        """Gets subscriber's town"""
        return self.cursor.execute("SELECT `city` FROM `cities` WHERE `user_id` = ?", (user_id,)).fetchall()[0][0]

    def get_status(self, user_id):
        return self.cursor.execute("SELECT `status` FROM `cities` WHERE `user_id` = ?", (user_id,)).fetchall()[0][0]

    def close(self):
        return self.conn.close()

def main():
    db = SQLighter("database.db")
    print(db.get_subscriptions(True))

if __name__ == "__main__":
    main()