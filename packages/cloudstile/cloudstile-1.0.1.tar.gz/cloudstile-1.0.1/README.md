# `⛅` CloudStile
 An unoffical Cloudflare Turnstile library with both asynchronous and synchronous support out of the box. 

 You can find more documention on how to use CloudStile in our [examples](https://github.com/notaussie/cloudstile/tree/main/examples) or our [wiki](https://github.com/notaussie/cloudstile/wiki).

## `📥` Installation
 **CloudStile** is available for download via PyPI, to install it simply do:
 ```shell
 pip install cloudstile
 ```

## `🎭` Example

Here are some *basic* examples of how to validate a user's turnstile token.

> Note: These examples expect the user's IP to be transparent, if you're using something like Cloudflare's proxy then you'll need to access the corresponding header for your use-case.

### `🍷` Quart *(Asynchronous)*

```python
from quart import Quart, request, jsonify
from cloudstile import AsyncTurnstile

app = Quart(__name__)
turnstile = AsyncTurnstile(token="...")

@app.route("/submit", methods=["POST"])
async def submit():

    body = await request.form

    response = await turnstile.validate(
        body.get("cf-turnstile-response", "..."),
        request.remote_addr,
    )

    return jsonify(response.dict()) # <- Response is a pydantic object

```

### `🏃‍♀️` FastAPI *(Asynchronous)*

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from cloudstile import AsyncTurnstile

app = FastAPI()
turnstile = AsyncTurnstile(token="...")

@app.post("/submit")
async def submit(request: Request):

    body = await request.form()

    response = await turnstile.validate(
        body.get("cf-turnstile-response", "..."),
        request.client.host,
    )

    return JSONResponse(response.dict()) # <- Response is a pydantic object

```


### `🦥` Flask *(Synchronous)*

```python
from flask import Flask, request, jsonify
from cloudstile import SyncTurnstile

app = Flask(__name__)
turnstile = SyncTurnstile(token="...")

@app.route("/submit", methods=["POST"])
def submit():

    body = request.form

    response = turnstile.validate(
        body.get("cf-turnstile-response", "..."),
        request.remote_addr,
    )

    return jsonify(response.dict()) # <- Response is a pydantic object

```