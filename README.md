# spug-20260922-flask
Flask examples for SPUG meetup on 2026-09-22



## Running with Docker

From the repository root, build the image with the Dockerfile in `src/docker`:

```bash
docker build -f src/docker/Dockerfile -t spug-flask .
```

Run the API and publish it on port 5000:

```bash
docker run --rm -p 5000:5000 spug-flask
```

Visit http://localhost:5000/docs for the interactive API documentation.
