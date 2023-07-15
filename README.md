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
docker run -e MODE_TEAM=honeycombio -e MODE_ACCESS_KEY=mykey -e MODE_ACCESS_SECRET=mysecret -e TOKEN=foo mode-wle-signer
```

# Developing

Make sure you have Python 3.11 and Poetry installed

Install dependencies:
```
poetry install
```

Run the dev server
```
MODE_TEAM=honeycombio \
  MODE_ACCESS_KEY=mykey \
  MODE_ACCESS_SECRET=mysecret \
  TOKEN=foo \
  poetry run flask run --debug
```

Update dependencies
```
poetry update
```

Local testing:
```
# try this in your browser
http://127.0.0.1:5000/report/account?iframe=true&token=foo&account_id=abc123
```

# TODO

* This isn't a smart thing to run open to everyone, you probably want this behind an authenticating proxy like Google IAP
* Document how to run this in Google Cloud Run or equivalent
* Linting and testing, some kind of CI
