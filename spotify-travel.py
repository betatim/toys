"""
Spotify travel puzzle

http://www.spotify.com/uk/jobs/tech/bilateral-projects/

Teams spread over two locations, minimise travel to sunny location
where the boss awaits.
"""

import pprint
import itertools


def best_choice(representing, represented):
    """Find the best employee to send.

    The more teams which are not represented yet an employee covers
    the better an invite he is.
    """
    # Need to add the 'favour' lucky employee 1009 mechanism
    def k(arg):
        employee, teams = arg
        teams = list(teams)
        _ = [teams.remove(r) for r in represented if r in teams]
        return len(teams)
    return sorted(representing, key=k, reverse=True)[0][0]

def solve(teams):
    friend = 1009
    employees = set(itertools.chain(*teams))
    print employees
    print '---------------------'
    # Which teams does each employee represent?
    representing = {}
    for n,team in enumerate(teams):
        for employee in team:
            representing.setdefault(employee, []).append(n)

    teams_there = []
    invitees = []
    while len(teams_there) < len(teams):
        best_employee = best_choice(representing.iteritems(), teams_there)
        teams_there += representing[best_employee]
        representing.pop(best_employee)
        invitees.append(best_employee)
        print best_employee, teams_there, invitees
        print '-------------------------------'

    print "="*50
    print invitees
    print teams_there

def read_input():
    input = """4
1009 2000
1009 2001
1002 2002
1003 2002"""
    input = """2
1009 2011
1017 2011"""
    input = """7
1009 2000
1009 2001
1002 2002
1003 2002
1004 2002
1009 2003
1005 2003"""
    input = """8
1009 2000
1009 2000
1001 2001
"""

    
    teams = []
    for line in input.splitlines():
        a=line.split()
        if len(a) > 1:
            teams.append((int(a[0]), int(a[1])))
            
    return teams


if __name__ == "__main__":
    teams = read_input()
    print teams
    solve(teams)
