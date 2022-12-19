import math
import models.tiebreak_dialog as tiebreak_dialog

class Project():
    """Class representing a Project"""
    projects = []
    popularity_scores = {}
    # max_num_projects = 2

    def __init__(self,
                name,
                cap,
                min_law,
                min_non_law):

        self.active = True
        self.name = name
        self.cap = cap
        self.min_law = min_law
        self.min_non_law = min_non_law

        self.picks = [] # a current list of picks
        self.scores = {}
        self.choices = [] # all 

        self.original_cap = cap

        self.popularity_score = 0
        self.num_law_students = 0
        Project.projects.append(self)

    def calculate_student_score(self, student) -> int:
        """parses student details and calculate score"""
        incrementer: int = len(Project.projects)
        score: int = 0

        if student.is_preadmitted:
            # print('student preadmitted')
            score += incrementer

        if student.preassignment == self.name:
            # print('student preassigned')
            score += math.inf

        # increment score based on student's preference of current proj
        score += student.numerize_student_preferences(
            self, len(Project.projects))

        # factor softs
        if (student.is_returning or 
            student.in_final_year or
            student.is_previously_unsuccessful):
            score += incrementer

        if student.for_capstone:
            score += 1

        # dual degree
        if len(student.degrees) > 1:
            score += 1

        # bidding rank
        score -= (student.bidding_rank - 1)
        return score

    def handle_tiebreak(self, applicant, picks, pick):
        valid_input = False

        while not valid_input:
            try:
                message = f"\n Choose between {applicant.name} (1) and {pick.name} (2) for {self.name}. (Type 1 or 2): "
                dlg = tiebreak_dialog.FixedWidthMessageDialog("Tiebreak!", message)

                if dlg.exec_():
                    print("Success!")
                else:
                    print("Cancel!")

                user_pick = dlg.user_pick
                print(user_pick)
                # user_pick = int(input(
                    # f"\n Choose between {applicant.name} (1) and {pick.name} (2) for {self.name}. (Type 1 or 2): "))
                # print(type(user_pick))
                # make sure they typed 1 or 2
                if user_pick == 1 or user_pick == 2:
                    valid_input = True
                else:
                    print("Invalid input. Type 1 or 2")
                    continue

            except ValueError:
                print("Invalid input. Type 1 or 2")

        if user_pick == 1:
            # user chose the applicant
            print(f"You chose {applicant.name}")
            replaced = pick
            replace_point = picks.index(pick)
            picks[replace_point] = applicant

            applicant.current_project = self
            replaced.find_next()
            return True
        else: # user picked 2
            return False

    def is_applicant_inserted(self, applicant, picks):
        # print(picks)
        # haven't exceeded capacity
        if len(picks) < self.cap:
            print(f"There's room for {self.name}")

            picks.append(applicant)
            # print(picks)

            # keep em ordered
            picks = sorted(picks, key=lambda r: self.choices.index(r))
            applicant.current_project = self
            return True

        print(
            f"{self.name} at capacity. Let's look at the scores\n")
        # print(self.scores)
        print(f"{self.name} scores:")
        print("="*len(self.name) + "=======")
        for st, sc in self.scores.items():
            print(f"{st.name}:{sc}")

        print("\n")
        for idx, pick in enumerate(picks[::-1]):
            print(f"comparing {applicant.name} with {pick.name}")

            if pick.locked:
                print(f"{pick.name} is locked. Next Project\n")
                continue

            applicant_score = self.scores[applicant]
            pick_score = self.scores[pick]
            if applicant_score > pick_score:
                # capacity is exceeded, but student is higher ranked than
                print(
                    f"{applicant.name} is higher ranked than {pick.name}\n")
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
                print(f"{applicant.name} and {pick.name} are equally matched")
                return self.handle_tiebreak(applicant, picks, pick)

            print(f"{applicant.name}'s score is smaller than {pick.name}'s score\n")
        return False

    def apply_to(self, applicant):
        print(f"{applicant.name} tentatively applies to {self.name}")

        if not self.active:
            print(f"{self.name} has been cancelled")
            return False

        print(f"\n{self.name}'s mininum number of law students is {self.min_law}")
        print(f"{self.name}'s mininum number of non-law students is {self.min_non_law}\n")

        if self.cap == 0:
            print("Cap is 0! Next Project\n")
            return False

        if self.picks:
            print(f"{self.name}'s current picks are:")
            for pick in self.picks:
                print(pick.name, end='')
                if pick.is_law_student:
                    print(", a law student\n")
                else:
                    print(", a non-law student\n")
        else:
            print(f"{self.name} has no students yet\n")

        return self.is_applicant_inserted(applicant, self.picks)
