from bs4 import BeautifulSoup

def getProblemNames(link,session):

    url = link

    response = session.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    excluded = ["act bottom dark", "bottom dark right"]
    problem_names = []
    final_problem_names = []
    table = soup.find('table', 'problems')
    for problem in table.find_all('td', _class = lambda x:x not in excluded):
        problem_names.append(problem.text.strip())

    letters = problem_names[::4]
    names = problem_names[1::4]
    for i in range(len(names)):
        names[i] = names[i][:names[i].index('\n')].strip()

    for i in range(len(letters)):
        final_problem_names.append(letters[i])
        final_problem_names.append(names[i])


    return final_problem_names