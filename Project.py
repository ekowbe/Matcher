import math

class Project():
    """Class representing a Project"""
    projects = []
    max_num_projects = 2

    def __init__(self, name, cap, min_num_law_students):
        self.name = name
        self.current_YLS_picks = []
        self.current_non_YLS_picks = []
        self.choices = []
        self.cap = cap
        self.min_num_law_students = min_num_law_students
        Project.projects.append(self)

    def current_picks(self):
        all_pics = self.current_non_YLS_picks + self.current_YLS_picks
        # print(all_pics)
        all_pics = sorted(all_pics, key=lambda r: self.choices.index(r))
        return all_pics

    def calculate_student_score(self, student)->int:
        """parses student details and calculate score"""
        score: int = 0

        if student.is_preadmitted:
            score+= 3

        if student.preassignment == self.name:
            score += math.inf

        score += student.numerize_student_preferences(self)

        if student.num_softs > 0:
            score += 3

        return score

    def get_idx(self, applicant, picks):
        """calculate rank of candidate for project"""
        applicant_rank = self.choices.index(applicant)
        print(f"Applicant rank: {applicant_rank}")
        current_ranks = [self.choices.index(c) for c in picks]

        for i, r in enumerate(current_ranks):
            if applicant_rank < r:
                return i

    def is_applicant_inserted(self, applicant, picks, for_law_students_arr: bool):
        if not for_law_students_arr:
            cap = self.cap - self.min_num_law_students
        else:
            cap = self.cap

        print(f"cap is: {cap}")
        current_picks = self.current_picks()
        # haven't exceeded capacity
        if len(current_picks) < cap:
            print(f"{self.name} capacity ({cap}) is not exceeded")
            picks.append(applicant)
            picks = sorted(picks, key=lambda r: self.choices.index(r))
            applicant.current_project = self
            return True

        # capacity is exceeded, but student is higher ranked
        if self.get_pick_rank(applicant) < self.get_pick_rank(picks[-1]):
            print(f"Even though {self.name} capacity ({cap}) is exceeded, {applicant.name} is higher ranked than {picks[-1].name}")
            idx = self.get_idx(applicant, picks)
            print(idx)
            picks.insert(idx, applicant)
            for pick in picks:
                print(pick.name)
            replaced = picks.pop()
            applicant.current_project = self
            replaced.find_next()
            return True
        return False

    def apply_to_2(self, applicant):
        print(f"{applicant.name} tentatively applies to {self.name}")
        print(f"{self.name}'s current picks are:")
        current_picks = self.current_picks()
        for pick in current_picks:
            print(pick.name)
        print(f"{self.name}'s capacity is {self.cap}")

        if len(self.current_YLS_picks) < self.min_num_law_students:
            print(f"We still need {self.min_num_law_students-len(self.current_YLS_picks)} law student for {self.name}")
            if applicant.in_YLS:
                print(f"{applicant.name} is a YLS student")
                return self.is_applicant_inserted(applicant, self.current_YLS_picks, True)
            else:
                print(f"{applicant.name} is not a YLS student")
                return self.is_applicant_inserted(applicant, self.current_non_YLS_picks, False)

        print(f"{applicant.name} is a YLS student, but we have enough law students for {self.name}")
        return self.is_applicant_inserted(applicant, self.current_YLS_picks, True)

    def get_pick_rank(self, applicant):
        return self.choices.index(applicant)
