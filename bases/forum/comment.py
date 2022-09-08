import dataclasses
import bases.forum.post
import bases.forum.user_forum

@dataclasses.dataclass
class Comment:
    id: int
    body: str
    user: bases.forum.user_forum.UserForum
    post: bases.forum.post.Post 
