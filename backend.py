from io import TextIOWrapper
import requests
from bs4 import BeautifulSoup
import re
import PyPDF2


def extract_skills_from_pdf(pdf_path):
    # Function to extract skills from text
    def extract_skills(requirements):
        skills = [skill.strip() for skill in requirements.split(',')]
        return skills

    # Function to extract computer science-related skills
    def extract_cs_skills(skills):
        cs_keywords = [
        # Programming Languages
        "Python", "Java", "JavaScript", "C++", "C#", "R", "SQL", "Scala", "Perl", "Ruby", "Go", "Swift", "Kotlin", 
        "HTML/CSS", "PHP", "MATLAB", "Julia",

        # Web Development
        "HTML", "CSS", "JavaScript", "React", "Angular", "Vue.js", "Node.js", "Express.js", "Django", "Flask", "Ruby on Rails",

        # Database Management
        "SQL", "MySQL", "PostgreSQL", "SQLite", "MongoDB", "Redis", "Oracle", "Microsoft SQL Server", "Amazon RDS", "Firebase",

        # Cloud Computing
        "Amazon Web Services (AWS)", "Microsoft Azure", "Google Cloud Platform (GCP)", "Serverless Computing", 
        "Docker", "Kubernetes", "Continuous Integration/Continuous Deployment (CI/CD)",

        # Data Science & Machine Learning
        "Machine Learning", "Deep Learning", "Natural Language Processing (NLP)", "Computer Vision", "Data Mining", 
        "Data Visualization", "Big Data", "Artificial Intelligence (AI)", "TensorFlow", "PyTorch", "Scikit-learn", 
        "Keras", "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn", "Plotly", "Tableau", "Power BI", "RapidMiner", 
        "Apache Spark", "Hadoop", "Apache Kafka", "Apache Flink",

        # Software Development
        "Software Development Life Cycle (SDLC)", "Agile Methodology", "Scrum", "Kanban", "Git", "GitHub", "GitLab", 
        "Bitbucket", "Jira", "Trello", "Confluence", "Code Review", "Unit Testing", "Integration Testing", 
        "Test-Driven Development (TDD)", "Continuous Integration (CI)", "Continuous Deployment (CD)",

        # Mathematics & Statistics
        "Linear Algebra", "Calculus", "Probability", "Statistics", "Discrete Mathematics",

        # Operating Systems
        "Linux", "Unix", "Windows", "macOS",

        # Networking
        "TCP/IP", "DNS", "HTTP/HTTPS", "SSL/TLS", "Firewalls", "Routers", "Switches", "Load Balancers","Shell", "Shell scripts"

        # Security
        "Cybersecurity", "Encryption", "Identity and Access Management (IAM)", "Vulnerability Assessment", 
        "Penetration Testing", "Security Operations Center (SOC)", "Intrusion Detection System (IDS)", 
        "Intrusion Prevention System (IPS)", "Security Information and Event Management (SIEM)", 
        "Threat Intelligence",

        # Education
        "Bachelor's Degree", "Bachelors", "Bachelor", "BS", "MS", "PhD", "Master's Degree", "PhD", "Computer Science", "Data Science", "Information Technology",
        "Software Engineering", "Statistics", "Mathematics", "Engineering", "Computer Engineering", "Information Systems",
        "Quantitative Analysis", "Applied Mathematics", "Computer Information Systems", "Computer Programming"
    ]

        cs_skills = set()
        
        for skill in skills:
            for keyword in cs_keywords:
                if re.search(r'\b{}\b'.format(re.escape(keyword)), skill, re.IGNORECASE):
                    cs_skills.add(keyword)
        
        return cs_skills

    # Initialize a list to store extracted skills
    extracted_skills = []

    # Open the PDF file
    pdfFileObj = open(pdf_path, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    pageObj = pdfReader.pages[0]
    text=(pageObj.extract_text()).replace("\n", " ")
            # Find the requirements section based on the presence of certain keywords
            # Extract skills from requirements text
    print(text)
    skills = extract_skills(text)
    # Add extracted skills to the list
    extracted_skills.extend(skills)

    # Extract computer science-related skills
    cs_skills = extract_cs_skills(extracted_skills)
    return cs_skills


def get_urls(url):
    # URL of the job posting

    # Send a GET request to the page
    response = requests.get(url)
    job_links = []
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the element containing the job requirements
    # (You will need to inspect the HTML structure of the page to do this correctly)
    job_requirements = soup.find_all('a', href=re.compile(r'myworkdayjobs'))
    pattern = r'href="([^"]*)"'
    # Find all matches
    for i in job_requirements:
        matches = re.findall(pattern, str(i))
        job_links.append(matches[0])
    job_requirements = soup.find_all('a', href=re.compile(r'boards.greenhouse.io'))
    pattern = r'href="([^"]*)"'
    # Find all matches
    for i in job_requirements:
        matches = re.findall(pattern, str(i))
        job_links.append(matches[0])
    return job_links


def extract_skills_from_url(url):
    # Function to extract skills from text
    def extract_skills(requirements):
        requirements_set = re.split(r'\n', requirements)
        skills_set = []
        for i in requirements_set:
            # Split the text whenever "and", "or", or comma is encountered
            skills = re.split(r'\s+and\s+|\s+or\s+|\s*,\s*', i)
            # Filter out empty strings and strip extra spaces
            skills = [skill.strip() for skill in skills if skill.strip()]
            skills_set.append(skills)
        return skills_set

    # Function to extract computer science-related skills
    def extract_cs_skills(skills):
        cs_keywords = [
            # List of computer science-related keywords
            "Python", "Java", "JavaScript", "C++", "C#", "R", "SQL", "Scala", "Perl", "Ruby", "Go", "Swift", "Kotlin", 
            "HTML/CSS", "PHP", "MATLAB", "Julia", "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express.js",
            "Django", "Flask", "Ruby on Rails", "MySQL", "PostgreSQL", "SQLite", "MongoDB", "Redis", "Oracle",
            "Microsoft SQL Server", "Amazon RDS", "Firebase", "Amazon Web Services (AWS)", "Microsoft Azure", 
            "Google Cloud Platform (GCP)", "Serverless Computing", "Docker", "Kubernetes", 
            "Continuous Integration/Continuous Deployment (CI/CD)", "Machine Learning", "Deep Learning", 
            "Natural Language Processing (NLP)", "Computer Vision", "Data Mining", "Data Visualization", 
            "Big Data", "Artificial Intelligence (AI)", "TensorFlow", "PyTorch", "Scikit-learn", "Keras", 
            "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn", "Plotly", "Tableau", "Power BI", "RapidMiner", 
            "Apache Spark", "Hadoop", "Apache Kafka", "Apache Flink", "Software Development Life Cycle (SDLC)", 
            "Agile Methodology", "Scrum", "Kanban", "Git", "GitHub", "GitLab", "Bitbucket", "Jira", "Trello", 
            "Confluence", "Code Review", "Unit Testing", "Integration Testing", "Test-Driven Development (TDD)", 
            "Continuous Integration (CI)", "Continuous Deployment (CD)", "Linear Algebra", "Calculus", "Probability", 
            "Statistics", "Discrete Mathematics", "Linux", "Unix", "Windows", "macOS", "TCP/IP", "DNS", 
            "HTTP/HTTPS", "SSL/TLS", "Firewalls", "Routers", "Switches", "Load Balancers", "Shell", 
            "Shell scripts", "Cybersecurity", "Encryption", "Identity and Access Management (IAM)", 
            "Vulnerability Assessment", "Penetration Testing", "Security Operations Center (SOC)", 
            "Intrusion Detection System (IDS)", "Intrusion Prevention System (IPS)", 
            "Security Information and Event Management (SIEM)", "Threat Intelligence", "Bachelor's Degree", 
            "Bachelors", "BS", "MS", "PhD", "Master's Degree", "PhD", "Computer Science", "Data Science", 
            "Information Technology", "Software Engineering", "Statistics", "Mathematics", "Engineering", 
            "Computer Engineering", "Information Systems", "Quantitative Analysis", "Applied Mathematics", 
            "Computer Information Systems", "Computer Programming"
        ]

        cs_skills = []

        for line in skills:
            line_skills = []
            for skill in line:
                for keyword in cs_keywords:
                    if re.search(r'\b{}\b'.format(re.escape(keyword)), skill, re.IGNORECASE):
                        line_skills.append(keyword)
            if line_skills != []:
                cs_skills.append(line_skills)
        return cs_skills

    # Send GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the requirements section based on the <h3> tag
    requirements_section = soup.find("h3", string=re.compile(r"(requirements|qualifications|You should apply if you|What you will bring|What you need to know)", re.IGNORECASE))
    extracted_skills = []
    if requirements_section:
        # Extract text from requirements section
        requirements_text = requirements_section.find_next("ul").get_text()
        # Extract skills from requirements text
        skills = extract_skills(requirements_text)
        for skill in skills:
            extracted_skills.append(skill)
    else:
        print("Requirements section not found.")

    # Extract computer science-related skills
    cs_skills = extract_cs_skills(extracted_skills)
    return cs_skills