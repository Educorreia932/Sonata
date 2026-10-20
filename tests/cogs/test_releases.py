from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from cogs.releases.releases import ReleasesCog


@pytest.mark.asyncio
async def test_release_command(releases_cog: ReleasesCog, mock_ctx: MagicMock) -> None:
    fake_release = {"name": "Test Album"}
    fake_embed = MagicMock()

    with (
        patch(
            "cogs.releases.releases.fetch_album",
            new=AsyncMock(return_value=fake_release),
        ) as mock_fetch,
        patch(
            "cogs.releases.releases.album_embed", return_value=fake_embed
        ) as mock_embed,
    ):
        await releases_cog.release.callback(
            releases_cog, mock_ctx, release_name="Test Album"
        )

        mock_fetch.assert_called_once_with("123", "Test Album")
        mock_embed.assert_called_once_with(fake_release)
        mock_ctx.send.assert_called_once_with(embed=fake_embed)


@pytest.mark.asyncio
async def test_who_rated_release(
    releases_cog: ReleasesCog, mock_ctx: MagicMock
) -> None:
    fake_release = {"name": "Test Album"}
    fake_ratings = [
        MagicMock(score=8),
        MagicMock(score=6),
    ]

    fake_view = MagicMock()
    fake_pages = [MagicMock()]

    with (
        patch(
            "cogs.releases.releases.fetch_album",
            new=AsyncMock(return_value=fake_release),
        ) as mock_fetch,
        patch("cogs.releases.releases.Rating") as mock_rating_model,
        patch(
            "cogs.releases.releases.paginate_embeds",
            return_value=(fake_view, fake_pages),
        ) as mock_paginate,
    ):
        mock_rating_model.select.return_value.where.return_value.order_by.return_value.iterator.return_value = fake_ratings

        await releases_cog.who_rated_release.callback(
            releases_cog, mock_ctx, release_name="Test Album"
        )

        mock_fetch.assert_called_once_with("123", "Test Album")
        mock_paginate.assert_called_once()
        mock_ctx.send.assert_called_once_with(
            embed=fake_pages[0],
            view=fake_view,
        )


@pytest.mark.asyncio
async def test_best_rated_releases_success(
    releases_cog: ReleasesCog, mock_ctx: MagicMock
) -> None:
    album1 = MagicMock()
    album1.rating_sum = 40
    album1.rating_count = 5

    album2 = MagicMock()
    album2.rating_sum = 27
    album2.rating_count = 3

    fake_albums = [album1, album2]

    fake_view = MagicMock()
    fake_pages = [MagicMock()]

    with (
        patch("cogs.releases.releases.Album") as mock_album_model,
        patch("cogs.releases.releases.Rating"),
        patch(
            "cogs.releases.releases.paginate_embeds",
            return_value=(fake_view, fake_pages),
        ) as mock_paginate,
    ):
        mock_album_model.select.return_value.join.return_value.where.return_value.group_by.return_value.having.return_value = fake_albums

        await releases_cog.best_rated_releases.callback(releases_cog, mock_ctx)

        mock_paginate.assert_called_once()

        mock_ctx.send.assert_called_once_with(
            embed=fake_pages[0],
            view=fake_view,
        )


@pytest.mark.asyncio
async def test_most_rated_releases(
    releases_cog: ReleasesCog, mock_ctx: MagicMock
) -> None:
    fake_view = MagicMock()
    fake_pages = [MagicMock()]

    mock_query = MagicMock()
    mock_query.__len__ = MagicMock(return_value=2)

    with (
        patch("cogs.releases.releases.Album") as mock_album,
        patch("cogs.releases.releases.Rating"),
        patch(
            "cogs.releases.releases.paginate_embeds",
            return_value=(fake_view, fake_pages),
        ),
    ):
        mock_album.select.return_value.where.return_value.join.return_value.group_by.return_value.order_by.return_value.limit.return_value = mock_query

        await releases_cog.most_rated_releases.callback(releases_cog, mock_ctx)

        mock_ctx.send.assert_called_once_with(embed=fake_pages[0], view=fake_view)


@pytest.mark.asyncio
async def test_random_rating(releases_cog: ReleasesCog, mock_ctx: MagicMock) -> None:
    fake_rating = MagicMock()
    fake_user = MagicMock()
    fake_embed = MagicMock()

    with (
        patch("cogs.releases.releases.Rating") as mock_rating,
        patch("cogs.releases.releases.rating_embed", return_value=fake_embed),
    ):
        mock_rating.select.return_value.where.return_value.order_by.return_value.first.return_value = fake_rating
        mock_ctx.bot.fetch_user = AsyncMock(return_value=fake_user)

        await releases_cog.random_rating.callback(releases_cog, mock_ctx)

        mock_ctx.send.assert_called_once_with(embed=fake_embed)


@pytest.mark.asyncio
async def test_album_of_the_year(
    releases_cog: ReleasesCog, mock_ctx: MagicMock
) -> None:
    fake_view = MagicMock()
    fake_pages = [MagicMock()]

    mock_query = MagicMock()
    mock_query.__len__ = MagicMock(return_value=2)

    with (
        patch("cogs.releases.releases.Rating") as mock_rating,
        patch(
            "cogs.releases.releases.paginate_embeds",
            return_value=(fake_view, fake_pages),
        ),
    ):
        mock_rating.select.return_value.join.return_value.where.return_value.order_by.return_value = mock_query

        await releases_cog.album_of_the_year.callback(releases_cog, mock_ctx, year=2025)

        mock_ctx.send.assert_called_once_with(embed=fake_pages[0], view=fake_view)
