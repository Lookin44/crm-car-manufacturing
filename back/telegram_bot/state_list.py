from telegram.ext import ConversationHandler


(
    CHOOSING,
    TYPING_REPLY,
    TYPING_CHOICE,
    REGISTRATION,
    ADD_MYSELF,
    CHOOSE_ACTION,
    CONFIRM,
    DISAGREE,
    NAME,
    LAST_NAME,
    PATRONYMIC,
    EMPLOYEE_ID,
    TYPING,
    PHOTO,
    SHIFT,
    POSITION,
    SHOP,
    ZONE,
    CHOOSE_EDIT_INFO
) = map(chr, range(19))
END = ConversationHandler.END
