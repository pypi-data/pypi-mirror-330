from common.api.funding_envs_images import *

# Class and singleton builds a list of tuples from the DB results
class FundingSources: 
    is_init: bool = False
    my_fs: dict

    def __init__(self, fs_arg: dict):
        if self.is_init:
            raise ValueError('FundingSources.load() already initialized')
        else:
            self.init = True
            self.my_fs= fs_arg

    @staticmethod
    def load():
        fs = list_funding_sources()
        if len(fs) == 0:
            return None
        # Loop through and add a custom "menu" item to each dict 
        for key, val in fs.items(): 
                val[FS_MENU] = f'{val[FS_NAME]} ({val[FS_TOKENS]} tokens available)'
        return FundingSources(fs)
        
    # Prompt toolkit needs a list of strings to display in the menu 
    def menu_items(self) -> list: 
        ret_list: list = []
        for _, val in self.my_fs.items():
            # just show names
            ret_list.append(val[FS_MENU])
        return ret_list
    
    def auto_complete_items(self) -> list: 
        ret_list: list = []
        for _, val in self.my_fs.items():
            # just show names
            ret_list.append((val[FS_ID],val[FS_MENU]))
        return ret_list

    # Return 'funding_group_id' using the val returned from session.prompt() 
    def id_from_menu_item(self, menu_item: str) -> str:
        for _, val in self.my_fs.items():
            if (val[FS_MENU] == menu_item):
                return val.get(FS_ID)
        return None

    def default_env_id_from_menu_item(self, menu_item: str) -> str:
        for _, val in self.my_fs.items():
            if (val[FS_MENU] == menu_item):
                return val.get(FS_DEF_ENV_ID)
        return None
    
    def default_env_name_from_menu_item(self, menu_item: str) -> str:
        for _, val in self.my_fs.items():
            if (val[FS_MENU] == menu_item):
                return val.get(FS_DEF_ENV_NAME)
        return None
    
    def default_env_name_from_fs_id(self, id: str) -> str:
        for _, val in self.my_fs.items():
                if (val[FS_ID] == id):
                    return val.get(FS_DEF_ENV_NAME)
        return None
    
    def default_env_id_from_fs_id(self, id: str) -> str:
        for _, val in self.my_fs.items():
                if (val[FS_ID] == id):
                    return val.get(FS_DEF_ENV_ID)
        return None
    
    def default_env_id(self) -> str:
        for _, val in self.my_fs.items():
            if (val[FS_TYPE] == FS_PERSONAL_TYPE):
                return val.get(FS_DEF_ENV_ID)
        return None
    
    def default_funding_source_id(self) -> str: 
        for _, val in self.my_fs.items():
            if (val[FS_TYPE] == FS_PERSONAL_TYPE):
                return val.get(FS_ID)
        return None
    
    def default_image_name(self, id: str) -> str:
        for _, val in self.my_fs.items():
            if (val[FS_ID] == id):
                return val.get(FS_DEFAULT_IMAGE_NAME)
        return None
    
    def default_image_id(self, id: str) -> str:
        for _, val in self.my_fs.items():
            if (val[FS_ID] == id):
                return val.get(FS_DEFAULT_IMAGE_ID)
        return None


# singleton for Environments
class Environments: 
    is_init: bool = False
    my_envs: dict

    def __init__(self, env_arg):
         if self.is_init:
            raise ValueError('Environments.load() already initialized')
         else:
            self.my_envs = env_arg
            self.is_init = True

    @staticmethod
    def load(fs_id: str):
        return_dict = {}
        envs = list_environments(fs_id)
        if len(envs) == 0:
            return None
        for key, val in envs.items():
            if not val.get(ENV_DELETED):
                return_dict[key] = val
                val[ENV_MENU_ITEM] = f"{val['environmentName']} ({val['tokensPerHour']} Tokens/Hour)" # shows in menu

        return Environments(return_dict)

    def menu_items(self) -> list: 
        menu_list = []
        for _, val in self.my_envs.items():
            menu_list.append(val[ENV_MENU_ITEM])
        return menu_list
    
    def auto_complete_items(self) -> list: 
        ret_list: list = []
        for _, val in self.my_envs.items():
            ret_list.append((val[ENV_ID],val[ENV_MENU_ITEM]))
        return ret_list

    def id_from_menu_item(self, menu_item: str) -> str:
        for _, val in self.my_envs.items():
            if (val[ENV_MENU_ITEM] == menu_item):
                return val.get(ENV_ID)
        return None

    def tokens_per_hour(self, env_id: str) -> str:
        for _, val in self.my_envs.items():
            if (val[ENV_ID] == env_id):
                return val.get(ENV_TPH)
        return None
    
    def cluster_type_from_env_id(self, env_id: str) -> str:
        for _, val in self.my_envs.items():
            if (val[ENV_ID] == env_id):
                return val.get(ENV_CLUSTER_TYPE)
        return None
        


# singleton for Environments
class Images: 
    is_init: bool = False
    my_images: dict

    def __init__(self, image_arg):
         if self.is_init:
            raise ValueError('Images.load() already initialized')
         else:
            self.my_images = image_arg
            self.is_init = True

    @staticmethod
    def load(fs_id: str, env_id: str):
        images = list_images(fs_id, env_id)
        if len(images) == 0:
            return None
        for _, val in images.items():
            val[IMAGE_MENU_ITEM] = f"{val[IMAGE_NAME]}" # shows in menu
        return Images(images)

    def menu_items(self) -> list: 
        menu_list = []
        for _, val in self.my_images.items():
            if val.get(IMAGE_DELETED) == False:
                menu_list.append(val[IMAGE_MENU_ITEM])
        return menu_list
    
    def auto_complete_items(self) -> list:
        menu_list = []
        for _, val in self.my_images.items():
            if val.get(IMAGE_DELETED) == False:
                menu_list.append(val[IMAGE_MENU_ITEM])
        return menu_list
        

    def name_from_menu_item(self, menu_item: str) -> str:
        for _, val in self.my_images.items():
            if (val[IMAGE_MENU_ITEM] == menu_item):
                return val.get(IMAGE_NAME)
        return None
    