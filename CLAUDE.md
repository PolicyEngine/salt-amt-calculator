# CLAUDE.md - Guidelines for Salt-AMT Calculator

## Environment & Commands
- Run app: `streamlit run app.py`
- Docker: `docker build -t salt-amt-calculator .` and `docker run -p 8080:8080 salt-amt-calculator`
- Format code: `black .`

## Code Style Guidelines
- Use Black for code formatting
- Import order: stdlib → third-party → first-party
- Variable naming: snake_case for variables and functions
- Type annotations: Prefer adding them, especially for function parameters/returns
- Error handling: Use try/except with specific messages for user feedback
- Documentation: Use docstrings and inline comments for complex logic
- Use f-strings for string formatting
- Follow PEP 8 spacing conventions
- For complex operations, prefer pandas and numpy vectorized operations

## Project Architecture
- Streamlit-based UI with two main calculators:
  - Personal calculator: Household-level tax impact simulation
  - Nationwide impacts: Distribution and budget analysis
- Data is stored in CSV files in `/data` directories
- Analysis notebooks in `/notebooks` directories