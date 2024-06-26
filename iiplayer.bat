::iPlayer location; %USERPROFILE%\Desktop\iPlayer Recordings
::ffmpeg export command; -c:v libx264 -c:a copy
::Keep Original Bit Rate?; True
::Output Extension; mp4
:: Two Pass?; True
::--defaults--

::the defaults are in order the first 5 lines, their data is after the semi-colons and space.
:: location can include enviroment variables and spaces
::ffmpeg export command requires video and audio, it can't be -c copy because it requires re-encoding
:: keeping original bit rate adds -b:v {bitrate}k. Two pass adds -pass 1 -f null /dev/null &&, and then -pass 2
:: so it encodes twice but it makes it the exact filesize as the original but only with h264.
::I recommend changing it to h264_nvenc if you can because it's magnitudes faster


@echo off
python "C:\Program Files\get_iplayer\iiplayer.py" %*
