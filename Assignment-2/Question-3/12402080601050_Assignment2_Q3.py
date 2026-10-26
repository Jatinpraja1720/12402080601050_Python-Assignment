import csv
import mysql.connector
from mysql.connector import Error

# Connect to MySQL and process student records
def main():
    connection = None
    cursor = None

    try:
        # Get database details
        user = input("Enter MySQL username: ").strip()
        password = input("Enter MySQL password: ")
        database = input("Enter database name: ").strip()

        course_id = input("Enter course ID: ").strip()
        spi_threshold = float(input("Enter SPI threshold: "))

        # Validate input
        if not user or not database or not course_id:
            print("Error: Fields cannot be empty.")
            return

        if not 0 <= spi_threshold <= 10:
            print("Error: SPI must be between 0 and 10.")
            return

        # Connect to MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user=user,
            password=password,
            database=database
        )

        cursor = connection.cursor()

        # Create Student table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Student (
                student_id INT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                spi DECIMAL(3,1) NOT NULL
            )
        """)

        # Create CourseRegistration table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS CourseRegistration (
                student_id INT,
                course_id VARCHAR(20),
                PRIMARY KEY (student_id, course_id),
                FOREIGN KEY (student_id)
                    REFERENCES Student(student_id)
            )
        """)

        # Add indexes for searching
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_spi
            ON Student(spi)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_course
            ON CourseRegistration(course_id)
        """)

        connection.commit()

        # Read and insert students in batches
        batch = []

        with open("student.csv", "r", newline="",
                  encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                student_id = int(row["student_id"])
                name = row["name"].strip()
                spi = float(row["spi"])

                if not name or not 0 <= spi <= 10:
                    raise ValueError("Invalid student record.")

                batch.append((student_id, name, spi))

                if len(batch) == 1000:
                    cursor.executemany("""
                        INSERT INTO Student (student_id, name, spi)
                        VALUES (%s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        name = VALUES(name), spi = VALUES(spi)
                    """, batch)
                    connection.commit()
                    batch.clear()

        if batch:
            cursor.executemany("""
                INSERT INTO Student (student_id, name, spi)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name), spi = VALUES(spi)
            """, batch)
            connection.commit()

        # Read and insert course registrations in batches
        batch = []

        with open("registration.csv", "r", newline="",
                  encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                student_id = int(row["student_id"])
                registered_course = row["course_id"].strip()

                if not registered_course:
                    raise ValueError("Invalid course ID.")

                batch.append((student_id, registered_course))

                if len(batch) == 1000:
                    cursor.executemany("""
                        INSERT IGNORE INTO CourseRegistration
                        (student_id, course_id)
                        VALUES (%s, %s)
                    """, batch)
                    connection.commit()
                    batch.clear()

        if batch:
            cursor.executemany("""
                INSERT IGNORE INTO CourseRegistration
                (student_id, course_id)
                VALUES (%s, %s)
            """, batch)
            connection.commit()

        # Find students registered for the selected course
        # whose SPI is greater than the threshold
        cursor.execute("""
            SELECT s.student_id, s.name, s.spi, r.course_id
            FROM Student s
            JOIN CourseRegistration r
                ON s.student_id = r.student_id
            WHERE r.course_id = %s AND s.spi > %s
            ORDER BY s.spi DESC, s.student_id ASC
        """, (course_id, spi_threshold))

        results = cursor.fetchall()

        # Display results
        for student_id, name, spi, registered_course in results:
            print(student_id, name, float(spi), registered_course)

        if not results:
            print("No matching students found.")

    except FileNotFoundError as error:
        print("CSV file not found:", error)

    except (ValueError, KeyError) as error:
        print("Invalid input or CSV data:", error)

    except Error as error:
        print("MySQL error:", error)

    except OSError as error:
        print("File error:", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()
