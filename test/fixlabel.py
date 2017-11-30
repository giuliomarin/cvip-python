from cvip import ymlparser as yml
import sys

label_info_path = '/Data/9_pg/line15/bundle/test/test/2017_11_09_09_45_14f/labelInfo.yml'
label = yml.parse(label_info_path)
model = yml.parse('/Data/9_pg/models3.yml')

label['model']['descriptors'] = model['model']['descriptors']

yml.write(label_info_path.replace('.yml', 'Model.yml'), label)