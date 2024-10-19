# payments

Payments Microservice

https://payments.buddyapp.link/docs

## Installation

```bash
pip install virtualenv
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Swagger Docs at: http://localhost:8000/docs

## Generate Lambda Function

When using Apple Silicon Chip, some of dependencies used are compiled for C so architecture is important. Lambda function uses x86 or arm architecture. In order to download dependencies that works in lambda function, run this command:

```bash
pip install -r requirements.txt --python-version 3.9 --platform manylinux2014_x86_64 --target layer/python --only-binary=:all:
```

Once that dependencies are located in `layer` folder, run these commands to generate `layer.zip` if new dependencies are installed and `function.zip` which contains `app` dir

```bash
chmod +x zip-lambda.sh
./zip-lambda.sh
```