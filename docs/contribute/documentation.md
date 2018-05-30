# Contributing: core documentation

The main documentation is written in markdown and then generated with [mkdocs](https://www.mkdocs.org/).

Install python packages
```bash
sudo pip install mkdocs mkdocs-material markdown-include pygments
```

Update the documentation in the `docs` folder placed in the root of the project.
Then, run dev server locally to check the result
```bash
mkdocs serve
```

When ready, send a pull request in the **dev** branch.
