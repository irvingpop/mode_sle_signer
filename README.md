# Mode WLE (WhiteLabel Embed) URL Signer

This is a small application, meant to be deployed in a docker container, that will sign Mode WLE URLs for you
It's based on the documentation here: https://mode.com/help/articles/white-label-embeds/#sign-the-embed-url-wle-only

# Deployment

This app can be run from your machine in a dev mode, or deployed as a container. Container is probably most straightforward.

3 environment variables must be set, it'll bomb out without them:
1. `MODE_ACCESS_KEY` (get this from Mode settings -> Sharing & Embedding -> Embedding)
2. `MODE_ACCESS_SECRET` (same)
3. `MODE_TEAM` (this is your URL slug in Mode, like `https://app.mode.com/organizations/<myteam>/` )

## Building the container

```
docker build -t mode-wle-signer .
```

## Running the container

docker run -e MODE_TEAM=honeycombio -e MODE_ACCESS_KEY=mykey -e MODE_ACCESS_SECRET=mysecret mode-wle-signer


# Developing

Make sure you have Python 3.9 and Poetry installed

Install dependencies:
```
poetry install
```

Run the dev server
```
FLASK_ENV=development MODE_TEAM=honeycombio MODE_ACCESS_KEY=mykey MODE_ACCESS_SECRET=mysecret poetry run flask run
```

Update dependencies
```
poetry update
```

# TODO

* there's a hard-coded report ID in there. Make a configurable list of report IDs and params.
* This isn't a smart thing to run open to everyone, you probably want this behind an authenticating proxy like Google IAP
* Document how to run this in Google Cloud Run or equivalent
* Linting and testing, some kind of CI
