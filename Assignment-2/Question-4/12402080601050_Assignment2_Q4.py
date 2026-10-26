import mysql.connector
from mysql.connector import Error
import re

# Allowed columns and their database names
columns = {
    "student.id": "s.student_id",
    "student.name": "s.name",
    "student.spi": "s.spi",
    "course.id": "c.course_id",
    "course.name": "c.name",
    "registration.student_id": "r.student_id",
    "registration.course_id": "r.course_id"
}

# Allowed filter operators
operators = ["=", ">", "<", ">=", "<=", "LIKE"]


def main():
    connection = None
    cursor = None

    try:
        # Database connection
        username = input("MySQL username: ").strip()
        password = input("MySQL password: ")
        database = input("Database name: ").strip()

        connection = mysql.connector.connect(
            host="localhost",
            user=username,
            password=password,
            database=database
        )
        cursor = connection.cursor()

        # Create Course table if it does not exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Course (
                course_id VARCHAR(20) PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            )
        """)

        # Add sample courses
        cursor.executemany("""
            INSERT IGNORE INTO Course (course_id, name)
            VALUES (%s, %s)
        """, [
            ("PY101", "Programming with Python"),
            ("DB101", "Database Management Systems")
        ])
        connection.commit()

        # Get selected columns
        selected = input(
            "Columns (comma-separated): "
        ).strip().split(",")

        selected = [x.strip().lower() for x in selected]

        if not selected or any(x not in columns for x in selected):
            print("Error: Invalid column name.")
            return

        # Get filter conditions
        filter_text = input(
            "Filters (example: course.id=PY101), or press Enter: "
        ).strip()

        conditions = []
        parameters = []

        if filter_text:
            filters = filter_text.split(",")

            for item in filters:
                match = re.fullmatch(
                    r"\s*([a-zA-Z_.]+)\s*(>=|<=|=|>|<|LIKE)\s*(.*?)\s*",
                    item,
                    re.IGNORECASE
                )

                if not match:
                    print("Error: Invalid filter format.")
                    return

                field, operator, value = match.groups()
                field = field.lower()
                operator = operator.upper()

                if field not in columns or operator not in operators:
                    print("Error: Invalid column or operator.")
                    return

                if not value:
                    print("Error: Filter value cannot be empty.")
                    return

                conditions.append(
                    columns[field] + " " + operator + " %s"
                )
                parameters.append(value)

        # Get order details
        order_column = input(
            "Order column (example: student.spi): "
        ).strip().lower()

        if order_column not in columns:
            print("Error: Invalid order column.")
            return

        direction = input("Sort direction (ASC/DESC): ").strip().upper()

        if direction not in ["ASC", "DESC"]:
            print("Error: Invalid sort direction.")
            return

        # Get limit
        limit = int(input("Limit (1-1000): "))

        if not 1 <= limit <= 1000:
            print("Error: Limit must be between 1 and 1000.")
            return

        # Build safe SQL
        selected_sql = ", ".join(
            columns[field] for field in selected
        )

        sql = f"""
            SELECT {selected_sql}
            FROM Student s
            JOIN CourseRegistration r
                ON s.student_id = r.student_id
            JOIN Course c
                ON r.course_id = c.course_id
        """

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        sql += f" ORDER BY {columns[order_column]} {direction}"
        sql += " LIMIT %s"
        parameters.append(limit)

        # Display generated SQL and parameters
        print("\nSQL_OK")
        print("Generated SQL:")
        print(sql)
        print("Parameters:", parameters)

        # Execute parameterized query
        cursor.execute(sql, tuple(parameters))
        results = cursor.fetchall()

        # Display result table
        print("\nQuery Results:")
        print(" | ".join(selected))

        for row in results:
            print(" | ".join(str(value) for value in row))

        if not results:
            print("No matching records found.")

    except ValueError:
        print("Error: Enter a valid number for the limit.")

    except Error as error:
        print("Database error:", error)

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()
