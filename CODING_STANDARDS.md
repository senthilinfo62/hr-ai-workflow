# Coding Standards

This document outlines the coding standards and best practices for the HR AI Workflow project.

## General Guidelines

- Write clean, readable, and maintainable code
- Follow the DRY (Don't Repeat Yourself) principle
- Use meaningful variable and function names
- Add comments for complex logic, but prefer self-documenting code
- Keep functions small and focused on a single responsibility
- Write tests for all new functionality

## Frontend (JavaScript/TypeScript)

### Code Formatting

- Use ESLint and Prettier for code formatting and linting
- Maximum line length: 100 characters
- Use 2 spaces for indentation
- Use single quotes for strings
- Use semicolons at the end of statements
- Use trailing commas in multi-line objects and arrays

### React Best Practices

- Use functional components with hooks instead of class components
- Keep components small and focused on a single responsibility
- Use TypeScript for type safety
- Use React Router for navigation
- Use proper error handling and loading states
- Follow the React component lifecycle

### TypeScript Guidelines

- Use TypeScript interfaces for defining props and state
- Use proper type annotations for variables, functions, and return types
- Avoid using `any` type when possible
- Use union types for variables that can have multiple types

## Backend (Python)

### Code Formatting

- Use Black for code formatting
- Use isort for import sorting
- Use Flake8 for code linting
- Use mypy for type checking
- Maximum line length: 100 characters
- Use 4 spaces for indentation

### Python Best Practices

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Use docstrings for functions, classes, and modules
- Use proper error handling with try/except blocks
- Use context managers for resource management
- Use proper logging instead of print statements

### FastAPI Best Practices

- Use Pydantic models for request and response validation
- Use dependency injection for shared resources
- Use proper status codes for responses
- Use proper error handling with HTTPException
- Use proper documentation with docstrings and OpenAPI

## Database

- Use SQLAlchemy for database operations
- Use migrations for database schema changes
- Use proper indexing for frequently queried columns
- Use foreign keys for relationships
- Use transactions for operations that need to be atomic

## Testing

- Write unit tests for all new functionality
- Use pytest for Python testing
- Use Jest for JavaScript/TypeScript testing
- Aim for high test coverage
- Write integration tests for critical paths

## Git Workflow

- Use feature branches for new features
- Use pull requests for code review
- Write meaningful commit messages
- Keep commits small and focused
- Rebase feature branches on main before merging

## Pre-commit Hooks

The project uses pre-commit hooks to enforce code quality standards. To install pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

This will run the following checks before each commit:
- Black (Python code formatting)
- isort (Python import sorting)
- Flake8 (Python code linting)
- mypy (Python type checking)
- ESLint (JavaScript/TypeScript code linting)
- Prettier (JavaScript/TypeScript code formatting)
- Various file checks (trailing whitespace, YAML validation, etc.)
