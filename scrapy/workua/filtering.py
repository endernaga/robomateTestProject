async def add_filter(url: str, *args, **kwargs):
    town_and_keywords = ""
    if "town" in kwargs:
        town_and_keywords += "-" + kwargs["town"]
    if "category" in kwargs:
        town_and_keywords += "-" + kwargs["category"]

    salarys_ids = {
        "1": 1,
        "2000": 2,
        "3000": 3,
        "4000": 4,
        "5000": 5,
        "6000": 6,
        "7000": 7,
        "8000": 8,
        "9000": 9,
        "10000": 10,
        "15000": 11,
        "20000": 12,
        "25000": 13,
        "30000": 14,
        "40000": 15,
        "50000": 16,
        "100000": 17,
    }

    experience_ids = {
        0: "0+1+164+165+166",
        1: "164+165+166",
        2: "164+165",
        3: "165+166",
        4: "165+166",
    }

    if "salaryfrom" in kwargs:
        kwargs["salaryfrom"] = salarys_ids[kwargs["salaryfrom"]]

    if "salaryto" in kwargs:
        kwargs["salaryto"] = salarys_ids[kwargs["salaryto"]]

    if "experience" in kwargs:
        if int(kwargs["experience"]) > 4:
            kwargs["experience"] = "166"
        else:
            kwargs["experience"] = experience_ids[int(kwargs["experience"])]

    query_filters = ["salaryfrom", "salaryto", "experience"]
    filtered_params = {
        key: value for key, value in kwargs.items() if key in query_filters
    }

    if filtered_params:
        url += "?" + "&".join(
            f"{key}={value}" for key, value in filtered_params.items()
        )

    if kwargs.get("keywords"):
        town_and_keywords += "-" + "+".join(kwargs["keywords"].split())

        url += "&notitle=1" if filtered_params else "?notitle=1"

    return url[:27] + town_and_keywords + url[28:]
