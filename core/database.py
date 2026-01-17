from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional, List
import uuid

# --- Database Models ---

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    skills: str  # JSON string or comma-separated
    experience: str
    education: str

class Job(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str
    description: str
    company: str
    requirements: str

class Application(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    job_id: str = Field(foreign_key="job.id")
    user_id: str = Field(foreign_key="user.id")
    score: float

# --- Database Setup ---

DATABASE_URL = "sqlite:///./hackthebias.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# --- User Operations ---

def add_user(user: User) -> User:
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def get_user(user_id: str) -> Optional[User]:
    with Session(engine) as session:
        return session.get(User, user_id)

def get_all_users() -> List[User]:
    with Session(engine) as session:
        return session.exec(select(User)).all()

# --- Job Operations ---

def add_job(job: Job) -> Job:
    with Session(engine) as session:
        session.add(job)
        session.commit()
        session.refresh(job)
        return job

def get_job(job_id: str) -> Optional[Job]:
    with Session(engine) as session:
        return session.get(Job, job_id)

def get_all_jobs() -> List[Job]:
    with Session(engine) as session:
        return session.exec(select(Job)).all()

def search_jobs(query: str) -> List[Job]:
    with Session(engine) as session:
        statement = select(Job).where(
            (Job.title.contains(query)) | 
            (Job.company.contains(query)) |
            (Job.description.contains(query))
        )
        return session.exec(statement).all()

# --- Application Operations ---

def add_application(application: Application) -> Application:
    with Session(engine) as session:
        session.add(application)
        session.commit()
        session.refresh(application)
        return application

def get_application(application_id: str) -> Optional[Application]:
    with Session(engine) as session:
        return session.get(Application, application_id)

def get_applications_for_job(job_id: str) -> List[Application]:
    with Session(engine) as session:
        statement = select(Application).where(Application.job_id == job_id)
        return session.exec(statement).all()

def get_applications_for_user(user_id: str) -> List[Application]:
    with Session(engine) as session:
        statement = select(Application).where(Application.user_id == user_id)
        return session.exec(statement).all()

# --- Seed Sample Data ---

def seed_sample_jobs():
    """Insert sample job data into the database."""
    sample_jobs = [
        Job(
            title="Software Engineer",
            company="Google",
            description="Build and maintain scalable software systems. Work on distributed systems and cloud infrastructure.",
            requirements="Python, Java, Distributed Systems, 3+ years experience"
        ),
        Job(
            title="Data Scientist",
            company="Meta",
            description="Analyze large datasets to derive insights. Build ML models for recommendation systems.",
            requirements="Python, SQL, Machine Learning, Statistics, 2+ years experience"
        ),
        Job(
            title="Machine Learning Engineer",
            company="OpenAI",
            description="Develop and deploy ML models at scale. Research and implement new algorithms.",
            requirements="Python, PyTorch, TensorFlow, Deep Learning, 3+ years experience"
        ),
        Job(
            title="Backend Developer",
            company="Amazon",
            description="Design and implement RESTful APIs. Work with microservices architecture.",
            requirements="Python, Node.js, AWS, Docker, Kubernetes, 2+ years experience"
        ),
        Job(
            title="Frontend Developer",
            company="Netflix",
            description="Build responsive web applications. Optimize for performance and user experience.",
            requirements="JavaScript, React, TypeScript, CSS, 2+ years experience"
        ),
        Job(
            title="DevOps Engineer",
            company="Microsoft",
            description="Manage CI/CD pipelines. Automate infrastructure and deployment processes.",
            requirements="AWS, Azure, Terraform, Docker, Kubernetes, 3+ years experience"
        ),
        Job(
            title="Product Manager",
            company="Stripe",
            description="Define product roadmap. Work with engineering and design teams to deliver features.",
            requirements="Product Management, Agile, Technical Background, 4+ years experience"
        ),
        Job(
            title="Full Stack Developer",
            company="Shopify",
            description="Build end-to-end features. Work on both frontend and backend systems.",
            requirements="React, Node.js, PostgreSQL, GraphQL, 3+ years experience"
        )
    ]
    
    with Session(engine) as session:
        for job in sample_jobs:
            session.add(job)
        session.commit()
    
    print(f"Inserted {len(sample_jobs)} sample jobs.")

def seed_test_user():
    """Insert a test user into the database."""
    test_user = User(
        id="test-user-001",
        skills="Python, FastAPI, PyTorch, TensorFlow, AWS, Docker, React, Node.js, PostgreSQL, Machine Learning",
        experience="Engineered a context-aware pipeline using LangChain and Gemini reducing maintenance time by 25%. Developed PyTorch inference microservices using FastAPI achieving latency under 100ms. Architected full-stack platform with React and Python microservices reducing latency by 40%.",
        education="University of Calgary, Bachelor of Science in Computer Science"
    )
    
    with Session(engine) as session:
        # Check if user already exists
        existing = session.get(User, "test-user-001")
        if not existing:
            session.add(test_user)
            session.commit()
            print("Inserted test user: test-user-001")
        else:
            print("Test user already exists.")