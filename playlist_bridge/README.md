# Playlist Bridge — Spotify CSV to YouTube playlist

A lightweight, local-first web app. No npm, paid plan, or Spotify developer credentials required. It **does not download songs**, bypass workplace network policies, or access Spotify's audio.

## Run

1. Extract the ZIP.
2. On a PC with Python 3, open a terminal in this folder and run `python server.py` (on Windows, `py server.py` also works).
3. Visit **http://localhost:8000** in your browser.
4. On your **personal connection** (off the restricted network), export your *own* Spotify playlist's metadata to CSV with an authorized playlist export service, and transfer the CSV file to your laptop according to workplace rules. A Spotify playlist URL **alone is not an import**.
5. Click **Import Spotify CSV**, then use **Search** and **Match** to select each YouTube music video. For 1,000 songs, in-app matching is optional if you configure a YouTube Data API key.
6. To upload, optionally configure Google API credentials as below. Or export progress and use the app to track matches manually.

## Google API configuration (optional)

1. Go to [Google Cloud Console](https://console.cloud.google.com/) on a permitted network.
2. Create a project, enable **YouTube Data API v3**.
3. Create an **API key** for searching tracks inside the app. Restrict it appropriately in Google Cloud. Key is stored in your browser's localStorage; use only on a device you trust.
4. Set up **OAuth consent screen**, and create an **OAuth client ID** (Web application). Add `http://localhost:8000` as an authorized JavaScript origin. Add your Google account as a test user if your OAuth app is in testing mode.
5. In app settings, enter the API key and OAuth client ID and click Save. Connect Google, create a private YouTube playlist, and upload matched songs in batches of ten.

Note: Google may restrict unverified apps and users should review its OAuth warnings. Some OAuth refreshes require reconnecting. Playlist write access uses the `youtube` OAuth scope. This app never asks for or stores your Google password.

## Limits and realities

- This is a **working manual matching and playlist-building tool**, **not** a one-click automatic 1,000-song migration service.
- YouTube's default Data API quota (as of October 2026) separately caps `search.list` to **100 calls per day**, and playlist insertions cost **50 quota units per song** out of the **10,000 combined daily units**. At default limits, 1,000 inserts require **multiple days**. Check latest official quotas in your Google Cloud project.
- Some video matches will be covers/remixes, region-blocked, or unavailable on YouTube Music. Verify each selection. YouTube playlists and YouTube Music visibility aren't guaranteed to have identical catalog behavior.
- The tool can resume uploads when opened again on the *same browser and device*, but clearing browser storage resets progress. Use **Export progress JSON** regularly.
- CSV formats vary; common column labels are supported. Download **example CSV** for a template.
- It does not import playlists automatically from Spotify's API; export Spotify metadata separately.
- Your playlist data and configured credentials are saved only in browser localStorage. Do not use on public/shared computers.

## Troubleshooting

- **Unable to access Cloud Console or Google OAuth from work**: do the integration steps on your own device and permitted network. You can still use the local CSV importer at work if allowed.
- **Could not load Google sign-in**: confirm browser network access to `accounts.google.com`, and authorized JS origin matches `http://localhost:8000`.
- **Quota exceeded**: stop and resume the next day. Upload history is saved after each successful addition.
- **No songs imported**: check CSV headers; the app expects song titles and artists. Download the example CSV for format.
- **File opened with `file://`**: viewing and CSV/matching may work, but OAuth is not expected to work. Use the included server instead.

Official docs: https://developers.google.com/youtube/v3/determine_quota_cost and https://developers.google.com/youtube/data/getting-started

## Automatic matching and upload (v1.1)

- Open the app, connect your Google account, and create a destination playlist if you have not already done so.
- Choose **Auto-match unmatched**, which will process up to 90 songs per run by default. Each search uses the official YouTube Data API through your OAuth token; a separate API key is no longer required for automatic matching.
- High-confidence matches are ready for automatic upload. Ambiguous matches are saved for review; the matching heuristic is not guaranteed to select the exact recording.
- Click **Upload all high-confidence matches** to add them to the existing playlist, up to 190 songs per run or the available daily quota.
- The app saves its state in browser localStorage using the **same key as v1**, so it should retain old CSV imports and progress when used on the **same browser and origin** (`http://localhost:8000`). Export a backup first.
- Quotas (Google's current documented defaults): 100 `search.list` calls/day, and 10,000 units/day shared among other methods. `playlistItems.insert` costs 50 units each. Quotas reset at midnight Pacific Time. The app pauses on errors and needs an open browser tab; it does not run in the background.
- This is a best-effort music/video matcher using publicly available YouTube search data. Results may differ from Spotify recordings. YouTube Music may not display every ordinary YouTube video as a music track.
