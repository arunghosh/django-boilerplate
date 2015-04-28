class ProcessUserLayout(object):
    ''' Middlware to get user type and set the navigation items based user type '''

    def process_request(self, request):
        user_type = "guest"
        if request.user.is_authenticated():
            user_type = request.user.type_str  
        request.layout = "layouts/" + user_type + ".html"
        request.nav = "navs/" + user_type + ".html"
