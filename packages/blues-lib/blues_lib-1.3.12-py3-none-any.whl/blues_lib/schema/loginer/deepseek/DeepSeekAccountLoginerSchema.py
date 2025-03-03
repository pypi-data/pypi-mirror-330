import sys,os,re
from .DeepSeekLoginerFieldMixin import DeepSeekLoginerFieldMixin
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.AccountLoginerSchema import AccountLoginerSchema

class DeepSeekAccountLoginerSchema(DeepSeekLoginerFieldMixin,AccountLoginerSchema):
  
  # === create the account subtype fields ===
  def get_before_fill_atom(self):
    atom = [
      self.atom_factory.createClickable('switch to account mode','.ds-tabs .ds-tab:nth-of-type(2)'),
    ]
    return self.atom_factory.createArray('switch atom',atom)

  def get_fill_atom(self):
    atom = [
      self.atom_factory.createInput('name','.ds-form-item input[placeholder*=Phone],.ds-form-item input[placeholder*=手机号]','17607614755'),
      self.atom_factory.createInput('password','.ds-form-item input[placeholder*=Password],.ds-form-item input[placeholder*=密码]','Langcai10.'),
      self.atom_factory.createClickable('agree protocal','.ds-form-item .ds-checkbox'),
    ]
    return self.atom_factory.createArray('fill atom',atom)

  def get_submit_atom(self):
    atom = [
      self.atom_factory.createClickable('submit','.ds-sign-up-form__register-button'),
    ]
    return self.atom_factory.createArray('submit atom',atom)

