"""
Data structures:
----------------

music := list of "genomes", each of which is a list of integers in [0,1]
music is therefore a list of lists of integers

likes := list of song_id integers corresponding to songs (genomes) in music
dislikes := same as above
"""

def next_song(likes, dislikes, music):
    # play the next unplayed song with the highest "goodness"
    played = likes + dislikes

    # undefined behavior when all songs have played. Here, we return 0.
    best_song_id, best_goodness = 0, -999999999999 # a very "bad" goodness

    # consider all songs in music
    for song_id in range(len(music)):
        # disregard songs that have played already
        if song_id in played:
            continue

        # what is the goodness of the song we're considering?
        g = goodness(likes, dislikes, song_id, music)

        # if song is better than best_so_far, update best_so_far
        if g > best_goodness:
            best_song_id = song_id
            best_goodness = g

    # at this point, considered all unplayed song, and must've seen the best
    return best_song_id

def goodness(likes, dislikes, song_id, music):
    # "goodness" function, as defined in the lab assignment
    # favor songs far away from disliked songs, but close to liked songs
    return average_distance(dislikes, song_id, music) - average_distance(likes, song_id, music)

def average_distance(song_id_list, song_id, music):
    # average distance is the sum of distances
    # divided by the number of distances considered
    d = 0
    for other_song_id in song_id_list:
        d += distance(music[song_id], music[other_song_id])
    return d/max(1, len(song_id_list)) # compute average; distance to empty playlist is 0

def distance(song_1, song_2):
    # Distance is defined to be the "manhattan distance" of genomes:
    #   the number of genes differing between songs
    d = 0
    for gene in range(len(song_1)): # assume songs have equal numbers of genes
        d += abs(song_1[gene]-song_2[gene])
    return d
