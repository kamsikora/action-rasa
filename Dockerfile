# Extend the official Rasa SDK image
FROM rasa/rasa-sdk:1.10.0

WORKDIR /app
# Change back to root user to install dependencies
USER root

ADD ./actions /app/actions/
# To install system dependencies
#RUN apt-get update -qq && \
#    apt-get install -y <NAME_OF_REQUIRED_PACKAGE> && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# To install packages from PyPI
#RUN pip install --no-cache-dir <A_REQUIRED_PACKAGE_ON_PYPI>

# Switch back to non-root to run code
USER 1001
