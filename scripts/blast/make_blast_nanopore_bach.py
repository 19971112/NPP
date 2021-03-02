import glob
import sys
import os

def main():
  data_path = sys.argv[1]
  work_path = sys.argv[2]
  dirs_path_list = glob.glob(data_path)
  
  script1 = open('~/github/NPP/scripts/nanopore_16S_1.sh', 'r')
  
  for each_dir_path in dirs_path_list:
    dir_basename = os.path.basename(each_dir_path)
    file_name = 'nanopore_16S_1_' + dir_basename + '.job'
    dir_path = data_path + data_basename
    custom_script = original_script1.replace("$working_dir", work_path)
    custom_script = custom_script.replace("$data_dir", dir_path)
    
    make_script_file(file_name,custom_script)

    
def make_script_file(FILE_NAME,SCRIPT_TXT):
  file = opne(FILE_NAME, 'w')
  file.write(SCRIPT_TXT)
  
  
main()
