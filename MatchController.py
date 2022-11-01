"""assigns students to projects"""
from Student import Student
from Project import Project
import pandas as pd

class MatchController():
    """this class
        1. processes ROLs for Students and Projects
        2. controls the match process
        3. returns the final results
    """
    
    # def __init__(self, program_data, applicant_data, cap_data) -> None:
    #     """takes XLSX file reads stuff."""
    #     pass

    # for now, we'll just have pre done stuff
    def __init__(self) -> None:

        self.projects = {}
        self.applicants = {}

        # initialize projects
        self.projects['Project A'] = Project('Project A', 2, 1)
        self.projects['Project B'] = Project('Project B', 2, 1)
        self.projects['Project C'] = Project('Project C', 2, 0)

        print("these are my projects")
        for project in self.projects.values():
            print(project)
            print(project.__repr__())

        print(self.projects)
        # this will soon pull directly from the sheet itself
        students: dict = {
            'Ali': ["YSE",
                    False, None,
                    'Project A', 'Project B', 'Project C',
                    True, False, False
                ],

            'Beatriz': ["YLS",
                        True, None,
                        'Project B', 'Project A', 'Project C',
                        False, False, True
                    ],

            'Charles': ["YSE",
                        False, None,
                        'Project B', None, None,
                        False, True, False
                    ],

            'Diya': ["YSE",
                    False, None,
                    'Project C', 'Project A', 'Project B',
                    True, True, True
                    ],

            'Eric': ["YLS",
                    True, None,
                    'Project C', 'Project B', 'Project A',
                    True, False, False
                    ],

            'Fatima': ["YSE",
                    False, None,
                    'Project A', 'Project C', None,
                    False, False, False
                    ],

            'Gabriel': ["YLS",
                        False, None,
                        'Project B', 'Project A', 'Project C',
                        True, False, True
                    ],

            'Hannah': ["YSE",
                    True, 'Project B',
                    'Project B', 'Project C', 'Project A',
                    False, False, False
                    ],

            'Isaac': ["YLS",
                    False, None,
                    'Project A', 'Project C', None,
                    True, False, False
                    ]
        }

        # initialize students
        for student_name, student_metadata in students.items():
            in_YLS: bool = True if student_metadata[0] == "YLS" else False

            # initialize choices for student
            choices = student_metadata[3:6]
            print(choices)
            choice_objs = []
            for proj in choices:
                if proj is not None:
                    choice_objs.append(self.projects[proj])

            print(choice_objs)

            num_softs:int = 0

            for soft in student_metadata[6:]:
                if soft:
                    num_softs += 1

            self.applicants[student_name] = Student(student_name,
                                                    in_YLS,
                                                    student_metadata[1],
                                                    student_metadata[2],
                                                    choice_objs,
                                                    num_softs)

        # initialize project choices
        for project in self.projects.values():
            proj_rankings = {}

            # calculate score for each applicant
            for student in self.applicants.values():
                student_score: int = project.calculate_student_score(student)
                proj_rankings[student] = student_score

            # sort rankings
            proj_rankings = {k: v for k, v in sorted(proj_rankings.items(), key=lambda item: item[1], reverse=True)}

            print(project.name)
            for k,v in proj_rankings.items():
                print(f"{k.name}: {v}")

            project.choices = [val for val in proj_rankings.keys()]
            project.scores = proj_rankings

    def start_match(self):
        """begins matching process"""
        for applicant in self.applicants.values():
            # start match from first applicant
            print(f"{applicant.name} begins their match.")
            applicant.find_next()

    def second_match(self):
        """second matching process"""

        # not necessary if number of projects = number of projects that CAN be run

        second_match_applicants = {}
        second_match_projects = {}
        project_popularity_scores = {}

        # let's populate it with 0's for now
        for project in self.projects.values():
            project_popularity_scores[project] = 0

        # calculate project popularity with matched applicants
        for applicant in self.applicants.values():
            if applicant.current_project is not None:
                score = 3
                for choice in applicant.choices:
                    project_popularity_scores[choice] += score
                    score -= 1

        # print(project_popularity_scores)
        # in order of rankings
        project_popularity_scores = {k: v for k, v in sorted(project_popularity_scores.items(), key=lambda item: item[1], reverse=True)}
        # print(project_popularity_scores)

        print("The scores are")
        for project, score in project_popularity_scores.items():
            print(f"{project.name}: {score}")

        # let the user cut the project
        project_to_cut = input("Which project do you want to cut: ")


        for name, project in self.projects.items():
            if name != project_to_cut: 
                second_match_projects[name] = project
            else: # it's the project.
                project_picks = project.current_picks()
                for student in project_picks:
                    second_match_applicants[student.name] = student
    
        print(f"{project_to_cut} deleted from match")

        print("The students who got cut off are")
        for student in second_match_applicants.keys():
            print(student)

        # with peeps who didn't match
        print("beginning second match with popular projects and unmatched students")
        for applicant in second_match_applicants.values():
            print(f"{applicant.name} begins their second match.")
            applicant.find_next()

    def print_results(self):
        """prints results"""
        for applicant_name, applicant in self.applicants.items():
            print(applicant_name)
            try:
                print(' ', applicant.current_project.name)
            except AttributeError:
                # doesn't have a current place
                print(' Did not match')

    def student_results_dict(self):
        """puts the results in a dict"""
        results_dict = {}

        for name, applicant_obj in self.applicants.items():
            try:
                results_dict[name] = applicant_obj.current_project.name
            except AttributeError:
                results_dict[name] = 'Did not match'

        return results_dict

    def get_output_csv(self):
        results = self.student_results_dict()

        results_df = pd.DataFrame.from_dict(
            results,
            orient='index'
        )

        results_df = results_df.reset_index()
        results_df.columns = ['Candidate', 'Matched Program']

        results_df.to_csv('results.csv', index=False)

