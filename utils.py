def validate_movie(movie):
    title = movie.title.strip()
    release_date = movie.release_date.strip()
    if (title == '' or release_date == ''):
        return False
    else:
        return True


def validate_actor(actor):
    name = actor.name.strip()
    age = actor.age.strip()
    gender = actor.gender.strip()
    if (name == '' or age == '' or gender == ''):
        return False
    else:
        return True
