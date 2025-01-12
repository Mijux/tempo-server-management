#!/usr/bin/env python3

from db.dao.user import add_user, get_user, remove_user, update_user, leave_user
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
        if get_user(id) is None: 
            add_user(user)
        else:
            update_user(user)           
        try:
            UserPresenceStatusDao.add_user_presence(id, username, date)
        except:
            raise
        return True
    
    @staticmethod
    def is_admin_user(id: str):
        user = get_user(id)
        if user is not None: 
            role = RoleE.from_number(user.permission_level)
            return role == RoleE.ADMIN
        else: 
            return False
       
    @staticmethod
    def retire_user(user_id: str):
        remove_user(user_id)
    
    @staticmethod
    def leave_user(user_id: str):
        return leave_user(user_id)