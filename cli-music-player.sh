#!/bin/bash

# this is a simple script that allows users to create playlist ,playsongs 
# and edit the playlist themselves. the script using bash with a python script 
# to handle the complex creation and modification of the playlist 

# TO USE THIS SCRIPT . MAKE SURE YOU HAVE INSTALLED THE "mpg123" or "mplayer" 
# because this script will use these CLI music player to play songs

# all created by me !(dobach)
# i'm still a noob so the code might have some issues or bug . but it will be 
# fixed soon!



typeofvar () {

    local type_signature=$(declare -p "$1" 2>/dev/null)

    if [[ "$type_signature" =~ "declare --" ]]; then
        retun 1
    elif [[ "$type_signature" =~ "declare -a" ]]; then
        return 2
    elif [[ "$type_signature" =~ "declare -A" ]]; then
        return 3
    else
        return 4
    fi

}

#imma using python for creating and adding playlist 


MUSIC_PLAYER=()
#this function let the user choose the music player (CLI)
#there are 2 available type "mpg123" and "mplayer"
get_music_player()
{
    echo "please enter your music player name (remember to install it first)"
    local name=""
    select name in "mpg123" "mplayer"
    do 
        case $name in 
            mpg123)
                MUSIC_PLAYER=$name
                break
                ;;
            mplayer)
                MUSIC_PLAYER=$name
                break
                ;;
            *)
                echo "unknown music player"
                sleep 3
        esac
    done


}


#global variables
MUSIC_PATH=""

# this function get the music path from the user to read all the music files from it!
# if the user doesn't type anything , then using the default path 
# /home/user/Music
get_music_path()
{
    #get the path to the music file
    echo "please enter your music directory(if none , it will select default ~/Music): "
    read MUSIC_PATH

    #if path is empty then using the default path
    MUSIC_PATH=${MUSIC_PATH:-"/home/$USER/Music"}
}
#array to store all the song name
ALL_SONG_NAME=()

# this function will create a temporary text file
# the text file that store all the name of the song
create_all_song_tempt_file()
{
    #get all the song names (all the mp3 files in the MUSIC_PATH
    local all_song_name=$(ls $MUSIC_PATH)
    #create a temporary playlist file . this file is write only
    touch playlist/all-song.txt 

    for song in $all_song_name
    do 
        #trim the .mp3 file extension
        song=(${song//.mp3/})
        ALL_SONG_NAME+=($song)
        echo $song >> playlist/all-song.txt
    done
    
    chmod -w playlist/all-song.txt
}

ALL_PLAYLIST_NAME=()

#this function gets all the playlist name (excluding the .txt extension)
#and puts it in the ALL_PLAYLIST_NAME array
get_all_playlist_name()
{
    ALL_PLAYLIST_NAME=()
    local raw_playlist_names=$(ls -m "playlist" | tr ',' ' ')
    for name in $raw_playlist_names
    do
        ALL_PLAYLIST_NAME+=(${name//.txt/})
    done
    
}

#this function let the user to select the exist playlist 
open_a_playlist()
{
    get_all_playlist_name
    local choice=""
    while true
    do
        clear
        echo "select a playlist name (:q to exit)"
        echo "${ALL_PLAYLIST_NAME[@]}"
        read choice
        typeofvar $ALL_PLAYLIST_NAME

        if [[ "$choice" = ":q" ]]
        then 
            break
        fi

        for index in "${!ALL_PLAYLIST_NAME[@]}"
        do 
            if [[ "${ALL_PLAYLIST_NAME[$index]}" = "$choice" ]]
            then 
            
                choose_song_to_play "$choice"
                continue 2
            fi
        done

        echo "Invalid name"
        sleep 3
    done
}



#argument is a playlist name
#this function let the user choose which song to play
choose_song_to_play()  
{
    local all_song_name=()
    local all_song_name+=($(cat playlist/$1.txt))

    
    while true
    do 
        clear
        local choice=""
        echo "1/exit 2/random (or type a name to play)"
        echo  ${all_song_name[*]}
        read choice

        if [[ $choice = "1" ]]
        then 
            return 
        fi

        if [[ $choice = "2" ]]
        then 
            #play a random song here
            index=$(( $RANDOM % ${#all_song_name[@]} ))
            play_a_song ${all_song_name[$index]}

            continue
        fi

        for name in  ${all_song_name[*]}
        do 
            if [[ $choice = $name ]]
            then
                play_a_song $name
                #play some song here
                continue 2
            fi
        done

        
        echo "invalid song name"
        sleep 3
    done


}

#argument is a name of the song
#this function play a song using mpg123
play_a_song()
{

    is_song_exist $1

    if [[ $? -eq 1 ]]  #if song exists
    then
        clear
        echo "song not exist!!"
        echo "it seems like this playlist is create for another music path"
        echo "please select another song or try another playlist"
        sleep 3

        return 1
    fi


    while true
    do 
        clear
        
        echo "now playing $MUSIC_PATH/$1.mp3"
        echo "type 'replay' to play from start or type anything to stop playing"
        
        #play the music using third-party libraries without  messages
        $MUSIC_PLAYER "$MUSIC_PATH/$1.mp3" > /dev/null 2>&1 &

        local choice=""
        read choice

        if [[ "$choice" = "replay" ]]
        then
            killall $MUSIC_PLAYER
            continue
        fi 

        break
    
    done

    killall $MUSIC_PLAYER
}

#argument song name to check
is_song_exist()
{
    for name in ${ALL_SONG_NAME[*]}
    do 
        if [[ $1 = $name ]]
        then
            return 0  #true
        fi
    done

    return 1  #false
}

main()
{
    get_music_path
    create_all_song_tempt_file
    get_music_player

    while true
    do 
        clear
        echo "1/exit  2/edit playlist 3/play a playlist"
        local choice=""
        read choice
            
            case $choice in 
                1)
                    break
                    ;;
                2)
                    python3 /home/gnomeright/programming/vs-project/cli-music-player/playlist_operation.py
                    ;;
                3)
                    open_a_playlist
                    ;;
                *)
                    echo  "invalid choice"
                    sleep 3
            esac

    done

    #remove the temporary files
    rm -f playlist/all-song.txt 

}



{ # try
    #save your output

    main

} || { # catch
    #remove the temporary file
    rm -f playlist/all-song.txt 
}








