"""
Generates a CSV file: directory tree for a given directory including the count of files in each folder.Represents the hierarchical structure of folders and subfolders within the specified directory. 

1. The count_files() Number of files in a directory and its subdirectories.

2. The create_tree() function generates a nested dictionary representing the directory tree structure. It uses os.walk() to traverse the directory and adds the file count as a special key 'file_count' in each folder node.

3. The print_tree() function recursively prints the directory tree to the console or a file.

4. The export_to_csv() It uses the csv.writer object to write the tree data, including column headers.

5. The write_to_csv() function is a helper function that recursively writes each folder's path and file count to the CSV file.

"""

import os
import csv

def count_files(directory):
    file_count = 0
    for _, _, files in os.walk(directory):
        file_count += len(files)
    return file_count

def create_tree(directory):
    tree = {}
    for root, dirs, files in os.walk(directory):
        if root == directory:
            continue
        path = os.path.relpath(root, directory)  # Get the relative path from the directory
        node = tree
        for folder in path.split(os.sep):
            node = node.setdefault(folder, {})
        node['__file_count__'] = count_files(root)
    return tree

def print_tree(tree, indent=0, file=None):
    for key, value in tree.items():
        if key == '__file_count__':
            if file:
                file.write(f"{' ' * indent}Total Files: {value}\n")
        else:
            if file:
                file.write(f"{' ' * indent}{key}/\n")
            print_tree(value, indent + 4, file)

def export_to_csv(tree, csv_filename):
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Folder', 'File Count'])
        write_to_csv(tree, writer)

def write_to_csv(tree, writer, folder=''):
    for key, value in tree.items():
        if key == '__file_count__':
            writer.writerow([folder, value])
        else:
            new_folder = os.path.join(folder, key)
            write_to_csv(value, writer, new_folder)

directory_path = r"C:\Users\pobe4699\OneDrive - The University of Sydney (Staff)\to_organise_One_drive\02_Work\02_Projects\04_Silicosis\Lung_CT_Data\2-Italian group"

#directory_path = r"C:\Users\pobe4699\OneDrive - The University of Sydney (Staff)\to_organise_One_drive\02_Work\02_Projects\04_Silicosis\data\inf_Net-data\COVID-SemiSeg\COVID-SemiSeg"

tree = create_tree(directory_path)

csv_filename = 'directory_tree_Italia.csv'
export_to_csv(tree, csv_filename)

print(f"Directory tree exported to: {csv_filename}")
