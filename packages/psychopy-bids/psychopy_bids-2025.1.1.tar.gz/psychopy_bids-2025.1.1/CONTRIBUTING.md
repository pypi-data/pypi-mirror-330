# Contributing

Contributions are welcome and greatly appreciated! Every bit helps, and credit will always be given.

## Types of Contributions

### Report Bugs

If you find a bug, please report it. When doing so, include:

- Your operating system name and version.
- Details about your Python version and any other relevant package versions.
- Any specifics about your local setup that could aid troubleshooting.
- Step-by-step instructions to reproduce the issue.

### Fix Bugs

Check the [GitLab Issues](https://gitlab.com/psygraz/psychopy-bids/issues) for bugs. Issues tagged with `bug` and `help wanted` are open to anyone interested in resolving them.

### Implement Features

If you’d like to add new functionality, look for issues tagged with `enhancement` and `help wanted`. These are features the community has expressed interest in, and you’re welcome to tackle them.

### Write Documentation

Good documentation is vital! Contributions are welcome in all forms, including:

- Improving the official documentation.
- Adding or enhancing docstrings in the code.
- Writing tutorials, blog posts, or articles about using `psychopy-bids`.

### Submit Feedback

If you have ideas for new features or general feedback:

- Explain your idea in detail, including how it would work.
- Keep the scope narrow to make implementation easier.
- Remember, this is a community-driven project, and contributions are voluntary.

---

## Get Started!

Ready to contribute? Follow these steps to set up `psychopy-bids` for local development:

### 1. Clone the Repository

Clone the repository to your local machine:

   ```bash
   git clone https://gitlab.com/psygraz/psychopy-bids.git
   cd psychopy-bids
   ```

### 2. Set Up a Virtual Environment (Optional but Recommended)

For an isolated development environment, create a virtual environment:

- **Linux/macOS**:

   ```bash
   python3 -m venv env
   source .venv/bin/activate
   ```

- **Windows**:

   ```bash
   python -m venv env
   .venv\Scripts\activate
   ```

### 3. Install Dependencies

Install the package in editable mode:

   ```bash
   pip install -e .[dev]
   ```

### 4. Create a Branch

Use Git (or similar) to create a branch for your work:

   ```bash
   git checkout -b name-of-your-bugfix-or-feature
   ```

Replace `name-of-your-bugfix-or-feature` with something descriptive, like `fix-typo` or `add-new-feature`.

---

### 5. Make Your Changes

Edit the code to fix bugs, implement features, or improve documentation. Ensure that:

- Your code follows the project’s style guide (e.g., PEP 8 for Python).
- You’ve added or updated tests to cover your changes.
- Documentation is updated, if applicable.

---

### 6. Test Your Changes

Before submitting your changes, ensure everything works as expected.

**Run Tests**  
Use `pytest` to test your changes:

```bash
pytest tests/
```

**Check and Apply Code Formatting**  
To maintain code consistency and ensure proper formatting, use the `python_auto_format.py` script located in the `tests` folder:

```bash
python tests/python_auto_format.py
```

This script will:

- Install required pip packages.
- Sort imports using `isort`.
- Format code using `black`.
- Fix remaining PEP8 issues using `autopep8`.
- Check code with `bandit`, `codespell`, `flake8` and `pylint`.

**Manually Verify Formatting**  
If you prefer to run the tools manually, use the following commands:

```bash
isort psychopy_bids/
black psychopy_bids/
autopep8 --in-place --recursive --max-line-length 99 psychopy_bids/
```
---

### 7. Commit and Push Your Changes

**Stage Your Changes**  
Add the modified files to the staging area:

```bash
git add .
```

**Commit Your Changes**  
Write a descriptive commit message:

```bash
git commit -m "Fix: Correct typo in README"
```

**Push Your Changes**  
Push your branch to your fork:

```bash
git push origin name-of-your-bugfix-or-feature
```

### 8. Submit a Merge Request

- Go to the [original repository](https://gitlab.com/psygraz/psychopy-bids/merge_requests) on GitLab.
- Click **New Merge Request** and select the branch from your fork.
- Provide:
   - A concise title for the merge request.
   - A detailed description of your changes.
   - References to any related issues.
- Submit the merge request!

## Merge Request Guidelines

To ensure smooth collaboration, make sure your merge request:

- Includes tests for any new functionality or bug fixes.
- Updates relevant documentation (if necessary).

## Code of Conduct

This project is released with a Code of Conduct. By contributing, you agree to abide by its terms, ensuring a respectful and inclusive community.