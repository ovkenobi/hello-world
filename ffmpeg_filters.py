import os
import sys

FFMPEG = "D:\\Cloud.Mail.ru\\Distr\\ffmpeg\\ffmpeg.exe"

def to_wav(file):
    newfile=file[:file.rfind(".")]+'.wav'
    if os.path.isfile(newfile):
        os.remove(newfile)
    cmd='"{}" -i "{}" -ac 1 "{}"'.format(FFMPEG, file, newfile)
    os.popen(cmd)
    if os.path.isfile(newfile) and os.stat(newfile).st_size>1000: return newfile
    return None


def normalize(file):
    ext = file[file.rfind("."):]
    newfile=file[:file.rfind(".")]+'_norm'+ext
    if os.path.isfile(newfile):
        os.remove(newfile)
    cmd='"{}" -i "{}" -af dynaudnorm "{}"'.format(FFMPEG, file, newfile)
    os.popen(cmd)
    if os.path.isfile(newfile) and os.stat(newfile).st_size>1000: return newfile
    return None


def cut_silence(file):
    ext = file[file.rfind("."):]
    newfile=file[:file.rfind(".")]+'_norm'+ext
    if os.path.isfile(newfile):
        os.remove(newfile)
    cmd='"{}" -i "{}" -af silenceremove=0:0:0:-1:0.9:-45dB "{}"'.format(FFMPEG, file, newfile)
    os.popen(cmd)
    if os.path.isfile(newfile) and os.stat(newfile).st_size>1000: return newfile
    return None


def get_duration(file):
    if not (os.path.isfile(file) and os.stat(file).st_size>10): return None
    cmd='"{}" -i "{}" 2>&1 | find "Duration"'.format(FFMPEG, file)
    res=os.popen(cmd).read()
    res=res[res.find("Duration: ")+10:res.find(", start")]
    hh,mm,ss = res.split(':')
    ss = float(ss) + float(mm)*60+float(hh)*3600
    return ss

def detect_part_witout_silence(file, duration, lavel):
    if not (os.path.isfile(file) and os.stat(file).st_size>10): return None
    cmd='"{}" -i "{}" -af silencedetect=n={}dB:d={} -f null nul 2>&1 | find "silencedetect"'.format(FFMPEG, file, lavel, duration)
    res=os.popen(cmd).read().split('\n')
    print(res)

#def multipart(file):
    


if __name__ == "__main__":
    if len(sys.argv)>1:
        detect_part_witout_silence(sys.argv[1], 0.4, -40)
        detect_part_witout_silence(sys.argv[1], 0.3, -30)
        print(get_duration(sys.argv[1]))
    else:
        print("Error args")
