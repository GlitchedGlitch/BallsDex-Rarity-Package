# Rarity Package
Create a rarity command, fully customizable in the settings file!
## How to install
Add this to config/extra.toml (or create the file if it doesn't exist)
```toml
# Rarity Package
[[ballsdex.packages]]
location = "git+https://github.com/GlitchedGlitch/Ballsdex-Rarity-Package.git@2.0.0"
path = "rarity"
enabled = true
```
## Settings
In the admin panel there are three settings:
* **Embed color**: That's the embed line color displayed on the message, you can leave it empty for no color at all
* **Style**: This changes the visual style of the rarity list between Embed (Ballsdex V2 style) or Container (Ballsdex V3 style)
* **Buttons**: If move the navigation buttons inside the rarity list message (available only in container style)
