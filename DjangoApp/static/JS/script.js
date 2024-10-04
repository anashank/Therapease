document.getElementById('send-button').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() !== "") {
        // Display user message
        addMessage(userInput, 'user-message');
        document.getElementById('user-input').value = '';

        // Simulate bot response
        setTimeout(() => {
            const botResponse = getBotResponse(userInput);
            addMessage(botResponse, 'bot-message');
        }, 1000);
    }
});

function addMessage(text, className) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', className);
    messageDiv.innerText = text;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}

function getBotResponse(userInput) {
    // Simple responses
    const responses = {
        'hi': 'Hello! How can I assist you today?',
        'how are you?': 'I am just a bot, but thanks for asking!',
        'bye': 'Goodbye! Have a great day!',
    };

    return responses[userInput.toLowerCase()] || "I'm sorry, I don't understand.";
}
