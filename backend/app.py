from flask import Flask, request, jsonify
import os
import openai
from PyPDF2 import PdfReader
import io
import pymysql
import json

app = Flask(__name__)

# Configure CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")

# Database connection
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='admin@123',
        database='hr_ai',
        cursorclass=pymysql.cursors.DictCursor
    )

def extract_text_from_pdf(content):
    reader = PdfReader(io.BytesIO(content))
    return "\n".join([page.extract_text() for page in reader.pages])

def extract_with_ai(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"""Extract following details from CV:
        - Educational qualification (100 words max)
        - Job history (100 words max)
        - Technical skills (bulleted list)
        - Phone number
        - City
        - Birthdate

        CV: {text}""",
        max_tokens=1000,
        temperature=0.3
    )
    return parse_ai_response(response.choices[0].text)

def parse_ai_response(content):
    result = {
        "education": "",
        "job_history": "",
        "skills": [],
        "phone": "",
        "city": "",
        "birthdate": ""
    }

    # Simple parsing logic
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
            result["education"] += line + " "
        elif current_section == "job_history":
            result["job_history"] += line + " "
        elif current_section == "skills" and line.startswith("-"):
            result["skills"].append(line[1:].strip())

    return result

def evaluate_candidate(data):
    profile = "Web developer with PHP, Python, JavaScript experience in Northern Italy"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"""Profile wanted: {profile}
        Give score 1-10 and considerations for the following candidate:

        {str(data)}""",
        max_tokens=500,
        temperature=0.3
    )
    return parse_evaluation(response.choices[0].text)

def parse_evaluation(content):
    # Simple parsing to extract score
    score = 0
    for line in content.split("\n"):
        if "score" in line.lower():
            # Try to find a number in the line
            import re
            numbers = re.findall(r'\d+', line)
            if numbers:
                score = int(numbers[0])
                break

    return {
        "score": score
    }

@app.route("/api/cv/candidates", methods=["POST"])
def create_candidate():
    name = request.form.get("name")
    email = request.form.get("email")
    cv_file = request.files.get("cv")

    if not name or not email or not cv_file:
        return jsonify({"error": "Missing required fields"}), 400

    # Read PDF content
    pdf_content = cv_file.read()

    # Extract text from PDF
    text = extract_text_from_pdf(pdf_content)

    # Process with AI
    extracted_data = extract_with_ai(text)
    evaluation = evaluate_candidate(extracted_data)

    # Combine results
    result = {
        **extracted_data,
        **evaluation,
        "name": name,
        "email": email
    }

    # Save to database
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO candidates
            (name, email, phone, city, birthdate, education, job_history, skills, score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                name,
                email,
                result.get('phone', ''),
                result.get('city', ''),
                result.get('birthdate', ''),
                result.get('education', ''),
                result.get('job_history', ''),
                json.dumps(result.get('skills', [])),
                result.get('score', 0)
            ))
            conn.commit()
            result['id'] = cursor.lastrowid
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

    return jsonify(result)

@app.route("/api/cv/candidates", methods=["GET"])
def get_candidates():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM candidates")
            candidates = cursor.fetchall()

            # Convert JSON strings back to lists
            for candidate in candidates:
                if candidate['skills'] and isinstance(candidate['skills'], str):
                    candidate['skills'] = json.loads(candidate['skills'])
                else:
                    candidate['skills'] = []

        return jsonify(candidates)
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        conn.close()

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Welcome to HR AI Workflow API"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
