#!/bin/python

import shutil
import argparse


def todo_archive(in_list, out_list):

    # in_list is a list containing todo items - including completed
    # out_list is a list of archived todo items
    # in_list will be replaced with a list of active todo items
    # out_list will be appended with completed todo items

    temp_list = []
    for line in in_list:
        if line[0] == 'x':
            out_list.append(line)
        else:
            temp_list.append(line)
    in_list[:] = temp_list  # Replace the contents of the passed list


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="todo.txt file path",
        metavar='in-file', type=argparse.FileType('rt+', encoding='utf-8'), required=True)
    parser.add_argument("-o", "--output", help="Archive file path",
    	metavar='in-file', type=argparse.FileType('rt+', encoding='utf-8'), required=True)
    args = parser.parse_args()

    in_file = args.input
    in_text = in_file.read()
    in_text = in_text.split('\n')
    in_text.remove('')  # split creates an empty record at the end list
    in_file.close()

    out_file = args.output
    out_text = out_file.read()
    out_text = out_text.split('\n')
    out_text.remove('')  # split creates an empty record at the end list
    out_file.close()

    todo_archive(in_text, out_text)

    for i in in_text:
        print(i)

    try:
        shutil.copy(args.input.name, args.input.name.replace("txt", "bak"))
    except:
        print("Error creating input backup\n")

    todo_f = open(args.input.name, 'w')
    for line in in_text:
        todo_f.write("%s\n" % line)
    todo_f.close()

    try:
        shutil.copy(args.output.name, args.output.name.replace("txt", "bak"))
    except:
        print("Error creating archive backup\n")

    arch_f = open(args.output.name, 'w')
    for line in out_text:
        arch_f.write("%s\n" % line)
    arch_f.close()
