# Repository for simplifying my life

Everytime you change a laptop, desktop, or even re-create environment.

You have to go through the pain of setting up shortcuts,etc from scratch.

These scripts simple contain some helper functions to speed up the developer workflow.

# How it works?

It is uses particular command such as `docker` or `git` in combination with `fzf` to make execution of commands more interactive and user-friendly.

# How to use ?

- Ensure the following are installed - `fzf`
- Ensure bash file associated is
- Clone the repository
- Inside you `~/.zshrc` or `~/.bashrc` file

```sh
source path/to/repo/commands/docker.sh
source path/to/repo/commands/git.sh
```

Voila !! You have some nice commanders at your service.

# Supercharged Commands

- [Docker](docs/docker.md)
- [Git](docs/git.md)


# TODO

- [ ] Add more utility functions for kubernetes
- [ ] Allow more options in existing scripts
