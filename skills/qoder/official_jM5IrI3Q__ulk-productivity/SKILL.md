---
name: ulk-productivity
description: "macOS productivity CLIs: remindctl (Apple Reminders), gogcli (Google Calendar), peekaboo (screenshot/OCR), ranger (file manager), notesmd (markdown notes), apple-notes-cli (Apple Notes), op (1Password). Use for task management, calendar, screenshots, and note-taking."
---

# Productivity CLIs

## remindctl (Apple Reminders)
Prerequisite: `command -v remindctl` — macOS only
Install: `brew install steipete/formulae/remindctl`

```bash
remindctl list                                    # List all reminders
remindctl add 'Ship v1.0' --list 'My Project' --due tomorrow  # Add reminder
remindctl complete <id>                           # Complete reminder
remindctl search 'deploy'                         # Search reminders
```

## gogcli (Google Calendar)
Prerequisite: `command -v gogcli` — macOS, requires OAuth
Install: `brew install steipete/formulae/gogcli`

```bash
gogcli events list --calendar primary --from today --to '+7d'
gogcli events create --title 'Standup' --start '2026-03-24T10:00' --duration 30m
gogcli calendars list
```

## peekaboo (Screenshot/OCR)
Prerequisite: `command -v peekaboo` — macOS only
Install: `brew install steipete/formulae/peekaboo`

```bash
peekaboo screenshot --output screen.png
peekaboo ocr --input screen.png
peekaboo list-windows
```

## ranger (File Manager TUI)
Prerequisite: `command -v ranger`
Install: macOS `brew install ranger` / Linux `pip install ranger-fm`

```bash
ranger /path/to/docs
ranger --choosefile=/tmp/selected
```

## notesmd (Markdown Notes)
Prerequisite: `command -v notesmd`
Install: `go install github.com/Yakitrak/notesmd-cli@latest`

```bash
notesmd create 'sprint-review'
notesmd list
notesmd search 'deploy'
```

## apple-notes-cli (Apple Notes.app)
Prerequisite: `command -v apple-notes-cli` — macOS only
Install: `git clone https://github.com/angelespejo/apple-notes-cli.git ~/apple-notes-cli && cd ~/apple-notes-cli && ./install.sh`

### Notes
```bash
apple-notes-cli add 'Sprint Review My Project'        # Create note
apple-notes-cli add 'My Project' 'Sprint Review'      # Create note in folder
apple-notes-cli open 'Sprint Review'             # Open note
apple-notes-cli exists 'Sprint Review'           # Check if note exists
apple-notes-cli rm 'Sprint Review'               # Delete note
```

### Folders
```bash
apple-notes-cli add-folder 'My Project'                # Create folder
apple-notes-cli add-folder 'My Project' 'Sprints'      # Create subfolder
apple-notes-cli rm-folder 'Sprints'               # Delete folder
```

## op (1Password CLI)
Prerequisite: `command -v op`
Install: macOS `brew install --cask 1password-cli`

```bash
op item get 'Vercel Token' --fields password
op read 'op://Vault/Item/password'
eval $(op signin)
```
