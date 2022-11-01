class Student():
    """Class representing student applying to be in a project"""
    students = []
    law_students = []

    def __init__(self, name:str, in_YLS: bool, is_preadmitted: bool, preassignment:str, choices: list, num_softs: int):
        self.name = name
        self.in_YLS = in_YLS
        self.is_preadmitted = is_preadmitted
        self.preassignment = preassignment
        self.choices = choices
        self.num_softs = num_softs
        self.current_project = None
        self.choice_idx = 0
        Student.students.append(self)

        if self.in_YLS:
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
        next_preference = self.choices[self.choice_idx]
        self.choice_idx += 1
        return next_preference

    def find_next(self):
        """matches student to their next possible match"""
        try:
            project = self.find_next_preference()
        except IndexError:
            self.current_project = None
            print("{} did not match.".format(self.name))
            return False

        #print(self.name, project.name)

        if project.apply_to_2(self):
            print("{} temp matched to {}".format(self.name, project.name))
            self.current_project = project
            return True

        self.find_next()
