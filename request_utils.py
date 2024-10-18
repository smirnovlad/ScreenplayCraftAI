from db import BiographyDatabaseManager
from category_description import (
    BIOGRAPGY_CATEGORY_NAME,
    BIOGRAPGY_CATEGORY_DESCRIPTION,
    BIOGRAPGY_CATEGORY_AUDIENCE
)

class RequestManager:
    def __init__(self, db_manager: BiographyDatabaseManager) -> None:
        self.db_manager = db_manager
        self.category_name = BIOGRAPGY_CATEGORY_NAME
        self.category_description = BIOGRAPGY_CATEGORY_DESCRIPTION
        self.category_audience = BIOGRAPGY_CATEGORY_AUDIENCE


    def make_request(self, person_id: int, use_facts: bool = True, use_histories: bool = True) -> str:
        person_info = self.db_manager.get_person(person_id)

        final_prompt = ""

        category_prompt = f"""
Твоя задача - написать сценарий для сюжета фильма.
Категория фильма: {self.category_name}\n
Описание категории: {self.category_description}\n
Целевая аудитория: {self.category_audience}\n
Персона: \n{person_info["name"]}: {person_info["info"]}.\n
        """

        final_prompt += category_prompt + '\n'

        if use_facts:
            facts_to_include = self.db_manager.get_person_facts(person_id, include=True)
            print("Facts to include: ", facts_to_include)
            if len(facts_to_include) > 0:
                facts_to_include_prompt = "В сюжете обязательно должны быть упомянуты следующие факты:\n"
                for idx, fact in enumerate(facts_to_include):
                    facts_to_include_prompt += f"{idx}. " + fact["fact"] + '\n'
                final_prompt += facts_to_include_prompt + '\n'

            facts_to_exclude = self.db_manager.get_person_facts(person_id, include=False)
            print("Facts to exclude: ", facts_to_exclude)
            if len(facts_to_exclude) > 0:
                facts_to_exclude_prompt = "В сюжете НЕ должны упоминаться следующие факты:\n"
                for idx, fact in enumerate(facts_to_exclude):
                    facts_to_exclude_prompt += f"{idx}. " + fact["fact"] + '\n'
                final_prompt += facts_to_exclude_prompt + '\n'

        if use_histories:
            histories = self.db_manager.get_person_histories(person_id)

            if len(histories) > 0:
                history_prompt = """
Помимо той информации, которая тебе известна, 
предлагаю также вдохновиться следующими историями о персоне:\n
                """
                for idx, history in enumerate(histories):
                    history_prompt += '{:_^20}\n'.format(f'История {idx}')
                    history_prompt += history + '\n\n\n'
                final_prompt += history_prompt

        tune_prompt = """
Для каждой сцены пиши максимально подробный сценарий, включая также информацию о длительности сцены.
        """

        final_prompt += tune_prompt + '\n'

        print("Final prompt: \n", final_prompt)

        return final_prompt
