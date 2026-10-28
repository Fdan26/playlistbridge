# 🎵 Playlist Bridge — User Guide

**Transfer your Spotify playlists to YouTube Music without downloading songs or manually matching every track.**

Playlist Bridge is a free, local-first web application that imports Spotify playlist information, searches YouTube for matching tracks, and creates a YouTube playlist using the official YouTube Data API.

## 1. Requirements

Before starting, make sure you have:

- A computer running Windows, macOS, or Linux.
- Python 3 installed.
- A Google account with a YouTube profile.
- A Spotify playlist exported as a CSV file.
- An internet connection with access to Google and YouTube services.

**Note:** You do not need Spotify Premium or YouTube Premium to use the migration app itself.

## 2. Download and run Playlist Bridge

1. Download the code — either click **Code → Download ZIP** on GitHub and extract it, or run:

```bash
git clone https://github.com/<your-username>/playlist-bridge.git
cd playlist-bridge
```

2. Open a terminal in the project folder (the one that contains `server.py`).
3. Run:

```bash
python server.py
```

On Windows, you can also try:

```bash
py server.py
```

4. Open your browser and visit:

```text
http://localhost:8000
```

The Playlist Bridge dashboard should appear.

Keep the terminal running while using the application.

## 3. Export your Spotify playlist

Spotify does not offer a built-in CSV export button, so use a playlist export service.

1. Visit https://exportify.app/ on a network where Spotify is accessible.
2. Sign in using your Spotify account.
3. Find the playlist you want to transfer.
4. Click **Export** to download its CSV file.
5. Save the file to your computer.

The CSV should contain information such as song titles, artist names, and albums.

Playlist Bridge supports common Exportify-style CSV formats.

## 4. Import your playlist

1. Open Playlist Bridge.
2. Click **Import Spotify CSV** or **Choose CSV / TSV / JSON file**.
3. Select your exported playlist file.
4. Wait for the import to finish.
5. Check the **Imported tracks** counter.

For example:

- Imported tracks: 556
- Matched: 0
- Uploaded: 0
- Remaining: 556

This is normal. Importing the file does not automatically upload songs.

## 5. Set up Google Cloud API

This setup is required to search for tracks automatically and create your YouTube playlist.

### A. Create a project

1. Visit https://console.cloud.google.com/
2. Sign in with your Google account.
3. Click **New Project**.
4. Name it `Playlist Bridge`.
5. Create the project.

### B. Enable YouTube Data API

1. Visit https://console.cloud.google.com/apis/library/youtube.googleapis.com
2. Select your Playlist Bridge project.
3. Click **Enable**.

### C. Configure Google OAuth

1. Open https://console.cloud.google.com/auth/overview
2. Configure the Google Auth Platform if prompted.
3. Set the application name to `Playlist Bridge`.
4. Set the audience to **External**.
5. Keep the application in **Testing** mode.
6. Go to **Audience → Test users**.
7. Click **Add users**.
8. Add your Google account and save.

**Important:** Your account must be included as a test user, or Google may display Error 403: Access denied.

### D. Create an OAuth Client ID

1. Open https://console.cloud.google.com/auth/clients
2. Click **Create Client**.
3. Select **Web application**.
4. Name it `Playlist Bridge Local`.
5. Under **Authorized JavaScript origins**, add:

```text
http://localhost:8000
```

6. Create the client.
7. Copy the generated **Client ID**.

The Client ID usually ends with:

```text
.apps.googleusercontent.com
```

Do not put your Google password or OAuth client secret into Playlist Bridge.

## 6. Connect Google to Playlist Bridge

1. Return to the Playlist Bridge dashboard.
2. Open **Google API & upload settings**.
3. Paste your Google OAuth Client ID.
4. Click **Save settings**.
5. Click **Connect Google account**.
6. Sign in using your authorized Google test account.
7. Review and approve the requested YouTube permissions.

If Google shows an unverified application warning, verify that the project and Client ID belong to you before choosing the available testing option.

Once connected, Playlist Bridge can search YouTube and manage playlists with your permission.

An additional YouTube API key is optional for the app's manual in-app search feature; the automatic matching function uses the Google OAuth connection.

## 7. Automatically match songs

This is the main feature of Playlist Bridge.

1. Locate the **Automatic transfer** section.
2. Find the **Maximum searches per run** field.
3. Leave its default value at `90`, or enter a smaller number.
4. Click **Auto-match unmatched**.
5. Confirm the action.
6. Keep the browser tab open while processing.

The app automatically searches YouTube using each song's title and artist.

Tracks are classified into:

- **High-confidence match:** The app found a likely corresponding song.
- **Needs review:** A result was found, but its accuracy is uncertain.
- **Unmatched:** No sufficiently convincing result was found.

You do not need to manually search high-confidence tracks, although occasional incorrect matches are possible.

**Important:** YouTube API quotas limit how many songs can be searched per day. If the limit is reached, the process pauses. You can resume in another session.

## 8. Create your YouTube playlist

1. Find **Build your playlist**.
2. Enter your preferred playlist name.
3. Make sure Google is connected.
4. Click **Create YouTube playlist**.
5. Wait for confirmation.

The app should display the destination playlist information.

Creating the playlist alone does not add songs. You must complete the upload step.

## 9. Automatically upload matched songs

After the matching process:

1. Locate **Automatic transfer**.
2. Click **Upload all high-confidence matches**.
3. Confirm the operation.
4. Keep the browser tab open.
5. Wait while Playlist Bridge adds the matching videos to your YouTube playlist.

The app skips tracks already recorded as uploaded.

For uncertain matches, review the selected result before uploading.

You can also use **Upload next 10 matched songs** for smaller batches.

## 10. Open your playlist in YouTube Music

Once the upload is complete, check:

- YouTube: https://www.youtube.com/feed/playlists
- YouTube Music: https://music.youtube.com/library/playlists

Sign in using the same Google account connected to Playlist Bridge.

**Note:** YouTube Music may not show every ordinary YouTube video as a music track. Some matches may be unavailable or may appear only on regular YouTube.

YouTube Music can be used for free, although advertisements and playback restrictions may apply.

## 11. Save your progress

Playlist Bridge stores playlist information and transfer progress in your browser's local storage.

To keep a backup:

1. Open **Backup & privacy**.
2. Click **Export progress JSON**.
3. Save the JSON file somewhere safe.

To restore a backup:

1. Click **Restore backup**.
2. Select the saved JSON.
3. Confirm the restoration.

Restoring a backup replaces the current local project.

**Avoid clearing your browser data before exporting a backup.**

## Project structure

```text
playlist-bridge/
├── public/            # Static web app served at http://localhost:8000
│   ├── index.html     # Page markup
│   ├── css/style.css  # Styles
│   └── js/app.js      # App logic (CSV import, matching, YouTube API, storage)
├── server.py          # Tiny local web server (Python standard library only)
└── README.md
```

Put your own Spotify CSV exports in a `my_playlists/` folder — it is listed in `.gitignore` so your personal data is never committed.

## API quotas

YouTube's default Data API quota allows **100 `search.list` calls per day** and **10,000 units per day** shared across other methods. Each `playlistItems.insert` costs **50 units**, so at default limits a 1,000-song playlist takes **several days** to upload. Quotas reset at midnight Pacific Time. Check the current values in your Google Cloud project: https://developers.google.com/youtube/v3/determine_quota_cost

## 12. Troubleshooting

| Problem | Solution |
|---|---|
| Google Error 403 | Add your Google account under OAuth Test users. |
| Google sign-in fails | Check the OAuth Client ID and `http://localhost:8000` origin. |
| Songs not imported | Verify the CSV headers and file format. |
| Playlist is empty | Run automatic matching and upload the matched songs. |
| API quota exceeded | Resume after your quota resets. |
| Wrong song matched | Review the match and choose the correct recording. |
| Playlist not visible in YouTube Music | Check the playlist on regular YouTube and verify that it contains music-compatible videos. |
| Progress disappeared | Restore your previously exported JSON backup. |
| App does not load | Check that Python is running and port 8000 is available. |
| Opened via `file://` | OAuth will not work — always use `python server.py` and `http://localhost:8000`. |

## 13. Important limitations

- Playlist Bridge does not download Spotify audio.
- The app does not provide Spotify's licensed audio directly.
- Automatic matching may occasionally select covers, live versions, remixes, or incorrect songs.
- Automatic transfers depend on official YouTube API quotas.
- You must keep the browser tab open during processing.
- Multiple Spotify playlists require separate project handling; the current version is primarily designed around one destination playlist.
- Browser-local data may be lost if storage is cleared.
- Do not use the app to bypass organizational network restrictions.

## 14. Recommended workflow

For large playlists, follow this order:

**Export Spotify CSV → Import into Playlist Bridge → Configure Google → Connect account → Auto-match songs → Create YouTube playlist → Upload high-confidence matches → Review remaining tracks → Open YouTube Music.**

Repeat the automatic matching and uploading steps as needed until the playlist is complete.

---

**Project:** Playlist Bridge — Automatic Edition

**Technology:** HTML, CSS, JavaScript, Python local HTTP server, Google OAuth 2.0, YouTube Data API v3

**Purpose:** Personal playlist migration without audio downloads.

**License and usage:** Personal experimental project. Respect the terms of the connected music platforms.

**Google API documentation:** https://developers.google.com/youtube/v3