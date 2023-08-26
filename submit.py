import datetime
import submissionListener
from bs4 import BeautifulSoup
from tkinter import messagebox
import threading
def submutSolution(link, session, problem, filepath):
    if not filepath:messagebox.showerror(title="Error",message="Please Choose a File");return
    bol = messagebox.askyesno(title="Confirmation", message="Are you sure that you want to submit this solution?")
    if not bol:return
    problem_id = problem
    if filepath[-1] == "y":
        programming_language = 'Python'
    elif filepath[-1] == "p":
        programming_language = 'C++'
    elif filepath[-1] == "a":
        programming_language = 'Java'

    submission_page = session.get(f"{link}/submit").content
    soup = BeautifulSoup(submission_page, 'html.parser')
    form_data = {}
    for field in ['csrf_token' ]:
        field_value = soup.find('input', {'name': field}).get('value', '')
        form_data[field] = field_value
    form_data['submittedProblemIndex'] = problem_id
    # Read the source code from the file and add it to the form data
    with open(filepath, 'r') as f:
        source_code = f.read()
    form_data['source'] = source_code

    # Set the programming language in the form data
    language_map = {
        'C++': '54',
        'Java': '36',
        'Python': '31',
        # Add more languages as necessary
    }
    form_data['programTypeId'] = language_map[programming_language]

    # Submit the solution
    response = session.post(f'{link}/submit', data=form_data)
    if "You have submitted exactly the same code before" in response.text:
        messagebox.showerror("Error","You submitted this code before.")
        return
    # Print the response status code and content
    if response.status_code == 200:
        messagebox.showinfo(title="Success!",message="Submited Successfuly")
        while True:
            try:
                data = session.get(f"{link}/my")
                break
            except:
                continue

        soup = BeautifulSoup(data.text, 'html.parser')
        submissions = soup.find('table', {'class': 'status-frame-datatable'})

        subnum = [td.text.strip() for td in submissions.find_all('tr')[1].find_all('td')][0]
        thread2 = threading.Thread(target = lambda :submissionListener.waitForIt(link,session,subnum))
        thread2.start()
    else:
        messagebox.showerror(title="Failure!",message="something went wrong, try again.")