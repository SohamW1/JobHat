from io import TextIOWrapper
import requests
from bs4 import BeautifulSoup
import re
import PyPDF2
import pandas as pd

data = {
    'Company': [],
    'Role': [],
    'Link': []
}

df = pd.DataFrame(data)  # Define df as a global DataFrame

cs_keywords = keywords = [
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
    "Computer Information Systems", "Computer Programming", "Problem Solving", "Analytical Skills", 
    "Critical Thinking", "Creativity", "Leadership", "Communication Skills", "Teamwork", 
    "Time Management", "Attention to Detail", "Organizational Skills", "Adaptability", "Flexibility", 
    "Interpersonal Skills", "Presentation Skills", "Project Management", "Customer Service", 
    "Client Management", "Sales", "Marketing", "Finance", "Accounting", "Human Resources", 
    "Operations", "Supply Chain", "Logistics", "Quality Assurance", "Quality Control", 
    "Healthcare", "Pharmaceutical", "Biotechnology", "Medical Devices", "Telecommunications", 
    "Retail", "E-commerce", "Hospitality", "Travel", "Tourism", "Education", "Nonprofit", 
    "Government", "Public Sector", "Military", "Legal", "Consulting", "Startups", "Venture Capital", 
    "Investment Banking", "Private Equity", "Real Estate", "Architecture", "Construction", 
    "Manufacturing", "Automotive", "Aerospace", "Energy", "Renewable Energy", "Oil and Gas", 
    "Mining", "Forestry", "Environmental", "Sustainability", "Urban Planning", "Architecture", 
    "Interior Design", "Graphic Design", "User Experience (UX)", "User Interface (UI)", 
    "Web Design", "Product Design", "Industrial Design", "Fashion Design", "Animation", 
    "Film", "Television", "Music", "Performing Arts", "Visual Arts", "Photography", 
    "Video Production", "Content Writing", "Copywriting", "Editing", "Proofreading", 
    "Technical Writing", "Creative Writing", "Journalism", "Public Relations", "Social Media", 
    "Digital Marketing", "Search Engine Optimization (SEO)", "Search Engine Marketing (SEM)", 
    "Email Marketing", "Content Marketing", "Affiliate Marketing", "Influencer Marketing", 
    "Web Development", "Front-End Development", "Back-End Development", "Full-Stack Development", 
    "Mobile Development", "iOS Development", "Android Development", "Game Development", 
    "Software Engineering", "Embedded Systems", "Internet of Things (IoT)", "Blockchain", 
    "Cryptocurrency", "Decentralized Finance (DeFi)", "Smart Contracts", "Cybersecurity", 
    "Network Security", "Information Security", "Data Privacy", "Cloud Security", 
    "Identity Management", "Risk Management", "Compliance", "Regulatory Affairs", 
    "Legal Compliance", "Financial Compliance", "Environmental Compliance", 
    "Quality Management", "Process Improvement", "Bachelor"
]


def get_scores(url, pdf_file):
    links = get_urls(url)
    extracted_skills = extract_skills_from_pdf(pdf_file)
    keyword_match_score = {}
    scores = []
    for link in links:
        skills = extract_skills_from_url(link)
        n = len(skills)
        if n == 0:
            scores.append(0)  # If no skills are extracted, assign score 0
        else:
            score = 0
            for line in skills:
                for skill in line:
                    if skill in extracted_skills:
                        score += 1
                        break
            if score / n > 0.60:
                scores.append(score / n)  # Append the normalized score
            else:
                scores.append(0)  # If score is below threshold, assign score 0

    # Add the 'Score' column to the DataFrame
    df['Score'] = scores
    sorted_df = df[df['Score'] > 0].sort_values(by='Score', ascending=False)
    
    def format_score(score):
        return str(round(100 * score, 2)) + "%"

    # Apply the function to the 'Score' column
    sorted_df['Score'] = sorted_df['Score'].apply(format_score)

    return sorted_df


def get_urls(url):
    # URL of the job posting
    if url == "https://github.com/SimplifyJobs/Summer2024-Internships":
        skiprows = 10
    else:
        skiprows = 8

    # Send a GET request to the page
    response = requests.get(url)
    job_links = []
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the element containing the job requirements
    job_rows = soup.find_all('tr')[skiprows:]

    for job in job_rows:
        # Check if job closed
        if job.find('td').find('a') == None:
            continue
        # Extract company name
        company = job.find('td').find('a').text

        # Extract role
        role = job.find_all('td')[1].text

        # Extract links. Assuming you are interested in the 'Application/Link' column which could have multiple links
        links_td = job.find_all('td')[3]
        # link = [a['href'] for a in links_td.find_all('a', href=True)][0].split("?")[0]
        try:
            link = [a['href'] for a in links_td.find_all('a', href=True)][0].split("?")[0]
        except IndexError:
            # locked posting
            continue

        if re.search(r'myworkdayjobs', link) or re.search(r'boards.greenhouse.io', link):
            # Append data to DataFrame
            try:
                df.loc[len(df)] = [company, role, link]
            except ValueError:
                print([company, role, link])
                print(len(df))
                continue

    return df["Link"]


def extract_skills_from_pdf(pdf_path):
    # Function to extract skills from text
    def extract_skills(requirements):
        skills = [skill.strip() for skill in requirements.split(',')]
        return skills

    # Function to extract computer science-related skills
    def extract_cs_skills(skills):
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
    text = ""
    for pageObj in pdfReader.pages:
        text += (pageObj.extract_text()).replace("\n", " ")

    # Find the requirements section based on the presence of certain keywords
    # Extract skills from requirements text
    skills = extract_skills(text)
    # Add extracted skills to the list
    extracted_skills.extend(skills)

    # Extract computer science-related skills
    cs_skills = extract_cs_skills(extracted_skills)
    return cs_skills


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

    tag_list = ["h3", "strong", "p", "b", "h4", "u"]
    i = 0
    requirements_section = None
    while (requirements_section == None) & (i < len(tag_list)):
        requirements_section = soup.find(tag_list[i], string=re.compile(r"(requirements|qualifications|You should apply if you|What you will bring|What you need to know|Your Expertise|You should apply if you|What we need to see|What you’ll need|To be successful in this role, you should possess)", re.IGNORECASE))
        i+=1
    extracted_skills = []
    if requirements_section:
        # Extract text from requirements section
        next_req = requirements_section.find_next("ul")
        if next_req != None:
            requirements_text = next_req.get_text()
            # Extract skills from requirements text
            skills = extract_skills(requirements_text)
            for skill in skills:
                extracted_skills.append(skill)
    # else:
        # print("Requirements section not found.")

    # Extract computer science-related skills
    cs_skills = extract_cs_skills(extracted_skills)
    return cs_skills
