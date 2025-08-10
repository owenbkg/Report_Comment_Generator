import customtkinter
import styles
import webbrowser #to link to google doc with information
import rbmanagement
from CTkMessagebox import CTkMessagebox
import re #email verification
from tkinter import filedialog


class settings(customtkinter.CTkFrame):
    
    #class variables for storing locations
    report_bank_location = ""
    temp_rb_location = ""

    def __init__(self,app):
        self.app = app
        super().__init__(app.main_container)


        #UI of the page
        self.settings_frame = self
        self.email_label = customtkinter.CTkLabel(self.settings_frame, text="Default Email",
                                        corner_radius= 20,
                                        **styles.DefaultLabel,
                                        width = 300,
                                        height = 50
                                        )
        self.email_label.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.email_entry = customtkinter.CTkEntry(self.settings_frame, 
                                                  placeholder_text= self.app.get_default_email(),width=300, font=("Inter", 20))
        self.email_entry.grid(row = 0, column = 1, columnspan = 2,   padx = 10, pady = 10)
        
        self.invalid_label = customtkinter.CTkLabel(self.settings_frame, 
                                                          text = "Please enter a valid Email!", text_color="red",
                                                          width=300, font=("Inter", 20))
        self.invalid_label.grid(row = 0, column = 2, padx = 10, pady = 10)
        self.app.hide_widget(self.invalid_label)


        self.rb_label = customtkinter.CTkLabel(self.settings_frame, text="Report Bank Location",
                                        corner_radius= 20,
                                        **styles.DefaultLabel,
                                        width = 300,
                                        height = 50
                                        )
        self.rb_label.grid(row = 1, column = 0, padx = 10, pady = 10)



        self.select_location_button = customtkinter.CTkButton(self.settings_frame, text = "Select Location", 
                                         fg_color="gray",
                                         hover_color="#5e5e5e",
                                         width = 100,
                                         height = 30,
                                         command = lambda : self.select_rb_location())
        self.select_location_button.grid(row = 1, column = 1, pady = 10, padx = 10)


        self.guide_button = customtkinter.CTkButton(self.settings_frame, text = "How does the Report Bank work?", 
                                         fg_color="gray",
                                         hover_color="#5e5e5e",
                                         width = 100,
                                         height = 30,
                                         command = lambda: self.open_guide())
        self.guide_button.grid(row = 1, column = 2, pady = 10, padx = 10)


        self.save_button = customtkinter.CTkButton(self.settings_frame, text = "Save Changes", 
                                         corner_radius = 20,
                                         width = 300,
                                         height = 50,
                                         font = ("Inter", 20),
                                         command = lambda : self.save_changes())
        self.save_button.grid(row = 2, column = 0, padx = 10, pady = 10)


    #getters and setters 
    def get_report_bank_location(self):
        return self.report_bank_location
    def set_report_bank_location(self, new_location):
        self.report_bank_location = new_location

    def get_temp_report_bank_location(self):
        return self.temp_rb_location
    def set_temp_report_bank_location(self, new_rb_location):
        self.temp_rb_location = new_rb_location


    #user can choose directory for report bank
    def select_rb_location(self):
        location = filedialog.askopenfilename()
        if location:  # Only set if user didn't cancel
            self.set_temp_report_bank_location(location)

    def open_guide(self):
        webbrowser.open("https://docs.google.com/document/d/1z9CG3u3u3qpjhE0w2TEf2YZIwLolXdpfe2zlEjnGevU/edit",new=1)


    #saves the changes to the program
    def save_changes(self):
        # Save Report Bank changes
        if self.get_temp_report_bank_location() != "":
            #create rb_manager object to read the report bank
            rb_manager = rbmanagement.rb_reader(self.get_temp_report_bank_location())
            rb = rb_manager.unpack()
            if self.rb_check(rb):
                self.app.set_rb_data(rb)
                self.set_report_bank_location(self.get_temp_report_bank_location())
                CTkMessagebox(title='Success!', 
                    message='Report Bank Imported!', 
                    sound='on')
            else:
                CTkMessagebox(title='Warning!', 
                    message='Report Bank Improper Format!', 
                    sound='on')  

        # Save Email changes
        if self.email_entry.get() and self.app.email_check(self.email_entry.get()):
            self.app.set_default_email(self.email_entry.get())
            # Update any UI elements that show the email
            CTkMessagebox(title='Success!', 
                message='Email Updated!', 
                sound='on')
    
    def rb_check(self, rb):
        if rb == -1:
            return False
        else:
            return True
    
    def show_widget(self,widget, error_type):
        if error_type == "rb":
            widget.configure(text = "Invalid RB formatting or location!") 
        elif error_type == "email":
            widget.configure(text = "Invalid Email!") 
        widget.grid()

