from fpdf import FPDF
from databasemanagement import read_class_comments
from datetime import datetime
import os

class pdf():
    def __init__(self, selected_classes, overall_grades):
        self.selected_classes = selected_classes
        self.overall_grades = overall_grades

    def pdf_generation(self):
        #get the data from each class first
        classes_data = {}
        for c in self.selected_classes:
            classes_data[c] = read_class_comments(c)
        #creating the PDF 
        pdf = FPDF('P',  'mm', 'A4')    
        pdf.add_page()
        pdf.set_font('helvetica', '', 16)
        i = 0
        print(classes_data)
        for class_name, students in classes_data.items():
            k = 0
            pdf.cell(0, 10, class_name, 0, 1)
            pdf.set_font('helvetica', '', 12)
            for student in students:
                pdf.cell(0, 6, '  '.join([student, str(self.overall_grades[i][k])]),  0, 1)
                if (classes_data[class_name][student] != ' '):
                    print(student, classes_data[class_name][student])
                    pdf.write(6, classes_data[class_name][student])
                    pdf.ln(10)
                else:
                    print("no comment")
                k+=1
            pdf.set_font('helvetica', '', 16)
            pdf.ln()
            i+=1
        # Save the PDF
        now = datetime.now()
        directory = r""
        name = 'Report_' + now.strftime("%H.%M.%S") +'.pdf'
        file_path = os.path.join(directory,name)
        pdf.output(file_path, 'F')   
        return file_path

