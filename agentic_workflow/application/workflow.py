
class WorkflowError(Exception):
    pass


class UserAlreadySetError(WorkflowError):
    def __init__(self):
        self.message = "User ID already set"
        self.status_code = 400
        super().__init__(self.message)

class UserNotFoundError(WorkflowError):
    def __init__(self):
        self.message = "User not found"
        self.status_code = 404
        super().__init__(self.message)



class WorkflowTest:
    def __init__(self) -> None:
        self._id: str | None = None

    def insert_id(self, user_id: str):
        if self._id is not None:
            raise UserAlreadySetError()
        self._id = user_id

    @property
    def id(self) -> str:
        if self._id is None:
            raise UserNotFoundError()
        return self._id