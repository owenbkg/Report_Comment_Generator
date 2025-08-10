import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def initialize_firebase():
  firebase_config = {

  }

  cred = credentials.Certificate(firebase_config)
  firebase_admin.initialize_app(cred, {
  })

def write_new_class(data):
  #create a reference to the class 
  class_ref = db.reference('classes')
  #data[0][:-5] is the class name 
  class_ref.child(data[0][:-5]).set(data[0][:-5])
  #data[1] is the dictionary of students and their grades
  for student in data[1]:
    student_data = {"critA" : data[1][student][0], "critB" : data[1][student][1], 
                    "critC" : data[1][student][2],"critD" : data[1][student][3],
                    "comment" : " "}
    #writing the student data to the database 
    class_ref.child(data[0][:-5]).child(student).set(student_data)

def remove_class(class_name):
  class_ref = db.reference(f'classes/{class_name}')
  class_ref.delete()

def read_class_grades(class_name):
  # FUNCTION READS DATA OF A SPECIFIC CLASS
  class_ref = db.reference(f'classes/{class_name}')
  class_data = class_ref.get()
  class_dict = {}
  if class_data:
      for student_key, student_data in class_data.items():
          student_name = student_key
          #get the criterion marks 
          crit_a = student_data.get("critA", 0)
          crit_b = student_data.get("critB", 0)
          crit_c = student_data.get("critC", 0)
          crit_d = student_data.get("critD", 0)
          #set the value of the student key to the array of grades
          class_dict[student_name] = [crit_a, crit_b, crit_c, crit_d]
  return class_dict

def read_class_comments(class_name):
  # FUNCTION READS DATA OF A SPECIFIC CLASS
  class_ref = db.reference(f'classes/{class_name}')
  class_data = class_ref.get()
  class_dict = {}
  if class_data:
      for student_key, student_data in class_data.items():
          student_name = student_key
          class_dict[student_name] = student_data.get("comment")
  return class_dict

#read the student comments of a specific class
def read_student_comments(class_name, student_name):
  student_ref = db.reference(f'classes/{class_name}/{student_name}')
  return student_ref.get()["comment"]

#get the list of student names
def get_class_list():
  class_ref = db.reference('classes')
  classes = class_ref.get()
  if classes:
    return list(classes)
  else:
     return None

def write_new_comment(student, student_class, comment):
   #create a reference to the class with name student_clas
   class_ref = db.reference(f'classes/{student_class}')
   #write the comment to the database
   class_ref.child(student).child('comment').set(comment)
   return



