from .db import Database

class Hub:
    def __init__(self, db_type="sqlite"):
        self.db = Database(db_type)
        self.db.create_table()  

    def pull(self, prompt_type: str, substitutions: dict = None) -> dict:
        """Fetches a prompt configuration by prompt_type.
        If a code_snippet is provided, it replaces the {code_snippet} placeholder
        in the system_message. Returns a dictionary with the configuration if found,
        otherwise None.
        """
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            if self.db.db_type == "postgres":
                query = (
                    "SELECT prompt_type, description, system_message, human_message, structured_output, output_format "
                    "FROM prompt_configurations WHERE prompt_type = %s"
                )
            else:
                query = (
                    "SELECT prompt_type, description, system_message, human_message, structured_output, output_format "
                    "FROM prompt_configurations WHERE prompt_type = ?"
                )
            cursor.execute(query, (prompt_type,))
            result = cursor.fetchone()
            if result:
                config = {
                    "prompt_type": result[0],
                    "description": result[1],
                    "system_message": result[2],
                    "human_message": result[3],
                    "structured_output": bool(result[4]),
                    "output_format": result[5]
                }
                # If a code snippet is provided, substitute it into the system_message
                if substitutions is not None:
                    config["system_message"] = config["system_message"].format(**substitutions)
                return config
            else:
                return None
        finally:
            conn.close()


    def create(self, prompt_type: str, description: str, system_message: str, human_message: str, structured_output: bool = False, output_format: str = "") -> bool:
        """Creates a new prompt configuration."""
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            if self.db.db_type == "postgres":
                query = (
                    "INSERT INTO prompt_configurations (prompt_type, description, system_message, human_message, structured_output, output_format) "
                    "VALUES (%s, %s, %s, %s, %s, %s)"
                )
            else:
                query = (
                    "INSERT INTO prompt_configurations (prompt_type, description, system_message, human_message, structured_output, output_format) "
                    "VALUES (?, ?, ?, ?, ?, ?)"
                )
            if self.db.db_type == "postgres":
                structured_output_val = structured_output  # Pass True/False directly
            else:
                structured_output_val = 1 if structured_output else 0  # 1 or 0 for SQLite

            cursor.execute(
                query,
                (prompt_type, description, system_message, human_message, structured_output_val, output_format)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error creating prompt: {e}")
            return False
        finally:
            conn.close()

    def update(self, prompt_type: str, description: str = None, system_message: str = None, human_message: str = None, structured_output: bool = None, output_format: str = None) -> bool:
        """Updates an existing prompt configuration. Only provided fields will be updated."""
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            fields = []
            params = []
            if description is not None:
                fields.append("description = %s" if self.db.db_type == "postgres" else "description = ?")
                params.append(description)
            if system_message is not None:
                fields.append("system_message = %s" if self.db.db_type == "postgres" else "system_message = ?")
                params.append(system_message)
            if human_message is not None:
                fields.append("human_message = %s" if self.db.db_type == "postgres" else "human_message = ?")
                params.append(human_message)
            if structured_output is not None:
                fields.append("structured_output = %s" if self.db.db_type == "postgres" else "structured_output = ?")
                params.append(1 if structured_output else 0)
            if output_format is not None:
                fields.append("output_format = %s" if self.db.db_type == "postgres" else "output_format = ?")
                params.append(output_format)
            if not fields:
                return True
            if self.db.db_type == "postgres":
                query = "UPDATE prompt_configurations SET " + ", ".join(fields) + " WHERE prompt_type = %s"
            else:
                query = "UPDATE prompt_configurations SET " + ", ".join(fields) + " WHERE prompt_type = ?"
            params.append(prompt_type)
            cursor.execute(query, tuple(params))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating prompt: {e}")
            return False
        finally:
            conn.close()

    def delete(self, prompt_type: str) -> bool:
        """Deletes a prompt configuration by prompt_type."""
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            if self.db.db_type == "postgres":
                query = "DELETE FROM prompt_configurations WHERE prompt_type = %s"
            else:
                query = "DELETE FROM prompt_configurations WHERE prompt_type = ?"
            cursor.execute(query, (prompt_type,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting prompt: {e}")
            return False
        finally:
            conn.close()

# Singleton instance
def init(db_type="sqlite"):
    """Initialize Hub with a database type."""
    return Hub(db_type)
