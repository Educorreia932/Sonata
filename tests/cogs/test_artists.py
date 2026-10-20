from unittest.mock import MagicMock, patch

import pytest
from cogs.artists.artists import ArtistCog


@pytest.mark.asyncio
async def test_artist_ratings_command(
    artists_cog: ArtistCog, mock_ctx: MagicMock
) -> None:
    fake_ratings = [
        MagicMock(score=8),
        MagicMock(score=6),
    ]
    fake_view = MagicMock()
    fake_pages = [MagicMock()]

    mock_artist = MagicMock(artist="Test Artist")

    mock_ratings_query = MagicMock()
    mock_ratings_query.__len__ = MagicMock(return_value=len(fake_ratings))
    mock_ratings_query.__iter__ = MagicMock(return_value=iter(fake_ratings))

    with (
        patch("cogs.artists.artists.AlbumIndex") as mock_album_index,
        patch("cogs.artists.artists.Rating") as mock_rating_model,
        patch(
            "cogs.artists.artists.paginate_embeds",
            return_value=(fake_view, fake_pages),
        ),
    ):
        mock_album_index.select.return_value.join.return_value.join.return_value.where.return_value.group_by.return_value.order_by.return_value.first.return_value = mock_artist
        mock_rating_model.select.return_value.join.return_value.where.return_value.order_by.return_value.limit.return_value = mock_ratings_query

        await artists_cog.artist_ratings.callback(
            artists_cog, mock_ctx, artist_name="Test Artist"
        )

        mock_ctx.send.assert_called_once_with(
            embed=fake_pages[0],
            view=fake_view,
        )


@pytest.mark.asyncio
async def test_best_rated_artists(artists_cog: ArtistCog, mock_ctx: MagicMock) -> None:
    fake_view = MagicMock()
    fake_pages = [MagicMock()]

    with (
        patch("cogs.artists.artists.Album"),
        patch("cogs.artists.artists.Rating"),
        patch(
            "cogs.artists.artists.paginate_embeds",
            return_value=(fake_view, fake_pages),
        ),
    ):
        await artists_cog.best_rated_artists.callback(artists_cog, mock_ctx)

        mock_ctx.send.assert_called_once_with(embed=fake_pages[0], view=fake_view)


@pytest.mark.asyncio
async def test_most_rated_artists(artists_cog: ArtistCog, mock_ctx: MagicMock) -> None:
    fake_view = MagicMock()
    fake_pages = [MagicMock()]

    with (
        patch("cogs.artists.artists.Album"),
        patch("cogs.artists.artists.Rating"),
        patch(
            "cogs.artists.artists.paginate_embeds",
            return_value=(fake_view, fake_pages),
        ),
    ):
        await artists_cog.most_rated_artists.callback(artists_cog, mock_ctx)

        mock_ctx.send.assert_called_once_with(embed=fake_pages[0], view=fake_view)
