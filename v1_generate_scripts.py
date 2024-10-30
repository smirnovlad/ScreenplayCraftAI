from lib.model import ExtendedModelWrapper
from lib.db import BiographyDatabaseManager
from lib.request_utils import RequestManager
import argparse
import time


parser = argparse.ArgumentParser(description = "An addition program")

# add argument
parser.add_argument("--use_facts", nargs='*', metavar="num", type=bool,
    help="All the numbers separated by spaces will be added.")
parser.add_argument("--use_histories", nargs='*', metavar="num", type=bool,
    help="All the numbers separated by spaces will be added.")

# parse the arguments from standard input
args = parser.parse_args()

db_manager = BiographyDatabaseManager(db_file="biography_storage.db")
db_manager.create_tables()
agent = ExtendedModelWrapper()
request_manager = RequestManager(db_manager)

for person_id in range(1, 14):
    print("Person: ", db_manager.get_person(person_id))
    request = request_manager.make_request(
        person_id,
        use_facts=args.use_facts,
        use_histories=args.use_histories
    )
    start = time.time()

    response = agent.get_response(request)
    print('{:_^20}\n'.format(f'SCREENPLAY'))
    print(response, end='\n')

    end = time.time()
    print(f"{person_id}. Elapsed time: ", end - start)

    # with open(f"prompts/{person_id}_prompt.txt", "w", encoding="utf-8") as text_file:
    #     text_file.write(request)
    #
    with open(f"mistralai_results/v1/{person_id}_script.txt", "w", encoding="utf-8") as text_file:
        text_file.write(response)

    agent.reset_context()