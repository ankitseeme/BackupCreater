import os
import csv
from shutil import copyfile
from time import time
from math import floor
from math import ceil



unix_path = "/home/ankit/Python"
dropbox_path = "/media/ankit/New Volume/Dropbox"
windows_path = "/media/ankit/New Volume/Python"
csv_file = "/home/ankit/temp/codeCopier.csv"


def get_details(path):
	"""get directories and files details from the
	given location"""
	os.chdir(path)
	directories = []
	files_dict = {}

	#find all directories name
	for dirpath, dirnames, files in os.walk('.'):
		for dirname in dirnames:
			directories.append(os.path.join(dirpath,dirname))

	#find all file names
	for dirpath, dirnames, files in os.walk('.'):
		for name in files:
			files_dict[os.path.join(dirpath, name)] = os.path.getmtime(os.path.join(dirpath, name))

	return directories,files_dict


def create_missing_directories(path,src_dirs,trg_dirs):
	"create missing directories"
	os.chdir(path)
	count=0
	for i in src_dirs:
		if i not in trg_dirs:
			count+=1
			os.mkdir(i)
			print("Created directory " + str(i))
	if count == 0:
		print("No Directories to create")
	print("")



def copy_new_and_modified_files(src_path,trg_path,src_files,trg_files):
	"copy any new or modified file"
	os.chdir(src_path)
	new_files = []
	newcount=0
	modcount=0
	for file in src_files.keys():
		if file not in trg_files.keys():
			newcount+=1
			copyfile(src_path + file[1:],trg_path+ file[1:])
			print("Created new file at: " + trg_path + file[1:])
		elif src_files[file] > trg_files[file]:
			modcount+=1
			copyfile(src_path + file[1:],trg_path + file[1:])
			print("Copied modified file to " + trg_path + file[1:])
	if newcount == 0:
		print("No new files to copy")
	else:
		print("New files: " + str(newcount))
	if modcount == 0:
		print("No modified files to copy")
	else:
		print("Modified files: " +str(modcount))
	print("")


def get_missing_directories(src_path,trg_path,src_dirs,trg_dirs):
	"get details of directories that are in target but not in source"
	missing_dirs = []
	for dire in trg_dirs:
		if dire not in src_dirs and not dire.startswith('./.'):
				missing_dirs.append(trg_path + dire[1:]) 
	if len(missing_dirs) > 0:
		print("Below directories are in " +trg_path+ " but not in "+src_path+ " ... Please Check")
		for ms_d in missing_dirs:
			print(ms_d)
		print("")


def get_missing_files(src_path,trg_path,src_files,trg_files):
	"get details of files that are in target but not in source"
	missing_files = []
	for file in trg_files:
		if file not in src_files and not file.startswith('./.'):
			missing_files.append(trg_path + file[1:])

	if len(missing_files) > 0:
		print("Below files are in " +trg_path+ " but not in "+src_path+ " ... Please Check")
		for ms_f in missing_files:
			print(ms_f)
		print("")


def get_newly_mod_files(src_path,trg_path,src_files,trg_files):
	newly_files = []
	warning = ''
	for file in trg_files:
		if int(float(trg_files.get(file,0))) > lastStop:
			print(int(float(trg_files.get(file,0))))
			newly_files.append(file)
	if len(newly_files) > 0:
		warning += "Below files in " + trg_path+ " are modified sometime after the last backup... Please check ... "
		print("Below files in " + trg_path+ " are modified sometime after the last backup... Please check")
		for n_f in newly_files:
			print(n_f)
			warning += n_f + ", " 
		print("")
	return warning


def write_to_csv(slNo,start,unix_directories,unix_files,dropbox_directories,dropbox_files,windows_directories,windows_files,warning,remarks=''):
	with open(csv_file,'a') as f:
		writer = csv.writer(f)
		writer.writerow([slNo,start,time(),time()-start,len(unix_directories)
			,len(unix_files),len(dropbox_directories),len(dropbox_files),len(windows_directories),len(windows_files),warning,remarks])



if __name__ == '__main__':

	os.system('clear')

	start = time()

	rows=[]

	with open(csv_file,'r') as f:
		csvreader = csv.reader(f)
		for row in csvreader:
			rows.append(row)
	if len(rows) > 1:
		slNo = int(rows[-1][0]) + 1
		lastStart = int(float(rows[-1][1])) - 5
		lastStop = int(float(rows[-1][2])) + 5
		lasterror = rows[-1][10]
	else:
		slNo = 1
		lastStop = sys.maxsize

	if len(lasterror) > 1:
		print("There's a warning form the last run that needs your attention...")
		print("*"*10)
		print(lasterror)
		print("*"*10)
		choice = input("Press y to go ahead with the copy and replace. This will replace the file: ").lower()
		if choice != 'y':
			write_to_csv(slNo,start,[ ],[ ],[ ],[ ],[ ],[ ],lasterror,'skipped')
			print("Exiting now ...")
			exit(0)



	print("Development Path".ljust(25,' ') + unix_path)
	print("Dropbox Path".ljust(25,' ') + dropbox_path)
	print("Windows Path".ljust(25,' ') + windows_path)
	print("")

	unix_directories,unix_files = get_details(unix_path)
	dropbox_directories,dropbox_files = get_details(dropbox_path)
	windows_directories,windows_files = get_details(windows_path)

	print("Creating Directories for " + dropbox_path)
	create_missing_directories(dropbox_path,unix_directories,dropbox_directories)
	
	print("Copying files for " + dropbox_path)
	copy_new_and_modified_files(unix_path,dropbox_path,unix_files,dropbox_files)

	print("Creating Directories for " + windows_path)
	create_missing_directories(windows_path,unix_directories,windows_directories)

	print("Copying files for " + windows_path)
	copy_new_and_modified_files(unix_path,windows_path,unix_files,windows_files)

	get_missing_directories(unix_path,dropbox_path,unix_directories,dropbox_directories)
	get_missing_directories(unix_path,windows_path,unix_directories,windows_directories)

	get_missing_files(unix_path,dropbox_path,unix_files,dropbox_files)
	get_missing_files(unix_path,windows_path,unix_files,windows_files)

	warn_dropbox = get_newly_mod_files(unix_path,dropbox_path,unix_files,dropbox_files)
	warn_windows = get_newly_mod_files(unix_path,windows_path,unix_files,windows_files)

	write_to_csv(slNo,start,unix_directories,unix_files,dropbox_directories,dropbox_files,windows_directories,windows_files,warn_dropbox+warn_windows,remarks='')
	
	print("FINISHED")
	print(time()-start)
