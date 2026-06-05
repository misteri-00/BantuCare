def detect(description):

    keywords = [
        "transfer sekarang",
        "jamin",
        "cepat kaya",
        "hadiah besar"
    ]

    for keyword in keywords:

        if keyword in description.lower():
            return True

    return False