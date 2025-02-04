FROM python:3.12-slim

# Install GNU Parallel for benchmark runs
RUN apt-get update && apt-get install -y parallel

# Install Poetry
RUN pip3 install poetry==2.0.1

# Set the working directory to the root of your project
WORKDIR /ucc

# Copy the entire project into the container
COPY . /ucc

ENV POETRY_NO_INTERACTION=1 \
POETRY_VIRTUALENVS_IN_PROJECT=1 \
POETRY_VIRTUALENVS_CREATE=true \
POETRY_CACHE_DIR=/tmp/poetry_cache

# Install (rarely changing) dependencies only using Poetry to leverage docker caching
RUN --mount=type=cache,target=/tmp/poetry_cache poetry install --no-root

# Install the `ucc` package itself
RUN poetry install

# Ensure the virtual environment is properly activated
ENV VIRTUAL_ENV=/ucc/.venv
ENV PATH="/ucc/.venv/bin:$PATH"

# Show installed package details
RUN poetry run pip show ucc

