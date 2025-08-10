import customtkinter
from tkinter import filedialog
import styles
import pdfgeneration
from databasemanagement import read_class_grades
from CTkMessagebox import CTkMessagebox
import export

class exportpage(customtkinter.CTkFrame):
    def __init__(self, app):
        self.custom_export_email = ""
        self.export_location = ""
        super().__init__(app.main_container)
        self.app = app
        self.export_frame = self
        self.toplevel_window = None
        self.email_popup_window = None
        self.select_classes = customtkinter.CTkLabel(self.export_frame, text="Select classes to export",
                                                corner_radius= 20,
                                                **styles.DefaultLabel,
                                                width = 250,
                                                height = 50
                                                )
        self.select_classes.grid(row = 0, column = 0, padx = 30, pady = 10)

        self.export_classes_frame = customtkinter.CTkScrollableFrame(self.export_frame, 
                                                                     width = 250, height = 350)
        self.export_classes_frame.grid(row = 1, column = 0, rowspan = 10, padx = 15, pady = 10)

        self.send_to_email_label = customtkinter.CTkLabel(self.export_frame, text="Send to Email",
                                        corner_radius= 20,
                                        **styles.DefaultLabel,
                                        width = 250,
                                        height = 50
                                        )
        self.send_to_email_label.grid(row = 0, column = 1, padx = 30, pady = 10)

        self.var = customtkinter.IntVar()
        self.email_choice_default = customtkinter.CTkRadioButton(self.export_frame, 
                                                                 text = "Default Email: " + self.app.get_default_email(), 
                                                                 variable = self.var, value = 1, 
                                                                 command = None)
        self.email_choice_default.grid(row = 1, column = 1, padx = 10)

        self.email_choice_custom = customtkinter.CTkRadioButton(self.export_frame, 
                                                                text = "Custom Email", 
                                                                variable =self.var, value = 2, 
                                                                command = self.generate_custom_email_popup)
        self.email_choice_custom.grid(row = 2, column = 1, padx = 10)

        self.save_to_computer_label = customtkinter.CTkLabel(self.export_frame, text="Save to Computer",
                                        corner_radius= 20,
                                        **styles.DefaultLabel,
                                        width = 250,
                                        height = 50
                                        )
        self.save_to_computer_label.grid(row = 0, column = 2, padx = 30, pady = 10)

        self.select_export_location_button = customtkinter.CTkButton(self.export_frame, text = "Select Location", 
                                         fg_color="gray",
                                         hover_color="#5e5e5e",
                                         width = 100,
                                         height = 30,
                                         command = lambda : self.select_export_location())
        self.select_export_location_button.grid(row = 1, column = 2, padx = 10)

        self.export_location_label = customtkinter.CTkLabel(self.export_frame, text = self.get_export_location(), 
                                                            font = ("Inter", 16), wraplength= 250)
        self.export_location_label.grid(row = 2, column = 2, padx = 10)

        self.generate_pdf_button = customtkinter.CTkButton(self.export_frame, text = "Generate PDF", 
                                         fg_color="gray",
                                         hover_color="#5e5e5e",
                                         width = 100,
                                         height = 30,
                                         command = lambda : self.create_export())
        self.generate_pdf_button.grid(row = 10, column = 2, padx = 10, pady = 10)   

        # Add the invalid_label to the exportpage class
        self.invalid_label = customtkinter.CTkLabel(self.export_frame, 
                                                    text="Please enter a valid Email!", 
                                                    text_color="red",
                                                    width=300, 
                                                    font=("Inter", 20))
        self.invalid_label.grid(row=3, column=1, padx=10, pady=10)
        self.app.hide_widget(self.invalid_label)  # Hide it initially

    def get_export_location(self):
        return self.export_location
    def set_export_location(self,new_location):
        self.export_location = new_location
    
    def get_custom_export_email(self):
        return self.custom_export_email
    def set_custom_export_email(self, new_email):
        self.custom_export_email = new_email

        
    def update_export_class_list(self):    
        self.variable = customtkinter.IntVar()
        self.app.add_variable(self.variable)
        self.checkbox = customtkinter.CTkCheckBox(self.export_classes_frame, 
                                                  text = self.app.get_classes()[-1], variable = self.variable, 
                                                  onvalue="1", offvalue="0")
        self.checkbox.grid(pady = 3)
        self.app.class_checkboxes.append(self.checkbox)


    def generate_custom_email_popup(self):
        if self.email_popup_window is None or not self.email_popup_window.winfo_exists():
            self.email_popup_window = custom_email_popup(self.app, self.close_custom_email_popup)  # Pass the app instance
            self.email_popup_window.attributes("-topmost", True)
    def close_custom_email_popup(self, email):
        self.set_custom_export_email(email)
        self.email_choice_custom.configure(text = self.get_custom_export_email())

    def select_export_location(self):
        self.set_export_location(filedialog.askdirectory())
        self.export_location_label.configure(text = self.get_export_location())


    def generate_pdf(self):
        #retrieving the array of 0's and 1's
        exportvars = self.app.get_variables()
        classes = []
        print(exportvars, self.app.get_classes())
        for i in range (len(exportvars)):
            if exportvars[i].get() == 1:
                #add the data to classes array if chosen by user to export
                classes.append(self.app.get_classes()[i])
        overall_grades = []
        for c in classes:
            arr = []
            class_info = read_class_grades(c)
            for grades_list in class_info.values():
                arr.append(self.app.calculate_overall_grade(grades_list))
            overall_grades.append(arr)

        self.pdfGenerator = pdfgeneration.pdf(classes, overall_grades)
        loc = self.pdfGenerator.pdf_generation()
        return loc

    def create_export(self):
        #firstly, check if user selected a location
        try:
            email = ""
            #check whether the default email or custom email option has been selected
            if self.var.get() == 1 and self.app.get_default_email():
                email = self.app.get_default_email()
            elif self.var.get() == 2:
                email = self.get_custom_export_email()
            loc = self.generate_pdf()
            #create newExport object 
            self.newExport = export.exports(email, loc, self.get_export_location())

            #send out to specified email address and or save to computer 
            if email:
                self.newExport.send_email()
            if self.get_export_location():
                self.newExport.save_to_computer()


            CTkMessagebox(title='Success!', 
                message='Report exported!', sound='on')  
        except Exception as error: 
            print(error)
            CTkMessagebox(title='Error!', 
                message='Something went wrong!', sound='on')  
        return

#custom email popup is a popup where the user can enter a custom email address to send the report to
class custom_email_popup(customtkinter.CTkToplevel):
    def __init__(self, app, on_close_callback):
        super().__init__()  # call the constructor of App.
        self.app = app  # Store the app instance
        self.geometry("300x200")
        self.resizable(False, False)

        self.entry = customtkinter.CTkEntry(self, width=200)
        self.entry.pack(padx=10, pady=10)

        self.submit_button = customtkinter.CTkButton(self, width=100, text="Submit", font=("Inter", 15), command=lambda: self.submit())
        self.submit_button.pack(padx=10, pady=10)

        self.invalid_label = customtkinter.CTkLabel(self, width=100, text="", text_color="red", font=("Inter", 15))
        self.invalid_label.pack(padx=10, pady=10)
        
        self.on_close_callback = on_close_callback

    #retrieve the email address given in the Entrybox
    def get_entry(self):
        return self.entry.get()

    def submit(self):
        email = self.get_entry()
        # Use the app instance to call email_check
        if self.app.email_check(email):
            self.on_close_callback(self.get_entry())
            # destroys the popup
            custom_email_popup.destroy(self)
        else:
            self.invalid_label.configure(text="Invalid Email")
