import math

class Project():
    """Class representing a Project"""
    projects = []
    popularity_scores = {}
    max_num_projects = 2

    def __init__(self, name, cap, min_num_law_students):
        self.name = name
        self.active = True
        self.current_YLS_picks = []
        self.current_non_YLS_picks = []
        self.scores = {}
        self.choices = []
        self.cap = cap
        self.min_num_law_students = min_num_law_students
        self.popularity_score = 0
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
            score+= incrementer

        if student.preassignment == self.name:
            # print('student preassigned')
            score += math.inf

        score += student.numerize_student_preferences(self)

        if student.num_softs > 0:
            score += incrementer

        return score

    def is_applicant_inserted(self, applicant, picks, for_law_students_arr: bool):
        if not for_law_students_arr:
            cap = self.cap - self.min_num_law_students
        else:
            cap = self.cap

        # TO DO: order the picks before doing anything
        # print(f"cap is: {cap}")
        current_picks = self.current_picks()
        # haven't exceeded capacity
        if len(current_picks) < cap:
            print(f"{self.name} capacity ({cap}) is not exceeded\n")
            picks.append(applicant)
            picks = sorted(picks, key=lambda r: self.choices.index(r)) # keep em ordered
            applicant.current_project = self
            return True

        for idx, pick in enumerate(current_picks[::-1]):
            print(f"Even though {self.name} capacity ({cap}) is exceeded. let's look at scores\n")
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
                user_pick = input(f"\n Choose between {applicant.name} and {pick.name} for {self.name}: ")
                
                if user_pick == applicant.name:
                    # user chose the applicant
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

    def apply_to_2(self, applicant):
        print(f"\n{applicant.name} tentatively applies to {self.name}\n")
        print(f"{self.name}'s current picks are:")
        current_picks = self.current_picks()
        for pick in current_picks:
            print(pick.name)
        print(f"\n{self.name}'s capacity is {self.cap}\n")

        if len(self.current_YLS_picks) < self.min_num_law_students:
            print(f"We still need {self.min_num_law_students-len(self.current_YLS_picks)} law student for {self.name}\n")
            if applicant.is_law_student:
                print(f"{applicant.name} is a YLS student\n")
                return self.is_applicant_inserted(applicant, self.current_YLS_picks, True)
            else:
                print(f"{applicant.name} is not a YLS student\n")
                return self.is_applicant_inserted(applicant, self.current_non_YLS_picks, False)

        print(f"we have enough law students for {self.name}\n")

        return self.is_applicant_inserted(applicant, self.current_YLS_picks, True)
