# Soundscape Player

A browser-based ambient mixer. Seven simultaneous looping tracks, each with a file dropdown and an independent volume slider, plus a master Play and master volume.

Built as a static site so you can host it free on GitHub Pages and share one link with your team.

## Folder layout

```
soundscape-player/
  index.html              ← the player
  start.command           ← Mac one-click launcher
  start.bat               ← Windows one-click launcher
  manifest.json           ← list of pieces, categories, files (generated)
  generate_manifest.py    ← rescans audio/ and rewrites manifest.json
  audio/
    Dusk Song/            ← one folder per "piece" (any human-readable name)
      world_sounds/       ← drop loops here
      neurotones/
      foundation/
      harmony/
      melody/
      accents/
      low_end/
    Another Piece/
      world_sounds/
      ...
```

The piece dropdown at the top of the player lists every folder under `audio/`. Selecting a piece repopulates the seven category dropdowns from that piece's files.

## Try it locally

Browsers refuse to load `<audio>` from `file://`, so you need a tiny HTTP server. There's a one-click launcher for each platform.

1. Drop a few audio files into the right `audio/<category>/` folders.
2. Regenerate the manifest:
   ```
   python3 generate_manifest.py
   ```
3. **Mac:** double-click `start.command`. **Windows:** double-click `start.bat`. Both will start a local server on port 8765 and open the player in your default browser.

   Manual alternative: `python3 -m http.server 8000` from this folder, then open <http://localhost:8000>.

> The first time you run `start.command` on Mac, macOS may block it with a Gatekeeper warning. Right-click → **Open** → **Open** to whitelist it. Or run `chmod +x start.command` in Terminal once.

## Publish on GitHub Pages

1. Create a new GitHub repo and push this folder to it.
2. In the repo: **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main`, folder: `/ (root)` → Save**.
3. Wait ~1 minute. Your URL will be `https://<your-username>.github.io/<repo-name>/`.
4. Share that URL with your team.

If your audio is large or you want to keep it out of git, see "Hosting audio elsewhere" below.

## Adding a new piece

1. Create a new folder under `audio/` named whatever you want (e.g. `audio/Morning Light/`).
2. Run `python3 generate_manifest.py` — it auto-creates the seven empty category subfolders inside.
3. Drop your loops into the appropriate category subfolders.
4. Run `python3 generate_manifest.py` again to refresh `manifest.json`.
5. Commit & push (or just refresh locally).

## Adding new audio to an existing piece

1. Drop the file into `audio/<piece>/<category>/`.
2. Run `python3 generate_manifest.py`.
3. Commit & push:
   ```
   git add audio/ manifest.json
   git commit -m "add new loops"
   git push
   ```
4. GitHub Pages updates within a minute. Hard-refresh the browser.

## Notes & gotchas

- **File formats — important for gapless**: looping is sample-accurate inside the browser's audio thread, but MP3 and AAC encoders add small amounts of silent padding to the start and end of every file, which produces an audible click or gap at the loop point regardless of player. **Use WAV, FLAC, OGG Vorbis, or Opus** for true gapless. WAV is largest but bulletproof; OGG Vorbis and Opus give big size savings without the padding problem.
- **Looping**: implemented via Web Audio API (`AudioBufferSourceNode.loop = true`), so the loop point is computed on the audio thread, not the JS event loop. As long as your source file's first and last sample line up (any properly-rendered loop), playback is gapless.
- **Sync**: all 7 tracks are started at the same `audioContext.currentTime` when you press Play, sample-aligned. They share one audio clock so they will not drift relative to each other.
- **Loading**: audio files are fetched and decoded once, then cached. The first Play press waits for decode (you'll see "Loading…" briefly); after that, switching dropdowns is instant for files you've already heard.
- **Categories are fixed at 7.** If you want to rename one (e.g. "Low End" → "Sub Bass"), edit `CATEGORIES` in both `generate_manifest.py` and near the top of `index.html`.
- **GitHub repo size**: GitHub recommends keeping repos under 1 GB. If your audio library will exceed that, host the audio on S3, Cloudflare R2, or Backblaze B2 and change `audio/...` paths in `manifest.json` (or in `setTrack()` inside `index.html`) to absolute URLs.

## Hosting audio elsewhere (optional)

If you put audio on a separate host:
- The host must serve CORS headers (`Access-Control-Allow-Origin: *` or your Pages domain).
- Replace the bare filename in `manifest.json` with a full URL, OR change one line in `setTrack()` to use that URL directly.
