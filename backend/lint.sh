#!/bin/bash

# Run isort to sort imports
echo "Running isort..."
isort .

# Run black to format code
echo "Running black..."
black .

# Run flake8 to check for code quality issues
echo "Running flake8..."
flake8 .

# Run mypy for type checking
echo "Running mypy..."
mypy src

echo "Linting complete!"
