konata-dance <br>
made by colyst, dc: .memo_ <br>

```
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
#  Quit:               crtl + shift + q                                                                                             #
#  Interaction Toggle: ctrl + shift + t (hold to drag)                                                                              #
#  Shadows Toggle:     ctrl + shift + y                                                                                             #
#  Spotify Toggle:     ctrl + shift + u (requires a setup and will prompt you to sign in through a browser when you first open it)  #
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

!!! Remember to change r'YOUR GIF PATH' with your GIF's path, such as: r'C:\Users\kiyom\OneDrive\Images\konata-dance.gif' .
this file is optimiezed and it doesn't eat up resources.
```
### !!! SCROLL DOWN FOR MORE INFOR AND CUSTOMIZATION !!!
 ***[Click here to download.](https://github.com/colyst/konata-dance/releases/download/gif-displayer/konata-dance.pyw)*** <br>
[Click here to download the GIF.](https://github.com/colyst/konata-dance/releases/download/gif-displayer/konata-dance.gif)
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
v
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

```
= = = = = = =
= FEATURES: =
= = = = = = =

-=> You can adjust the GIF's size by changing target_width. The aspect ratio will be the same. (Default is 400)
-=> You can adjust how many shadows are present and how frequently they update. Look below at "1-" for more info.
-=> You can change what feature is enabled and disabled when the app starts. Look below at "2-" for more info.
-=> The GIF can adjust its speed to match the current song's BPM. Look beloaw at "3-" for more info.
-=> You can change the color of the shadows at "shadow_color". RGB values. (Default is shadow_color = QColor(23, 44, 180, transparency))

!-> REMEMBER TO REPLACE gif_path IN THE FILE WITH WHERE YOUR GIF IS.
#-> REMEMBER TO PUT YOUR SPOTIFY APP'S CLIENT ID AND SECRET IF YOU WANT TO USE THE "ADJUST GIF SPEED WITH BPM" FEATURE. ALSO, REMEMBER TO PUT http://localhost:8888/callback AS THE REDIRECT URI WHEN YOU ARE CREATING THE SPOTIFY APP.
```

===========================================================================

## 1- Adjusting shadows:
   - self.shadow_timer.start(100)        -> every 100ms, adjust as you like.
   - self.shadow_delay_timer.start(100)  -> every 100ms, adjust as you like.
   - self.shadow_widgets = [QLabel(self) for _ in range(4)]   -> "in range(4)" means there will be 4 shadows. Less is fine but if you want more than 4 shadows, you'll need to adjust the maths. If you want 1 shadow, use "in range(1)".

===========================================================================
 
 ## 2- Choose which features are enabled or disabled when the app starts:
 
   - self.interaction_enabled = True    -> Interaction is enabled by default. (True for enabled False for disabled.) FIRST LETTER IS CASE SENSITIVE.

   - self.shadows_enabled = False    -> Shadows are disabled by default. (True for enabled False for disabled.) FIRST LETTER IS CASE SENSITIVE.

   - self.bpm_speed_adjustment_enabled = False    -> GIF speed adjustment is disabled by default. (True for enabled False for disabled.) FIRST LETTER IS CASE SENSITIVE.
```
! REMEMBER TO PROPERLY TYPE True AND False OTHERWISE IT'LL GIVE AN ERROR.
```

===========================================================================

## 3- Using Spotify to adjust the GIF speed:
  - Log in to Spotify. (on your web browser)
  - Go to "https://developer.spotify.com/dashboard/create"
  - Name it, give it a description, and leave the website part blank.
  - Put "http://localhost:8888/callback" as a redirect URI and click the Add button.
  - Choose Web API in the boxes.
  - Understand and agree with Spotify's Developer Terms of Service and Design Guidelines
  
   After these steps are done,
  - Go to "https://developer.spotify.com/dashboard" and click on your app, then click Settings.
  - Copy your client ID and replace 'put your client id' with your client ID in the code.
  - Go back to the dashboard, click on View client secret, and copy it. Then replace 'put your client secret' with your client secret in the code.

   LAST STEP:
  - UNCOMMENT THESE 3 LINES:
    ```
    #SPOTIPY_CLIENT_ID = 'put your client id'
    #SPOTIPY_CLIENT_SECRET = 'put your client secret'
    #SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback' #USE THIS REDIRECT URI FOR SIMPLICITY
    ```
  - It should look like this:
     ```
     SPOTIPY_CLIENT_ID = '62135randomnumbersandletters'
     SPOTIPY_CLIENT_SECRET = 'evenmore361278random127numbers1623and1236754letters'
     SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback' #USE THIS REDIRECT URI FOR SIMPLICITY
     ```
   Then open the app, do CTRL + SHIFT + U to turn on speed adjustment, and log in to Spotify when it asks.
  - ! Tip: If the GIF doesn't match the song, adjust scaling_factor as you like. (Default is 0.4)
  - It will check if the song is changed every 5 seconds, so be patient. (adjust with self.bpm_timer.start(5000), default is 5000, it's in ms.).

===========================================================================
