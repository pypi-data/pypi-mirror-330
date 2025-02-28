# install dependencies
FROM codeberg.org/slidge/slidge-builder AS builder

COPY uv.lock pyproject.toml /build/
RUN uv export --no-dev > requirements.txt
RUN uv venv /venv/
RUN uv pip install --requirement requirements.txt

# ci container
FROM builder AS woodpecker-matteridge
# In CI we copy /venv to .venv, then update it for the whole workflow.
ENV PATH=".venv/bin:$PATH"
RUN uv export > requirements.txt
RUN uv pip install --requirement requirements.txt

# main container
FROM codeberg.org/slidge/slidge-base AS matteridge
COPY --from=builder /venv /venv
COPY ./matteridge /venv/lib/python/site-packages/legacy_module

# dev container
FROM codeberg.org/slidge/slidge-dev AS dev

COPY --from=builder /venv /venv
