def add_filter(url: str, *args, **kwargs):
    if "salaryfrom" in kwargs.keys():
        url += f"&salaryfrom={kwargs['salaryfrom']}"
    if "salaryto" in kwargs.keys():
        url += f"&salaryto={kwargs['salaryto']}"
    if "experience" in kwargs.keys():
        url += f"&experience={kwargs['experience']}"
    if "town" in kwargs.keys():
        url = url[:27] + kwargs["town"] + "/" + url[28:]

    return url