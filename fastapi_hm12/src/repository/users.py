from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from src.entity import UsersTable, UserTokensTable
from src.database import get_connection_db
from src.schemas import NewUserSchema, TokenUpdateRequest
from src.config import logger


async def get_user_by_email(
    email: str, db: AsyncSession = Depends(get_connection_db)
) -> UsersTable | None:
    """
    Return a user object from the database bu email

    Args:
        email (str): The email addres of the user to search for.
        db (AsyncSession): The database session for executing queries.

    Returns:
        UsersTable|None: The user object if found, otherwise None.
    """
    user_query = select(UsersTable).filter_by(email=email)
    user = await db.execute(user_query)
    user = user.scalar_one_or_none()
    return user


async def create_user(
    body: NewUserSchema, db: AsyncSession = Depends(get_connection_db)
) -> UsersTable:
    """
    Create a new user in the database

    Args:
        body (NewUserSchema): The data for the new user, incliding email,
        password, etc.
        db (AsyncSession, optional): The database session for executing queries.
        Defaults to Depends(get_connection_db).

    Returns:
        UsersTable: The newly created user object

    Raises:
        Exception: If there is an error fetching the Gravatar image
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar: str = g.get_image()
    except Exception as err:
        logger.error(err)
    new_user = UsersTable(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(
    user: UsersTable,
    token: TokenUpdateRequest | None,
    token_type: str,
    db: AsyncSession,
) -> None:
    """
    Update or add a token for a user in the databese

    Args:
        user (UsetsTable): The user obj with the user's id.
        token (str): The new token value to store.
        token_type (str): The type of token (e.g., "refresh_token").
        db (AsyncSession): The database session for executing queries.

    What the function does:
        1. Finds the user's tokens in the database.
            user_tokens = UserTokensTable(
                    user_id=1,
                    refresh_token="old_token",
                    email_token="email_token"
                    )
        2. If user_tokens not None, reload tokens value
        3. If user_tokens is None, create new UserTokensTable object with user_id and token value
        4. Saves the changes to the database.
        5. Handles errors by rolling back the transaction.

    Returns:
        None
    """
    try:
        user_query = select(UserTokensTable).filter_by(user_id=user.id)
        result = await db.execute(user_query)
        user_tokens = result.scalar_one_or_none()
        if user_tokens:
            setattr(user_tokens, token_type, token)
            update_query = (
                update(UserTokensTable)
                .where(UserTokensTable.user_id == user.id)
                .values(**{token_type: token})
            )
            await db.execute(update_query)

        else:
            new_token = UserTokensTable(user_id=user.id, **{token_type: token})
            db.add(new_token)
            user_tokens = new_token

        await db.commit()
        await db.refresh(user_tokens)

    except Exception as err:
        await db.rollback()
        logger.error(f"Failed to update user's token: {err}/{token_type}")
        raise err


async def get_token(user: UsersTable, token_type: str, db: AsyncSession) -> str | None:
    """
    Get the token value for a user with the database

    Args:
        user (UsersTable): object user from database
        token_type (str): the type of token
        db (AsyncSession): async session for executing queries

    Returns:
        str|None: encoded token:str  or  None
    """
    try:
        user_query = select(UserTokensTable).filter_by(user_id=user.id)
        result = await db.execute(user_query)
        user_token = result.scalar_one_or_none()

        if user_token:
            return getattr(user_token, token_type, None)
        else:
            return None
    except Exception as err:
        logger.error(f"Failed to get user token: {err}/{token_type}")
        raise err


async def confirmed_email(email: str, db: AsyncSession) -> None:
    """change confirmed status of user to True"""
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()
    await db.refresh(user)


async def update_user_password(user: UsersTable, password: str, db: AsyncSession):
    """change user password"""
    user = await get_user_by_email(email=user.email, db=db)
    user.password = password
    await db.commit()
    await db.refresh(user)
    return user


async def update_avatar_url(email: str, url: str | None, db: AsyncSession):
    """change user avatar url"""
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user
