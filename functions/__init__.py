# functions/__init__.py

from .workload_distribution import get_workload_distribution
from .project_workflow import get_project_workflow
from .flowchart_generation import generate_flowchart
from .project_structure_generation import generate_project_structure
from .project_naming import suggest_project_names
from .utils import extract_text    
from .project_files_structure import generate_project_files_structure
from config import API_KEY, BASE_URL, MODEL_NAME
from openai import OpenAI

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

