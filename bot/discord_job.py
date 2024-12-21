#!/usr/bin/env python3
import utils.db.user as UserOrm

class DiscordJob:
    
    def add_user(self,id: str, username: str, avatar: str):
        if UserOrm.get_user(id) is None: 
            user = {
                "id": id,
                "username": username,
                "avatar": avatar.url
            }
            UserOrm.add_user(user)
        print(UserOrm.get_user(id))