import os
from bs4 import BeautifulSoup

def count_multiple_condtion(folder_path):
    html_files = [f for f in os.listdir(folder_path) if f.endswith(".html")]

    count = 0
    for html_file in html_files:
        f_count = 0
        file_path = os.path.join(folder_path, html_file)
        with open(file_path, "r", encoding="utf-8") as f:
            html_data = f.read()

        soup = BeautifulSoup(html_data, "html.parser")
        tds = soup.find_all("td", class_="linebranch")

        for td in tds:
            if ('switch' in td.parent.contents[7].text):
                continue
            taken_branches = td.find_all(class_="takenBranch")
            if len(taken_branches) >= 3:
                count += 1
                f_count += 1
        print(html_file + " 멀티플 condition 개수: " + str(f_count))
    return count

folder_path = ""
result = count_multiple_condtion(folder_path)
print("##### 멀티플 condition 분기문 총 개수: "+ str(result))
