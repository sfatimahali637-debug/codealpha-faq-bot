def load_faq(filename):
    faq = {}
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
    for i in range(0, len(lines), 2):
        question = lines[i].strip().replace("Q: ", "").lower()
        answer = lines[i+1].strip().replace("A: ", "")
        faq[question] = answer
    return faq

faq = load_faq("faq.txt")
print("Bot: Hello! I am CodeAlpha FAQ Bot. Type 'exit' to quit.")

while True:
    user_input = input("You: ").lower().strip().replace("q: ", "")

    if user_input == "exit":
        print("Bot: Bye!")
        break

    answer = faq.get(user_input, "Sorry, I don't have an answer for that.")
    print("Bot:", answer)