import requests

# Implementing codebeamer API class
class codebeamer_API():
    def request_session(self, url, id, pwd):
        self.cb_url = url;
        self.session = requests.Session()
        self.session.auth = (id, pwd)
        
    def get_session_auth(self):
        return self.session.auth
    
    def get_project_uri(self, project_key):
        response = self.session.get(self.cb_url + '/project/' + project_key)
        if response.status_code == 200:
            project = response.json()
            return project['uri']
    
    def get_tracker_list(self, project_uri):
        response = self.session.get(self.cb_url + project_uri + '/trackers')
        if response.status_code == 200:
            tracker_list = response.json()
            return tracker_list
        
    def get_category_swe4_tc_uri(self, project_uri):
        response = self.session.get(self.cb_url + project_uri + '/categories')
        if response.status_code == 200:
            category_list = response.json()
            for category in category_list:
                if category['name'] in "Software Unit Test Cases":
                    return category['uri']
    
    def post_tracker(self, tracker_headers, tracker_body):
        '''
        tracker_headers = {'Content-Type': 'application/json'}
        
        tracker_body = {
            "project"     : "projectURL",
            "type"        : "/tracker/type/Requirement",
            "name"        : "Python Test Post",
            "keyName"     : "PTP",
            "description" : "A Test tracker for Rest-Api tests",
            "descFormat"  : "Wiki",
            "workflow"    : True
        }
        '''
        response = self.session.post(self.cb_url + '/tracker', headers=tracker_headers, json=tracker_body, auth=self.session.auth)
        if response == 201:
            print(response.status_code)
        else:
            print(response.status_code)
            
    def post_item(self, item_headers, item_body):
        '''
        item_headers = {'Content-Type': 'application/json'}
        
        item_body = {
            "name"        : "Test Item",
            "tracker"     : "trackerURL",
            "status"      : "New",
            "type"        : "Functional",
            "description" : "Test item description",
            "preAction"   : "",
            "testSteps"   : "",
            "postAction"  : "",
            "comments"    : ""
        }
        '''
        response = self.session.post(self.cb_url + '/item', headers=item_headers, json=item_body, auth=self.session.auth)
        if response == 201:
            print(response.status_code)
        else:
            print(response.status_code)


# Test main script
if __name__ == "__main__":
    cb = codebeamer_API()
    # cb.request_session('your code beamer uri', 'id', 'pwd')
    
