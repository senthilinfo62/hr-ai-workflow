# backend/src/infrastructure/ai/cv_processor.py
import io
import json
import logging
import os

import openai
import pymysql
from fastapi import HTTPException
from PyPDF2 import PdfReader

# Set up logging
logger = logging.getLogger(__name__)


class CVProcessor:
    def __init__(self):
        # Set OpenAI API key
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            logger.error("OpenAI API key not found")
            raise ValueError("OpenAI API key not found in environment variables")
        openai.api_key = openai_api_key

        # Database connection parameters
        self.db_config = {
            "host": os.getenv("DB_HOST", "db"),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", "admin@123"),
            "database": os.getenv("DB_NAME", "hr_ai"),
            "cursorclass": pymysql.cursors.DictCursor,
        }

    async def process_cv(self, name: str, email: str, pdf_content: bytes) -> dict:
        try:
            # Extract text from PDF
            text = self._extract_text_from_pdf(pdf_content)

            if not text.strip():
                raise ValueError(
                    "Could not extract text from PDF. The file may be corrupted or empty."
                )

            # Extract structured data
            extracted_data = await self._extract_with_ai(text)

            # Evaluate candidate
            evaluation = await self._evaluate_candidate(extracted_data)

            # Combine results
            result = {**extracted_data, **evaluation, "name": name, "email": email}

            # Save to database
            await self._save_candidate_to_db(result)

            return result
        except Exception as e:
            logger.error(f"Error processing CV: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing CV: {str(e)}")

    async def get_all_candidates(self) -> list:
        """Get all candidates from the database"""
        try:
            conn = pymysql.connect(
                host=self.db_config["host"],
                user=self.db_config["user"],
                password=self.db_config["password"],
                database=self.db_config["database"],
                cursorclass=self.db_config["cursorclass"],
            )
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM candidates")
                    candidates = cursor.fetchall()

                    # Convert JSON strings back to lists
                    for candidate in candidates:
                        if candidate["skills"] and isinstance(candidate["skills"], str):
                            candidate["skills"] = json.loads(candidate["skills"])
                        else:
                            candidate["skills"] = []

                return candidates
            finally:
                conn.close()
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def _save_candidate_to_db(self, data: dict) -> None:
        """Save candidate data to the database"""
        try:
            conn = pymysql.connect(
                host=self.db_config["host"],
                user=self.db_config["user"],
                password=self.db_config["password"],
                database=self.db_config["database"],
                cursorclass=self.db_config["cursorclass"],
            )
            try:
                with conn.cursor() as cursor:
                    sql = """
                    INSERT INTO candidates
                    (name, email, phone, city, birthdate, education, job_history, skills, score)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(
                        sql,
                        (
                            data.get("name", ""),
                            data.get("email", ""),
                            data.get("phone", ""),
                            data.get("city", ""),
                            data.get("birthdate", ""),
                            data.get("education", ""),
                            data.get("job_history", ""),
                            json.dumps(data.get("skills", [])),
                            data.get("score", 0),
                        ),
                    )
                    conn.commit()

                    # Get the ID of the inserted row
                    data["id"] = cursor.lastrowid
            finally:
                conn.close()
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def _extract_text_from_pdf(self, content: bytes) -> str:
        reader = PdfReader(io.BytesIO(content))
        return "\n".join([page.extract_text() for page in reader.pages])

    async def _extract_with_ai(self, text: str) -> dict:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that extracts information from CVs.",
                },
                {
                    "role": "user",
                    "content": f"""Extract following details from CV:
                - Educational qualification (100 words max)
                - Job history (100 words max)
                - Technical skills (bulleted list)
                - Phone number
                - City
                - Birthdate

                CV: {text}""",
                },
            ],
            max_tokens=1000,
            temperature=0.3,
        )
        return self._parse_ai_response(response.choices[0].message["content"])

    def _parse_ai_response(self, content: str) -> dict:
        result: dict = {
            "education": "",
            "job_history": "",
            "skills": [],
            "phone": "",
            "city": "",
            "birthdate": "",
        }

        # Simple parsing logic - in a real app, this would be more robust
        lines = content.split("\n")
        current_section = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if "education" in line.lower() or "qualification" in line.lower():
                current_section = "education"
                continue
            elif "job history" in line.lower() or "work experience" in line.lower():
                current_section = "job_history"
                continue
            elif "skills" in line.lower() or "technical skills" in line.lower():
                current_section = "skills"
                continue
            elif "phone" in line.lower():
                parts = line.split(":")
                if len(parts) > 1:
                    result["phone"] = parts[1].strip()
                continue
            elif "city" in line.lower():
                parts = line.split(":")
                if len(parts) > 1:
                    result["city"] = parts[1].strip()
                continue
            elif "birth" in line.lower():
                parts = line.split(":")
                if len(parts) > 1:
                    result["birthdate"] = parts[1].strip()
                continue

            if current_section == "education":
                result["education"] = result["education"] + line + " "
            elif current_section == "job_history":
                result["job_history"] = result["job_history"] + line + " "
            elif current_section == "skills" and line.startswith("-"):
                if isinstance(result["skills"], list):
                    result["skills"].append(line[1:].strip())

        return result

    async def _evaluate_candidate(self, data: dict) -> dict:
        profile = "Web developer with PHP, Python, JavaScript experience in Northern Italy"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that evaluates job candidates.",
                },
                {
                    "role": "user",
                    "content": f"""Profile wanted: {profile}
                Give score 1-10 and considerations for the following candidate:

                {str(data)}""",
                },
            ],
            max_tokens=500,
            temperature=0.3,
        )
        return self._parse_evaluation(response.choices[0].message["content"])

    def _parse_evaluation(self, content: str) -> dict:
        # Simple parsing to extract score
        score = 0
        for line in content.split("\n"):
            if "score" in line.lower():
                # Try to find a number in the line
                import re

                numbers = re.findall(r"\d+", line)
                if numbers:
                    score = int(numbers[0])
                    break

        return {"score": score}
