def validate_movie(title, release_date):
    title = title.strip()
    release_date = release_date.strip()
    if (title == '' or release_date == ''):
        return False
    else:
        return True


def validate_actor(name, age, gender):
    name = name.strip()
    age = age.strip()
    gender = gender.strip()
    if (name == '' or age == '' or gender == ''):
        return False
    else:
        return True
