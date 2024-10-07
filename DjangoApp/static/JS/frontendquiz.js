const toggleSwitch = document.querySelector('.light-dark-switch input[type="checkbox"]');
document.querySelector(".start-menu").classList.toggle("visible");

function switchMode(event) {
    if (event.target.checked) {
        document.documentElement.setAttribute('data-theme', 'dark');
        console.log("switched to dark");
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
        console.log("switched to light");
    }
}

toggleSwitch.addEventListener('change', switchMode, false);

var quizButtons = document.querySelectorAll(".quiz-type");
var quizType;

quizButtons.forEach(button => {
    button.addEventListener("click", function () {
        quizType = this.id;
        console.log(quizType);
        saveUserType(quizType);
        questionScreen(quizType);
    });
});

function questionScreen(type) {
    document.querySelector(".start-menu").classList.toggle("visible");
    setSubjectBars(type);
    document.querySelector(".question-screen").classList.toggle("visible");
    getQuiz(type);
}

function setSubjectBars(type) {
    var bars = document.querySelectorAll(".curr-subject");
    bars.forEach(bar => {
        bar.lastElementChild.textContent = type;
        if (type === "Looking for a Therapist?") {
            bar.firstElementChild.firstElementChild.src = "/static/images/icon-eyes.svg";
            bar.firstElementChild.firstElementChild.style.height = '90px';
        } else if (type === "Want to be a Therapist?") {
            bar.firstElementChild.firstElementChild.src = "/static/images/icon-owl.svg";
            bar.firstElementChild.firstElementChild.style.height = '90px';
        }
        bar.style.visibility = "visible";
    });
}

var quizChosen;
var qCount = -1;
var totalQuestions;
var score = 0;
var submit = document.querySelector(".submit-answer");
var increment;

async function getQuiz(type) {
    try {
        const response = await fetch('/static/json/frontend.json');
        const data = await response.json();
        quizChosen = data.quizzes.find(quiz => quiz.title === type);
        if (quizChosen) {
            totalQuestions = quizChosen.questions.length;
            document.querySelector(".question-total").textContent = totalQuestions;
            increment = (1 / totalQuestions) * 100;
            makeQuestions(quizChosen);
        } else {
            console.error('Quiz type not found.');
        }
    } catch (error) {
        console.error('Error fetching quiz data:', error);
    }
}

function makeQuestions(quizChoice) {
    qCount++;
    if (qCount >= totalQuestions - 1) {
        submit.textContent = "See Results";
    } else {
        submit.textContent = "Next Question";
    }
    document.querySelector(".question-number").textContent = (qCount + 1);
    document.querySelector(".progress-bar.done").style.width = `${increment * (qCount + 1)}%`;

    let options = document.querySelectorAll(".option");
    document.querySelector(".question").textContent = quizChoice.questions[qCount].question;

    options.forEach(option => {
        option.classList.remove("selected", "invalid", "correct");
    });

    quizChoice.questions[qCount].options.forEach((option, i) => {
        options[i].innerHTML = `<div class='option-box'>${String.fromCharCode(65 + i)}</div>`;
        options[i].append(option);
    });
}

var options = document.querySelectorAll(".option");

options.forEach(option => {
    option.addEventListener("click", function () {
        options.forEach(opt => {
            opt.classList.remove("selected");
            opt.firstChild.classList.remove("selected-box");
        });
        this.classList.add("selected");
        this.firstChild.classList.add("selected-box");
    });
});

submit.addEventListener("click", function () {
    let selectedBox = document.querySelector(".selected");
    const selectPrompt = document.querySelector(".select-prompt");

    if (submit.textContent === "Next Question") {
        if (selectedBox) {
            const answer = selectedBox.firstChild.innerText;
            const questionText = document.querySelector(".question").textContent;
            saveUserResponse(questionText, answer);
            makeQuestions(quizChosen);
            selectPrompt.style.visibility = "hidden";
        } else {
            selectPrompt.style.visibility = "visible";
        }
        return;
    }

    if (submit.textContent === "See Results") {
        showQuizComplete();
        return;
    }

    if (selectedBox) {
        selectedBox.classList.remove("selected");
        selectedBox.firstChild.classList.remove("selected-box");
        selectPrompt.style.visibility = "hidden";
        makeQuestions(quizChosen);
    }
});

function saveUserResponse(questionText, responseValue) {
    fetch('/save-response/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
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
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ usertype: usertype }),
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
        cookies.forEach(cookie => {
            cookie = cookie.trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}

function showQuizComplete() {
    document.querySelector(".question-screen").classList.toggle("visible");
    document.querySelector(".quiz-complete").classList.toggle("visible");

    const loader = document.getElementById('loader');
    loader.style.display = 'block';

    const fetchDelay = 5000;

    setTimeout(async () => {
        try {
            const response = await fetch('/run-python/');
            const data = await response.json();

            loader.style.display = 'none';

            const matchMessage = document.querySelector(".scored");
            matchMessage.textContent = `You matched with... ${data.output}`;

            const recentMatchResponse = await fetch('/get-recent-match/');
            const recentMatchData = await recentMatchResponse.json();

            if (recentMatchData.recentMatch) {
                displayRecentMatch(recentMatchData.recentMatch);
            } else {
                console.log("No recent match found");
            }

        } catch (error) {
            loader.style.display = 'none';
            console.error('Error:', error);
        }
    }, fetchDelay);
}

function displayRecentMatch(recentMatch) {
    const recentMatchContainer = document.querySelector(".recent-match-container");

    if (!recentMatch) {
        console.log("No recent match data available");
        recentMatchContainer.innerHTML = "No recent matches found";
        recentMatchContainer.style.display = 'block';
        return;
    }

    recentMatchContainer.innerHTML = '';
    const recentMatchElement = document.createElement('div');
    recentMatchElement.classList.add('recent-match-item');
    recentMatchElement.textContent = `You most recently matched with ${recentMatch.matched_with} on ${recentMatch.date}`;
    recentMatchContainer.appendChild(recentMatchElement);

    recentMatchContainer.style.display = 'block';
}

document.querySelector(".restart1").addEventListener("click", function () {
    document.querySelector(".quiz-complete").classList.toggle("visible");
    document.querySelector(".start-menu").classList.toggle("visible");
    document.querySelector(".curr-subject").style.visibility = "hidden";
    document.querySelector(".scored").textContent = `You matched with...`;
    qCount = -1;
    score = 0;
});

document.querySelector(".restart2").addEventListener("click", function () {
    document.querySelector(".quiz-complete").classList.toggle("visible");
    document.querySelector(".start-menu").classList.toggle("visible");
    document.querySelector(".curr-subject").style.visibility = "hidden";
    document.querySelector(".scored").textContent = `You matched with...`;
    qCount = -1;
    score = 0;
});
