from yamlforge.main import generate, generate_schemas, generate_models
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_generate():
    generate()

def test_generate_models():
    generate_models()

def test_generate_schemas():
    generate_schemas()
    