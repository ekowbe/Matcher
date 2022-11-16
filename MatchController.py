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
            print(f"\nStudent Scores for {project.name}")
            print("=================" + "="*len(project.name))
            for k,v in proj_rankings.items():
                print(f"{k.name}: {v}")

            project.choices = [val for val in proj_rankings.keys()]
            project.scores = proj_rankings

    def start_match(self, applicants=None):
        """begins matching process

            If applicants is not None, it means we have specified
            the group of students who are participating in the match."""

        if applicants:
            students_to_match = applicants
        else:
            students_to_match = self.applicants.values()

        # match law students

        # match non-law students

        # start match from first applicant
        for idx, applicant in enumerate(students_to_match):
            print(f"\nApplicant {idx+1}")
            print("===========")

            print(f"\n{applicant.name} begins their match.\n")

            # check preassignments first. if applicant is preassigned apply to that first
            if applicant.preassignment is not None:
                preassigned_project = self.projects[applicant.preassignment]
                print(f"\n{applicant.name} is preassigned to {preassigned_project.name}")

                # if applicant is able to apply then we move on to the next student
                if preassigned_project.apply_to(applicant):
                    continue

            # either applicant is not preassigned
            # or he wasn't able to apply to his preassignment because it's cancelled
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

    def print_summary(self):
        """prints a comprehensive summary of projects and matches
            and student info"""
        idx = 1
        for project_name, project in self.projects.items():
            # prints only if project is active
            if project.active:
                print(f"{project_name} ({idx})")
                print("="*len(project_name))
                print(f"Capacity: {project.cap}")
                print(f"Min Law: {project.min_num_law_students}\n")
                
                # print other factors
                for pick in project.picks:
                    print(f"{pick.name}", end ="")
                    if pick.is_law_student:
                        print(", law student", end ="")

                    if pick.is_preadmitted:
                        print(", was preadmitted", end ="")

                    if pick.preassignment is not None:
                        print(f", was preassigned to {pick.preassignment}", end ="")
                    
                    print(f", number of softs: {pick.num_softs}", end="")

                    print(f", student score: {project.scores[pick]}")
        
                # print preference score
                print(f"\nPreference score for {project_name}: {project.popularity_score}\n")
                idx +=1
        
        # print cancelled projects
        print("\nCancelled Projects")
        print("==================")

        for name, obj in self.projects.items():
            if not obj.active:
                print(name)

        # print students who have to rematch
        print("\nStudents who didn't match")
        print("===========================")

        for name, obj in self.applicants.items():
            if obj.current_project is None:
                print(name)

        return

    def resize_results_dict(self):
        """resizes the dict so it can be df'ed"""
        results = self.student_results_dict()
        max_len = 0

        for matches in results.values():
            if len(matches) > max_len:
                max_len = len(matches)
        
        for name, matches in results.items():
            if len(matches) < max_len:
                results[name] = matches + [None] * (max_len - len(matches))
        
        return results

    def student_results_dict(self):
        """puts the results in a dict"""
        results_dict = {}

        for name, proj_obj in self.projects.items():
            if proj_obj.active:
                results_dict[name] = [pick.name for pick in proj_obj.picks]

        return results_dict

    def get_output_csv(self):
        results = self.resize_results_dict()
        # print(results)

        results_df = pd.DataFrame.from_dict(
            results,
            orient='columns'
        )

        # results_df = results_df.reset_index()
        # results_df.columns = ['Candidate', 'Matched Program']
        results_df.to_csv('results.csv',index=False)
        # df.to_csv('filename.txt', sep=' ', header=False)

