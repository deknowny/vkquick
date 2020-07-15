import vkquick as vq

from . import config


@vq.Cmd(prefs=config.PREFS, names=config.NAMES)
@vq.Reaction("message_new")
def imp(id_: int, sender: vq.Sender()):
    """
    Помечает заметку как "важное"
    """
    note = vq.current.Notes.fetch_by_id(
        id_=id_, owner_id=sender.id
    )
    if note is None:
        return config.ANSWER_NOT_EXIST.format(
            id=id_
        )

    note.important = True
    vq.current.session.add(note)
    vq.current.session.commit()

    return config.ANSWER.format(
        id=id_,
        text=note.text
    )
