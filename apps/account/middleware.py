class ProcessUserLayout(object):
    ''' Middlware to get user type and set the navigation items based user type '''

    def process_request(self, request):
        user_type = "guest"
        if request.user.is_authenticated():
            user_type = 'auth' #request.user.profile.user_type  
        request.layout = "layouts/" + user_type + ".html"
        request.nav = "navs/" + user_type + ".html"
