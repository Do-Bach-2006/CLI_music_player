#this file is use to edit playlist in playlist folder follow by an input name
import os
import time

PLAYLIST_FOLDER = "playlist/"
RECENT_CREATE_PLAYLIST_PATH = ""


def print_message(message: str) -> None:
    """
        this function prints a message to the console and sleeps for 3 seconds
        arguments: message string , a string to be displayed
        return: None
    """
    print(message)
    time.sleep(3)



def create_new_playlist() -> bool:
    """
        this function creates a new playlist 
        arguments : none
        returns: true if successful
    """
    os.system("clear")

    all_playlists = get_all_playlist()
    name = input("playlist name: ")

    if name in all_playlists:
        confirmination = input("playlist already exists! overwrite it ? (type 'no' to discard)\n")

        if confirmination == "no":
            return False

    _ = open(PLAYLIST_FOLDER+name+".txt","w")

    global RECENT_CREATE_PLAYLIST_PATH
    RECENT_CREATE_PLAYLIST_PATH = PLAYLIST_FOLDER+name+".txt"
    
    try: 
        if edit_playlist(name):
            return True 
        
    except :# if something happen wrong or the program was interrupted
        os.remove(RECENT_CREATE_PLAYLIST_PATH)

    return False
    


def get_all_playlist() -> set:
    """
        this function use to get all the existing playlists in the playlist folder
        arguments:none
        return: list of playlists name
    """
    
    all_playlists = set()

    for playlist in set(os.listdir("playlist")):
        all_playlists.add(playlist.replace(".txt",""))

    return all_playlists




def edit_playlist(playlist_name: str) -> bool:
    """
        this function use to edit a play list a helper of edit_a_playlist_function !
        this function should not be called directlr
        arguments: playlist_name str name of the playlist to be edited
        returns: True if successful, False otherwise

    """
    all_songs = get_all_songs()
    old_songs = get_old_song(playlist_name)
        
    ADD = "1"
    REMOVE = "2"
    DONE = "3"
    ABORT = "4"


    while True:
        os.system("clear")
        print(old_songs)
        choice = input("1/add song  2 /remove song 3/done 4/abort\n ")
        
        
        if choice == ADD:
            insert_a_song(all_songs,old_songs)

        elif choice == REMOVE:
            remove_a_song(old_songs)

        elif choice == DONE:
            break

        elif choice == ABORT:
            os.remove(RECENT_CREATE_PLAYLIST_PATH)
            return False
        
        else:
            print_message("invalid choice")
    
    #write the song to file 
    if len(old_songs) == 0:

        print_message("can't create a new empty playlist! this will be aborted!")
        os.remove(RECENT_CREATE_PLAYLIST_PATH)
        return False
    
    insert_to_playlist_file(playlist_name,old_songs)

    return True




def get_all_songs() -> set:
    """
        this function returns a list of songs in the all_song_tmp.txt file
        arguments: none
        return: a list of songs in the all_song_tmp.txt file
    """
    #get the path to all song file and get all the available songs from it
    all_song_file = open("playlist/all-song.txt", "r")
    all_song_name = set()

    for name in set(all_song_file.readlines()):
        all_song_name.add(name.replace("\n" ,""))

    return all_song_name




def get_old_song(playlist_name : str) -> set:
    """
        this function returns a list of old songs that exist in the playlist/playlist_name.txt
        argument: the name of the playlist
        returns: a list of song names
    """
    #get the path to the playlist file and get all the old song in it
    playlist_file = open(PLAYLIST_FOLDER + playlist_name + ".txt","r")
    playlist_old_song = set()

    for song in set(playlist_file.readlines()):
        playlist_old_song.add(song.replace("\n",""))

    return playlist_old_song




def insert_a_song(all_song,song_in_playlist) -> None:
    """ 
        this function let user select a song to insert to the play list
        argument: all_song - set of all available songs
                    song_in_playlist - set of songs in the play list
        return : none
    """

    while True:
        os.system("clear")

    
        print("available songs:")
        print(all_song)
        print("songs in playlist:")
        print(song_in_playlist)
        choice = input("select a name to be added (:q to finish)")

        if choice == ":q":
            break

        if choice in all_song:

            song_in_playlist.add(choice)
            continue

        print_message("invalid song name")




def remove_a_song(song_in_playlist) -> None:
    """ 
        this function let user select a song to remove from the play list
        argument: song_in_playlist - set of songs in the play list
        return : none
    """
    while True:
        os.system("clear")


        print("song in play list:")
        print(song_in_playlist)
        choice = input("select a song name to remove from play list (:q to escape)")

        if choice == ":q":
            break;

        if choice in song_in_playlist:
            song_in_playlist.remove(choice)
            continue

        print_message("invalid song name")




def insert_to_playlist_file(playlist_name,edited_song_list) -> None:
    """
        this function is used to insert the edited song to the playlist
        overwrite the old song

        argument: playlist_name str , the name of the playlist
                edited_song_list set , the list of the new song

        return : none
    """

    playlist_file = open(PLAYLIST_FOLDER + playlist_name + ".txt","w")

    for name in edited_song_list:
        playlist_file.write(name+ "\n")





def edit_a_playlist() -> bool:
    """
        this function ask user to input a playlist name to be edited and call the edit_playlist function 
        arguments: none
        returns: true it successfully edits the playlist
    """
    all_playlist = get_all_playlist()
    while True:
        os.system("clear")


        print("playlist :")
        print(all_playlist)
        choice = input("please enter a playlist name to be edited (:q to done) \n")

        if choice == ":q":
            break

        if choice == "all-song":
            print_message("can't edit this playlist because it contains all the available songs")
            
            continue

        if choice in get_all_playlist():

            if edit_playlist(choice):
                print("edit playlist successfully")

            continue

        print_message("invalid playlist name")
        

    return True




def delete_playlist() -> bool:
    """
        this function delete a existing playlist
        argument: none
        return: true if successful false otherwise
    """
    deleted = False
    while True:
        os.system("clear")

        all_playlist = get_all_playlist()

        print("available playlists: ")
        print(all_playlist)
        choice = input("enter playlist name to delete(:q to quit)\n")

        if choice == ":q":
            break

        if choice == "all-song":

            print_message("can't delete this playlist because it contains all the available songs")
            continue

        if choice in all_playlist :

            print("are you sure you want to delete this playlist?")
            confirmation = input("you will permanently delete this play list!(type 'cancel' to cancel)")

            if confirmation == 'cancel':
                continue
            
            if os.path.exists(PLAYLIST_FOLDER + choice + ".txt"):
                os.remove(PLAYLIST_FOLDER + choice + ".txt")
            
            deleted = True
            continue

        print_message("invalid name")
        

    return deleted




def main():
    # select the choice 
    EDIT_PLAYLIST = "1"
    ADD_PLAYLIST = "2"
    DELETE_PLAYLIST = "3"

    while True:
        os.system("clear")
        print("choose option:")
        print("1/edit existing playlist 2/add new playlist 3/delete playlist 4/exit ")
        choice = input()

        if choice in ["1" , "2" , "3" , "4"]:
            break

        print_message("invalid choice")
        

    if choice == EDIT_PLAYLIST:
        if edit_a_playlist():
            print_message("edit successfully")
        else:
            print_message("edit failed")
    if choice == ADD_PLAYLIST:
        if create_new_playlist():
            print_message("create successfully")
        else:
            print_message("create failed")
    if choice == DELETE_PLAYLIST:
        if delete_playlist():
            print_message("delete successfully")
        else:
            print_message("delete failed")
    os.system("clear")


if __name__ == "__main__":
    main()



