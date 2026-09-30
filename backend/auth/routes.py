from fastapi import APIRouter, HTTPException, status

from backend.api.schemas import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    TokenResponse,
)

from backend.auth.service import (
    register_user,
    authenticate_user,
)


router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    request: RegisterRequest
):

    try:

        user = register_user(
            username=request.username,
            email=request.email,
            password=request.password
        )

        return user

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    request: LoginRequest
):

    result = authenticate_user(
        email=request.email,
        password=request.password
    )

    if result is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return result