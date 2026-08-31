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
To exit the settings you must create a new file called `rarity_settings.txt`, and paste the following

```
embed_color=
style=
buttons_inside=
```
embed color is the color of the line on the message
style is the style of the message, can be either embed or container
buttons_inside is if make the navigation buttons inside the message, available only if style is container
