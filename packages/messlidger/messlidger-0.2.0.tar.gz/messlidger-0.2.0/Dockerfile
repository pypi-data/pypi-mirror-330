# install dependencies
FROM codeberg.org/slidge/slidge-builder AS builder
ENV UV_PROJECT_ENVIRONMENT=/venv/
COPY uv.lock pyproject.toml /build/
RUN uv sync --frozen --no-install-project --no-dev

# ci container
FROM builder AS woodpecker-messlidger
# In CI we copy /venv to .venv, then update it for the whole workflow.
ENV PATH=".venv/bin:$PATH"
RUN uv sync --frozen --no-install-project --all-extras

# main container
FROM codeberg.org/slidge/slidge-base AS messlidger
COPY --from=builder /venv /venv
COPY ./messlidger /venv/lib/python/site-packages/legacy_module

# dev container
FROM codeberg.org/slidge/slidge-dev AS dev
COPY --from=builder /venv /venv
