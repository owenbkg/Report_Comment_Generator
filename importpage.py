import customtkinter
from customtkinter import filedialog
from tkinterdnd2 import DND_ALL
from CTkMessagebox import CTkMessagebox


import excelmanagement

class importpage(customtkinter.CTkFrame):
    def __init__(self,app):

        self.app = app
        super().__init__(app.main_container)
        self.import_frame = self
        
        #create the box widget as a placeholder for the drag and drop
        self.entryWidget = customtkinter.CTkEntry(self.import_frame, width = 300, height = 200)
        self.entryWidget.configure(state = 'readonly')
        self.entryWidget.pack(padx=5, pady=10)

        self.pathLabel = customtkinter.CTkLabel(self.import_frame, text="Drag and drop file in the entry box, or select a file from your computer.")
        self.import_location_label = customtkinter.CTkLabel(self.import_frame, text = "No file chosen")

        #set the box widget as the target for the drag and drop
        self.entryWidget.drop_target_register(DND_ALL)
        self.entryWidget.dnd_bind("<<Drop>>", self.get_path)

        self.import_select_location_button = customtkinter.CTkButton(self.import_frame, text = "Select Location", 
                                         fg_color="gray",
                                         hover_color="#5e5e5e",
                                         width = 100,
                                         height = 30,
                                         command = lambda : self.select_import_location())
        self.import_select_location_button.pack( padx = 10, pady = 5)
        self.pathLabel.pack()
        self.import_location_label.pack( padx = 10, pady = 5)
    
        self.import_save_button = customtkinter.CTkButton(self.import_frame, text = "Import",                   
                                        fg_color="gray",
                                        hover_color="#5e5e5e",
                                        width = 100,
                                        height = 30,
                                        command = lambda : self.save_new_import())
        self.import_save_button.pack( padx = 10, pady = 10)

    #allows user to select an Excel file from their computer 
    def select_import_location(self):
        self.app.set_temp_import_location(filedialog.askopenfilename(title="Select a File", filetypes=[("Text files", "*.xlsx"), ("All files", "*.*")]))
        if len(self.app.get_temp_import_location()) != 0 :
            self.import_location_label.configure(text = self.app.get_temp_import_location())

    def save_new_import(self):
        #saves a new import to the firebase database
        #create an excel reader object to read the imported excel file
        excel_reader = excelmanagement.excel_reader()
        temp = excel_reader.create_class_dict(self.app.get_temp_import_location())
        if temp:
            #check for overwrites
            if temp[0][:-5] not in self.app.get_classes():
                self.app.add_new_class(temp)
            elif temp[0][:-5] in self.app.get_classes():
                overwriteMessage = CTkMessagebox(title='Error!', 
                    message='Class Already Exists. Overwrite data?', sound='on', option_1='Yes', option_2='No') 
                response = overwriteMessage.get()  
                #overwrite the data if the user chooses to
                if response == "Yes":
                    self.app.delete_class(temp[0][:-5])
                    self.app.add_new_class(temp)

                else:
                    return
            else:
                #account for exceptions
                CTkMessagebox(title='Error!', 
                    message='Something went wrong!', sound='on')                
                return
        else:
            return
    
    #returns the path of the import 
    def get_path(self, event):
        self.app.set_temp_import_location(event.data.strip('{}'))
        self.import_location_label.configure(text = self.app.get_temp_import_location())