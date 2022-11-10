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

    # for now, we'll just have pre done stuff
    def __init__(self, projects, students):

        self.projects = projects
        self.applicants = students

        # initialize project choices
        for project in self.projects.values():
            proj_rankings = {}

            # calculate score for each applicant
            for student in self.applicants.values():
                student_score: int = project.calculate_student_score(student)
                proj_rankings[student] = student_score

            # sort rankings
            proj_rankings = {k: v for k, v in sorted(proj_rankings.items(), key=lambda item: item[1], reverse=True)}

            # print project and rankings for student (sorted)
            print(project.name)
            for k,v in proj_rankings.items():
                print(f"{k.name}: {v}")

            project.choices = [val for val in proj_rankings.keys()]
            project.scores = proj_rankings

    def start_match(self, applicants=None):
        """begins matching process"""
        
        if applicants:
            students_to_match = applicants
        else:
            students_to_match = self.applicants.values()
        for applicant in students_to_match:
            # start match from first applicant
            print(f"{applicant.name} begins their match.\n")
            applicant.find_next()

    def calculate_popularity(self):
        """after the first match, calculates popularity for
            each project, based on admitted students"""

        project_popularity_scores = {}

        for project in self.projects.values():
            # let's populate it with 0's for now
            project_popularity_scores[project] = 0

            project_picks = project.current_picks()

            # calculate project popularity with matched applicants
            for applicant in project_picks:
                score = len(Project.projects)
                for choice in applicant.choices: # goes down choice list in order
                    if choice == project:
                        project_popularity_scores[choice] += score
                        choice.popularity_score += score
                    score -= 1

        # in order of rankings
        project_popularity_scores = {k: v for k, v in sorted(project_popularity_scores.items(), key=lambda item: item[1], reverse=True)}
        Project.popularity_scores = project_popularity_scores

    def second_match(self):
        """second matching process"""
        second_match_applicants = {}

        # let the user choose the project(s) to cut
        projects_to_cut = [proj for proj in input("Which project(s) do you want to cut (Type each name separated by a comma): \n").split(', ')]

        # print project(s) that got deleted
        for project_name in projects_to_cut:
            print(f"\n{project_name} deleted from match")
            # print students that need to rematch
            for name, project in self.projects.items():
                if project_name == name:
                    project.active = False
                    project_picks = project.current_picks()
                    for student in project_picks:
                        second_match_applicants[student.name] = student



        # print students that need to rematch
        for name, project in self.projects.items():
            if name in projects_to_cut:
                project_picks = project.current_picks()
                for student in project_picks:
                    second_match_applicants[student.name] = student


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

    def print_summary(self):
        """prints a comprehensive summary of projects and matches
            and student info"""
        for project_name, project in self.projects.items():
            if project.active:
                print(project_name)
                print("=========")
                picks = project.current_picks()

                for pick in picks:
                    print(f"{pick.name}", end ="")
                    if pick.is_law_student:
                        print(", law student", end ="")

                    if pick.is_preadmitted:
                        print(", was preadmitted", end ="")

                    if pick.preassignment is not None:
                        print(f", was preassigned to {pick.preassignment}", end ="")
                    
                    print(f", number of softs: {pick.num_softs}")
        

                print(f"\nPreference score for {project_name}: {project.popularity_score}")
                print("\n")
        return


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

