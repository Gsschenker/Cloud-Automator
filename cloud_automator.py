#!/usr/bin/env python3.10

#author - @libertyunix

#Import our modules
from shutil import which
import sys
import os
import subprocess
import time
# import keyboard

#Create a banner
banner = """

 _______  _        _______           ______     _______          _________ _______  _______  _______ _________ _______  _______ 
(  ____ \( \      (  ___  )|\     /|(  __  \   (  ___  )|\     /|\__   __/(  ___  )(       )(  ___  )\__   __/(  ___  )(  ____ )
| (    \/| (      | (   ) || )   ( || (  \  )  | (   ) || )   ( |   ) (   | (   ) || () () || (   ) |   ) (   | (   ) || (    )|
| |      | |      | |   | || |   | || |   ) |  | (___) || |   | |   | |   | |   | || || || || (___) |   | |   | |   | || (____)|
| |      | |      | |   | || |   | || |   | |  |  ___  || |   | |   | |   | |   | || |(_)| ||  ___  |   | |   | |   | ||     __)
| |      | |      | |   | || |   | || |   ) |  | (   ) || |   | |   | |   | |   | || |   | || (   ) |   | |   | |   | || (\ (   
| (____/\| (____/\| (___) || (___) || (__/  )  | )   ( || (___) |   | |   | (___) || )   ( || )   ( |   | |   | (___) || ) \ \__
(_______/(_______/(_______)(_______)(______/   |/     \|(_______)   )_(   (_______)|/     \||/     \|   )_(   (_______)|/   \__/

================== A Tool for Automating the Boring Stuff in the Cloud ===============
                          Please Select An Option Below
======================================================================================
[1] Check for necessary prerequisites and install if needed
[2] Configure AWS and give correct user access (necessary for steps 5-10)
[3] Locally build an image of Ubuntu through Vagrant, and SSH into VM
[4] Destroy image of Ubuntu
[5] Create an S3 bucket
[6] Destroy an S3 bucket
[7] Upload file in current directory to S3 bucket
[8] Delete any file from an S3 bucket
[9] Create ECR
[10] Delete ECR
[99] Exit process
======================================================================================
"""

loop=True
while loop:
    print(banner)
    x = input ("Select An Option: ")
    if x == '1':
        if which('choco') is None: 
            print ("Downloading Choco.") 
            os.system("Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))") 
        if which('vagrant') is None :
            print ("Downloading Vagrant.")
            os.system('choco install vagrant')
        if which('awscli') is None :
            print ("Downloading AWSCLI.")
            os.system('choco install awscli')
        if which('virtualbox') is None :
            print ("Downloading VirtualBox")
            os.system('choco install virtualbox')
    elif x == '2':
        print("Configure AWS.")
        os.system('aws configure')
    elif x == '3':
        print ("Creating image of Ubuntu through Vagrant.")
        os.system('vagrant init bento/ubuntu-22.04')

        print ("Booting image of Ubuntu.")
        os.system('vagrant up')

        print ("SSH into Ubuntu VM.")
        os.system('vagrant ssh')

        print ("Type 'exit' to return back to CloudAutomator.")
    elif x == '4':
        print ("Suspending VM.")
        os.system('vagrant suspend')

        print ("Destroying VM.")
        os.system('vagrant destroy')
    elif x == '5':
        print ("Creating an S3 bucket.")
        bucketName1 = input ("Name of the S3 bucket: ")
        os.system("aws s3api create-bucket --bucket "  + bucketName1 + " --region us-east-1")
        print ("Make sure to delete your Buckets!")
    elif x == '6':
        print ("Destroying an S3 bucket.")
        bucketName2 = input ("Name of the S3 bucket you'd like to destroy: ")
        os.system("aws s3api delete-bucket --bucket "  + bucketName2 + " --region us-east-1")
        print ("S3 bucket destroyed.")
    elif x == '7':
        print ("Uploading file to specific bucket.")
        bucketName3 = input ("Specific S3 Bucket to send to: ")
        fileName = input ("File name to upload to bucket: ")
        os.system("aws s3 cp " + fileName + " s3://" +bucketName3)

        print ("File uploaded to the cloud.")

        print ("Current objects in given S3 bucket: ")
        os.system("aws s3 ls s3://" +bucketName3)
    elif x == '8':
        print ("Deleting file from a bucket.")
        bucketName4 = input ("What bucket do you want to delete from: ")
        print ("Current objects in given S3 bucket: ")
        os.system("aws s3 ls s3://" +bucketName4)

        objectName = input ("What object do you want to delete from the bucket: ")
        os.system("aws s3api delete-object --bucket " + bucketName4 + " --key " + objectName)
        print ("Object deleted.")
    elif x == '9':
        print ("Creating ECR.")
        ecrName = input ("What is the name of this ECR: ")
        os.system("aws ecr create-repository --repository-name " + ecrName)
        print ("Repository created.")
    elif x == '10':
        print ("Deleting ECR.")
        ecrName = input ("What is the name of this ECR: ")
        os.system("aws ecr delete-repository --repository-name " + ecrName)
        print ("Repository deleted.")
    elif x == '99':
        print ("Exiting process")
        quit()
