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

            for choice in project.choices:
                print(choice.name)

    def start_match(self):
        """begins matching process"""
        for applicant in self.applicants.values():
            # start match from first applicant
            print(f"{applicant.name} begins their match.")
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

