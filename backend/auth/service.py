from backend.auth.models import (
    create_user,
    get_user_by_email,
)

from backend.auth.security import (
    create_access_token,
    hash_password,
    verify_password,
)


def register_user(
    username: str,
    email: str,
    password: str
):

    existing_user = get_user_by_email(
        email
    )

    if existing_user:

        raise ValueError(
            "A user with this email already exists"
        )


    password_hashed = hash_password(
        password
    )


    user_id = create_user(
        username=username,
        email=email,
        password_hash=password_hashed
    )


    return {
        "id": user_id,
        "username": username,
        "email": email,
        "role": "user"
    }


def authenticate_user(
    email: str,
    password: str
):

    user = get_user_by_email(
        email
    )


    if not user:

        return None


    if not verify_password(
        password,
        user["password_hash"]
    ):

        return None


    access_token = create_access_token(
        user_id=user["id"],
        email=user["email"],
        role=user["role"]
    )


    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
    }