# iiplayer
A little Python script to make get_iplayer videos interlaced back to 25fps


If you just want the ffmpeg command to convert 50fps 50p videos to 25i interlaced here it is:
 -filter_complex "[0:v]select='mod(n-1,2)'[top],[0:v]select='not(mod(n-1,2))'[bottom],[top]field=top[t],[bottom]field=bottom[b],[t][b]vstack,il=l=i:c=i" -r 25

 The rest of the python code just searches the default get_iplayer folder and allows you to convert it.
