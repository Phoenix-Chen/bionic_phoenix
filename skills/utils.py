
def has_access(update, conf):
    """
        this function checks whether user has access
    """
    user = update.message.from_user
    id = int(user['id'])
    if id not in conf["white_list"]:
        update.message.reply_text("You don't have access to me yet.")
        return False
    return True