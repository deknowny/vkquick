import vkquick as vq

from . import config


@vq.Cmd(prefs=config.PREFS, names=config.NAMES)
@vq.Reaction("message_new")
async def all_(sender: vq.Sender(), peer_id: vq.PeerID()):
    """
    Возвращает список всех заметок
    """
    query = vq.current.session.query(
        vq.current.Notes
    )

    important_notes = query.filter_by(
        owner_id=sender.id, important=True, done=False
    ).all()

    undone_notes = query.filter_by(
        owner_id=sender.id, important=False, done=False
    ).all()

    done_notes = query.filter_by(
        owner_id=sender.id, done=True
    ).all()

    important_notes_list = _get_list(important_notes)
    undone_notes_list = _get_list(undone_notes)
    done_notes_list = _get_list(done_notes)

    document_text = config.DOCUMENT_TEXT_PATTERN.format(
        important_notes=important_notes_list,
        undone_notes=undone_notes_list,
        done_notes=done_notes_list
    )
    document = vq.Doc.message(
        document_text,
        peer_id=peer_id,
        type_="doc"
    )
    document = await document(title="tasks.txt")

    return vq.Message(
        config.ANSWER,
        attachment=document
    )


def _get_list(notes):
    """
    Возвращает текстовый список тех или иных заметок
    """
    if notes:
        return "\n".join(
            f"{ind}. [{note.id}]: {note.text}"
            for ind, note in enumerate(notes, 1)
        )
    else:
        return config.NOT_EXIST
