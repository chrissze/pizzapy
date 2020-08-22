#!/usr/bin/python3

import os
import sys


def start() :
    print("Please choose the action:")
    print("1) System Update")
    print("2) Install Utilities")
    print("3) Create File")
    print("4) Exit the program")
    ans = input("Enter a number: ")
    print(ans)
    if ans=='1':
         system_update()
    elif ans=='4':
        exit()
    else:
        print('invalid input')
        start()


def system_update():
    print('Which sys action do you want to do')
    print('1) # yum update')
    print('2) go to home screen')
    ans = input("Enter your ans:\n ")
    if ans=='1':
        confirm = input('Run # yum update (y/n)?')
        if confirm=='y':
            os.system('yum update')
        else:
            system_update()
    elif ans=='2':
        start()


if __name__=='__main__':
    start()


