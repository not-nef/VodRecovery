
# Donations
* <a href="https://paypal.me/VodRecovery" class="button">Support The Project</a> - Donations are not expected in any circumstances or are required to use the script. However if you do decide to donate know that it is greatly appreicated.


# VodRecovery
* Created By: ItIckeYd
* Initial Release: May 3rd, 2022
* The script is used to retrieve sub-only and deleted videos/clips from twitch.
* Credits to daylamtayari - [TwitchRecover](https://github.com/TwitchRecover/TwitchRecover) repository helped with the logic to recover twitch videos.

# Script Installation
1. Download/Install Python - [Python Website](https://www.python.org/downloads/)
2. Clone repository
3. Navigate into cloned directory
4. Install required packages ``` pip install -r requirements.txt ``` (Run in terminal)
5. Run Script

```
git clone https://github.com/ItIckeYd/VodRecovery
cd vodrecovery
pip install -r requirements.txt
python recovervod.py
```

# Script Notes
* The script CANNOT recover every single vod. The script can only recover vods that still exist on the twitch vod domains.
* Twitch saves broadcasts for up to 14 days (60 days for Partners, Turbo and Prime Users). The script notify you how old the broadcast is.
* The script uses UTC timezone as default when recovering vods.
* If using manual recover please ensure to input the seconds value as 00 when running the script as the script brute forces the seconds value automatically.
* TwitchTracker/StreamsCharts/Sullygnome are the sites that are currently supported by the script for vod and clip recovery.
* **SullyGnome Note:**  vod retrieval for SullyGnome assumes the year is the current year as there is no year indication on the website when looking at a particlular stream.

# Script Preview
```
WELCOME TO VOD RECOVERY
1) Recover Vod
2) Recover Clips
3) Unmute an M3U8 file
4) Check M3U8 Segments
5) Generate M3U8 file (ONLY includes valid segments)
6) Download M3U8 (.MP4 extension)
7) Exit

Please choose an option:
```

# Downloading of M3U8 links
* In order to download an M3U8 choose option 5 in the main menu and input the M3U8 link.
* The script **ONLY** downloads the available segments.. if there are invalid segments the vod will skip to the next available segment.
* The MP4 will be created in your **Documents** folder. Temp files are automatically removed once download is complete.

# Analytical Sites
* The following sites can be used to provide the information that the script requires:
1. [TwitchTracker.com](https://twitchtracker.com/)
2. [Sullygnome.com](https://sullygnome.com/)
3. [Streamscharts.com](https://streamscharts.com/)

# Optional IDE
* Python has a few code editors that can be used which include the following:
1. PyCharm - [Pycharm Download](https://www.jetbrains.com/pycharm/download/#section=windows)
2. Visual Studio Code - [Visual Studio Code Download](https://code.visualstudio.com/)

# Additional Notes
* If creating an issue for a problem that your experiencing please provide atleast 1 example.
* If you are not getting results back from the script. Please try vods from other streamers, if the other streamers vods give you results then the original vods you were trying probably just don't exist. 


# Latest Release
[Stable Release 1.0.5.0](https://github.com/ItIckeYd/VodRecovery/releases/tag/1.0.5.0-Full-Release)
**- For fully updated code please download code from the **Main** branch** 

