pref_file = "musicrecplus.txt"

def main():
    '''This is the starting point of the application where we first open up a file and check whether the entered user 
    name exists in the file. If the user name does not exist then he/she needs to mention the name of their favorite
    artists and if the user name do exists in the file then he/she is provided with a menu comprising of different functions'''

    user_data = loadUsers(pref_file)
    user_name = input('Enter your name ( put a $ symbol after your name if you wish your preferences to remain private ): ')

    if user_name not in user_data:
        
        enter_preferences(user_name, user_data, pref_file)
    else:
        menu(user_name, user_data)

def loadUsers(filename):
    '''This function reads the specified file name and returns back a dictionary comprising of all the users and a list 
    of their favorite artists'''

    userInfo = {}
    try:
        file = open(filename, 'r')

        for line in file:
            [username, artists] = line.strip().split(':')
            artists = artists.split(',')
            artists.sort()
            
            unique_artists_list = []

            for x in artists:

                if x not in unique_artists_list:
                    unique_artists_list.append(x)

            artists_list = [x.title() for x in unique_artists_list]
            userInfo[username] = artists_list
        file.close()
        return userInfo
    except:
        return userInfo

def menu(user_name, user_data):
    '''This function displays a menu of options comprising of the functions that the user can perform. The list of options
    is displayed after every function has been carried out unless the user opts to save and quit.'''

    while True:
        print('Enter a letter to choose an option:' + '\n' +
            'e - Enter preferences' + '\n' + 
            'r - Get recommendations' + '\n' +
            'p - Show most popular artists' + '\n' +
            'h - How popular is the most popular' +'\n' +
            'm - Which user has the most likes' + '\n' + 
            'd - Delete Preferences' + '\n' +
            's - Show Preferences' + '\n' +
            'q - Save and quit')
        
        choice = input()
        
        if choice == 'p':
            mostpopular(pref_file)
        elif choice == 'h':
            howpopular(pref_file)
        elif choice == 'd':
            delete_preferences(user_name, user_data)
        elif choice == 'm':
            UserLikeMost(user_data)
        elif choice == 's':
            show_preferences(user_name, user_data)
        elif choice == 'e':
            enter_preferences(user_name, user_data, pref_file)
        elif choice == 'r':
            recs = get_recs(user_name, user_data)
            print_recs(recs)
        elif choice == 'q':
            try:
                update_db(user_name, user_data, pref_file, user_data[user_name])
                break
            except:
                break

def mostpopular(userInfo):
    """Returns the most popular artist , will return upto 3 artists if there is a tie in votes.

    Input: Filename
    Output: Artist names each on a new line."""

    
    userInfo = loadUsers(pref_file)
    updated_userInfo = exclude(userInfo)
    list1 = listall(updated_userInfo)
    counter1 = counter(list1)
    three = counter1[0:3]
    final = []
    if three == []:
        print("Sorry, no artists found.")
    elif three[0][0] == '':
        print("Sorry, no artists found.")
    else:
        ymax = three[0][1]
        for x, y in three:
            if y > ymax:
                ymax = y
            elif y == ymax:
                final.append(x)
    
    
    for z in sorted(final):
        print(z)

def listall(dic):
    """Takes a dictionary and makes a list using all present values. Keys are not included.

       Input: Dictionary
       Output: List containing all values from dictionary."""
    
    combined_list = list(dic.values())
    remove_nested = [x for l in combined_list for x in l]
    return remove_nested

def counter(lst):
    """Returns a nested list which shows occurrences in a list.
       Output list is also sorted in descending order.

       Input: List.
       Output: Nested list where first element is artist name and second element shows number of occurences."""
    
    dic = {}

    for x in lst:
        if x not in dic:
            dic[x] = 1
        else:
            dic[x] +=1
    return sorted(dic.items(), key=lambda x: x[1],reverse = True)

def howpopular(pref_file):
    """Returns how popular the most popular artist is. Since list is already sorted in descending order, first occurrence value will be the required number.
    Input: filename.
    Output: Number of times the most popular artist shows up."""

    
    userInfo = loadUsers(pref_file)
    updated_userInfo = exclude(userInfo)
    list1 = listall(updated_userInfo)
    counter1 = counter(list1)
    if counter1 == []:
        print("Sorry, no artists found.")
    elif counter1[0][0] == '':
        print("Sorry, no artists found.")
    else:
        print(counter1[0][1])

def UserLikeMost(userMap):
    '''Which User Likes The Most Artists:

        Input: Dictionary name
        Output: List with users likes most '''


    userlist = userMap.keys()
    if userlist == [] :
        print("Sorry, no user found.")
    listuser = []
    for users in userlist :
        if users[-1] == "$" :
            pass
        else :
            listuser = [(users, userMap[users])] + listuser
            listuser.sort()
    #print(listuser)
    list2=listuser
    length=1
    user=[]
    for index in list2:
        if len(index[1]) >  length  :
            length = len(index[1])
            user = [index[0]]
        elif len(index[1]) == length :
            user += [index[0]]
    for x in user:
       print (x)

def delete_preferences(user_name, user_data):
    '''This function is used to delete an artists name. First a user is displayed the list of artists that he had 
    earlier mentioned as preferences. Then the user needs to write down the name of the artist that he/she wishes to remove
    from the list. After deleting we make the necessary changes to the database.'''

    list_of_artists = show_preferences(user_name, user_data)

    delete_artist = input("Enter the artist you wish to delete: ")

    if delete_artist in list_of_artists:
        
        list_of_artists.remove(delete_artist)
        
    update_db(user_name, user_data, pref_file, list_of_artists)

def show_preferences(user_name, user_data):
    '''This function displays the name of the artists preferred by a particular user '''

    file = open(pref_file, 'r')

    result = []
    stored_username = []

    for line in file:
        [username, artists] = line.strip().split(':')
        artists = artists.split(',')
        artists.sort()
        stored_username.append(username)

    for i in (stored_username):
        if user_name == i:
            result = result + user_data[i]
            break

    print(result)
    return result

def exclude_helper(dic):
    """Used as a helper function for exclude
       Makes a list of indices of keys which end with $
       
       Input: Dictionary name
       Output: List with indices """
    
    keys = list(dic.keys())
    k = []
    for i in range(len(keys)):
        if keys[i][-1] == "$":
            k.append(i)
            i += 1
    return k

def exclude(dic):
    """Removes keys which end with $ using indices from helper function

       Input: Dictionary
       Output: Updated dictionary which now excludes private users."""
    
    i = 0
    index = exclude_helper(dic)
    delete = []
    for key in dic.keys():
        if i in index:
            delete.append(key)
        i += 1
    for key in delete:
        if key in dic:
            del dic[key]
    return dic

def enter_preferences(user_name, user_data, pref_file):
    '''Through this function a user is asked to enter the artists name. If the user name exists in the file name then 
    the entered artists name is appended to the preferences list if it wasn't existing earlier in the list'''
    
    preferences = []

    if user_name not in user_data:

        new_pref = input("Enter an artist that you like (Enter to finish):")
        while new_pref != '':
            
            if new_pref not in preferences:
                preferences.append(new_pref)

            new_pref = input("Enter an artist that you like (Enter to finish):")
            
    else:
        preferences = user_data[user_name]

        new_pref = input("Enter an artist that you like ( Enter to finish ):")
        while new_pref != '':
            if new_pref not in preferences:
                preferences.append(new_pref)

            new_pref = input("Enter an artist that you like (Enter to finish):")    
    
    preferences.sort()

    artists_list = [x.title() for x in preferences]
    artists_list.sort()
    
    update_db(user_name, user_data, pref_file, artists_list)
    menu(user_name, user_data)

def update_db(user_name, user_data, pref_file, preferences):
    '''This function is used to keep the database updated. It stores the most recent changes made by the user to their
    preferences list.'''

    user_data[user_name] = preferences

    file = open(pref_file, 'w')

    for user in sorted(user_data.keys()):
        toSave = str(user) + ':' + ','.join(user_data[user]) + '\n'        
        file.write(toSave)
    file.close()

def print_recs(recs):
    '''This function is used to print the name of the recommended artists'''
    if len(recs) == 0 or recs==[]:
        
        print("No recommendations available at this time.")
    else:
        print('\n'.join(recs))

def numMatches(list1, list2):
    '''This function returns the number of matches that the given two lists has between them.'''
    matches = 0
    i = 0
    j = 0

    while i<len(list1) and j<len(list2):

        if list1[i] == list2[j]:
            matches += 1
            i += 1
            j += 1
        elif list1[i]<list2[j]:
            i += 1
        else:
            j += 1
    return matches

def get_recs(user_name, user_data):
    '''Through this function the user gets a recommendation of artists. The artist's list of the user that has logged in
    is compared with list of artists of all the other users.'''
    list_of_users = user_data.keys()
    
    if(len(list_of_users) == 1):
        return []
      
    matched_user = None
    max_match = 0

    for user in list_of_users:

        if user[-1] == "$":
            continue
        elif user_data[user] == []:
            continue
        elif user_data[user] != user_data[user_name]:
            given_user = user_data[user_name]
            to_compare_user = user_data[user]
            num_matches = numMatches(given_user, to_compare_user)

            if num_matches>max_match:
                max_match = num_matches
                matched_user = user
            elif num_matches == max_match:
                continue

    artist_list = []
    artist_list = artist_list + dropMatches(user_data[user_name], user_data[matched_user])

    unique_artist_list = []

    for x in artist_list:
        if x not in unique_artist_list:
            unique_artist_list.append(x)

    return unique_artist_list

def dropMatches(list1, list2):
    '''This function is used to drop the names of artists that exists in both the given lists. It returns back a list 
    of artists which are not present in the first list'''

    list1.sort()
    list2.sort()

    req_list = []
    i = 0
    j = 0

    while i<len(list1) and j<len(list2):

        if list1[i] == list2[j]:
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            req_list.append(list2[j])
            j += 1

    while j<len(list2):
        req_list.append(list2[j])
        j += 1

    return req_list
main()