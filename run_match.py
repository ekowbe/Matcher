"""this modules runs the match"""
from sys import argv
import pandas as pd
import numpy as np
from Project import Project
from Student import Student
from MatchController import MatchController

def run_match(projects, students):
    """run the match"""
    # projects = get_projects_easy()

    match = MatchController(projects, students)
    new_round_applicants = []

    count = 1
    match_complete = False
    while not match_complete:
        match.start_match(new_round_applicants)
        match.calculate_popularity()

        print(f"Match {count}")
        print("=======\n")

        match.print_summary()

        projects_to_cut = []

        # projects_to_cut = [int(proj_num) for proj_num in input("\nWhich project(s) do you want to cut (Type each number separated by a comma or None if done): \n").split(', ')]
        valid_input = False
        
        while not valid_input:
            projects_to_cut = [proj_num for proj_num in input("\nWhich project(s) do you want to cut (Type each number separated by a comma or None if done): \n").split(',')]
            # print(projects_to_cut)

            # error checking
            if projects_to_cut == ["None"]:
                print("Okay. If there are no more projects to cut, matching complete!\n")
                valid_input = True
                match_complete = True
                break

            # if it's not none, it should be comma separated ints
            try:
                projects_to_cut = [int(el) for el in projects_to_cut]
            except ValueError:
                print("invalid input. Try again.\n")
                continue

            # they are all ints, but are they in range?
            for project_num in projects_to_cut:
                if project_num < 1 or project_num > len(projects):
                    print("invalid input. Try again.\n")
                    continue

            # while loop will stop on next run
            valid_input = True

            # figure out projects we need to cut
            for proj_num in projects_to_cut:
                idx = proj_num-1
                # print(idx)
                proj_obj = list(projects.values())[idx]
                proj_obj.active = False
                project_picks = proj_obj.picks

                # figure out students who need to apply
                for student in project_picks:
                    new_round_applicants.append(student)

                # if there are no new round applicants, we end
                if not new_round_applicants:
                    print("There are no students to match\n")
                    break

            # show the user the peeps who have to reapply
            for applicant in new_round_applicants:
                print(f"{applicant.name} has to retry")

            match.start_match(new_round_applicants)

        count += 1
    print("broke out of while loop")

import xlwings as xw  # pip install xlwings

EXCEL_FILE = 'F22 formatted.xlsx'
# OUTPUT_DIR = Path(__file__).parent / 'Output'


def splice_sheets():

    with xw.App(visible=False) as app:
        wb = app.books.open(EXCEL_FILE)
        for sheet in wb.sheets:
            wb_new = app.books.add()
            sheet.copy(after=wb_new.sheets[0])
            wb_new.sheets[0].delete()
            wb_new.save(f'{sheet.name}.xlsx')
            wb_new.close()

def get_projects_easy():
    projects = {}
    projects['Project A'] = Project('Project A', 3, 1)
    projects['Project B'] = Project('Project B', 3, 1)
    projects['Project C'] = Project('Project C', 3, 0)

    return projects

def get_students_easy(projects):
        applicants = {}
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
            
            is_law_student: bool = True if student_metadata[0] == "YLS" else False

            is_preadmitted = True if student_metadata[1] == "Y" else False
            preassignment = None if student_metadata[2] is not None else student_metadata[2]

            
            # initialize choices for student
            choices = student_metadata[3:6]
            print(choices)
            choice_objs = []
            for proj in choices:
                if proj is not None:
                    choice_objs.append(projects[proj])

            num_softs:int = 0

            for soft in student_metadata[6:]:
                if soft:
                    num_softs += 1

            
            applicants[student_name] = Student(student_name,
                                                    is_law_student,
                                                    is_preadmitted,
                                                    preassignment,
                                                    choice_objs,
                                                    num_softs)
        return applicants

def get_projects():
    projects = {}
    project_data = pd.read_csv('project_data.csv')

    # convert to dict
    project_dicts = project_data.to_dict(orient='records')

    # instantiate objs
    for project_dict in project_dicts:
        projects[project_dict['name']] = Project(project_dict['name'],
                                                 project_dict['cap'],
                                                 project_dict['min_num_law_students'])
    return projects

def get_students(projects):
    students = {}
    student_data = pd.read_csv('student_data.csv')
    student_data = student_data.replace({np.nan: None})
    student_dicts = student_data.to_dict(orient='records')

    for student_dict in student_dicts:
        # get name
        name = student_dict['name']
        print(name)

        #check if they're a law student
        degrees = student_dict['degrees']
        print(f'Degrees: {degrees}')
        if "JD" in degrees or "LLM" in degrees:
            is_law_student = True
        else:
            is_law_student = False

        # check if pre admitted
        admitted = student_dict['admitted']
        print(f'Admitted: {admitted}')
        if admitted == "Y":
            is_preadmitted = True
        else:
            is_preadmitted = False

        # check if pre_assigned
        preassignment = None
        if is_preadmitted:
            assignment = student_dict['assign']
            if assignment is not None:
                preassignment = list(projects)[idx]
        print(f'Admitted: {preassignment}')
        # rankings
        rankings = student_dict['rankings'].split(',')
        print(f'Rankings: {rankings}')

        choices = []
        for project in rankings:
            idx = int(project) - 1
            project_name = list(projects)[idx]
            choices.append(projects[project_name])

        print(f'Choices: {choices}')

        # softs
        num_softs = 0
        if student_dict['in_final_year'] == "Y":
            num_softs += 1
            in_final_year = True
        else:
            in_final_year = False

        if student_dict['is_capstone_project'] == "Y":
            num_softs += 1
            is_capstone_project = True
        else:
            is_capstone_project = False

        if student_dict['is_previously_unsuccessful'] == "Y":
            num_softs += 1
            is_previously_unsuccessful = True
        else:
            is_previously_unsuccessful = False

        students[name] = Student(name,
                                is_law_student,
                                is_preadmitted,
                                preassignment,
                                choices,
                                num_softs)

        print('\n')

    return students

def main():
    if len(argv) == 2:
        if argv[1] == "easy":
            projects = get_projects_easy()
            students = get_students_easy(projects)
    else:
        projects = get_projects()
        students = get_students(projects)
    
    run_match(projects, students)

if __name__ == '__main__':
    main()
