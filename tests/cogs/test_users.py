from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from cogs.users.users import UsersCog


@pytest.mark.asyncio
async def test_set_lastfm(users_cog: UsersCog, mock_ctx: MagicMock) -> None:
    with patch("cogs.users.users.UserInfo") as mock_user_info:
        mock_user_info.get_or_create.return_value = (MagicMock(), True)

        await users_cog.set_lastfm.callback(users_cog, mock_ctx, username="testuser")

        mock_user_info.get_or_create.assert_called_once_with(
            user_id=str(mock_ctx.author.id),
            defaults={"lastfm_username": "testuser"},
        )
        mock_ctx.send.assert_called_once_with(
            "Your last.fm username has been set to **testuser**."
        )


@pytest.mark.asyncio
async def test_ratings_rank(users_cog: UsersCog, mock_ctx: MagicMock) -> None:
    fake_view = MagicMock()
    fake_view.pages = [MagicMock()]

    with (
        patch("cogs.users.users.Rating"),
        patch("cogs.users.users.ratings_rank_view", return_value=fake_view),
    ):
        await users_cog.ratings_rank.callback(users_cog, mock_ctx)

        mock_ctx.send.assert_called_once_with(embed=fake_view.pages[0], view=fake_view)


@pytest.mark.asyncio
async def test_profile(users_cog: UsersCog, mock_ctx: MagicMock) -> None:
    fake_embed = MagicMock()

    with (
        patch("cogs.users.users.Rating") as mock_rating,
        patch("cogs.users.users.Album"),
        patch("cogs.users.users.profile_embed", return_value=fake_embed),
    ):
        mock_rating.select.return_value.where.return_value.scalar.return_value = 7.5
        mock_rating.select.return_value.join.return_value.where.return_value.group_by.return_value.count.return_value = 5

        await users_cog.profile.callback(users_cog, mock_ctx)

        mock_ctx.send.assert_called_once_with(embed=fake_embed)


@pytest.mark.asyncio
async def test_import_ratings(users_cog: UsersCog, mock_ctx: MagicMock) -> None:
    csv_content = (
        "RYM Rating,Rating,Title, First Name,Last Name,Release_Date\r\n"
        "3.50,7,Test Album,Test,Artist,2020\r\n"
    )
    fake_response = MagicMock(ok=True, text=csv_content)
    fake_attachment = MagicMock(url="http://example.com/ratings.csv")
    mock_ctx.message.attachments = [fake_attachment]

    with (
        patch("cogs.users.users.requests.get", return_value=fake_response),
        patch("cogs.users.users.Rating") as mock_rating,
        patch(
            "cogs.users.users.UsersCog.import_rating",
            new=AsyncMock(),
        ) as mock_import,
    ):
        mock_rating.delete.return_value.where.return_value.execute.return_value = None

        await users_cog.import_ratings.callback(users_cog, mock_ctx)

        assert mock_import.call_count == 1
        mock_ctx.send.assert_called_once()
