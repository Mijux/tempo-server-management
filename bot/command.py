#!/usr/bin/env python3
import db.dao.user as UserOrm
from db.dao.user_presence_status import UserPresenceStatusDao
from utils.enums.role import RoleE

class CommandHandler:
      
    @staticmethod
    def add_user(id: str, username: str, avatar: str, date: str):
        user = {
                "id": id,
                "username": username,
                "avatar": avatar.url if avatar != None else None
            }
        if UserOrm.get_user(id) is None: 
            UserOrm.add_user(user)
        else:
            UserOrm.update_user(user)           
        try:
            UserPresenceStatusDao.add_user_presence(id, username, date)
        except:
            raise
        return True
    
    @staticmethod
    def is_admin_user(id: str):
        user = UserOrm.get_user(id)
        if user is not None: 
            role = RoleE.from_number(user.permission_level)
            return role == RoleE.ADMIN
        else: 
            return False
       
    @staticmethod
    def retire_user(id: str):
        UserOrm.remove_user(id)