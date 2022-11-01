"""this modules runs the match"""

from MatchController import MatchController

def run_match():
    """run the match"""

    match = MatchController()
    match.start_match()
    match.print_results()

    
    match.second_match()

    print("second match results")
    match.print_results()
    match.get_output_csv()

if __name__ == '__main__':
    run_match()
