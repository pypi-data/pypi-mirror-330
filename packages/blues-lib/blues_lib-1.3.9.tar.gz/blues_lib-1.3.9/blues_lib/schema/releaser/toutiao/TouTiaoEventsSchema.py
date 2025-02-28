import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.releaser.EventsReleaserSchema import EventsReleaserSchema

class TouTiaoEventsSchema(EventsReleaserSchema):
  
  PLATFORM = 'toutiao'

  def create_url_atom(self):
    self.url_atom = self.atom_factory.createURL('events page','https://mp.toutiao.com/profile_v4/weitoutiao/publish')

  def create_content_atom(self):
    atoms = [
      # value placeholder 2: material_body_text
      self.atom_factory.createTextArea('content','.ProseMirror','${material_body_text}',1),
    ]
    self.content_atom = self.atom_factory.createArray('content atom',atoms)

  def create_others_atom(self):
    atoms = [
      # by default it's selected the original
      self.atom_factory.createClickable('not original','.exclusive .byte-checkbox-checked .byte-checkbox-mask',timeout=1),
      #self.atom_factory.createClickable('first pub','.exclusive .byte-checkbox-mask'),
      self.atom_factory.createClickable('source','.source-info-wrap label'),
    ]

    self.others_atom = self.atom_factory.createArray('content atom',atoms)

  def create_gallery_atom(self):
    # use the filed plachehoders
    atoms = [
      self.atom_factory.createClickable('Popup the dialog','.toolbar .weitoutiao-image-plugin'),
      # value placeholder 1: material_body_image ,set wait_time as 5
      self.atom_factory.createFile('Select images','.upload-handler input[type="file"]','${material_body_image}',5),
      self.atom_factory.createClickable('Upload images','.upload-image-panel .footer .byte-btn-primary'),
    ]

    self.gallery_atom = self.atom_factory.createArray('gallery atom',atoms)

  def create_preview_atom(self):
    return None

  def create_submit_atom(self):
    atoms = [
      self.atom_factory.createClickable('submit','.footer .publish-content'),
    ]
    self.submit_atom = self.atom_factory.createArray('submit',atoms)

  def create_popup_atom(self):
    atoms = [
      self.atom_factory.createClickable('tip','.modal-content .main-btn'),
    ]
    self.popup_atom = self.atom_factory.createArray('popup',atoms)

  def create_activity_atom(self):
    pass