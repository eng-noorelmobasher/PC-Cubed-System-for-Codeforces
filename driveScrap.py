import requests
from bs4 import BeautifulSoup
from tkinter import messagebox,filedialog
import concurrent.futures
# Replace this with the Google Drive folder URL you want to download from

"""
make sure that the statements pdf file name is lexicographically less than the contest link file
for example statements file => a.pdf , contest link file => z.txt
make sure that there is only two files in the folder and the folder is public
make sure that the statements file is in pdf extension and the contest link file is in txt extension
contest link file should ONLY contain the contest link without an EOLN in the end of the file
for ex: https://codeforces.com/group/XXXXXX/contest/XXXXXX (DON'T PUT WWW IN THE LINK)
"""

folder_url = "https://drive.google.com/drive/folders/YOR_FOLDER_ID"

# Replace FOLDER_ID with the actual folder ID from the URL
folder_id = "YOUR_FOLDER_ID"

def getContestLink(folder_url=folder_url, folder_id=folder_id):

    response = requests.get(folder_url)
    global file_ids
    if response.status_code == 200:
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        sp = soup.find_all('div',attrs={"data-target": "doc"})
        
        file_ids = []
        for i in sp:
            i = str(i)
            file_ids.append(i[i.index('data-id=')+9:i.index('data-target=') - 2])


        file_id = file_ids[-1]
        contest_url = f"https://drive.google.com/uc?id={file_id}"
        response = requests.get(contest_url)

        if response.status_code == 200:

            filename = 'temp.txt'


            with open(filename, "wb") as pdf_file:
                pdf_file.write(response.content)
            return open('temp.txt','r').readline()
        else:
            stat = messagebox.askretrycancel(title="error",message="Something went wrong ... Please check your internet connection")
            if stat:
                getContestLink()
            else:
                return False
    else:
        stat = messagebox.askretrycancel(title="error",message="Something went wrong ... Please check your internet connection")
        if stat:
            getContestLink()
        else:
            return False

def getStatments(dest=None):

    if not dest:
        dest = filedialog.askdirectory()

    if not dest:
        messagebox.showerror(title="Info", message="Please Choose a Path!")
        return
    
    messagebox.showinfo(title="Info", message="Downloading file, Please wait..")

    file_id = file_ids[0]
    pdf_url = f"https://drive.google.com/uc?id={file_id}"
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(lambda: DownloadProg(pdf_url, dest=dest))
        result = future.result()

    if result:
        messagebox.showinfo(title="Success!", message="Statements file downloaded successfuly.")
    else:
        stat = messagebox.askretrycancel(title="error",message="Something went wrong ... Please check your internet connection")
        if stat:
            getStatments(dest=dest)
        else:
            return

def DownloadProg(url,dest):
    response = requests.get(url)

    if response.status_code == 200:

        # Extract the filename from the URL
        filename = f'{dest}\\statements.pdf'

        # Save the PDF to your local directory
        with open(filename, "wb") as pdf_file:
            pdf_file.write(response.content)
        return True
    
    else:
        return False
