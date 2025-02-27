[![pypi](https://img.shields.io/pypi/v/bard-cli)](https://pypi.org/project/bard-cli)
![](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fperrette%2Fbard%2Frefs%2Fheads%2Fmain%2Fpyproject.toml)

# Bard  <img src="https://github.com/perrette/bard/raw/main/bard_data/share/icon.png" width=48px>

Bard is a text to speech client that integrates on the desktop

## Install

Install libraries or system-specific dependencies:

```bash
sudo apt-get install portaudio19-dev xclip #  portaudio19-dev becomes portaudio with Homebrew
sudo apt install libcairo-dev libgirepository1.0-dev gir1.2-appindicator3-0.1  # Ubuntu ONLY (not needed on MacOS)
pip install PyGObject # Ubuntu ONLY (not needed on MacOS)
```

Install the main app with all its optional dependencies:

```bash
pip install bard-cli[all]
```

### GNOME

On GNOME desktop you can subsequently run:
```bash
bard-install [...] --openai-api-key $OPENAI_API_KEY
```
to produce a `.desktop` file for GNOME's quick-launch
(the `[...]` indicates any argument that `bard` takes)

## Usage

In a terminal:

```bash
bard
```
which defaults to:
```bash
bard --backend openaiapi --voice allow --model tts-1
```
(this assumes the environment variable `OPENAI_API_KEY` is defined)

An icon should show up almost immediately in the system tray, with options to copy the content of the clipboard (the last thing you copy-pasted)
and send that to the AI model for reading aloud.

<img src=https://github.com/user-attachments/assets/a90ccd1c-7431-4554-9d41-0e9c1b4399f2 width=300px>

You can also do a one-off reading by indicating the source content with one of the following:

```bash
bard --text "Hello world, how are you today"
bard --clipboard
bard --url "example.com" # also accepts file://
bard --html-file /path/to/downloaded.html # access a page with paywal, download it, feed it to bard
bard --pdf-file /path/to/document.pdf  # careful if you pay for it... (the full thing will be transcribed even if you listen to a small bit of it)
bard --audio-file /path/to/audio.mp3 # no actual request, only useful for testing the audio player
```
The above command will still launch the system tray icon, and so provide access to the audio player's (basic) controls.
There is also a terminal version via the `--no-tray` parameter, with the same elementary controls as in the system tray.
And for a one-off execution of the program without controls, use `--no-prompt`.

The clipboard parsing capabilities are elaborate enough so that it can detect an URL, a file path or common HTML markup.
If a file path is detected, the extension is checked for `.html`-ish and `.pdf`, and the data is extracted accordingly.
Here we make good use of the most useful work on [readability](https://pypi.org/project/readability-lxml).
In particular, this allows relatively easy reading out of webpages behind paywals, by right-clicking on "View Page Source" (or download the html file if the source doesn't contain the text), select all text, copy and just proceed with bards' "Process Copied Text" or `--clipboard` options.
For other articles not protected by a paywall, copying the URL should suffice.

You can resume the previous recording (the audio won't play right away in this case, but you can use the reader):
```bash
bard --resume
```
You can ask also ask the app to removed your (local) traces:
```bash
bard --clean-cache-on-exit
```

## Fine-tuning

```bash
bard --chunk-size 500  # that's the default
```
sets the maximum length (in characters) of a request. That means about 30 seconds of speech.
The program will split up the text in chunks (according to the punctuation) and download them sequentially.
The reading will start with the first chunk, that's why it is convenient to keep it small.
You can set that smaller or up to the maximum allowed by the openai API (4096).

## Player

The player was devised in conversation with Mistral's Le Chat and Open AI's Chat GPT, and my own experience with `pystray` on [scribe](https://github.com/perrette/scribe). It works.
I'm open for suggestion for other, platform-independent integrations to the OS.
TODO: I want to add a functioning "Open with external reader" option. At the moment it is experimental and only accounts for the first file.

## Android

I was able to install bard on Android via the excellent [Termux](https://termux.dev) emulator. Not everything works: the tray system app does not work, the clipboard option only partially works (**only plain text is copied**). However I could obtain a decent workflow for one-off reading (no player controls) via:
```bash
bard --no-tray --clipboard
```
For paywalled articles, I ended up opening them in Firefox, acessing the Reading mode (excellent, though sometimes the icon is hidden in the URL bar), selecting all text, copying, and running the above command (for free articles just copy paste the URL). This requires the termux API `pkg install termux-api`.


## Roadmap

Include more backends including local ones.