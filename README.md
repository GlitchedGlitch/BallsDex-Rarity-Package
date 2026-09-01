# Rarity Package

Creates a rarity command, fully customizable in the admin panel!

## How to install

Add this to `config/extra.toml` (or create the file if it doesn't exist):

```toml
# Rarity Package
[[ballsdex.packages]]
location = "git+https://github.com/GlitchedGlitch/Ballsdex-Rarity-Package.git@3.0.0"
path = "rarity"
enabled = true
```

## Features

| Feature              | Description                                                                                                                                |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Embed Color**      | Changes the embed line color displayed on the message. Leave it empty for no color.                                                        |
| **Style**            | Changes the visual style of the rarity list between **Embed** (BallsDex V2 style) and **Container** (BallsDex V3 style).                   |
| **Buttons**          | Moves the navigation buttons inside the rarity list message. Available only in **Container** style.                                        |
| **Tier Mode**        | Replaces the standard rarity calculation with a simpler system using tiers instead of raw rarity values.                                   |
| **Entries per Page** | Controls how many rarity entries are displayed per page. **7 is recommended** to prevent the command from becoming too large or cluttered. |
| **Thumbnail**        | Controls whether the bot's profile picture is displayed as a thumbnail.                                                                    |
| **Search**           | Enables or disables searching for a specific ball or special.                                                                              |
| **Rarity Search**    | Expands the search feature to allow searching for balls by their rarity value. Requires **Search** to be enabled.                          |
| **Ephemeral**        | Enables or disables ephemeral mode, allowing the rarity list to be visible only to the user who ran the command.                           |
