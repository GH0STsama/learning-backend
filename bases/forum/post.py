import dataclasses
import bases.forum.comment
import bases.forum.user_forum

@dataclasses.dataclass
class Post:
    id: int
    title: str
    body: str
    users: list[bases.forum.user_forum.UserForum]
    comments: list[bases.forum.comment.Comment]
