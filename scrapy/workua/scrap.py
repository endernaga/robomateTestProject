import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def fetch_content(url: str, session: aiohttp.ClientSession):
    async with session.get(url) as response:
        return await response.text()


async def get_resume_information(url: str, session: aiohttp.ClientSession):
    content = await fetch_content(url, session)
    soup = BeautifulSoup(content, "html5lib")

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

    additional_information = soup.find("dl", class_="dl-horizontal")
    all_criterial = [item.text for item in additional_information.find_all("dt")]
    for index, item in enumerate(all_criterial):
        if "Місто" in item:
            location = additional_information.find_all("dd")[index].text.strip().replace("\xa0", " ")
            break
    else:
        location = None

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
        "url": url
    }


async def get_resumes_pages(content, session):
    soup = BeautifulSoup(content, "html5lib")

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

    resume_urls = [
        "https://www.work.ua" + resume.find("a").get("href")
        for resume in resumes
    ]

    tasks = [get_resume_information(url, session) for url in resume_urls]
    return await asyncio.gather(*tasks)


async def get_resumes_pages_with_pagination(url: str):
    async with aiohttp.ClientSession() as session:
        req = await fetch_content(url, session)
        soup = BeautifulSoup(req, "html5lib")

        labels = soup.find("div", {"class": "col-md-8"})

        while not labels.find("li", {"class": "no-style disabled add-left-default"}):
            resumes = await get_resumes_pages(req, session)
            yield resumes

            next_page_li = labels.find("li", {"class": "no-style add-left-default"})
            if not next_page_li:
                break

            next_page_url = "https://www.work.ua" + next_page_li.find("a").get("href")

            req = await fetch_content(next_page_url, session)
            soup = BeautifulSoup(req, "html5lib")

            labels = soup.find("div", {"class": "col-md-8"})


async def main():
    async for resumes in get_resumes_pages_with_pagination("https://www.work.ua/resumes/?period=6"):
        print(len(resumes))


if __name__ == "__main__":
    asyncio.run(main())
