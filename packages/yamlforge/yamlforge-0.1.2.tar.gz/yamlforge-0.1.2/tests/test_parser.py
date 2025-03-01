import pytest
from pathlib import Path
from yamlforge.parser import load_yaml_config
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture
def path():
    return Path("models_config.yaml")

def test_load_yaml_config_with_models(path):
    config = load_yaml_config(path)

    assert isinstance(config, dict)
    assert all(key in config for key in ["User", "Post", "Role"])

    assert "User" in config
    user_fields = config["User"]["fields"]
    user_relationships = config["User"]["relationships"]

    assert len(user_fields) == 4
    assert user_fields[0]["name"] == "id"
    assert user_fields[0]["type"] == "int"
    assert user_fields[0]["primary_key"] is True
    assert user_fields[1]["name"] == "username"
    assert user_fields[1]["type"] == "str"
    assert user_fields[1]["required"] is True
    assert user_fields[2]["name"] == "email"
    assert user_fields[2]["type"] == "str"
    assert user_fields[2]["required"] is True
    assert user_fields[3]["name"] == "hashed_password"
    assert user_fields[3]["type"] == "str"
    assert user_fields[3]["required"] is True

    assert len(user_relationships) == 2
    assert user_relationships[0]["type"] == "OneToMany"
    assert user_relationships[0]["model"] == "Post"
    assert user_relationships[0]["back_populates"] == "author"
    assert user_relationships[1]["type"] == "ManyToMany"
    assert user_relationships[1]["model"] == "Role"
    assert user_relationships[1]["association_table"] == "user_role"

    assert "Post" in config
    post_fields = config["Post"]["fields"]
    post_relationships = config["Post"]["relationships"]

    assert len(post_fields) == 4
    assert post_fields[0]["name"] == "id"
    assert post_fields[0]["type"] == "int"
    assert post_fields[0]["primary_key"] is True
    assert post_fields[1]["name"] == "title"
    assert post_fields[1]["type"] == "str"
    assert post_fields[1]["required"] is True
    assert post_fields[2]["name"] == "content"
    assert post_fields[2]["type"] == "str"
    assert post_fields[3]["name"] == "author_id"
    assert post_fields[3]["type"] == "int"
    assert post_fields[3]["foreign_key"] == "User.id"

    assert len(post_relationships) == 1
    assert post_relationships[0]["type"] == "ManyToOne"
    assert post_relationships[0]["model"] == "User"
    assert post_relationships[0]["back_populates"] == "posts"

    assert "Role" in config
    role_fields = config["Role"]["fields"]

    assert len(role_fields) == 2
    assert role_fields[0]["name"] == "id"
    assert role_fields[0]["type"] == "int"
    assert role_fields[0]["primary_key"] is True
    assert role_fields[1]["name"] == "name"
    assert role_fields[1]["type"] == "str"
    assert role_fields[1]["required"] is True

def test_load_yaml_config_empty():
    content = """
    models:
    """
    path = Path("empty_config.yaml")
    path.write_text(content)
    config = load_yaml_config(str(path))
    path.unlink()
    assert config is None

def test_load_yaml_config_no_models():
    content = """
    other_key: value
    """
    path = Path("no_models_config.yaml")
    path.write_text(content)
    config = load_yaml_config(str(path))
    path.unlink()
    assert isinstance(config, dict)
    assert len(config) == 0