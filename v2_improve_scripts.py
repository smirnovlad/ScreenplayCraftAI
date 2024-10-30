from model import ExtendedModelWrapper
from db import BiographyDatabaseManager
from request_utils import RequestManager
import time


agent = ExtendedModelWrapper()

db_manager = BiographyDatabaseManager(db_file="biography_storage.db")
db_manager.create_tables()
agent = ExtendedModelWrapper()
request_manager = RequestManager(db_manager)

for person_id in range(1, 14):
    new_script = ""
    name = db_manager.get_person(person_id)['name']
    with open(f"mistralai_results/v1/{person_id}_script.txt", "r", encoding="utf-8") as text_file:
        content = text_file.read()
        
    scenes = content.split('Сцена ')[1:] 
    
    for i, scene in enumerate(scenes, start=1):
        start = time.time()
        lines = scene.strip().split('\n')[1:]
        scene_text = '\n'.join(lines).strip()
        request = \
            f"Представьте, что вы сценарист художественного фильма, \
            основанного на биографии выдающегося российского ученого {name}. \
            Фильм должен вдохновлять зрителей на познание, исследование и стремление к достижениям. \
            Зрители должны сопереживать герою, разделяя его радости и преодолевая вместе с ним трудности. \
            Необходимо показать вклад ученого в развитие науки и общества, вызывая у зрителей уважение и признание. \n \
            Ниже приведена сцена, которую нужно переделать. Ваша цель – сделать ее более живой, \
            динамичной и эмоционально насыщенной. Добавьте яркие детали, раскрывающие характер героя, \
            его внутренний мир и мотивацию. Уберите сухие безжизненные реплики, вместо этого создайте \
            правдоподобные и захватывающие диалоги. Можно начать сцену с более отвлеченных тем, \
            постепенно переходя к сути диалога. Не стесняйтесь добавлять художественные детали, \
            но старайтесь не искажать основные биографические факты и сохранять достоверность научной деятельности героя. \
            \n\n {scene_text} "
       
   

        response = agent.get_response(request)
        new_scene_text = f'#### Сцена {i}:\n{response}\n\n'
        new_script += new_scene_text
        
        print('{:_^20}\n'.format(f'SCREENPLAY'))
        print(new_scene_text, end='\n')
        
        end = time.time()
        print(f"Person {person_id}. Scene {i}. Elapsed time: ", end - start)
        # if end - start < 61:
        #     time.sleep(61 - (end - start))
       
    agent.reset_context()
    with open(f"mistralai_results/v2/{person_id}_script.txt", "w", encoding="utf-8") as text_file:
        text_file.write(new_script)