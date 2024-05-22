#!/usr/bin/env python3

"""
The plan:
	list stuff
		friend_cli list
			list all friends
		friend_cli list lists
			list all the lists of friends
		friend_cli list list_name
			list all the friends in the list

	search stuff
		friend_cli search friend_name
			find all friends where "friend_name in friend.name"
		friend_cli fzf friend_name
			fuzzy find friend_name

	add data
		friends_cli add friend_name date
			add the date to that friend's description
		friends_cli add friend_name
			add today    to that friend's description
		friends_cli add friend_name -2
			add today -2 to that friend's description

	edit data
		friends_cli edit friend_name
			open nano, with its comtent as that card's description

	delete data
		friends_cli remove friend_name date
			delete that date from that friend's description


"""
