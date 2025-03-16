from datetime import datetime
from models import Project

def generate_project_id(village_code, project_type):
    """Generate unique project ID combining village code, project type and year"""
    year = datetime.now().year
    project_type_code = project_type[:3].upper()
    return f"{village_code}-{project_type_code}-{year}"

def check_duplicates(village_code, project_type, location):
    """Check for potential duplicate projects"""
    similar_projects = Project.query.filter(
        Project.village_code == village_code,
        Project.project_type == project_type,
        Project.location.like(f"%{location}%"),
        Project.status.in_(['planned', 'ongoing'])
    ).all()
    
    return similar_projects
