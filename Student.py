class Student():
    """Class representing student applying to be in a project"""
    students = []
    law_students = []

    def __init__(self, name:str, is_law_student: bool, is_preadmitted: bool, preassignment:str, choices: list, num_softs: int):
        self.name = name
        self.is_law_student = is_law_student
        self.is_preadmitted = is_preadmitted
        self.preassignment = preassignment
        self.choices = choices
        self.num_softs = num_softs
        self.current_project = None
        self.choice_idx = 0
        Student.students.append(self)

        if self.is_law_student:
            Student.law_students.append(self)

    # def __repr__(self):
    def numerize_student_preferences(self, project)->int:
        """looks at student's preferences and gives appropriate score"""
        score: int = 3

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

        #print(self.name, project.name)

        if project.apply_to_2(self):
            print(f"{self.name} temp matched to {project.name}\n")
            self.current_project = project

            if self.is_law_student:
                project.num_law_students += 1
            return True

        self.find_next()
