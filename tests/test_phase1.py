"""
Phase 1 Tests: Project Scaffold Verification
=============================================
Run with: python -m pytest tests/test_phase1.py -v
"""

import os
import subprocess
import sys

# Get project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestProjectStructure:
    """Verify all required files and folders exist."""
    
    def test_readme_exists(self):
        """README.md should exist with implementation plan."""
        readme_path = os.path.join(PROJECT_ROOT, "README.md")
        assert os.path.exists(readme_path), "README.md not found"
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert "PythonBook" in content, "README should mention PythonBook"
        assert "Implementation" in content or "Phase" in content, "README should have implementation details"
    
    def test_requirements_exists(self):
        """requirements.txt should exist with dependencies."""
        req_path = os.path.join(PROJECT_ROOT, "requirements.txt")
        assert os.path.exists(req_path), "requirements.txt not found"
        with open(req_path, 'r') as f:
            content = f.read()
        assert "streamlit" in content, "streamlit should be in requirements"
        assert "supabase" in content, "supabase should be in requirements"
        assert "google-generativeai" in content, "google-generativeai should be in requirements"
    
    def test_backend_folder_exists(self):
        """backend/ folder should exist."""
        backend_path = os.path.join(PROJECT_ROOT, "backend")
        assert os.path.isdir(backend_path), "backend/ folder not found"
        init_path = os.path.join(backend_path, "__init__.py")
        assert os.path.exists(init_path), "backend/__init__.py not found"
    
    def test_prompts_folder_exists(self):
        """prompts/ folder should exist with all templates."""
        prompts_path = os.path.join(PROJECT_ROOT, "prompts")
        assert os.path.isdir(prompts_path), "prompts/ folder not found"
        
        required_prompts = [
            "part1_theory.md",
            "part2_practice.md",
            "part3_mentor.md",
            "weekly_summary.md"
        ]
        for prompt_file in required_prompts:
            prompt_path = os.path.join(prompts_path, prompt_file)
            assert os.path.exists(prompt_path), f"prompts/{prompt_file} not found"
    
    def test_views_folder_exists(self):
        """views/ folder should exist."""
        views_path = os.path.join(PROJECT_ROOT, "views")
        assert os.path.isdir(views_path), "views/ folder not found"
    
    def test_assets_folder_exists(self):
        """assets/ folder should exist with SQL schema."""
        assets_path = os.path.join(PROJECT_ROOT, "assets")
        assert os.path.isdir(assets_path), "assets/ folder not found"
        sql_path = os.path.join(assets_path, "setup_tables.sql")
        assert os.path.exists(sql_path), "assets/setup_tables.sql not found"
    
    def test_github_workflow_exists(self):
        """GitHub Actions workflow should exist."""
        workflow_path = os.path.join(PROJECT_ROOT, ".github", "workflows", "textbook_scheduler.yml")
        assert os.path.exists(workflow_path), ".github/workflows/textbook_scheduler.yml not found"


class TestCLI:
    """Test the CLI entry point."""
    
    def test_cli_help(self):
        """CLI should show help message."""
        result = subprocess.run(
            [sys.executable, "run_textbook_bot.py", "--help"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"CLI help failed: {result.stderr}"
        assert "--day" in result.stdout, "Help should mention --day"
        assert "--part" in result.stdout, "Help should mention --part"
        assert "--weekly" in result.stdout, "Help should mention --weekly"
        assert "--final" in result.stdout, "Help should mention --final"
    
    def test_cli_day_argument(self):
        """CLI should accept --day argument."""
        result = subprocess.run(
            [sys.executable, "run_textbook_bot.py", "--day", "1", "--part", "part1"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        # Should run without error (even if not implemented)
        assert result.returncode == 0, f"CLI failed: {result.stderr}"
        output = result.stdout + result.stderr  # Logging goes to stderr
        assert "Day 1" in output or "not yet implemented" in output
    
    def test_cli_weekly_argument(self):
        """CLI should accept --weekly argument."""
        result = subprocess.run(
            [sys.executable, "run_textbook_bot.py", "--weekly", "1"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"CLI failed: {result.stderr}"
    
    def test_cli_final_argument(self):
        """CLI should accept --final argument."""
        result = subprocess.run(
            [sys.executable, "run_textbook_bot.py", "--final"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"CLI failed: {result.stderr}"


class TestPromptTemplates:
    """Verify prompt templates have required sections."""
    
    def test_part1_theory_template(self):
        """Part 1 template should have key sections."""
        prompt_path = os.path.join(PROJECT_ROOT, "prompts", "part1_theory.md")
        with open(prompt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "{{topic}}" in content or "{{day}}" in content, "Template should have placeholders"
        assert "What You'll Learn" in content, "Should have 'What You'll Learn' section"
        assert "Theory" in content, "Should have 'Theory' section"
        assert "IMAGE_PLACEHOLDER" in content, "Should explain image placeholder format"
    
    def test_part2_practice_template(self):
        """Part 2 template should have key sections."""
        prompt_path = os.path.join(PROJECT_ROOT, "prompts", "part2_practice.md")
        with open(prompt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "Real-World" in content, "Should have real-world use case section"
        assert "Quiz" in content, "Should mention quiz questions"
        assert "Boss" in content or "Challenge" in content, "Should mention boss challenge"
    
    def test_part3_mentor_template(self):
        """Part 3 template should have key sections."""
        prompt_path = os.path.join(PROJECT_ROOT, "prompts", "part3_mentor.md")
        with open(prompt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "Pro Tip" in content, "Should have pro tips section"
        assert "Mentor" in content, "Should have mentor moment section"
        assert "Exercise" in content, "Should have exercises section"
    
    def test_weekly_summary_template(self):
        """Weekly template should have key sections."""
        prompt_path = os.path.join(PROJECT_ROOT, "prompts", "weekly_summary.md")
        with open(prompt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "week" in content.lower(), "Should mention week"
        assert "Summary" in content or "summary" in content, "Should have summary section"


class TestDatabaseSchema:
    """Verify SQL schema has required tables."""
    
    def test_schema_has_chapters_table(self):
        """Schema should define textbook_chapters table."""
        sql_path = os.path.join(PROJECT_ROOT, "assets", "setup_tables.sql")
        with open(sql_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "textbook_chapters" in content, "Should have textbook_chapters table"
        assert "day INTEGER" in content, "Should have day column"
        assert "content_part1_theory" in content, "Should have content_part1_theory column"
    
    def test_schema_has_images_table(self):
        """Schema should define textbook_images table."""
        sql_path = os.path.join(PROJECT_ROOT, "assets", "setup_tables.sql")
        with open(sql_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "textbook_images" in content, "Should have textbook_images table"
        assert "suggested_urls" in content, "Should have suggested_urls column"
    
    def test_schema_has_craft_table(self):
        """Schema should define textbook_craft table."""
        sql_path = os.path.join(PROJECT_ROOT, "assets", "setup_tables.sql")
        with open(sql_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "textbook_craft" in content, "Should have textbook_craft table"


class TestStreamlitApp:
    """Verify Streamlit app is importable."""
    
    def test_streamlit_app_syntax(self):
        """Streamlit app should have valid Python syntax."""
        app_path = os.path.join(PROJECT_ROOT, "streamlit_app.py")
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", app_path],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Syntax error in streamlit_app.py: {result.stderr}"


if __name__ == "__main__":
    # Run tests with pytest
    import pytest
    pytest.main([__file__, "-v"])
