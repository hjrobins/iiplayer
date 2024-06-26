# iiplayer
A little Python script to make get_iplayer videos interlaced back to 25fps

This only requires ffmpeg and python.
I'm running it in Python 3.11.7
and ffmpeg version 7.0-essentials_build

If you just want the ffmpeg command to convert 50p videos to 25i interlaced here it is:
` -filter_complex "[0:v]select='mod(n-1,2)'[top],[0:v]select='not(mod(n-1,2))'[bottom],[top]field=top[t],[bottom]field=bottom[b],[t][b]vstack,il=l=i:c=i" -r 25`
 
The filter just takes the upper field from even frames and lower field from odd frames.

 If you want to convert 59.94p to 29.97i then just change -r to 29.97 or to 30000/1001. 

The python code is useful because it allows you to run right after downloading get_iplayer files with just the pid. It searches the default get_iplayer folder and converts it.

Adding both iiplayer.bat and iiplayer.py into get_iplayer should allow you to run iiplayer from the terminal if get_iplayer is already in environment variables.

iiplayer.bat features the default encoding options in the first 5 lines, their data is after the semi-colon and space.
The defaults are to try and maintain the original mp4 file, so it copies the original bitrate and does two-pass encoding. I have also made it libx264 in case this is run on computers that can't run nvenc but I recommend changing that to h264_nvenc if you can because it's magnitudes faster.
The iPlayer Recordings folder can include enviroment variables and spaces, it will add quotation marks around it.
ffmpeg export command requires video and audio, it can't be -c copy because the filters make it require re-encoding.
Keeping original bit rate adds `-b:v {bitrate}k`. 
Two pass adds `-pass 1 -f null /dev/null &&` and the same ffmpeg command again but with `-pass 2`, so it encodes twice but it makes it the exact filesize as the original but only with h264.


The usage is `iiplayer [input_filename or PID]`
Optional flags are `[-interlaced] [-interlacedbff] [-inverted]`

`-interlace` adds `setfield=tff` and `-flags +ildct`, and `-interlacebff` adds `setfield=bff` and `-flags +ildct`.
Also there is `-invert` which takes swaps the frames around so it will take the top field from the odd frames, and bottom field from the even frames. This might be useful if you're trying to output a progressive video but the fields are the wrong way or if you know your deinterlaced video is definitely bottom field first you can make sure it stays that way.

You can find me on Twitter @HjRobins
