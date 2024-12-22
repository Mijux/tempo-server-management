#!/usr/bin/env python3
import db.dao.user as UserOrm

@staticmethod
class CommandHandler:
      
    def add_user(self,id: str, username: str, avatar: str):
        if UserOrm.get_user(id) is None: 
            user = {
                "id": id,
                "username": username,
                "avatar": avatar.url
            }
            UserOrm.add_user(user)
        print(UserOrm.get_user(id))