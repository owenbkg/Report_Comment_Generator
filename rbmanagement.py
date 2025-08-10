import os

class rb_reader():
    def __init__(self, report_bank_location):
        self.report_bank_location = report_bank_location
        
    def unpack(self):
            try:
                assert os.path.isfile(self.report_bank_location)
                with open(self.report_bank_location, "r") as file:
                    lines = file.readlines()
                    curr_crit = "Crit A"
                    #dictionaries for each criteria
                    crit_A_comments = {}
                    crit_B_comments = {}
                    crit_C_comments = {}
                    crit_D_comments = {}
                    criteria = ["Crit A", "Crit B", "Crit C", "Crit D"]
                    #so the program can refer to the dictionaries by their name
                    comments_dict = {
                        "Crit A": crit_A_comments,
                        "Crit B": crit_B_comments,
                        "Crit C": crit_C_comments,
                        "Crit D": crit_D_comments,
                    }
                    for i in range (len(lines)):
                        for crit in criteria:
                            #check if a new criteria has started
                            if crit in lines[i]:
                                curr_crit = crit
                                break
                        #for each crit's 3-4, 5-6, 7-8
                        if lines[i][0].isdigit():
                            curr_grade = lines[i][:3]
                            #get the lines after it
                            arr = []
                            for j in range(i+1 , len(lines)):
                                if lines[j] != '\n':
                                    arr.append(lines[j][1:-2])
                                else:
                                    break
                            #move on to the next criteria 
                            if curr_crit in comments_dict:
                                comments_dict[curr_crit][curr_grade] = arr.copy()   
                    #error checking
                    keys = ["3-4", "5-6", "7-8"]
                    if any(list(comments.keys()) != keys for comments in [crit_A_comments, crit_B_comments, crit_C_comments, crit_D_comments]):
                        return -1
                    return [crit_A_comments, crit_B_comments, crit_C_comments, crit_D_comments]
            except:
                return -1

