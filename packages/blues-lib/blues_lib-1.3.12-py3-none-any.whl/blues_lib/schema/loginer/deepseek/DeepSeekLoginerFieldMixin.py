class DeepSeekLoginerFieldMixin():

  # === common fields of BaiJia login ===
  def get_login_page_url_atom(self):
    '''
    @description: set the login's page url {URLAtom}
    '''
    return self.atom_factory.createURL('Log in url','https://chat.deepseek.com/sign_in')

  def get_loggedin_page_url_atom(self):
    '''
    @description: set the loggedin's page url {URLAtom}
    '''
    return self.atom_factory.createURL('Homepage url','https://chat.deepseek.com/')

  def get_login_page_identifier_atom(self):
    '''
    @description: set the css selector of the identifier in the login page{ElementAtom}
    '''
    return self.atom_factory.createElement('Login page identifier','.ds-sign-up-form__register-button')

  def get_max_login_waiting_time_atom(self):
    '''
    @description: set the max login waiting time {DataAtom}
    '''
    return self.atom_factory.createData('Wait for 5 seconds to confirm the login status',5)

  def get_proxy_config_atom(self):
    '''
    @description: set the browser proxy for persistent loginer {DataAtom}
    '''
    config = {
      'scopes': ['.*chat.deepseek.com.*'],
    }
    return self.atom_factory.createData('proxy config',config)

  def get_cookie_filter_config_atom(self):
    '''
    @description: set the logged cookie filter patterns for persistent loginer {DataAtom}
    '''
    config = {
      'url_pattern':'/api/v0/chat_session/',
      'value_pattern':None
    }
    return self.atom_factory.createData('cookie filter config',config)
  
