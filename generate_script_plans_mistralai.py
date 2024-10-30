from lib.model import ExtendedModelWrapper
from lib.db import BiographyDatabaseManager
from lib.request_utils import RequestManager
import time

db_manager = BiographyDatabaseManager(db_file="biography_storage.db")
db_manager.create_tables()
agent = ExtendedModelWrapper()
request_manager = RequestManager(db_manager)

with open(f"prompt.txt", "r", encoding="utf-8") as text_file:
    prompt = text_file.read()
    
for person_id in range(1, 14):
    print("Person: ", db_manager.get_person(person_id))
    
    name = db_manager.get_person(person_id)['name']
    history = db_manager.get_person_histories(person_id)[0]['history']
    request = prompt.format(name, history)
            
    start = time.time()

    response = agent.get_response(request)
    print('{:_^20}\n'.format(f'SCREENPLAY'))
    print(response, end='\n')

    end = time.time()
    print(f"{person_id}. Elapsed time: ", end - start)

    with open(f"script_outlines/mistralai/{person_id}_outline.txt", "w", encoding="utf-8") as text_file:
        text_file.write(response)

    agent.reset_context()