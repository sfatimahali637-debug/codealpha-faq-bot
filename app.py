from flask import Flask, render_template_string, request
app = Flask(__name__)
faq = {
    "hello": "Hello! I am CodeAlpha FAQ Bot. How can I help you?",
    "hi": "Hi there! Ask me anything about CodeAlpha.",
    "hey": "Hey! Welcome to CodeAlpha Bot 🤖",
        "codealpha": "CodeAlpha is a platform that offers free virtual internships. You work on real projects and get a certificate.",
    "what is codealpha": "CodeAlpha is a platform that offers free virtual internships. You work on real projects and get a certificate.",
    "internship": "CodeAlpha offers 4-week virtual internships in Web Dev, Python, Java, AI/ML, Cyber Security. All are free.",
    "about internship": "CodeAlpha offers 4-week virtual internships in Web Dev, Python, Java, AI/ML, Cyber Security. All are free.",
    "duration": "Each internship lasts for 4 weeks.",
    "how long": "Each internship lasts for 4 weeks.",
    "certificate": "Yes! You will get a completion certificate + LinkedIn recommendation after submitting all tasks.",
    "cert": "Yes! You will get a completion certificate + LinkedIn recommendation after submitting all tasks.",
    "apply": "You can apply on the CodeAlpha website www.codealpha.tech. Registration is free.",
    "how to apply": "You can apply on the CodeAlpha website www.codealpha.tech. Registration is free.",
    "task": "You will get 2-3 tasks to complete during the internship. You have to submit them on GitHub.",
    "tasks": "You will get 2-3 tasks to complete during the internship. You have to submit them on GitHub.",
    "domain": "Available Domains: 1. Web Development 2. Python Programming 3. Java Programming 4. AI/ML 5. Cyber Security",
    "domains": "Available Domains: 1. Web Development 2. Python Programming 3. Java Programming 4. AI/ML 5. Cyber Security",
    "stipend": "No, CodeAlpha internships are free and do not provide any stipend. But you get certificate.",
    "paid": "No, CodeAlpha internships are free and do not provide any stipend. But you get certificate.",
    "exit": "Goodbye! Have a great day!",
    "bye": "Bye! Come back anytime!"
}

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeAlpha FAQ Bot</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            padding: 20px;
        }
        
       .chat-container {
            width: 100%;
            max-width: 500px;
            height: 90vh;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 25px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
       .chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            text-align: center;
            font-size: 22px;
            font-weight: 700;
        }
        
       .suggestions {
            display: flex;
            gap: 8px;
            padding: 15px;
            background: #f0f2ff;
            overflow-x: auto;
        }
       .suggestions button {
            padding: 8px 15px;
            border: none;
            background: white;
            border-radius: 20px;
            cursor: pointer;
            font-size: 13px;
            white-space: nowrap;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
       .suggestions button:hover { background: #667eea; color: white; }
        
       .chat-messages {
            flex: 1;
            padding: 25px;
            overflow-y: auto;
            background: #f8f9ff;
        }
        
       .message { margin-bottom: 18px; display: flex; animation: slideIn 0.3s ease; }
        @keyframes slideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
       .message.user { justify-content: flex-end; }
        
       .message-content {
            max-width: 75%;
            padding: 14px 18px;
            border-radius: 20px;
            line-height: 1.5;
            font-size: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
       .message.bot.message-content { background: white; color: #333; border-bottom-left-radius: 5px; }
       .message.user.message-content { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-bottom-right-radius: 5px; }
        
       .chat-input { display: flex; padding: 20px; background: white; border-top: 1px solid #e0e0e0; gap: 10px; }
       .chat-input input { flex: 1; padding: 14px 20px; border: 2px solid #e0e0e0; border-radius: 30px; outline: none; font-size: 15px; }
       .chat-input input:focus { border-color: #667eea; }
       .chat-input button { padding: 14px 28px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 30px; cursor: pointer; font-weight: 600; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">🤖 CodeAlpha FAQ Bot</div>
        
        <div class="suggestions">
            <button onclick="quickAsk('internship')">Internship</button>
            <button onclick="quickAsk('certificate')">Certificate</button>
            <button onclick="quickAsk('domain')">Domains</button>
            <button onclick="quickAsk('tasks')">Tasks</button>
        </div>

        <div class="chat-messages" id="chatMessages">
            <div class="message bot">
                <div class="message-content">Hello! I am CodeAlpha FAQ Bot. Ask me anything about CodeAlpha internships! ✨<br><br>Or click buttons above 👆</div>
            </div>
        </div>
        <div class="chat-input">
            <input type="text" id="userInput" placeholder="Ask me something..." onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            if (message === '') return;
            addMessage(message, 'user');
            input.value = '';
            fetch('/get', { method: 'POST', headers: {'Content-Type': 'application/x-www-form-urlencoded'}, body: 'msg=' + encodeURIComponent(message) })
           .then(response => response.text())
           .then(data => { addMessage(data, 'bot'); });
        }
        function quickAsk(q) {
            document.getElementById('userInput').value = q;
            sendMessage();
        }
        function addMessage(text, sender) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + sender;
            messageDiv.innerHTML = '<div class="message-content">' + text + '</div>';
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
    </script>
</body>
</html>
"""
@app.route("/")
def home():
    return render_template_string(HTML)
@app.route("/get", methods=["POST"])
def get_bot_response():
    userText = request.form["msg"].lower()

    for key in faq:
        if key in userText:
            return faq[key]

    return "Sorry, I don't understand that. Try: internship, certificate, domain, tasks"
if __name__ == "__main__":
    app.run(debug=True)