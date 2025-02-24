FROM python:3.12-slim

# Install GNU Parallel for benchmark runs
RUN apt-get update && apt-get install -y parallel

# Install Poetry
RUN pip3 install poetry==2.0.1

# Set the working directory to the root of your project
WORKDIR /ucc

# Copy the entire project into the container
COPY . /ucc

# Store the virtual env in /venv to avoid clashing with directory
# mapped as part of benchmark github action
ENV POETRY_NO_INTERACTION=true \
POETRY_VIRTUALENVS_IN_PROJECT=false \
POETRY_VIRTUALENVS_CREATE=true \
POETRY_CACHE_DIR=/tmp/poetry_cache \
POETRY_VIRTUALENVS_PATH=/venv

# Install (rarely changing) dependencies only using Poetry to leverage docker caching
RUN --mount=type=cache,target=/tmp/poetry_cache poetry install --no-root

# Install the `ucc` package itself
RUN poetry install

# Show installed package details
RUN poetry run pip show ucc

