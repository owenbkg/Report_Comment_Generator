import customtkinter
import tkinter
from customtkinter import filedialog
from tkinterdnd2 import TkinterDnD
from CTkMessagebox import CTkMessagebox
import styles #defauolt styles
import re
from databasemanagement import initialize_firebase, write_new_class, read_class_grades, get_class_list, remove_class
#from excelmanagement import create_class_dict
import pdfgeneration
import export

#UI
import homepage, importpage, exportpage, settings

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        #frame containing the frame objects
        self.frames = {"Homepage" : None, "Import" : None, 
                "Export" : None, "Settings" : None}
        
        #default email
        self.default_email = "None set"

        #dictionary storing the report bank
        self.rb_data = {}

        #temp import location before the user clicks import 
        self.temp_import_location = ""

        #MYP grade boundaries
        self.myp_gradeboundaries = {
            5: 1,
            9: 2,
            14: 3,
            18:4,
            23:5,
            27:6,
            32:7
        }    
        self.classes = [] #class names
        self.class_buttons = [] #class buttons in the homepage
        self.current_class_dict = {} #dictionary for current class data
        self.student_buttons = [] #buttons for each student 
        self.delete_buttons = [] #delete buttons for the classes 
        self.current_class_page = None #name of class currently open
        self.class_checkboxes = [] #class export options
        self.exportvars = [] #array storing whether the user has decided to export the class
    

        self.TkdndVersion = TkinterDnD._require(self)

        #creates the main container of all the frames
        self.main_container = customtkinter.CTkFrame(self)
        self.main_container.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)
    
        #create the panel for the buttons
        self.selection_panel = customtkinter.CTkFrame(self.main_container, height = 100)
        self.selection_panel.pack(side=tkinter.TOP, fill=tkinter.X, expand=False, padx=10, pady=10)
        #activity panel creation
        self.activity_panel = customtkinter.CTkFrame(self.main_container)
        self.activity_panel.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True, padx=10, pady=10)

        #create objects for each frame/page
        self.homepage_obj = homepage.homepage(self)
        self.import_obj = importpage.importpage(self)
        self.export_obj = exportpage.exportpage(self)
        self.settings_obj = settings.settings(self)

        self.title("Report Bank Generator Application")
        self.geometry('1000x600')
        self.resizable(False, False)


        self.startup_function()

        #buttons for all the pages 
        self.homepage_button = customtkinter.CTkButton(self.selection_panel , text="Homepage", **styles.PageButton, command= self.homepage_selector)
        self.homepage_button.grid(row=0, column=0, padx=20, pady=10)

        self.import_button = customtkinter.CTkButton(self.selection_panel, text="Import New Data", **styles.PageButton, command=self.import_selector)
        self.import_button.grid(row=0, column=1, padx=20, pady=10)

        self.export_button = customtkinter.CTkButton(self.selection_panel, text="Export", **styles.PageButton, command=self.export_selector)
        self.export_button.grid(row=0, column=2, padx=20, pady=10)

        self.settings_button = customtkinter.CTkButton(self.selection_panel, text="Settings", **styles.PageButton, command=self.settings_selector)
        self.settings_button.grid(row=0, column=3, padx=20, pady=10)


    #getters and setters
    def get_default_email(self):
        return self.default_email
    def set_default_email(self, new_email):

        self.default_email = new_email
        self.export_obj.email_choice_default.configure(text = "Default Email: " + self.get_default_email())

    def get_temp_import_location(self):
        return self.temp_import_location
    def set_temp_import_location(self, new_import_location):
        self.temp_import_location = new_import_location

    def get_classes(self):
        return self.classes
    def add_class(self, class_name):
        self.classes.append(class_name)
    def remove_class_from_arr(self, class_name):
        for i in range(len(self.get_classes())):
            if self.get_classes()[i] == class_name:
                self.classes.pop(i)
                break

    def get_current_class_page(self):
        return self.current_class_page
    def set_current_class_page(self, new_page):
        self.current_class_page = new_page

    def get_current_class_dict(self):
        return self.current_class_dict
    def set_current_class_dict(self, new_class_name):
        self.current_class_dict = read_class_grades(new_class_name)

    def get_rb_data(self):
        return self.rb_data
    def set_rb_data(self,new_data):
        self.rb_data = new_data.copy()

    def get_student_buttons(self):
        return self.student_buttons
    def clear_student_buttons(self):
        for button in self.student_buttons:
            button.destroy()
        self.student_buttons.clear()
    def add_student_button(self, new_button):
        self.student_buttons.append(new_button)

    def get_variables(self):
        return self.exportvars
    def add_variable(self, var):
        self.exportvars.append(var)

    def get_report_bank_location(self):
        return self.settings_obj.get_report_bank_location()


    """
    Selectors for each possible frame/class
    """
    #selecting different pages 
    def homepage_selector(self):
        # Hide all frames first
        for frame in self.frames.values():
            if frame is not None:
                frame.pack_forget()
        # Clear the frames dictionary
        for key in self.frames:
            self.frames[key] = None
        # Set and show homepage frame
        self.frames['Homepage'] = self.homepage_obj
        self.frames['Homepage'].pack(in_=self.activity_panel, 
                                     side=tkinter.TOP, fill=tkinter.BOTH, 
                                     expand=True, padx=0, pady=0)

    def import_selector(self):
        for frame in self.frames.values():
            if frame is not None:
                frame.pack_forget()
        for key in self.frames:
            self.frames[key] = None
        self.frames['Import'] = self.import_obj
        self.frames['Import'].pack(in_=self.activity_panel, side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)

    def export_selector(self):
        for frame in self.frames.values():
            if frame is not None:
                frame.pack_forget()
        for key in self.frames:
            self.frames[key] = None
        self.frames['Export'] = self.export_obj
        self.frames['Export'].pack(in_=self.activity_panel, side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)


    def settings_selector(self):
        for frame in self.frames.values():
            if frame is not None:
                frame.pack_forget()
        for key in self.frames:
            self.frames[key] = None
        self.frames['Settings'] = self.settings_obj
        self.frames['Settings'].pack(in_=self.activity_panel, side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)



    #functions
    def email_check(self,email):
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email) and email != "":
            self.show_widget(self.export_obj.invalid_label, "email")
            return False
        self.hide_widget(self.export_obj.invalid_label)
        return True
    
    #add a class to the class list and database
    def add_new_class(self, temp):
        write_new_class(temp)
        self.add_class(temp[0][:-5])
        self.homepage_obj.update_class_button_list(temp[0][:-5])
        self.export_obj.update_export_class_list()
        read_class_grades(temp[0][:-5])
        CTkMessagebox(title='Success!', 
            message='Class Imported!', sound='on')  

    #confirm deletion of a class from the database 
    def delete_confirmation(self, class_name):
        delete_confirmation = CTkMessagebox(title='Warning!', 
            message='Are you sure you want to delete this class?', sound='on', option_1="Yes", option_2="No")
        response = delete_confirmation.get()
        if response == "Yes":
            self.delete_class(class_name)
        else: 
            pass
    
    #delete a class from the database and the UI/class list
    def delete_class(self, class_name):
        #locate index 
        class_idx = self.get_classes().index(class_name)

        #remove all UI elements to do with the class
        self.class_checkboxes[class_idx].destroy()
        self.class_checkboxes.pop(class_idx)
        self.exportvars.remove(self.exportvars[class_idx])

        self.delete_buttons[class_idx].destroy()
        self.delete_buttons.pop(class_idx)

        self.class_buttons[class_idx].destroy()
        self.class_buttons.pop(class_idx)

        #remove the class from the database
        remove_class(class_name)
        self.remove_class_from_arr(class_name)

        #open the next class list if it exists
        if len(self.get_classes()) > 0:
            try:
                self.homepage_obj.change_class_view(self.get_classes()[class_idx+1])
            except:
                self.homepage_obj.change_class_view(self.get_classes()[class_idx-1])
        else:
            self.clear_student_buttons()        


    def hide_widget(self,widget):
        widget.grid_forget()


    def calculate_overall_grade(self, grades):
        #Calculates the overall grade for a student based on their individual grades.
        # Sum the grades
        grades_sum = sum(grades)
        
        # Iterate over the MYP grade boundaries to determine the overall grade
        for boundary in self.myp_gradeboundaries:
            if grades_sum <= boundary:
                return self.myp_gradeboundaries[boundary]
        
        # If no boundary is met, return the highest grade
        return 7    




    def startup_function(self):
        temp = get_class_list()
        if temp:
            for c in temp:
                #add the classes to the homepage
                self.add_class(c)
                self.homepage_obj.update_class_button_list(c)
                self.export_obj.update_export_class_list()
        #set the initial page to the homepage
        self.homepage_selector()


if __name__ == "__main__":
    initialize_firebase()
    instance = App()
    instance.mainloop()


