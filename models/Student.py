class Student():
    """Class representing student applying to be in a project"""
    students = []
    law_students = []

    def __init__(self, name:str, 
                degrees: list[str], 
                is_preadmitted: bool, 
                preassignment:str, 
                choices: list, 
                in_final_year: bool, 
                for_capstone: bool, 
                is_previously_unsuccessful: bool, 
                is_returning: bool, 
                bidding_rank: int,
                num_softs: int):

        # stuff from csv file
        self.name = name
        self.degrees = degrees
        self.is_law_student = "JD" in degrees or "LLM" in degrees
        self.is_preadmitted = is_preadmitted
        self.preassignment = preassignment
        self.choices = choices
        self.in_final_year = in_final_year
        self.for_capstone = for_capstone
        self.is_previously_unsuccessful = is_previously_unsuccessful
        self.is_returning = is_returning
        self.bidding_rank = bidding_rank
        self.num_softs = num_softs

        # other important stuff
        self.current_project = None
        self.choice_idx = 0
        self.locked = False # some students are locked into a place
        Student.students.append(self)

        if self.is_law_student:
            Student.law_students.append(self)

    def numerize_student_preferences(self, project, num_projects)->int:
        """looks at student's preferences and gives appropriate score"""
        score: int = num_projects

        for ranked_project in self.choices:
            if ranked_project == project:
                return score
            score -= 1

        return 0

    def find_next_preference(self):
        """returns the student's next preferred choice"""
        while True:
            next_preference = self.choices[self.choice_idx]
            self.choice_idx += 1
            if next_preference.active:
                break

        return next_preference

    def find_next(self):
        """matches student to their next possible match"""
        try:
            project = self.find_next_preference()
        except IndexError:
            self.current_project = None
            print("{} has exhausted preference list.\n".format(self.name))
            return False

        # tentative application
        if project.apply_to(self):
            print(f"\n{self.name} temp matched to {project.name}\n")
            self.current_project = project

            if self.is_law_student:
                project.num_law_students += 1
            return True

        self.find_next()
