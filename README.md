# HR AI Workflow

An AI-powered HR workflow application for processing and analyzing candidate CVs.

## Features

- Upload and process candidate CVs
- Extract information using AI
- Score candidates against job requirements
- Store candidate data in a database

## Tech Stack

- **Frontend**: React, TypeScript, Vite
- **Backend**: FastAPI, Python
- **Database**: MySQL
- **AI**: OpenAI API

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.9+ (for local development)
- OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/hr-ai-workflow.git
   cd hr-ai-workflow
   ```

2. Create a `.env` file with your OpenAI API key:
   ```bash
   echo "OPENAI_KEY=your_openai_api_key_here" > .env
   ```

3. Start the application with Docker Compose:
   ```bash
   docker compose up --build
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend

1. Create a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the backend:
   ```bash
   uvicorn main:app --reload
   ```

#### Frontend

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Run the frontend:
   ```bash
   npm run dev
   ```

## Code Standards

This project follows strict code standards enforced by linting tools. See [CODING_STANDARDS.md](CODING_STANDARDS.md) for details.

### Frontend Linting

```bash
cd frontend
npm run lint        # Check for issues
npm run lint:fix    # Fix issues automatically
npm run format      # Format code with Prettier
```

### Backend Linting

```bash
cd backend
./lint.sh           # Run all linting tools
black .             # Format code
isort .             # Sort imports
flake8 .            # Check for code quality issues
mypy src            # Type checking
```

### Pre-commit Hooks

Install pre-commit hooks to automatically run linting before each commit:

```bash
pip install pre-commit
pre-commit install
```

## Testing

### Backend Tests

```bash
cd backend
pytest
pytest --cov=src    # With coverage report
```

### Frontend Tests

```bash
cd frontend
npm test
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
