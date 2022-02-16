import base64
import datetime
import os
import uuid

from blog.config.config import Settings
from blog.model.db import Database

settings = Settings()

IMG_BASE_DIR = settings.img_dir
MAIN_DIR = settings.main_dir
DB_USER = settings.db_user
DB_PWD = settings.db_pwd
DB_HOST = settings.db_server
DB_PORT = settings.db_port
POST_TABLE_NAME = settings.post_name
POST_PRIM_KEY = settings.post_prim_key
METADATA_TABLE_NAME = settings.metadata_name
METADATA_PRIM_KEY = settings.metadata_prim_key

IMG_DIR_PATH = os.path.join(settings.main_dir, settings.img_dir)


class PostService:

    def __init__(self):
        pass

    def get(self):
        pass

    def create(self, post):
        
        try:
            self.post = post
            self.extract_obj_attr()
            self.handle_images()
            self.insert_post()
            self.insert_metadata()
            return True, f"Successfully inserted post with title {self.post.title}"
            # return self.post_attr_dict.update(self.metadata_attr_dict)
        
        except Exception as e:
            return False, e
    
    def extract_obj_attr(self):

        self.post_attr_dict = {}
        self.post_attr_dict['title'] = self.post.title
        self.post_attr_dict['published_at'] = self.det_publish_time()
        self.post_attr_dict['content'] = self.post.content
        self.post_attr_dict['links'] = self.post.links
        self.post_attr_dict = {k: v for k, v in self.post_attr_dict.items() 
                           if v is not None}
        
        self.metadata_attr_dict = {}
        self.metadata_attr_dict['metadata_key'] = self.post.metadata_key
        self.metadata_attr_dict['metadata_content'] = self.post.metadata_content

    def det_publish_time(self):

        if not self.post.published_at:
            return datetime.datetime.now()
        return self.post.published_at
    
    def handle_images(self):

        # TODO: Add exception handling
        image_name = self.create_img_name() + '.jpg'
        image_path = os.path.join('..', IMG_BASE_DIR, image_name)
        decoded_image = base64.b64decode(self.post.image_contents)
        with open(image_path, 'wb') as file:
            file.write(decoded_image)
        self.post_attr_dict['images'] = image_path
    
    def create_img_name(self):
        return str(uuid.uuid4())

    def insert_post(self):

        db_obj = Database(DB_USER, 
                          DB_PWD, 
                          DB_HOST,
                          DB_PORT, 
                          POST_TABLE_NAME, 
                          POST_PRIM_KEY)
        db_obj.connect()
        db_obj.insert(**self.post_attr_dict)
        db_obj.close_conn()

    def insert_metadata(self):

        db_obj = Database(DB_USER, 
                          DB_PWD, 
                          DB_HOST,
                          DB_PORT, 
                          METADATA_TABLE_NAME, 
                          METADATA_PRIM_KEY)
        db_obj.connect()
        db_obj.insert(**self.metadata_attr_dict)
        db_obj.close_conn()

    def update():
        pass

    def delete():
        pass