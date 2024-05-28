# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Julia,05/26/2024,Edited assignment07-starter
# ------------------------------------------------------------------------------------------ #

# Lets us work with json files
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str  # Hold the choice made by the user.

class Person:
    """ This is the person class

    """
    def __init__(self,
                 first_name: str = '',
                 last_name: str = ''):

        # Check to make sure the given values are strings, otherwise error
        if isinstance(first_name, str) and isinstance(last_name, str):
            self._first_name = first_name
            self._last_name = last_name
        else:
            raise TypeError('First Name and Last Name must be strings')

    def get_first_name(self):
        """ Allows us to get the first name"""
        return self._first_name

    def get_last_name(self):
        """ Allows us to get the last name"""
        return self._last_name

    def set_first_name(self, first_name):
        """ Allows us to set the first name"""
        if isinstance(first_name, str):
            self._first_name = first_name
        else:
            raise TypeError('first_name must be a string.')

    def set_last_name(self, last_name):
        """ Allows us to set the last name"""
        if isinstance(last_name, str):
            self._last_name = last_name
        else:
            raise TypeError('last_name must be a string.')

    def __str__(self):
        return f'{self._first_name}, {self._last_name}'


class Student(Person):
    """ This is a student class which inherits attributes from Person object
    """
    def __init__(self,
                 first_name: str = '',
                 last_name: str = '',
                 course_name: str = ''):
        """ Super allows to take attributes from Person object
        """
        super().__init__(first_name, last_name)

        if isinstance(course_name, str):
            self._course_name = course_name
        else:
            raise TypeError('course_name must be a string.')

    def get_course_name(self):
        return self._course_name

    def set_course_name(self, course_name):
        if isinstance(course_name, str):
            self._course_name = course_name
        else:
            raise TypeError('course_name must be a string.')


    def __str__(self):
        """
        Basically, allows the class to return a formatted string when called within a print function
        :return: comma separated string first name, last name, course name
        """
        return f'{self._first_name}, {self._last_name}, {self._course_name}'


# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """ This function reads data from a json file and loads it into a list of Student objects

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Julia Westfall,5/26/2024,Updated function to load data into a list of Student objects.

        :param file_name: string data with name of file to read from
        :param student_data: list of Student objects to be filled with file data

        :return: list
        """
        try:
            file = open(file_name, "r")
            temp_student_data = json.load(file)
            file.close()

            # load the data into Student objects and append them to student_data
            for student in temp_student_data:
                _student = Student(first_name=student['FirstName'],
                                   last_name=student['LastName'],
                                   course_name=student['CourseName'])
                student_data.append(_student)

        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)
        finally:
            if file.closed == False:
                file.close()

        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a json file with data from a list of Student objects

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :param file_name: string data with name of file to write to
        :param student_data: list of objects to be writen to the file

        :return: None
        """

        # create the list of dicts to be written
        output_data_list = []
        for student in student_data:
            output_data_list.append({
                'FirstName': student.get_first_name(),
                'LastName': student.get_last_name(),
                'CourseName': student.get_course_name()
            })

        # Dumping output_data_list into the json file
        try:
            file = open(file_name, "w")
            json.dump(output_data_list, file)
            file.close()

            # Prints out the data we are dumping into json
            IO.output_student_and_course_names(student_data=student_data)
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message, error=e)
        finally:
            if file.closed == False:
                file.close()


# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    RRoot,1.2.2030,Added menu output and input functions
    RRoot,1.3.2030,Added a function to display the data
    RRoot,1.4.2030,Added a function to display custom error messages
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays custom error messages to the user

        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function

        :param message: string with message data to display
        :param error: Exception object with technical message to display

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function


        :return: None
        """
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message

        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list):
        """ This function displays the student and course names to the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :param student_data: list of dictionary rows to be displayed

        :return: None
        """

        print("-" * 50)
        for student in student_data:
            print(f'Student {student.get_first_name()} '
                  f'{student.get_last_name()} is enrolled in {student.get_course_name()}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the student's first name and last name, with a course name from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :param student_data: list of dictionary rows to be filled with input data

        :return: list
        """

        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            course_name = input("Please enter the name of the course: ")
            student = Student(first_name=student_first_name,
                              last_name=student_last_name,
                              course_name=course_name)
            student_data.append(student)
            print()
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="One of the values was the correct type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data


# Start of main body

# When the program starts, read the file data into a list of lists (table)
# Extract the data from the file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while (True):

    # Present the menu of choices
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_and_course_names(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, or 3")

print("Program Ended")
