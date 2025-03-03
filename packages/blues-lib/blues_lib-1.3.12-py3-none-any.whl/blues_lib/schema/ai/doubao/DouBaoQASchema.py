import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.ai.AIQASchema import AIQASchema

class DouBaoQASchema(AIQASchema):

  def create_url_atom(self):
    self.url_atom = self.atom_factory.createURL('QA page url','https://www.doubao.com/chat/')

  def create_question_atom(self):
    atoms = [
      # value placeholder 2: material_body_text
      #self.atom_factory.createClickable('swich','div[data-testid="create_conversation_button"]'),
      self.atom_factory.createInput('input','textarea.semi-input-textarea','${question}'),
    ]

    self.question_atom = self.atom_factory.createArray('question',atoms)

  def create_submit_atom(self):
    atoms = [
      # value placeholder 2: material_body_text
      self.atom_factory.createClickable('submit','#flow-end-msg-send'),
    ]

    self.submit_atom = self.atom_factory.createArray('submit',atoms)

  def create_answer_atom(self):
    vertical_copy_sel = 'div[data-testid="receive_message"] button[data-testid="message_action_copy"]'
    horizontal_copy_sel = 'div[data-testid="container_inner_copy_btn"]'
    # horizontal 选择器优先
    copy_sel = [horizontal_copy_sel,vertical_copy_sel]
    
    atoms = [
      self.atom_factory.createPause('wait to answer',20),
      self.atom_factory.createClickable('copy',copy_sel),
    ] 
    self.answer_atom = self.atom_factory.createArray('wait and copy',atoms)
    