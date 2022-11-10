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
            # print(students_to_match)
            
        else:
            students_to_match = self.applicants.values()
            
        for idx, applicant in enumerate(students_to_match):
            print(f"Applicant {idx+1}")
            print("-------------------")
            # start match from first applicant
            print(f"\n{applicant.name} begins their match.\n")
            applicant.find_next()

    def calculate_popularity(self):
        """after the first match, calculates popularity for
            each project, based on admitted students"""

        # reset to zero every time this is called
        for project in self.projects.values():
            project.popularity_score = 0

        project_popularity_scores = {}

        for project in self.projects.values():
            # let's populate it with 0's for now
            project_popularity_scores[project] = 0

            project_picks = project.picks

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
        idx = 0
        for project_name, project in self.projects.items():
            if project.active:
                print(f"{project_name} ({idx})")
                print("=========")
                print(f"Capacity: {project.cap}")
                print(f"Min Law: {project.min_num_law_students}\n")
                
                for pick in project.picks:
                    print(f"{pick.name}", end ="")
                    if pick.is_law_student:
                        print(", law student", end ="")

                    if pick.is_preadmitted:
                        print(", was preadmitted", end ="")

                    if pick.preassignment is not None:
                        print(f", was preassigned to {pick.preassignment}", end ="")
                    
                    print(f", number of softs: {pick.num_softs}")
        

                print(f"\nPreference score for {project_name}: {project.popularity_score}")
                idx +=1

        print("\nCancelled Projects")
        print("==================")

        for name, obj in self.projects.items():
            if not obj.active:
                print(name)

        print("\nStudents who didn't match")
        print("===========================")

        for name, obj in self.applicants.items():
            if obj.current_project is None:
                print(name)

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

