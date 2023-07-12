from bs4 import BeautifulSoup

def getProblemNames(link,session):

    url = link
    classPart = link[link.index("/group"):]+'/problem/'
    response = session.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    problem_names = []


    for problem_link in soup.find_all('a', href=lambda x: x and classPart in x):
        problem_names.append(problem_link.text.strip())

    return problem_names