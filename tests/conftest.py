"""Shared pytest fixtures for tests."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from cogs.artists.artists import ArtistCog
from cogs.releases.releases import ReleasesCog
from cogs.tracks.tracks import TracksCog
from cogs.users.users import UsersCog
from discord.ext import commands


@pytest.fixture
def bot() -> MagicMock:
    """Create a mock bot instance."""
    return MagicMock()


@pytest.fixture
def artists_cog(bot: commands.Bot) -> ArtistCog:
    """Create an ArtistsCog instance with a mocked bot."""
    return ArtistCog(bot)


@pytest.fixture
def releases_cog(bot: commands.Bot) -> ReleasesCog:
    """Create a ReleasesCog instance with a mocked bot."""
    return ReleasesCog(bot)


@pytest.fixture
def tracks_cog(bot: commands.Bot) -> TracksCog:
    """Create a TracksCog instance with a mocked bot."""
    return TracksCog(bot)


@pytest.fixture
def users_cog(bot: commands.Bot) -> UsersCog:
    """Create a UsersCog instance with a mocked bot."""
    return UsersCog(bot)


@pytest.fixture
def mock_ctx() -> commands.Context:
    """Create a mock Discord context with common properties."""
    ctx = MagicMock()
    ctx.send = AsyncMock()
    ctx.author = MagicMock(id=123)
    ctx.author.display_name = "TestUser"
    ctx.message = MagicMock(author=MagicMock(id=123))
    ctx.guild = MagicMock(
        name="Test Server",
        members=[MagicMock(id=123), MagicMock(id=456)],
    )
    ctx.bot = MagicMock()
    ctx.bot.fetch_user = AsyncMock()

    # Setup typing context manager
    ctx.typing = MagicMock()
    ctx.typing.return_value.__aenter__ = AsyncMock()
    ctx.typing.return_value.__aexit__ = AsyncMock()

    return ctx


@pytest.fixture
def mock_ctx_with_fetch_user(mock_ctx: commands.Context) -> commands.Context:
    """Create a mock context with a pre-configured fetch_user."""

    def setup_fetch_user(user_id: str) -> MagicMock:
        return MagicMock(id=user_id)

    mock_ctx.bot.fetch_user = AsyncMock(side_effect=setup_fetch_user)

    return mock_ctx
