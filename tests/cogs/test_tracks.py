from unittest.mock import MagicMock, patch

import pytest
from cogs.tracks.tracks import TracksCog


@pytest.mark.asyncio
async def test_lyrics(tracks_cog: TracksCog, mock_ctx: MagicMock) -> None:
    fake_view = MagicMock()
    fake_pages = [MagicMock()]
    fake_user = MagicMock(lastfm_username="testuser")
    synced_lyrics = "[00:01.00] Line one\n[00:02.00] Line two"

    with (
        patch("cogs.tracks.tracks.UserInfo") as mock_user_info,
        patch(
            "cogs.tracks.tracks.get_last_played",
            return_value=("Test Album", "Test Artist", "Test Track"),
        ),
        patch("cogs.tracks.tracks.search", return_value=synced_lyrics),
        patch(
            "cogs.tracks.tracks.paginate_embeds",
            return_value=(fake_view, fake_pages),
        ),
    ):
        mock_user_info.get_or_none.return_value = fake_user

        await tracks_cog.lyrics.callback(tracks_cog, mock_ctx)

        mock_ctx.send.assert_called_once_with(embed=fake_pages[0], view=fake_view)


@pytest.mark.asyncio
async def test_samples(tracks_cog: TracksCog, mock_ctx: MagicMock) -> None:
    fake_embed = MagicMock()
    fake_relationships = {
        "artist_name": "Test Artist",
        "track_name": "Test Track",
        "cover_url": "http://example.com/cover.jpg",
        "url": "http://example.com",
        "relationships": {
            "samples": [MagicMock()],
            "interpolates": [],
            "sampled_in": [],
        },
    }

    with (
        patch(
            "cogs.tracks.tracks.get_track_relationships",
            return_value=fake_relationships,
        ),
        patch("cogs.tracks.tracks.samples_embed", return_value=fake_embed),
    ):
        await tracks_cog.samples.callback(tracks_cog, mock_ctx, track_name="Test Track")

        mock_ctx.send.assert_called_once_with(embed=fake_embed)
