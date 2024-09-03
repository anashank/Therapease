import os
import django

# Set the environment variable to your settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoApp.settings')

# Setup Django
django.setup()


from searchapp.models import Article

articles = [
    {
        "title": "Signs Your Past Trauma is Triggered",
        "content": "This article explains why triggers happen, signs of being triggered, and how to heal from trauma.",
        "url": "https://psych2go.net/signs-your-past-trauma-is-triggered/",
        "thumbnail_url": "https://psych2go.net/wp-content/uploads/2023/02/pexels-daniel-reche-3601097-1536x1024.jpg"
    },
    {
        "title": "6 Things Your Anxiety is Trying to Tell You",
        "content": "This article explores six messages that anxiety might be trying to convey about your inner needs and mental state.",
        "url": "https://psych2go.net/6-things-your-anxiety-is-trying-to-tell-you/",
        "thumbnail_url": "https://psych2go.net/wp-content/uploads/2022/08/iStock-1293042761_wide.jpg"
    },
    {
        "title": "4 Things to Do to Stop Overthinking Mistakes",
        "content": "This article discusses four practices recommended by therapists to help manage and overcome rumination and overthinking.",
        "url": "https://psych2go.net/4-things-to-do-to-stop-overthinking-mistakes/",
        "thumbnail_url": "https://psych2go.net/wp-content/uploads/2022/07/pexels-brett-sayles-1194196-1536x1024.jpg"
    },
    {
        "title": "Why You're Always Tired (and How to Fix It)",
        "content": "This article identifies common reasons for constant tiredness and provides tips on how to improve energy levels.",
        "url": "https://psych2go.net/why-youre-always-tired-and-how-to-fix-it/",
        "thumbnail_url": "https://psych2go.net/wp-content/uploads/2023/02/pexels-pixabay-206396-1536x1022.jpg"
    },
    {
        "title": "5 Signs You Have Chronic Depression",
        "content": "This article outlines five key signs of persistent depressive disorder (PDD), also known as chronic depression.",
        "url": "https://psych2go.net/5-signs-you-have-chronic-depression/",
        "thumbnail_url": "https://psych2go.net/wp-content/uploads/2022/07/people-geef56d67a_1920-1536x1022.jpg"
    },
    {
        "title": "Don't Ignore Your Emotions… Here's Why",
        "content": "This article discusses the dangers of ignoring emotions like anger, loneliness, jealousy, and shame, highlighting their impact on mental health and the importance of addressing them to prevent anxiety and other issues.",
        "url": "https://psych2go.net/dont-ignore-your-emotions-heres-why/",
        "thumbnail_url": "https://psych2go.net/wp-content/uploads/2023/02/pexels-pixabay-207983-1024x721.jpg"
    },
]


for article in articles:
    Article.objects.create(**article)
