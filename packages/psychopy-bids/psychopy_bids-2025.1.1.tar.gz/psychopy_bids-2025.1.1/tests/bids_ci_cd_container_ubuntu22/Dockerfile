FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install required dependencies
RUN apt-get update && \
    apt-get install -y curl git xvfb unzip

# Install Deno
RUN curl -fsSL https://deno.land/install.sh | sh && \
    echo 'export DENO_INSTALL="$HOME/.deno"' >> ~/.bashrc && \
    echo 'export PATH="$DENO_INSTALL/bin:$PATH"' >> ~/.bashrc && \
    ln -s $HOME/.deno/bin/deno /usr/local/bin/deno

# Clone the repository and set permissions
RUN git clone https://github.com/bids-standard/bids-validator.git /home/gitlab-runner/bids-validator && \
    chmod +x /home/gitlab-runner/bids-validator/local-run

RUN /home/gitlab-runner/bids-validator/local-run || true

# Set the PATH explicitly
ENV DENO_INSTALL="/root/.deno"
ENV PATH="$DENO_INSTALL/bin:$PATH"

RUN curl -O https://raw.githubusercontent.com/wieluk/psychopy_linux_installer/main/psychopy_linux_installer && \
    chmod +x psychopy_linux_installer && \
    for version in 3.10 3.9 3.8; do \
        ./psychopy_linux_installer --python-version=$version \
                                   --psychopy-version=latest \
                                   --install-dir=/home/gitlab-runner/psychopy_$version \
                                   --additional-packages=pytest,pytest-cov,seedir \
                                   --no-versioned-install-dir \
                                   --non-interactive \
                                   --disable-path \
                                   --disable-shortcut \
                                   -f; \
    done && \           
    rm psychopy_linux_installer && \
    rm -rf /usr/local/psychopy_python/wx_wheels && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
