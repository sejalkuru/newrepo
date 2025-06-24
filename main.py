from flask import Flask, request, jsonify, render_template_string
import os
from openai import OpenAI

app = Flask(__name__)

# Initialize OpenAI client with your API key from environment variable
client = OpenAI(api_key=os.getenv("chatBot"))

@app.route("/")
def index():
    return render_template_string("""
    <!doctype html>
    <html>
    <head>
      <title>Craig Long LLC Chatbot</title>
      <link href="https://fonts.googleapis.com/css2?family=DM+Sans&display=swap" rel="stylesheet">
      <style>
        body {
          font-family: 'DM Sans', sans-serif;
          background-color: #f0f8ff; /* very light blue */
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          margin: 0;
        }
        #chat-container {
          width: 600px;
          height: 400px;
          background: #e6f0fa; /* light blue shade */
          box-shadow: 0 4px 10px rgba(0,0,50,0.1);
          border-radius: 12px;
          display: flex;
          flex-direction: column;
          padding: 20px;
        }
        #chatbox {
          flex: 1;
          border: 1px solid #c3d1f4;
          background: #fff;
          border-radius: 8px;
          padding: 15px;
          overflow-y: auto;
          margin-bottom: 15px;
          font-size: 1rem;
          color: #003366;
        }
        #input-area {
          display: flex;
        }
        #input {
          flex: 1;
          font-family: 'DM Sans', sans-serif;
          font-size: 1rem;
          padding: 10px;
          border: 1px solid #aac4ff;
          border-radius: 8px 0 0 8px;
          outline: none;
          color: #003366;
        }
        #input:focus {
          border-color: #5a8dee;
          box-shadow: 0 0 5px #5a8dee;
        }
        #send {
          background-color: #5a8dee;
          border: none;
          color: white;
          font-weight: 600;
          font-size: 1rem;
          padding: 10px 20px;
          cursor: pointer;
          border-radius: 0 8px 8px 0;
          transition: background-color 0.3s ease;
        }
        #send:hover {
          background-color: #3f6ed8;
        }
        .message {
          margin-bottom: 12px;
          line-height: 1.4;
          white-space: pre-wrap;
        }
        .user {
          color: #2a4365;
          font-weight: 600;
        }
        .bot {
          color: #2a5a9a;
          font-style: italic;
        }
      </style>
    </head>
    <body>
      <div id="chat-container">
        <div id="chatbox"></div>
        <div id="input-area">
          <input id="input" autocomplete="off" placeholder="Type your question here..." />
          <button id="send">Send</button>
        </div>
      </div>

      <script>
        const chatbox = document.getElementById('chatbox');
        const input = document.getElementById('input');
        const send = document.getElementById('send');

        document.addEventListener("DOMContentLoaded", function() {
          appendMessage("Hello! I'm the Craig Long LLC virtual assistant. How can I help you today?", 'bot');
        });

        function appendMessage(text, cls) {
          const div = document.createElement('div');
          div.className = 'message ' + cls;

          if (cls === 'bot') {
            const img = document.createElement('img');
            img.src = 'https://i.postimg.cc/VktGpw2C/Untitled-design-1.png'; // chatbot icon URL
            img.alt = 'bot icon';
            img.style.width = '24px';
            img.style.height = '24px';
            img.style.verticalAlign = 'middle';
            img.style.marginRight = '8px';
            div.appendChild(img);
          }

          const span = document.createElement('span');
          span.textContent = text;
          div.appendChild(span);

          chatbox.appendChild(div);
          chatbox.scrollTop = chatbox.scrollHeight;
        }

        send.onclick = () => {
          const msg = input.value.trim();
          if (!msg) return;
          appendMessage('You: ' + msg, 'user');
          input.value = '';
          fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
          })
          .then(res => res.json())
          .then(data => {
            if (data.response) {
              appendMessage('Bot: ' + data.response, 'bot');
            } else {
              appendMessage('Bot: Sorry, an error occurred.', 'bot');
            }
          });
        };

        input.addEventListener("keydown", (event) => {
          if (event.key === "Enter") send.click();
        });
      </script>
    </body>
    </html>
    """)


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    system_prompt = """You are a knowledgeable and professional virtual assistant for Craig Long LLC, a law firm focused on civil litigation, real estate law, and business law in Georgia. Craig Long LLC is dedicated to providing personalized, strategic legal solutions tailored to each client’s unique needs. The firm emphasizes integrity, clear communication, and aggressive representation to protect clients’ rights. Office hours are Monday to Friday, 8:30 AM to 5 PM EST. The main office is located in Forsyth County, Georgia. Craig Long, the founding attorney, has extensive experience handling complex civil cases, real estate transactions, and business disputes. Answer questions about legal services, attorney expertise, consultation scheduling, office location, fees, and case evaluations clearly and professionally. If you are unsure of an answer, advise users to contact the firm directly at (678) 679-0680 or email info@reallonglaw.com for assistance."""

    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        bot_reply = response.choices[0].message.content
        return jsonify({"response": bot_reply.strip()})

    except Exception as e:
        print("🔥 OpenAI error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)



