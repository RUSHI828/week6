import json
from abc import ABC, abstractmethod


# ---------- ABSTRACTION ----------
class Person(ABC):

    def __init__(self, name, age):
        self.name = name
        self.age = age

    @abstractmethod
    def show_details(self):
        pass


# ---------- INHERITANCE ----------
class Student(Person):

    def __init__(self, name, age, marks):
        super().__init__(name, age)
        self.__marks = marks  # Encapsulation

    def get_marks(self):
        return self.__marks

    def set_marks(self, marks):
        self.__marks = marks

    # ---------- POLYMORPHISM ----------
    def show_details(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Marks: {self.__marks}")
        print("-" * 30)

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "marks": self.__marks
        }


# ---------- MAIN PROJECT ----------
class StudentManagementSystem:

    def __init__(self):
        self.students = []
        self.filename = "students.json"
        self.load_students()

    # Load records from file
    def load_students(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)

            self.students = [
                Student(item["name"], item["age"], item["marks"])
                for item in data
            ]

        except FileNotFoundError:
            self.students = []

        except (json.JSONDecodeError, KeyError, TypeError):
            print("Warning: Student data file is invalid.")
            self.students = []

    # Save records to file
    def save_students(self):
        try:
            with open(self.filename, "w") as file:
                json.dump(
                    [student.to_dict() for student in self.students],
                    file,
                    indent=4
                )
        except OSError:
            print("Error: Could not save student records.")

    # Add student
    def add_student(self):
        name = input("Enter student name: ").strip()

        if not name:
            print("Name cannot be empty.")
            return

        try:
            age = int(input("Enter student age: "))
            marks = float(input("Enter student marks (0-100): "))

            if age <= 0:
                print("Age must be greater than zero.")
                return

            if marks < 0 or marks > 100:
                print("Marks must be between 0 and 100.")
                return

        except ValueError:
            print("Please enter valid numbers for age and marks.")
            return

        student = Student(name, age, marks)
        self.students.append(student)
        self.save_students()

        print("Student added successfully!")

    # Show all students
    def show_students(self):
        if not self.students:
            print("No student records found.")
            return

        print("\n===== ALL STUDENTS =====")

        for student in self.students:
            student.show_details()

    # Search student
    def search_student(self):
        name = input("Enter student name to search: ").strip().lower()

        for student in self.students:
            if student.name.lower() == name:
                student.show_details()
                return

        print("Student not found.")

    # Update student marks
    def update_student(self):
        name = input("Enter student name to update: ").strip().lower()

        for student in self.students:
            if student.name.lower() == name:

                try:
                    marks = float(input("Enter new marks (0-100): "))

                    if marks < 0 or marks > 100:
                        print("Marks must be between 0 and 100.")
                        return

                except ValueError:
                    print("Please enter valid marks.")
                    return

                student.set_marks(marks)
                self.save_students()

                print("Student updated successfully!")
                return

        print("Student not found.")

    # Delete student
    def delete_student(self):
        name = input("Enter student name to delete: ").strip().lower()

        for student in self.students:
            if student.name.lower() == name:
                self.students.remove(student)
                self.save_students()

                print("Student deleted successfully!")
                return

        print("Student not found.")

    # Main menu
    def run(self):
        while True:
            print("\n===== STUDENT MANAGEMENT SYSTEM =====")
            print("1. Add Student")
            print("2. Show All Students")
            print("3. Search Student")
            print("4. Update Student Marks")
            print("5. Delete Student")
            print("6. Exit")

            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Please enter a number from 1 to 6.")
                continue

            if choice == 1:
                self.add_student()

            elif choice == 2:
                self.show_students()

            elif choice == 3:
                self.search_student()

            elif choice == 4:
                self.update_student()

            elif choice == 5:
                self.delete_student()

            elif choice == 6:
                print("Thank you for using Student Management System!")
                break

            else:
                print("Invalid choice. Please try again.")


# ---------- PROGRAM STARTS HERE ----------
if __name__ == "__main__":
    system = StudentManagementSystem()
    system.run()



