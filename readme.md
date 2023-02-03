API's using fastAPI
==============================

## Project Structure
```
├── config.py
├── load_csv.py
├── main.py
├── models.py
├── readme.md
├── repositories.py
├── requirements.txt
├── schemas.py
└── utils.py
```
- [x] SQL Alchemy, connecting POSTGRES, and automatically creating tables at beginning
- [x] Type checking with `Pydantic` Schemas.

## Getting started

1. Create a Virtual Environment using virtualenv
```zsh
python -m virtualenv env
env/scripts/activate
```

2. Install dependencies
```zsh
pip install -r requirements.txt
```

3. Run the main file to start the server at localhost
```zsh
python main.py
```
Open your browser at http://127.0.0.1:8000/report
You will see the JSON response as:

```json
{"report_id": 4146956711014268672}
```
it will return a random store_id

### **Interactive api docs**

Now go to http://127.0.0.1:8000/docs.

You will see the automatic interactive API documentation (provided by [Swagger UI](https://github.com/swagger-api/swagger-ui)).

