# Therapease

A Django web app that matches users with therapists based on questionnaire compatibility.

Users and therapists both complete a set of questions. Therapease scores their responses against each other and surfaces the best match — similar to how compatibility-based apps work, applied to mental health care.

## How it works

1. Sign up as either a **User** (seeking therapy) or a **Therapist**
2. Complete the matching questionnaire
3. The matching algorithm compares your responses against all profiles on the other side, scoring each pair by percentage alignment
4. Returns your best match with a compatibility score

## Tech stack

| Layer | Tech |
|---|---|
| Backend | Django, Python |
| Database | SQLite |
| Frontend | Django Templates, JavaScript, CSS |
| Auth | Django built-in auth |

## Setup

```bash
cd DjangoApp
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open [http://localhost:8000](http://localhost:8000).
