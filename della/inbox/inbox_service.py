def get_participants(user_1, user_2):
    if user_1.id > user_2.id:
        return user_2, user_1
    return user_1, user_2
