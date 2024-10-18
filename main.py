from model import ExtendedModelWrapper
from db import BiographyDatabaseManager
from request_utils import RequestManager
import argparse


parser = argparse.ArgumentParser(description = "An addition program")

# add argument
parser.add_argument("--use_facts", nargs='*', metavar="num", type=bool,
    help="All the numbers separated by spaces will be added.")
parser.add_argument("--use_histories", nargs='*', metavar="num", type=bool,
    help="All the numbers separated by spaces will be added.")

# parse the arguments from standard input
args = parser.parse_args()

def get_action():
    return list(map(int, input().split()))[0]

if __name__ == '__main__':
    db_manager = BiographyDatabaseManager(db_file="biography_storage.db")
    db_manager.create_tables()
    agent = ExtendedModelWrapper()
    request_manager = RequestManager(db_manager)

    actions = {
        0: "Quit",
        1: "Generate screenplay",
        2: "Print available persons",
        3: "Get person info by id",
    }

    while True:
        print("Choose an action:")
        for idx, action in actions.items():
            print(f"\t{idx}: {action}")

        inp = get_action()
        if inp == 0:
            break
        elif inp == 1:
            print("Enter person id: ", end="")
            person_id = get_action()
            print("Person: ", db_manager.get_person(person_id))
            request = request_manager.make_request(
                person_id,
                use_facts=args.use_facts,
                use_histories=args.use_histories
            )
            response = agent.get_response(request)
            print('{:_^20}\n'.format(f'SCREENPLAY'))
            print(response, end='\n')
        elif inp == 2:
            all_persons = db_manager.get_all_persons()
            for person in all_persons:
                print(person)
        elif inp == 3:
            print("Enter person id: ", end="")
            person_id = get_action()
            print(db_manager.get_person(person_id))
