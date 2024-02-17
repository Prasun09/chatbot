import json
from difflib import get_close_matches


def load_database(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
        return data


def save_database(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file)


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, database: dict) -> str | None:
    for q in database["questions"]:
        if q["question"] == question:
            return q["answer"]


def chat_bot():
    database: dict = load_database('database.json')
    while True:
        user_input: str = input('You: ')
        if user_input.lower() == 'quit':
            break

        best_match: str | None = find_best_match(user_input, [q["question"] for q in database["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, database)
            print(f'Bot:{answer}')
        else:
            print("I don't know the answer. Can you teach me?")
            new_answer: str = input('Type the answer or "skip" to skip: ')
            if new_answer.lower() != 'skip':
                database["questions"].append({"question": user_input, "answer": new_answer})
                save_database('database.json', database)
                print('Bot: Thank you! I learned a new response!')


if __name__ == '__main__':
    chat_bot()
