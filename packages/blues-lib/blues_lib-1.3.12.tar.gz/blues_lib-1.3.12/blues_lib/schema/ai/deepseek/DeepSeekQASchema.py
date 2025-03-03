import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.ai.AIQASchema import AIQASchema

class DeepSeekQASchema(AIQASchema):

  def create_url_atom(self):
    self.url_atom = self.atom_factory.createURL('QA page url','https://chat.deepseek.com/')

  def create_question_atom(self):
    atoms = [
      self.atom_factory.createInput('input','#chat-input','${question}'),
    ]
    self.question_atom = self.atom_factory.createArray('question',atoms)

  def create_submit_atom(self):
    atoms = [
      self.atom_factory.createClickable('submit','div[role="button"][aria-disabled]'),
    ]
    self.submit_atom = self.atom_factory.createArray('submit',atoms)

  def create_answer_atom(self):
    atoms = [
      self.atom_factory.createPause('wait to answer',45),
      self.atom_factory.createClickable('copy','.ds-markdown+div .ds-icon-button:first-child'),
    ]
    self.answer_atom = self.atom_factory.createArray('wait and copy',atoms)
    

