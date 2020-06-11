#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# main.py
# Copyright (C) 2020 Benrick Smit <metatronicprogramming@hotmail.com>
# 
# Musicly is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Musicly is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

# This function will not contain any classes, instead will use primarily function to achieve its goal
# therefore it requires no classes.

# The program works in the following methdo:
#   -   The program starts                                                  [Done]  
#   -   The program obtains a directory to scan                             [Done]
#   -   The program uses this directory to make sure it's a directory       [Done]
#           if its not a directory, it uses the directory                   
#   -   The program obtains a list of files in the directory                [Done]
#   -   The program determines which of these are music files               [Done]
#   -   The program then cycles through the music files and obtains a       [Done]
#           list of artist names                                            
#   -   The program moves all the music files in to the directory that      [Done]
#           suit its artist name                                            
#   -   Once inside the respective artist directory, the program creates    [Done]
#           folders for albums into which the files are next organised      
#   -   The program then moves the files into the correct album.            [Done]
#   -   The Program exits                                                   [Done]

import sys 
import os 

from tkinter import filedialog
from tkinter import *
import eyed3

# This function ensures the program exits
def exit_program():
    # Stops the program from continuing execution
    print("Closing Program.")
    sys.exit()
    return None


# This function contains the main loop of the program
def main(string_path):
    print("Starting Program: Music Classification")
    
    print("Obtaining Path...")
    # Obtain the path to the file you wish to categorize
    string_path_to_use = string_path
    
    # Obtain the directory to use
    string_path_to_use = is_directory(string_path_to_use)

    # obtain a list of mp3 files in the directory
    print("Obtaining Music Files...")
    list_files = get_files(string_path_to_use)

    # Determine whether to proceed or not
    if list_files == []:
        print("\tNo Music Files Found.")
        exit_program()
    else:
        print("\tMusic Files Found: ", len(list_files))
    
    # Obtain a list of artist names
    print("Obtaining Artists...")
    list_artists = get_artists(list_files)

    # Determine whether to proceed or not
    if list_artists == []:
        print("\tNo Artists Found.")
        exit_program()
    else:
        print("\tArtists Found: ", len(list_artists))
    
    # Create the folders as specified by the names
    print("Creating Artist Folders...")
    string_where_create_path = string_path_to_use
    list_paths = create_artist_dirs(string_where_create_path, list_folders=list_artists)
    
    # Determine whether to proceed or not
    if list_paths == []:
        print("\tFiles Not Created.")
        exit_program()

    # Create the Albums required for the paths
    print("Creating Album Folders...")
    list_albums = create_album_dirs(list_files)
    
    # Determine whether to continue or not
    if list_albums == []:
        print("\tNo Albums Found; Files Not Created.")
        exit_program()
    else:
        print("\tAlbums Found: ", len(list_albums))

    # Move the files into the respective paths
    print("Organising Tree...")
    move_files(list_files)

    # Stop execution
    exit_program()

    return None


# This function determines whether the path given is a directory, if not
# it only uses the directory
def is_directory(string_path):
    string_to_return = os.path.abspath(string_path)

    if not os.path.isdir(string_to_return):
        string_to_return = os.path.abspath(os.path.dirname(string_to_return))

    return string_to_return


# This function will obtain and return a list of all files that are music files
# in this case .mp3
def get_files(string_path):
    list_to_return = []

    # obtain a list of files in the directory
    for file_data in os.listdir(string_path):
        if file_data.endswith(".mp3"):
            file_path = string_path+"/"+file_data
            file_path = os.path.abspath(file_path)
            list_to_return.append(file_path)

    list_to_return = list(set(list_to_return))

    return list_to_return


# This function will obtain the artist names from the files used the eyed3 package
# and add these names to the list
def get_artists(list_paths):
    # NOTE: This function expects the list to contain paths
    list_to_return = []

    # cycle through all the elements in the list
    for path in list_paths:
        if os.path.isfile(path):
            # Only continue if the file exists
            file_audiofile = eyed3.load(str(path))
            # Add the artist to the list
            string_artist = str(file_audiofile.tag.artist)
            if string_artist.lower() == "None".lower():
                string_artist = "Unknown Artist"

            list_to_return.append(string_artist)

    list_to_return = list(set(list_to_return))

    return list_to_return


# This function will create the required Artist folders in the base folder
def create_artist_dirs(string_base_path, list_folders):
    # This function assumes the path specified exists
    list_to_return = []

    # Create the folders
    string_path = string_base_path + "/Unknown Artists"
    for folder_name in list_folders:
        # Create the path
        string_abs_path = string_base_path + "/" + folder_name
        string_abs_path = os.path.abspath(string_abs_path)
        
        list_to_return.append(string_abs_path)
        list_to_return.append(string_path)

    # Ensure Unique Entries
    list_to_return = list(set(list_to_return))

    # Create the directories
    for path in list_to_return:
        try:
            # Create the directory
            os.makedirs(path)
        except:
            continue

    return list_to_return


# This function will create the albums for the artists based on the provided 
# files, and the artist folders created
def create_album_dirs(list_music_files):
    # In essence this function will use the files for the music and
    # create the required album in artist directory, if "None" found, it will
    # use the "unknown album" folder
    
    # PS: "None" is what eyed3 uses to indicate no values 

    list_to_return = []

    # Cycle through the music files and obtain the album paths
    # to create
    list_album_paths = []
    for music_file in list_music_files:
        # Obtain the base directory
        string_dir_path = os.path.dirname(music_file)

        file_audiofile = eyed3.load(str(music_file))
        # Obtain the artist name
        string_artist = str(file_audiofile.tag.artist)

        # Obtain the album
        string_album = str(file_audiofile.tag.album)

        if string_album.lower() == "None".lower():
            string_album = "Unknown Album"

        # Create the new path to create
        string_album_path = string_dir_path + "/" + string_artist
        string_album_path = string_album_path + "/" + string_album

        list_album_paths.append(string_album_path)

    # Ensure only single entries
    list_to_return = list(set(list_album_paths))

    # Create the directories
    for path in list_to_return:
        try:
            # Create the directory
            os.makedirs(path)
        except:
            continue

    return list_to_return


# This function will employ the help of os.rename to move the files into the required
# already created directories
def move_files(list_paths):

    for music_file in list_paths:
        # Obtain the current path
        string_source = music_file

        # Create the destination path;
        file_audiofile = eyed3.load(str(string_source))
        string_artist = str(file_audiofile.tag.artist)
        if string_artist.lower() == "None".lower():
            string_artist = "Unknown Artist"
        string_album = str(file_audiofile.tag.album)
        if string_album.lower() == "None".lower():
            string_album = "Unknown Album"
        string_file = os.path.abspath(music_file)
        string_file = os.path.basename(string_file)
        string_dir = os.path.abspath(music_file)
        string_dir = os.path.dirname(string_dir)

        string_destination = string_dir + "/" + string_artist
        string_destination = string_destination + "/" + string_album
        string_destination = string_destination + "/" + string_file 

        # Move the file
        os.rename(string_source, string_destination)

    return None



# Contains the path to the music to categorise
root = Tk()
root.withdraw()
string_path_to_music = filedialog.askdirectory()

main(string_path_to_music)