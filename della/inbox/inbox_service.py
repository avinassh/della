def get_participants(user_1, user_2):
    if user_1.id > user_2.id:
        return user_2, user_1
    return user_1, user_2


def get_recipient(thread, sender):
    if thread.participant_1 == sender:
        recipient = thread.participant_2
    else:
        recipient = thread.participant_1
    return recipient
