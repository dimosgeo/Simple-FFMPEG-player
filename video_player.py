from tkinter import filedialog,Tk
from os import path,system
import ffmpeg
import sys

def browseFiles():
	filename = filedialog.askopenfilename(initialdir = "./", title = "Select a File", filetypes = (("Video","*.mkv;*.mp4;*.avi"),("all files","*.*")))
	return filename

def check_ass(f_path,video_name):
	return path.isfile(f_path+"/"+video_name+".ass")

def create_ass(f_path,video_name):
	v_file=f_path+"\\"+video_name
	if(path.isfile(f_path+"/"+video_name+".srt")):
		cmd='ffmpeg -sub_charenc ISO-8859-7 -i "{}.srt" "{}.ass"'.format(v_file,v_file)
		system(cmd)
		return 1
	return 0

def play_video(f_path,subs_path,video_name,video_ext,sub_is_true):
	v_file=f_path+"\\"+video_name
	s_file=subs_path+"\\\\"+video_name
	cmd=''
	#-loglevel quiet
	#drawer="drawtext=text='%{pts\\:hms}':box=1:x=(w-tw):y=h-(lh)"
	if(sub_is_true==1):
		drawer="drawtext=text='%{pts\\:hms}':box=1:x=(w-tw):y=h-(lh)"
		cmd='ffplay -autoexit -vf "subtitles=\'{}.ass\':force_style=\'Fontsize=24\', {}" -i "{}{}"'.format(s_file,drawer,v_file,video_ext)
	else:
		cmd='ffplay -autoexit -i "{}{}"'.format(v_file,video_ext)
	system(cmd)		

if __name__ == '__main__':
	root = Tk()
	root.withdraw()
	f_path=browseFiles()
	path_array=[p for p in f_path.split("/")]
	video_ext=path_array[-1][-4:]
	video_name=path_array[-1][:-4]
	subs_path=list(path_array[0])
	subs_path="\\".join(subs_path)
	subs_path=subs_path+"\\\\"+"\\\\".join(path_array[1:-1])
	f_path="\\".join(path_array[:-1])
	temp='"'+f_path+"\\"+video_name+'.mkv"'
	sub_is_true=0
	if(video_name==""):
		sys.exit()
	if(not check_ass(f_path,video_name)):
		sub_is_true=create_ass(f_path,video_name)
	else:
		sub_is_true=1
	play_video(f_path,subs_path,video_name,video_ext,sub_is_true)