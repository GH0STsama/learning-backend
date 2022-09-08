import bases.forum.comment
import bases.forum.post
import bases.user

class UserForum(bases.user.User):
    def __init__(self) -> None:
        self.comments: list[bases.forum.comment.Comment]
        self.posts: list[bases.forum.post.Post]
