from server.models.dicts.base.user_base_dict import UserBaseDict


class UserUpdateDict(UserBaseDict, total=False):
    """TypedDict for UserUpdate request model.\n
    This TypedDict is used to define the structure of the UserRegister data.\n
    """

    group_ids: list[int]


class UserRegisterDict(UserUpdateDict, total=False):
    """TypedDict for UserRegister request model.\n
    This TypedDict is used to define the structure of the UserRegister data.\n
    """

    name: str
    email: str
