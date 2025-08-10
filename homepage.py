import customtkinter
import tkinter
from CTkMessagebox import CTkMessagebox
from functools import partial
from databasemanagement import write_new_comment, read_student_comments
import styles
import genai

class homepage(customtkinter.CTkFrame):
    #A class to represent the homepage of the application.
    def __init__(self, app):
        #Initializes the homepage with the given application object.
        self.app = app
        super().__init__(app.main_container)
        self.homepage_frame = self

        # Creating the sidebar for the different classes
        self.sidebar_container = customtkinter.CTkScrollableFrame(self.homepage_frame, fg_color="#0d233b")
        self.sidebar_container.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=False)

        # Creating the container for the student page
        self.student_page_container = customtkinter.CTkScrollableFrame(self.homepage_frame, fg_color=None)
        self.student_page_container.pack(fill=tkinter.BOTH, expand=True)

        # Creating the combobox for sorting students
        self.sort_combobox = customtkinter.CTkComboBox(
            master=self.student_page_container,
            values=["Alphabetical ascending", "Alphabetical descending", "MYP ascending", "MYP descending"],
            command=self.sorts
        )
        self.sort_combobox.pack(padx=10, pady=10)
        self.sort_combobox.set("Sort by...")

        # Packing the homepage frame into the activity panel
        self.homepage_frame.pack(in_=app.activity_panel, side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)

        # Initializing the top-level window and email popup window as None
        self.toplevel_window = None
        self.email_popup_window = None

    def update_class_button_list(self, class_name):
        #create button for new class 
        new_button = customtkinter.CTkButton(
            self.sidebar_container,
            text=class_name,
            command=partial(self.change_class_view, class_name)
        )
        #delete_class_button
        delete_button = customtkinter.CTkButton(
            self.sidebar_container,
            text = "-",
            fg_color= "#c93437",
            hover_color="#a1282b",
            width = 20,
            command = lambda : self.app.delete_confirmation(class_name)
        )
        # Get the index of the class to place the buttons correctly
        class_idx = self.app.get_classes().index(class_name)
        
        # Place the new class button in the grid
        new_button.grid(row=class_idx, column=0, pady=10, padx=10)
        
        # Place the delete button next to the new class button
        delete_button.grid(row=class_idx, column=1, pady=10, padx=10)
        
        # Append the new buttons to the application's button lists
        self.app.class_buttons.append(new_button)
        self.app.delete_buttons.append(delete_button)


    def change_class_view(self, class_name):
        #Change the view to display the selected class and its students.
        #This method updates the application to show the students of the specified class.
        # Set the current class page and dictionary in the application
        self.app.set_current_class_page(class_name)
        self.app.set_current_class_dict(class_name)
        
        # Clear existing student buttons
        self.app.clear_student_buttons()

        # Iterate over students in the current class dictionary
        for student in self.app.get_current_class_dict():
            # Calculate the student's overall grade
            overall_grade = self.app.calculate_overall_grade(self.app.get_current_class_dict()[student])
            
            # Create a partial function to open the student page
            open_student_page_partial = partial(self.open_student_page, student)
            
            # Add a new student button to the application
            self.app.add_student_button(customtkinter.CTkButton(
            self.student_page_container, 
            anchor="w",
            text=f"{student} |  {overall_grade}", 
            font=("Inter", 15), 
            width=500, 
            command=open_student_page_partial
            ))
            
            # Pack the new student button with padding
            self.app.get_student_buttons()[-1].pack(pady=10)


    def open_student_page(self, student):
        #Opens the student page for the given student.
        #If the report bank location is not set, shows an error message.
        #If the top-level window does not exist, creates a new student window.
        # Check if the report bank location is set
        if not self.app.get_report_bank_location():
            # Show an error message if the report bank location is not set
            CTkMessagebox(title='Error!', 
            message='Import a report bank to edit comments!', sound='on')  
            return
        
        # Check if the top-level window does not exist
        if (self.toplevel_window is None or not self.toplevel_window.winfo_exists()):
            # Get the grades for the student
            grades = self.app.get_current_class_dict()[student]
            
            # Create a new student window
            self.toplevel_window = student_window(student, grades, self.app.get_current_class_page(), self.app.get_rb_data()) 
            
            # Set the window to be always on top
            self.toplevel_window.attributes("-topmost", True)

    def sorts(self, sorttype):
        #Sorts the student buttons based on the selected sort type.
        # Firstly unpack all the existing students
        for button in self.app.get_student_buttons():
            button.pack_forget()

        def selectionSort(data):
            #Sorts the data using the selection sort algorithm.
            n = len(data)
            # Using a selection sort
            for i in range(n - 1):
                min_idx = i
                for j in range(i + 1, n):
                    # Compare using the key index
                    if data[j][0] < data[min_idx][0]:
                        min_idx = j
                if min_idx != i:
                    # Swapping the positions if there's a suitable swap
                    data[i], data[min_idx] = data[min_idx], data[i]
            return data

        def sort_by_name(sorttype):
            #Sorts the students by their names.
            student_names = self.app.get_current_class_dict().keys()
            # Zipping the two together so the student buttons are sorted as well
            name_button_zipped = list(zip(student_names, self.app.get_student_buttons())) 
            # Sort the zipped list using selection sort
            name_button_zipped = selectionSort(name_button_zipped)
            # Reverse the list if sorting in descending order
            if sorttype == "Alphabetical descending":
                name_button_zipped = name_button_zipped[::-1]
            # Recreate the buttons and pack them
            for i in range(len(student_names)):
                name_button_zipped[i][1].pack(pady=10)

        def sort_by_grade(sorttype):
            #Sorts the students by their grades.
            # Get the overall grades for each student
            student_grades = [self.app.calculate_overall_grade(self.app.get_current_class_dict()[student]) for student in self.app.get_current_class_dict().keys()]
            
            # Zip the grades with the corresponding student buttons
            grade_button_zipped = list(zip(student_grades, self.app.get_student_buttons()))
            
            # Sort the zipped list using selection sort
            grade_button_zipped = selectionSort(grade_button_zipped)
            
            # Reverse the list if sorting in descending order
            if sorttype == "MYP descending":
                grade_button_zipped = grade_button_zipped[::-1]
            
            # Recreate the buttons and pack them
            for i in range(len(student_grades)):
                grade_button_zipped[i][1].pack(pady=10)

        # Determine the sorting method based on the sort type
        if sorttype == "MYP ascending" or sorttype == "MYP descending":
            sort_by_grade(sorttype)
        else:
            sort_by_name(sorttype)

class student_window(customtkinter.CTkToplevel):
    #A class to represent the student window.
    def get_comments(self, grades, rb):
        #Retrieves comments based on the student's grades and the report bank data.
        # Initialize an empty list to store the categories
        categories = []
        
        # Iterate over the grades to determine the category for each grade
        for grade in grades:
            if grade == 3 or grade == 4:
                categories.append('3-4')
            elif grade == 5 or grade == 6:
                categories.append('5-6')
            elif grade == 7 or grade == 8:
                categories.append('7-8')
        
        # Create a dictionary mapping criteria (A, B, C, D) to the corresponding comments from the report bank
        comment_dict = dict(zip('ABCD', map(lambda i: rb[i][categories[i]], range(4))))
        
        # Return the dictionary containing the comments
        return comment_dict
    
    def generate_comment(self, comments, student):
        #Generates a comment for a student using an AI model and inserts it into the comment box.
        # Check if the comment box already contains text and clear it if necessary
        if len(self.comment_box.get("1.0", "end-1c")):
            self.comment_box.delete('1.0', "end-1c")
        
        # Generate a nedw comment using the AI model and insert it into the comment box
        self.comment_box.insert('1.0', self.ai_model.api_comment_generation(student, comments), tags=None)
    
    def save_changes(self):
        #Saves the changes made in the comment box for a student.
        write_new_comment(self.student,self.student_class, self.comment_box.get("1.0", "end-1c"))
    
    def __init__(self,student,grades, student_class, rb_data):
        #Initializes the homepage window with student data, grades, and comments.
        super().__init__()
        self.geometry("500x800")
        self.resizable(False, False)

        #initializes data from superclass
        self.rb_data = rb_data
        self.student_class = student_class
        self.student = student
        self.saved_comment = read_student_comments(self.student_class, self.student)

        self.comments = self.get_comments(grades, self.rb_data)

        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.name_label = customtkinter.CTkLabel(self.frame, text = student, **styles.DefaultLabel, corner_radius= 20, width = 300)
        self.name_label.pack(pady = 10)

        # Initialize the list of dropdowns
        self.dropdowns = []

        # Initialize the AI model
        self.ai_model = genai.ai_model()

        # Create the labels and dropdowns
        criteria = [
            ('A', grades[0], self.comments['A']),
            ('B', grades[1], self.comments['B']),
            ('C', grades[2], self.comments['C']),
            ('D', grades[3], self.comments['D'])
        ]

        # Create a label and dropdown for each criterion
        for criterion, grade, options in criteria:
            label_text = f"Select Crit {criterion}                       {str(grade)}"
            label = customtkinter.CTkLabel(self.frame, text=label_text, anchor="w", **styles.DefaultLabel, corner_radius=20, width=300)
            label.pack(pady=10)
            
            # Create the dropdown for the criterion 
            dropdown = customtkinter.CTkComboBox(self.frame, values=options, width=300, state='readonly')
            dropdown.pack(pady=5)

            # Store the dropdown in the dictionary
            self.dropdowns.append(dropdown)
                    
        # Create the textbook for the comment
        self.generate_comment_button = customtkinter.CTkButton(self.frame, text = "Generate Comment",                   
                                        fg_color="gray",
                                        hover_color="#5e5e5e",
                                        width = 100,
                                        height = 30,
                                        command = lambda : self.generate_comment([dropdown.get() for dropdown in self.dropdowns], student))
        self.generate_comment_button.pack(pady = 10)

        self.comment_box = customtkinter.CTkTextbox(self.frame, wrap = 'word',  height = 200, width = 300)
        self.comment_box.pack(pady = 5)
        self.comment_box.insert('1.0',self.saved_comment, tags = None)

        # Create the Save Button
        self.save_button = customtkinter.CTkButton(self.frame, text = "Save Changes",                   
                                        fg_color="gray",
                                        hover_color="#5e5e5e",
                                        width = 100,
                                        height = 30,
                                        command = lambda : self.save_changes())
        
        # Pack the window. 
        self.save_button.pack(pady = 10)