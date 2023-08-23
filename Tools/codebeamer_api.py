# -*- coding: utf-8 -*-
"""codebeamer_api.py tool description.

The CodeBeamerAPI class is a library implemented to request get, post, 
    put, and delete data from the server using the codebeamer Rest API.

See function comment out for further explanation.
"""
import requests

class CodeBeamerAPI():
    
    # ---------------------------- function seperation line ------------------------------------ #
    def request_session(self, uri, id, pwd):
        ''' Request session connection to codebeamer server
        
        Args:
            uri: codebeamer REST API server uri
            id: codebeamer user id (rest api permission required)
            pwd: codebeamer user password
        
        Ret:
            return type list, value = [response.status_code, ret_value]
            response.status_code: success number 200, failure number not 200
            ret_value: messages about success and failure
        '''
        self.cb_uri = uri;
        self.session = requests.Session()
        self.session.auth = (id, pwd)
        response = self.session.get(self.cb_uri + '/version')
        if response.status_code == 200:
            return [response.status_code, 'connected session']
        else:
            return [response.status_code, 'check your ID/Password']
    
    # ---------------------------- function seperation line ------------------------------------ #
    def get_session_auth(self):
        ''' Get currently connected session account information
        
        Args: none
        
        Ret:
            session account information(id, password)
        '''
        return self.session.auth
    
    # ---------------------------- function seperation line ------------------------------------ #
    def get_project_uri(self, project_name):
        ''' Get project uri by project name
         
        Args:
            project_name: the name of the required project uri
            
        Ret:
            return type list, value = [response.status_code, ret_value]
            response.status_code: success number 200, failure number not 200
            ret_value: project uri on success, message on failure
        '''
        response = self.session.get(self.cb_uri + '/projects')
        if response.status_code == 200:
            project_list = response.json()
            for project in project_list:
                if project['name'] in project_name:
                    return [response.status_code, project['uri']]
            return [999, project_name + ' project does not exist.']
        else:
            return [response.status_code, 'check your project_name']
    
    # ---------------------------- function seperation line ------------------------------------ #
    def get_category_uri(self, project_uri, category_name):
        ''' Get category uri by category name
        
        Args:
            project_uri: project uri to which the category belongs
            category_name: the name of the required category uri
            
        Ret:
            return type list, value = [response.status_code, ret_value]
            response.status_code: success number 200, failure number not 200
            ret_value: category uri on success, message on failure
        '''
        response = self.session.get(self.cb_uri + project_uri + '/categories')
        if response.status_code == 200:
            category_list = response.json()
            for category in category_list:
                if category['name'] == category_name:
                    return [response.status_code, category['uri']]
            return [999, category_name + ' category does not exist.']
        else:
            return [response.status_code, 'check your project_uri or category_name']
    
    # ---------------------------- function seperation line ------------------------------------ #
    def get_item_uri(self, project_uri, tracker_category_uri, item_name):
        ''' Get item uri by item name
        
        Args:
            project_uri: project uri to which the category belongs
            tracker_category_uri: tracker/category uri to which the item belongs
            item_name: the name of the required item uri
            
        Ret:
            return type list, value = [response.status_code, ret_value]
            response.status_code: success number 200, failure number not 200
            ret_value: item uri on success, message on failure
        '''
        response = self.session.get(self.cb_uri + project_uri + tracker_category_uri + '/items')
        if response.status_code == 200:
            item_list = response.json()
            for item in item_list['items']:
                if item['name'] == item_name:
                    return [response.status_code, item['uri']]
            return [999, item_name + ' item does not exist.']
        else:
            return [response.status_code, 'check your project_uri, tracker_category_uri or item_name']
    
    # ---------------------------- function seperation line ------------------------------------ #
    def get_tracker_list(self, project_uri):
        ''' Get tracker list for the project uri
        
        Args:
            project_uri: project uri to which the tracker belongs
            
        Ret:
            return type list, value = [response.status_code, ret_value]
            response.status_code: success number 200, failure number not 200
            ret_value: tracker list on success, message on failure
        '''
        response = self.session.get(self.cb_uri + project_uri + '/trackers')
        if response.status_code == 200:
            tracker_list = response.json()
            return [response.status_code, tracker_list]
        else:
            return [response.status_code, 'check your project_uri']

    # ---------------------------- function seperation line ------------------------------------ #
    def get_tracker_item_schema(self, project_uri, tracker_uri):
        ''' Get item schema(attribute) for that tracker
        
        Args:
            project_uri: project uri to which the tracker belongs
            tracker_uri: tracker uri to which the item belongs
            
        Ret:
            return type list, value = [response.status_code, ret_value]
            response.status_code: success number 200, failure number not 200
            ret_value: item schema(attribute) on success, message on failure
        '''
        response = self.session.get(self.cb_uri + project_uri + tracker_uri + '/newItem')
        if response.status_code == 200:
            return [response.status_code, response.json()]
        else:
            return [response.status_code, 'check your project_uri or tracker_uri']
    
    # ---------------------------- function seperation line ------------------------------------ #
    def get_category_item_schema(self, project_uri, category_uri):
        ''' Get item schema(attribute) for that category
        
        Args:
            project_uri: project uri to which the category belongs
            category_uri: category uri to which the item belongs
            
        Ret:
            return type list, value = [response.status_code, ret_value]
            response.status_code: success number 200, failure number not 200
            ret_value: item schema(attribute) on success, message on failure
        '''
        response = self.session.get(self.cb_uri + project_uri + category_uri + '/newItem')
        if response.status_code == 200:
            return [response.status_code, response.json()]
        else:
            return [response.status_code, 'check your project_uri or category_uri']
    
    # ---------------------------- function seperation line ------------------------------------ #
    def post_tracker(self, tracker_headers, tracker_body):
        ''' Create a tracker for the project
        
        Args:
            tracker_headers: post data header(see comments below)
            tracker_body: post json data body(see comments below)
            
        Ret:
            return type list, value = [response.status_code, ret_value]
            response.status_code: success number 201, failure number not 201
            ret_value: messages about success and failure
        '''
        
        '''
        tracker_headers = {'Content-Type': 'application/json'}
        
        tracker_body = {
            "project"     : "project_uri",
            "type"        : "/tracker/type/Requirement",
            "name"        : "Python Test Post",
            "keyName"     : "PTP",
            "description" : "A Test tracker for Rest-Api tests",
            "descFormat"  : "Wiki",
            "workflow"    : True
        }
        '''
        response = self.session.post(self.cb_uri + '/tracker', headers=tracker_headers, json=tracker_body, auth=self.session.auth)
        if response.status_code == 201:
            return [response.status_code, 'completed post API']
        else:
            return [response.status_code, 'check your tracker_headers or tracker_body']
    
    # ---------------------------- function seperation line ------------------------------------ #        
    def post_item(self, item_headers, item_body):
        ''' Create a item for the tracker/category
        
        Args:
            item_headers: post data header(see comments below)
            item_body: post json data body(see comments below)
            
        Ret:
            return type list, value = [response.status_code, ret_value]
            response.status_code: success number 201, failure number not 201
            ret_value: messages about success and failure
        '''
        
        '''
        item_headers = {'Content-Type': 'application/json'}
        
        # Tracker item (draft body)
        item_body = {
            "name"        : "",
            "tracker"     : "project_uri + '/' + tracker_uri",
            "status"      : "",
            "type"        : "",
            "description" : "",
            "preAction"   : "",
            "testSteps"   : "",
            "postAction"  : "",
        }
        
        # Category item properties = get_category_item_schema(project_uri, category_uri)
        # Tracker item properties = get_tracker_item_schema(project_uri, tracker_uri)
        item_body = {
            "name"        : "",
            "tracker"     : "project_uri + '/' + tracker_uri",
            "status"      : "",
            "type"        : "",
            "description" : "",
            "priority"    : "",
            "reusable"    : True or False
        }
        '''
        response = self.session.post(self.cb_uri + '/item', headers=item_headers, json=item_body, auth=self.session.auth)
        if response.status_code == 201:
            return [response.status_code, 'completed post API']
        else:
            return [response.status_code, 'check your item_headers or item_body']
    
    # ---------------------------- function seperation line ------------------------------------ #
    def delete_item(self, item_uri):
        ''' Delete a item
        
        Args:
            item_uri: item uri to delete
            
        Ret:
            return type list, value = [response.status_code, ret_value]
            response.status_code: success number 200, failure number not 200
            ret_value: messages about success and failure
        '''
        response = self.session.delete(self.cb_uri + item_uri)
        if response.status_code == 200:
            return [response.status_code, 'deleted item']
        else:
            return [response.status_code, 'check your item_uri']
    
    # ---------------------------- function seperation line ------------------------------------ #
    def put_item(self, item_headers, item_body):
        ''' Update a item for the tracker/category
        
        Args:
            item_headers: put data header(see comments below)
            item_body: put json data body(see comments below)
            
        Ret:
            return type list, value = [response.status_code, ret_value]
            response.status_code: success number 200, failure number not 200
            ret_value: messages about success and failure
        '''
        
        '''
        item_headers = {'Content-Type': 'application/json'}
        
        item_body = {
            "uri" : "item_uri",
            "description" : "updated description"
        }
        '''
        response = self.session.put(self.cb_uri + '/item', headers=item_headers, json=item_body, auth=self.session.auth)
        if response.status_code == 200:
            return [response.status_code, 'completed put API']
        else:
            return [response.status_code, 'check your item_headers or item_body']
