from model import ExtendedModelWrapper
from db import BiographyDatabaseManager
from request_utils import RequestManager
import time

import re

def split_string_by_scene(input_string):
    pattern = re.compile(r'Сцена \d+')
    matches = list(pattern.finditer(input_string))
    if not matches:
        return [input_string]
    result = []
    start = 0
    for match in matches:
        end = match.start()
        result.append(input_string[start:end].strip())
        start = match.end()

    result.append(input_string[start:].strip())
    return result



openai_folder = "script_outlines/openai"
mistralai_folder = "script_outlines/mistralai"


agent = ExtendedModelWrapper()

db_manager = BiographyDatabaseManager(db_file="biography_storage.db")
db_manager.create_tables()
agent = ExtendedModelWrapper()
request_manager = RequestManager(db_manager)

for person_id in list(range(1, 12)) + [13]:
    new_script = ""
    name = db_manager.get_person(person_id)['name']
    
    with open(f"{openai_folder}/{person_id}_outline.txt", "r", encoding="utf-8") as text_file:
        content = text_file.read()
        
    scenes = split_string_by_scene(content)[1:]
    full = f"Запомните полный план фильма: \n {content}. \n\n Теперь сфокусируйтесь лишь на  сцене. "
    for i, scene in enumerate(scenes, start=1):
        start = time.time()
        inserted = full if i == 1 else ""
        request = \
            f"Представьте, что вы сценарист художественного фильма, \
            основанного на биографии выдающегося российского ученого {name}. \
            Фильм должен вдохновлять зрителей на познание, исследование и стремление к достижениям. \
            Зрители должны сопереживать герою, разделяя его радости и преодолевая вместе с ним трудности. \
            Необходимо показать вклад ученого в развитие науки и общества, вызывая у зрителей уважение и признание. \n \
            {inserted} \
            Ниже приведен план сцены. Ваша цель – сделать её живой, \
            динамичной и эмоционально насыщенной. Добавьте яркие детали, раскрывающие характер героя, \
            его внутренний мир и мотивацию. Создайте правдоподобные и захватывающие диалоги. \
            Можно начать сцену с более отвлеченных тем, постепенно переходя к сути диалога. \
            Не стесняйтесь добавлять художественные детали, \
            но старайтесь не искажать основные биографические факты и сохранять достоверность научной деятельности героя. \
            \nПлан сцены:\n {scene} " 

        response = agent.get_response(request)
        new_scene_text = f'{response}\n\n'
        new_script += new_scene_text
        
        print('{:_^20}\n'.format(f'SCREENPLAY'))
        print(new_scene_text, end='\n')
        
        end = time.time()
        print(f"Person {person_id}. Scene {i}. Elapsed time: ", end - start)
       
    agent.reset_context()
    with open(f"mistralai_results/v3/{person_id}_script.txt", "w", encoding="utf-8") as text_file:
        text_file.write(new_script)