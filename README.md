# Simple chat

## Description
`Chat` is a simple chat website where different people can
communicate with each other. Anyone can enter the chat or create it 
without the need to register on the site.

## Installation
### Prerequisites
Make sure you have installed all the following prerequisites on your development machine:
- Python 3.6+ (*with `setuptools`,  `wheel` and `virtualenv` packages*)
- Docker
- `make` utility (*Windows only*)

## Set up project
- **Clone repository**
```bash
git clone https://github.com/antkrit/chat.git
```

- **Move into project root folder:**
```bash
cd chat
```

- **Create and activate virtual environment:**

*Linux:*
```bash
virtualenv venv
source venv/bin/activate
```

*Windows:*
```bash
virtualenv venv
venv\Scripts\activate
```

- **Install dependencies:**

Development requirements (*includes production requirements*)
```bash
python -m pip install -e .[dev]
```

Production requirements
(*if you are only interested in launching the application,
these requirements are enough for you*)
```bash
python -m pip install -e .
```

- **Set the following environment variables:**
```bash
POSTGRES_DB=<db_name>
POSTGRES_USER=<username>
POSTGRES_PASSWORD=<password>
POSTGRES_HOST=<host or 'localhost'>
POSTGRES_PORT=<port>
```

- **Run database on docker:**
```bash
make db-run
make db-upgrade
make db-populate # optional
```

## Run application
### Configuration
All configuration (`.yaml`) files are stored in [config](config) folder.

After `<variable name>:` use:
- `<variable value>` to set variable values
- `!include <filename>.yaml` if you want to include variable values from another `.yaml` file
- `!ENV ${ENV_NAME}` if you want to read a variable from the environment

### Run development server
```bash
python app.py
```
Web app will be available locally `http://127.0.0.1:8080/`.

## Documentation
You can view sphinx documentation of the project with [this](documentation/_build/html/index.html) file

## Additional utilities

**All configs for utilities are in [setup.cfg](setup.cfg) file.**
**All tests are stored in [tests](tests) folder**

- Run tests with coverage report:
```bash
make test
```

- Code analysis:
```bash
flake8 src
```

- Alembic revision:
```bash
make db-revision msg="some message"
```
