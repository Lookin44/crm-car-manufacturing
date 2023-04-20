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
) = map(chr, range(8))
END = ConversationHandler.END
