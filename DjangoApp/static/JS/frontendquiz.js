const toggleSwitch = document.querySelector('.light-dark-switch input[type="checkbox"]');
document.querySelector(".start-menu").classList.toggle("visible")


function switchMode(event) {
    if (event.target.checked) {
        document.documentElement.setAttribute('data-theme', 'dark');
        console.log("switched to dark");
    }
    else {
        document.documentElement.setAttribute('data-theme', 'light');
        console.log("switched to light");
    }
}

toggleSwitch.addEventListener('change', switchMode, false);

var quizButtons = document.querySelectorAll(".quiz-type");
var quizType;

for (var i = 0; i < quizButtons.length; i++) {
    quizButtons[i].addEventListener("click", function () {
        quizType = this.id;
        //save user type to user profile database based on selection
        console.log(quizType)
        saveUserType(quizType)
        questionScreen(quizType);
    })
}

function questionScreen(type) {
    document.querySelector(".start-menu").classList.toggle("visible")
    setSubjectBars(type)
    document.querySelector(".question-screen").classList.toggle("visible")

    //retrieve quiz data based on selection
    getQuiz(type);
}

function setSubjectBars(type) {
    var bars = document.querySelectorAll(".curr-subject");
    for (let bar of bars) {
        bar.lastElementChild.innerHTML = type
        if (type == "Looking for a Therapist?") {
            bar.firstElementChild.firstElementChild.src = "/static/images/icon-eyes.svg"
            bar.firstElementChild.firstElementChild.style.height = '90px';
        }
        else if (type == "Want to be a Therapist?") {
            bar.firstElementChild.firstElementChild.src = "/static/images/icon-owl.svg"
        }
        else if (type == "Find an Article!") {
            bar.firstElementChild.firstElementChild.src = "/static/images/icon-js.svg"
        }
        else {
            bar.firstElementChild.firstElementChild.src = "/static/images/icon-accessibility.svg"
        }
        bar.style.visibility = "visible"
    }
}


var quizChosen;
var qCount = -1;
var totalQuestions;
var score = 0;
var submit = document.querySelector(".submit-answer");
var increment;

// fetch returns a Promise, .json() returns a *2nd* Promise, therefore 2 .thens
async function getQuiz(type) {
    const response = await fetch('/static/json/frontend.json');
    const data = await response.json();
    for (const quiz of data.quizzes) {
        if (quiz.title == type) {
            quizChosen = quiz;
            totalQuestions = quizChosen.questions.length;
            document.querySelector(".question-total").textContent = totalQuestions
            increment = (1 / totalQuestions) * 100;
        }
    }
    makeQuestions(quizChosen)
}

// quiz flow:
// populate fields -> submit event handler validates (wrong - show wrong, do nothing. right - show right, move on)

function makeQuestions(quizChoice) {
    qCount++;
    if (qCount >= (totalQuestions - 1)) {
        submit.textContent = "See Results"

    }
    else {
        submit.textContent = "Next Question";
    }
    document.querySelector(".question-number").textContent = (qCount + 1);
    document.querySelector(".progress-bar.done").style.width = (increment * (qCount + 1)).toString() + "%";

    let options = document.querySelectorAll(".option");

    document.querySelector(".question").textContent = quizChoice.questions[qCount].question;

    for (let option of options) {
        option.classList.remove("selected")
        option.classList.remove("invalid")
        option.classList.remove("correct")
    }

    for (let i = 0; i < options.length; i++) {
        switch (i) {
            case 0: options[i].innerHTML = "<div class='option-box'>A</div>"
                break;
            case 1: options[i].innerHTML = "<div class='option-box'>B</div>"
                break;

        }
        options[i].append(quizChoice.questions[qCount].options[i])
    }
}

var options = document.querySelectorAll(".option");

for (let i = 0; i < options.length; i++) {
    options[i].addEventListener("click", function () {
        for (option of options) {
            option.classList.remove("selected")
            option.firstChild.classList.remove("selected-box")
        }
        options[i].classList.add("selected")
        options[i].firstChild.classList.add("selected-box")
    })
}

submit.addEventListener("click", function () {
    let selectedBox, answerText;

    if (submit.textContent == "Next Question") {
        for (let i = 0; i < options.length; i++){
            if(options[i].classList.contains('selected')){
                console.log(options[i].firstChild.innerText);
                answer = options[i].firstChild.innerText
                questionText = document.querySelector(".question").textContent
                saveUserResponse(questionText, answer);
            } 
        }
        
        makeQuestions(quizChosen);
        return;
    }

    if (submit.textContent == "See Results") {
        showQuizComplete();
        return;
    }
    if (selectedBox = document.querySelector(".selected")) {


        // remove selection letter from string
        //answerText = selectedBox.textContent.slice(1, selectedBox.textContent.length);

        // once submit is pressed, is a selected box exists, remove it's selected classes
        selectedBox.classList.remove("selected")
        selectedBox.firstChild.classList.remove("selected-box")
        //document.querySelector(".select-prompt").style.visibility = "visible"
        makeQuestions(quizChosen);
    }
    return;
})


function saveUserResponse(questionText, responseValue) {
    fetch('/save-response/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // Get CSRF token
        },
        body: JSON.stringify({ question: questionText, response: responseValue }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function saveUserType(usertype) {
    fetch('/save-type/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // Get CSRF token
        },
        body: JSON.stringify({ usertype: usertype}),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// function validate(selected) {
//     let question = quizChosen.questions[qCount];
//     return (selected === selected)
// }

function showQuizComplete() {
    document.querySelector(".question-screen").classList.toggle("visible")
    document.querySelector(".quiz-complete").classList.toggle("visible")
    //display output of compare_responses() function in utils.py
    const loader = document.getElementById('loader');

    // Show the loading circle
    loader.style.display = 'block';

    const fetchDelay = 5000;

    setTimeout(() => {
        fetch('/run-python/')
            .then(response => response.json())
            .then(data => {
                loader.style.display = 'none';
                // Display the output in the console
                // Optionally, display the output in the HTML
                document.getElementById('output').innerText = data.output;
            })
            .catch(error => {
                loader.style.display = 'none';
                console.error('Error:', error)}
                );
    }, fetchDelay);


    // document.querySelector(".final-score").textContent = score
    // document.querySelector(".complete-question-total").textContent = totalQuestions
}

document.querySelector(".restart").addEventListener("click", function () {
    document.querySelector(".quiz-complete").classList.toggle("visible")
    document.querySelector(".start-menu").classList.toggle("visible")
    document.querySelector(".curr-subject").style.visibility = "hidden"
    document.getElementById('output').innerText = "";
    qCount = -1
    score = 0
})
