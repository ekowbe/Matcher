"""this modules runs the match"""
from sys import argv
import pandas as pd
import numpy as np
from models.Project import Project
from models.Student import Student
from controllers.MatchController import MatchController
import models.match_summary_dialog as match_summary_dialog
import models.generic_dialog as generic_dialog

def initialize_project_choices(projects, students):
    """adds choices for each project"""

    for project in projects.values():
        proj_rankings = {}

        # calculate score for each applicant
        for student in students.values():
            student_score: int = project.calculate_student_score(student)
            proj_rankings[student] = student_score

        # sort rankings
        proj_rankings = {k: v for k, v in sorted(proj_rankings.items(), key=lambda item: item[1], reverse=True)}

        # print project and rankings for student (sorted)
        print(f"\nStudent Scores for {project.name}")
        print("===================" + "="*len(project.name))
        for k,v in proj_rankings.items():
            print(f"{k.name}: {v}")

        project.choices = [val for val in proj_rankings.keys()]
        # print(project.choices)
        project.scores = proj_rankings

def run_prelim_match(projects, students, law:bool):
    """run the prelim law match and return projects in current state"""
    # restrict capacity of each project to number of law students
    for project in projects.values():
        if law:
            project.cap = project.min_law
        else:
            project.cap = project.min_non_law

    # run match for just law students
    match = MatchController(projects, students)
    match.start_match()
    match.print_summary()

    # lock in the students
    for student in students.values():
        # if matched
        if student.current_project is not None:
            student.locked = True

    return projects


def run_match(projects, students):
    """run the match"""
    # projects = get_projects_easy()

    # initialize project choices
    initialize_project_choices(projects, students)

    # step 1: match with law students only
    print("\nLAW MATCH")
    print("=========")
    law_students = {k:v for k,v in students.items() if v.is_law_student}
    projects = run_prelim_match(projects, law_students, law=True)
    
    # step 2: match with non law students only
    print("\nNON-LAW MATCH")
    print("=============")
    non_law_students = {k:v for k,v in students.items() if not v.is_law_student}
    projects = run_prelim_match(projects, non_law_students, law=False)

    # step 3: match the students who weren't matched
    print("\nREST OF MATCH")
    print("=============")

    # reset capacities to original capacities
    for project in projects.values():
        project.cap = project.original_cap

    count = 1
    match_complete = False
    while not match_complete:
        unmatched_students = {k:v for k,v in students.items() if v.current_project is None}

        # reset indexes for each student
        for student in unmatched_students.values():
            student.choice_idx = 0

        # print(unmatched_students)
        match = MatchController(projects, unmatched_students)
        match.start_match()
        match.calculate_popularity()

        print(f"Remainder Match {count}")
        print("=================\n")

        # match.print_summary()
        projects_to_cut = []

        valid_input = False

        # keep asking for input until it's valid
        while not valid_input:
            summary_str = match.get_summary()
            print(summary_str)
            dlg = match_summary_dialog.FixedWidthMessageDialog(summary_str)

            if dlg.exec_():
                print("Success!")
            else:
                print("Cancel!")

            user_picks = dlg.user_picks
            try:
                projects_to_cut = [proj_num for proj_num in user_picks.split(',')]
            except AttributeError:
                msg_dialog = generic_dialog.FixedWidthMessageDialog(message="invalid input. Try again.")
                if msg_dialog.exec_():
                    print("Success!")
                else:
                    print("Cancel!")
                continue

            # print(projects_to_cut)
            print(projects_to_cut)

            # error checking
            if projects_to_cut == ["None"]:
                msg_dialog = generic_dialog.FixedWidthMessageDialog(message="Okay. If there are no more projects to cut, matching complete!")
                print("Okay. If there are no more projects to cut, matching complete!\n")
                valid_input = True
                match_complete = True
                break

            # if it's not none, it should be comma separated ints
            try:
                projects_to_cut = [int(el) for el in projects_to_cut]
            except ValueError:
                # msg_dialog = generic_dialog.FixedWidthMessageDialog(message="invalid input. Try again.")
                print("invalid input. Try again.\n")
                continue

            # they are all ints, but are they in range?
            num_projects_to_cut = len(projects_to_cut)
            c = 0

            for project_num in projects_to_cut:
                # print(len(projects), project_num)
                if project_num < 1 or project_num > len(projects):
                    break
                c += 1

            # while loop will stop on next run
            print(c, num_projects_to_cut)
            if c == num_projects_to_cut:
                valid_input = True
            else:
                valid_input = False

            if not valid_input:
                continue

            # figure out projects we need to cut
            for proj_num in projects_to_cut:
                idx = proj_num-1
                # print(idx)
                proj_obj = list(projects.values())[idx]
                proj_obj.active = False
                print(f"\nYou cancelled {proj_obj.name}\n")
                project_picks = proj_obj.picks

                # figure out students who need to reapply
                if project_picks:
                    for student in project_picks:
                        student.locked = False
                        student.current_project = None
                else:
                    # if there are no new round applicants, we end
                    print("There are no students to match\n")
                    match_complete = True
                    break

            # show the user the peeps who have to reapply
            for applicant in students.values():
                if applicant.current_project is None:
                    print(f"{applicant.name} has to retry")

        count += 1
    print("broke out of while loop")
    match.get_output_csv()

def get_projects(easy=False):
    projects = {}
    if easy:
        project_data = pd.read_csv('project_data_easy.csv')
    else:
        project_data = pd.read_csv('project_data.csv')

    # convert to dict
    project_dicts = project_data.to_dict(orient='records')

    # instantiate objs
    for project_dict in project_dicts:
        projects[project_dict['name']] = Project(project_dict['name'],
                                                 project_dict['cap'],
                                                 project_dict['min_law'],
                                                 project_dict['min_non_law'])
    return projects

def get_students(projects, easy=False):
    students = {}

    if easy:
        student_data = pd.read_csv('student_data_easy.csv')
    else:
        student_data = pd.read_csv('student_data.csv')

    print(student_data)

    student_data = student_data.replace({np.nan: None})
    print(student_data)
    student_dicts = student_data.to_dict(orient='records')

    for student_dict in student_dicts:

        # get name
        name = student_dict['name']
        print(name)

        # check if they're a law student
        degrees = student_dict['degrees']
        print(f'Degrees: {degrees}')

        # check if pre admitted
        admitted = student_dict['admitted']
        print(f'Admitted: {admitted}')
        if admitted == "Y":
            is_preadmitted = True
        else:
            is_preadmitted = False

        # check if pre_assigned
        preassignment = None

        assignment = student_dict['assign']
        if assignment is not None:
            assignment = int(assignment) - 1
            preassignment = list(projects)[assignment]

        print(f'Admitted: {preassignment}')

        # rankings
        rankings = student_dict['rankings'].split(',')
        print(f'Rankings: {rankings}')

        choices = []
        for project in rankings:
            idx = int(project) - 1
            project_name = list(projects)[idx]
            choices.append(projects[project_name])

        print(f'Choices: {[c.name for c in choices]}')

        # softs
        num_softs = 0
        if student_dict['in_final_year'] == "Y":
            print(f"{name} is in final year")
            num_softs += 1
            in_final_year = True
        else:
            in_final_year = False

        if student_dict['for_capstone'] == "Y":
            num_softs += 1
            print(f"{name} is doing this for capstone")
            for_capstone = True
        else:
            for_capstone = False

        if student_dict['is_previously_unsuccessful'] == "Y":
            num_softs += 1
            is_previously_unsuccessful = True
            print(f"{name} is previously unsuccessful")
        else:
            is_previously_unsuccessful = False
        
        if student_dict['is_returning'] == "Y":
            num_softs += 1
            is_returning = True
            print(f"{name} is returning")
        else:
            is_returning = False

        bidding_rank = student_dict['bidding_rank']
        print(f"Number of softs: {num_softs}")

        students[name] = Student(name,
                                 degrees,
                                 is_preadmitted,
                                 preassignment,
                                 choices,
                                 in_final_year,
                                 for_capstone,
                                 is_previously_unsuccessful,
                                 is_returning,
                                 bidding_rank,
                                 num_softs)

        print('\n')

    return students


def match():
    """main func"""

    easy = False
    if len(argv) == 2:
        if argv[1] == "easy":
            easy = True

    projects = get_projects(easy)
    students = get_students(projects, easy)

    run_match(projects, students)

if __name__ == '__main__':
    match()
