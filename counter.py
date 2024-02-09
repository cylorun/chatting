import os
def count_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return len(file.readlines())

def search_and_count_lines(root_directory):
    t = 0
    for folder, _, files in os.walk(root_directory):
        for file_name in files:
            if file_name.endswith('.py'):
                file_path = os.path.join(folder, file_name)
                line_count = count_lines(file_path)
                t+=line_count
    return t

if __name__ == "__main__":
    print(search_and_count_lines("C:\\Users\\alfgr\\Desktop\\school\\forri2-verk\\"))
    print(search_and_count_lines('/home/alfgrimur/Desktop/school/sem2/forri2/forri2-verk/'))

