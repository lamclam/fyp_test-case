# test-case

This is the source code of the test case checking system

## Get started

### Requirnment

- **[Python 3](https://www.python.org/downloads/)** for api server
- **[Node.js LTS version](https://nodejs.org/en/download)** for frontend

### How to run

First, create a [python virtual environment](https://docs.python.org/3/library/venv.html) in the `test-case-api` folder and enter the python virtual environment

```text
cd test-case-api
python -m venv .venv

# if you are using CMD
.venv\Scripts\activate.bat

# if you are using Powershel (Visual Studio Code default terminal)
.\.venv\Scripts\Activate.ps1
```

Install the requirnment library

```text
pip install -r requirements.txt
```

When finished, you can run the api server

```text
python main.py
```

The server will running on `http://127.0.0.1:5000`

Next, install the requirnment nodejs modules

```text
cd test-case-frontend

# using npm
npm install

# using yarn
yarn install
```

When finished, you can start the frontend of the system

```test
# using npm
npm run dev

# using yarn
yarn dev
```

The frontend is started in [http://127.0.0.1:3000](http://localhost:3000)
