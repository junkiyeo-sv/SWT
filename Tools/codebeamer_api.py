import requests, json

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
    
    def post_test_cases(self, project_uri, category_uri, test_data):
        # Implementing...
        print()

# Test main script
if __name__ == "__main__":
    cb = codebeamer_API()
    cb.request_session('your code beamer uri', 'id', 'pwd')
