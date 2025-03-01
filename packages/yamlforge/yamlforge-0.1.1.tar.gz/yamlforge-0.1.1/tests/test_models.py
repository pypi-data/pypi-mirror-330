from pathlib import Path
import pytest
from yamlforge.main import generate_models

@pytest.fixture
def cleanup():
    yield
    for file in Path("db/models").glob("*.py"):
        file.unlink()
    Path("db/models").rmdir()
    Path("db").rmdir()

def test_generate_simple_model(cleanup):
    config = {
        "User": {
            "fields": [
                {"name": "id", "type": "int", "primary_key": True},
                {"name": "name", "type": "str"},
                {"name": "email", "type": "str"}
            ]
        }
    }
    
    generate_models(config)
    
    assert Path("db/models/user.py").exists()
    with open("db/models/user.py") as f:
        content = f.read()
        assert "class User(SQLModel, table=True):" in content
        assert "id: int = Field(default=None, primary_key=True)" in content
        assert "name: str = None" in content
        assert "email: str = None" in content

def test_generate_model_with_relationships(cleanup):
    config = {
        "Post": {
            "fields": [
                {"name": "id", "type": "int", "primary_key": True},
                {"name": "title", "type": "str"}
            ],
            "relationships": [
                {
                    "type": "OneToMany",
                    "model": "Comment",
                    "back_populates": "comments"
                }
            ]
        }
    }
    
    generate_models(config)
    
    assert Path("db/models/post.py").exists()
    with open("db/models/post.py") as f:
        content = f.read()
        assert "class Post(SQLModel, table=True):" in content
        assert "comments: list['Comment'] = Relationship(back_populates='comments')" in content

def test_generate_model_with_many_to_many(cleanup):
    config = {
        "Student": {
            "fields": [
                {"name": "id", "type": "int", "primary_key": True}
            ],
            "relationships": [
                {
                    "type": "ManyToMany",
                    "model": "Course",
                    "back_populates": "courses",
                    "association_table": "StudentCourseLink"
                }
            ]
        }
    }
    
    generate_models(config)
    
    assert Path("db/models/student.py").exists()
    with open("db/models/student.py") as f:
        content = f.read()
        assert "class Student(SQLModel, table=True):" in content
        assert "courses: list['Course'] = Relationship(link_model=StudentCourseLink)" in content