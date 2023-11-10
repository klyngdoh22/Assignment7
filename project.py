import sqlite3

class ProjectDB:
    def __init__(self, db_name='projects.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            image_filename TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_project(self, title, description, image_filename):
        query = "INSERT INTO projects (title, description, image_filename) VALUES (?, ?, ?)"
        self.conn.execute(query, (title, description, image_filename))
        self.conn.commit()

    def get_projects(self):
        query = "SELECT * FROM projects"
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def delete_project(self, project_id):
        query = "DELETE FROM projects WHERE id = ?"
        self.conn.execute(query, (project_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

# Example usage:
if __name__ == "__main__":
    db = ProjectDB()
    db.add_project('Sample Project', 'This is a sample project description.', 'sample_image.png')
    projects = db.get_projects()
    for project in projects:
        print(project)
    # db.delete_project(project_id=1)  
