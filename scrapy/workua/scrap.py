import requests
from bs4 import BeautifulSoup


def get_resume_information(url: str):
    req = requests.get(url).content
    soup = BeautifulSoup(req, "html5lib")

    soup = soup.find("div", {"class": "card wordwrap mt-0"})

    job_position = (
        soup.find("h2", class_="mt-lg sm:mt-xl").text.strip().replace("\xa0", " ")
    )

    work_experiences = soup.find_all("p", class_="mb-0")
    years_of_experience = []
    for experience in work_experiences:
        years = experience.find("span", class_="text-default-7")
        if years:
            years_of_experience.append(years.text.strip().replace("\xa0", " "))

    skills = [
        skill.text.strip().replace("\xa0", " ")
        for skill in soup.find_all("span", class_="label label-skill label-gray-100")
    ]

    location = soup.find("dd").text.strip().replace("\xa0", " ")

    salary = (
        soup.find("span", {"class": "text-muted-print"}).text.replace("\xa0", " ")
        if soup.find("span", {"class": "text-muted-print"})
        else None
    )

    return {
        "job_position": job_position,
        "years_of_experience": years_of_experience,
        "skills": skills,
        "location": location,
        "salary": salary,
    }


def get_resumes_pages(req):
    soup = BeautifulSoup(req, "html5lib")

    labels = soup.find("div", {"class": "col-md-8"})

    resumes = labels.find_all(
        "div",
        {
            "class": [
                "card card-hover card-search resume-link card-visited wordwrap mt-lg",
                "card card-hover card-search resume-link card-visited wordwrap",
            ]
        },
    )

    return [
        get_resume_information("https://www.work.ua" + resume.find("a").get("href"))
        for resume in resumes
    ]


def get_resumes_pages_with_pagination(url: str):
    req = requests.get(url).content
    soup = BeautifulSoup(req, "html5lib")

    labels = soup.find("div", {"class": "col-md-8"})

    while not labels.find("li", {"class": "no-style disabled add-left-default"}):

        yield get_resumes_pages(req)

        next_page_li = labels.find("li", {"class": "no-style add-left-default"})
        next_page_url = "https://www.work.ua" + next_page_li.find("a").get("href")

        req = requests.get(next_page_url).content
        soup = BeautifulSoup(req, "html5lib")

        labels = soup.find("div", {"class": "col-md-8"})


if __name__ == "__main__":
    for i in get_resumes_pages_with_pagination("https://www.work.ua/resumes/?period=6"):
        print(len(i))