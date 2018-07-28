## Configuration

Change `users` dict variable as you need
You will probably want to change `ALLOWED_EXTENSIONS` too.

## Usage

Install requirements

```
$ pip install -r requirements.txt
```

Start the server

```
python -u app.py
```

Download file

```
curl -O http://user1:1234@localhost:8000/files/example.txt
```

Upload file

```
curl -F 'file=@test_file.txt' http://user1:1234@localhost:8000/files/
```
