# Mode WLE (WhiteLabel Embed) URL Signer

This is a small application, meant to be deployed in a docker container, that will sign Mode WLE URLs for you
It's based on the documentation here: https://mode.com/help/articles/white-label-embeds/#sign-the-embed-url-wle-only

# Deployment

This app can be run from your machine in a dev mode, or deployed as a container. Container is probably most straightforward.

3 environment variables must be set, it'll bomb out without them:
1. `MODE_ACCESS_KEY` (get this from Mode settings -> Sharing & Embedding -> Embedding)
2. `MODE_ACCESS_SECRET` (same)
3. `MODE_TEAM` (this is your URL slug in Mode, like `https://app.mode.com/organizations/<myteam>/` )
4. `TOKEN` (a cheap security measure in case you can't use something sophisticated like Google IAP)

## Building the container

```
docker build -t mode-wle-signer .
```

## Running the container
```
docker run -it \
  -e MODE_TEAM=honeycombio \
  -e MODE_ACCESS_KEY=modekey \
  -e MODE_ACCESS_SECRET=modesecret \
  -e TOKEN=foo \
  -e OTEL_SERVICE_NAME=mode_wle_signer \
  -e HONEYCOMB_API_KEY=honeykey \
  -p 8080:8080 \
  mode-wle-signer
```

# Local Development mode

Make sure you have Python 3.11 and Poetry installed

Install dependencies:
```
poetry install
```

Write out a .flaskenv file for local development
```
cat > .flaskenv << EOF
MODE_TEAM=honeycombio
MODE_ACCESS_KEY=mykey
MODE_ACCESS_SECRET=mysecret
TOKEN=foo
```

Run the dev server with OTel enabled
```
OTEL_SERVICE_NAME=mode_wle_signer \
  HONEYCOMB_API_KEY=myhoneycombkey \
  HONEYCOMB_ENABLE_LOCAL_VISUALIZATIONS=true \
  DEBUG=true  \
  poetry run opentelemetry-instrument flask run --debug
```

Local testing:
```
# try this in your browser
http://127.0.0.1:5000/report/account?iframe=true&token=foo&account_id=abc123
```


Update dependencies
```
poetry update
```

# TODO

* This isn't a smart thing to run open to everyone, you probably want this behind an authenticating proxy like Google IAP
* Document how to run this in Google Cloud Run or equivalent
* Linting and testing, some kind of CI
