
import sys,os,re
from .TouTiaoLoginerFieldMixin import TouTiaoLoginerFieldMixin

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.MACLoginerSchema import MACLoginerSchema

class TouTiaoMACLoginerSchema(TouTiaoLoginerFieldMixin,MACLoginerSchema):
  
  # === create mac subclass fields ===
  def get_before_fill_atom(self):
    pass

  def get_fill_atom(self):
    '''
    Typed atom
    Fill the phone number for send sms
    '''
    atom = [
      # wait the form dialog popup in 10 seconds
      self.atom_factory.createInput('Phone number','.web-login .web-login-normal-input__input','17607614755',timeout=10),
      self.atom_factory.createClickable('Agree privacy','.web-login .web-login-confirm-info__checkbox'),
    ]
    return self.atom_factory.createArray('Fill phone number',atom)

  def get_send_atom(self):
    '''
    Typed atom
    Send the sms
    '''
    atom = [
      self.atom_factory.createClickable('Next step','.web-login .web-login-button-input__button-text'),
    ]
    return self.atom_factory.createArray('Send the sms',atom)

  def get_code_atom(self):
    '''
    Typed atom
    Fill in the auth code
    Only one character can be entered in the input field at a time
    It will receive a dynamic value
    '''
    return self.atom_factory.createInput('Char input','.web-login .web-login-button-input__input','')

  def get_submit_atom(self):
    '''
    Typed atom
    Submit to login, this site will submit automatically after the auth code are filled
    '''
    atom = [
      self.atom_factory.createClickable('submit button','.web-login .web-login-button'),
    ]
    return self.atom_factory.createArray('Submit',atom)



