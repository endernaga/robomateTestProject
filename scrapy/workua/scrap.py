import requests
from bs4 import BeautifulSoup


def get_resume_information(url: str):
    req = requests.get(url).content
    soup = BeautifulSoup(req, "html5lib")

    soup = soup.find("div", {"class": "card wordwrap mt-0"})

    job_position = soup.find('h2', class_='mt-lg sm:mt-xl').text.strip()

    work_experiences = soup.find_all('p', class_='mb-0')
    years_of_experience = []
    for experience in work_experiences:
        years = experience.find('span', class_='text-default-7')
        if years:
            years_of_experience.append(years.text.strip())

    skills = [skill.text.strip() for skill in soup.find_all('span', class_='label label-skill label-gray-100')]

    location = soup.find('dd').text.strip()

    salary = soup.find("span", {"class": "text-muted-print"}).text

    return {"job_position": job_position, "years_of_experience": years_of_experience, "skills": skills,
            "location": location, "salary": salary}


if __name__ == "__main__":
    print(get_resume_information("https://www.work.ua/resumes/5455653/"))
