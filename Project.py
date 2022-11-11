import math

class Project():
    """Class representing a Project"""
    projects = []
    popularity_scores = {}
    max_num_projects = 2

    def __init__(self, name, cap, min_num_law_students):
        self.name = name
        self.active = True
        self.picks = []
        self.current_YLS_picks = []
        self.current_non_YLS_picks = []
        self.scores = {}
        self.choices = []
        self.cap = cap
        self.min_num_law_students = min_num_law_students
        self.popularity_score = 0
        self.num_law_students = 0
        Project.projects.append(self)

    def current_picks(self):
        all_pics = self.current_non_YLS_picks + self.current_YLS_picks
        # print(all_pics)
        all_pics = sorted(all_pics, key=lambda r: self.choices.index(r))
        return all_pics

    def calculate_student_score(self, student)->int:
        """parses student details and calculate score"""
        incrementer = len(Project.projects)
        score: int = 0

        if student.is_preadmitted:
            # print('student preadmitted')
            score += incrementer

        if student.preassignment == self.name:
            # print('student preassigned')
            score += math.inf

        score += student.numerize_student_preferences(self,len(Project.projects))

        if student.num_softs > 0:
            score += incrementer

        return score

    def is_applicant_inserted(self, applicant, picks, for_law_students: bool):
        if not for_law_students:
            cap = self.cap - self.min_num_law_students
        else:
            cap = self.cap
            

        # haven't exceeded capacity
        if len(picks) < cap:
            if not for_law_students:
                print(f"{self.name}'s non-law capacity ({cap}) is not exceeded\n")
            else:
                print(f"{self.name}'s max capacity ({cap}) is not exceeded\n")
            picks.append(applicant)
            picks = sorted(picks, key=lambda r: self.choices.index(r)) # keep em ordered
            applicant.current_project = self
            return True

        print(f"Even though {self.name} capacity ({cap}) is exceeded. let's look at scores\n")
        for idx, pick in enumerate(picks[::-1]):
            
            print(f"{applicant.name}'s score: {self.scores[applicant]}")
            print(f"{pick.name}'s score: {self.scores[pick]}")
            applicant_score = self.scores[applicant]
            pick_score = self.scores[pick]
            if applicant_score > pick_score:
                # capacity is exceeded, but student is higher ranked than
                print(f"Even though {self.name} capacity ({cap}) is exceeded, {applicant.name} is higher ranked than {pick.name}\n")
                # print(idx)
                replaced = pick
                replace_point = picks.index(pick)
                picks[replace_point] = applicant
                # for pick in picks:
                #     print(pick.name)
                applicant.current_project = self
                replaced.find_next()
                return True
  
            if applicant_score == pick_score:
                # capacity is exceeded, but current applicant and any of current picks are equally matched
                user_pick = int(input(f"\n Choose between {applicant.name} (1) and {pick.name} (2) for {self.name}. (Type 1 or 2): "))
                
                if user_pick == 1:
                    # user chose the applicant
                    print(f"You chose {applicant.name}")
                    replaced = pick
                    replace_point = picks.index(pick)
                    picks[replace_point] = applicant

                    applicant.current_project = self
                    replaced.find_next()
                    return True
                else:
                    return False

            print(f"{applicant.name}'s score is smaller than {pick.name}'s score\n")

        return False

    def apply_to(self, applicant):
        print(f"\n{applicant.name} tentatively applies to {self.name}\n")

        if not self.active:
            print(f"{self.name} has been cancelled")
            return False

        print(f"{self.name}'s current picks are:")
        current_picks = self.picks
        for pick in current_picks:
            print(pick.name)
        print(f"\n{self.name}'s capacity is {self.cap}\n")

        if self.num_law_students < self.min_num_law_students:
            print(f"We still need {self.min_num_law_students-self.num_law_students} law student(s) for {self.name}\n")
        else:
            print(f"we have enough law students for {self.name}\n")

        if applicant.is_law_student:
            print(f"{applicant.name} is a YLS student\n")
            return self.is_applicant_inserted(applicant, self.picks, True)
        else:
            print(f"{applicant.name} is not a YLS student\n")
            return self.is_applicant_inserted(applicant, self.picks, False)
