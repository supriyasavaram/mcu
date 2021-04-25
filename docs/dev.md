## TO LOAD JSON FILES
FILE FORMAT: 
```[{
    "pk": 1,
    "model": DATABASE TABLE NAME,
    "fields": {
        "title": "Iron Man",
        "synopsis": "After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil.",
        "year": "(2008)",
        "runtime": "126 min"
    }
},...]```

- Add to /fixtures/filename.json
- Run python manage.py loaddata filename.json