import glob
import sys
import os

def main():
  data_path = sys.argv[1]
  work_path = sys.argv[2]
  dirs_path_list = glob.glob(data_path)
  
  scr1 = '/home/t16965tw/github/NPP/scripts/nanopore_16S_1.sh'
  scr2 = '/home/t16965tw/github/NPP/scripts/nanopore_16S_2.sh'
  
  for each_dir_path in dirs_path_list:
    file_name = return_file_name(each_dir_path, '1')
    custom_script = return_custum_script(scr1,work_path,each_dir_path)
    make_script_file(file_name,custom_script)

    
def make_script_file(FILE_NAME,SCRIPT_TXT):
  file = opne(FILE_NAME, 'w')
  file.write(SCRIPT_TXT)

  
def return_file_name(DIR_PATH, NUMBER):
  dir_basename = os.path.basename(DIR_PATH)
  file_name = 'nanopore_16S_' + NUMBER + '_' + dir_basename + '.job'
  return file_name


def return_custum_script(SCRIPT_PATH,WORK_PATH,EACH_DIR_PATH):
  output = open(SCRIPT_PATH, 'r')
  output_txt = output.read()
  output_txt = output_txt.replace("$working_dir", WORK_PATH)
  output_txt = output_txt.replace("$data_dir", EACH_DIR_PATH)
  return output_txt
  
main()
