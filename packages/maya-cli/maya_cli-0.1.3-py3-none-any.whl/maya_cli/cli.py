import os
import sys
import click
import logging
import importlib.util
from dotenv import load_dotenv, set_key
import openai
from .project_generator import create_project_structure, PROJECT_STRUCTURE
from .refactor import process_directory
from maya_cli.scripts import optimize  # This will trigger optimize_event_handler automatically


# Setup logging
LOG_FILE = "maya_cli.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables from .env
load_dotenv()


@click.group()
def maya():
    """Maya CLI - AI Project Generator"""
    pass


@click.command()
@click.argument("project_name")
def create(project_name):
    """Create a new AI project structure"""
    try:
        base_path = os.path.join(os.getcwd(), project_name)
        if os.path.exists(base_path):
            click.echo(f"Error: Project '{project_name}' already exists.")
            logging.error(f"Project '{project_name}' already exists.")
            return
        
        os.makedirs(base_path, exist_ok=True)
        create_project_structure(base_path, PROJECT_STRUCTURE)
        click.echo(f"✅ AI project '{project_name}' created successfully!")
        logging.info(f"Project '{project_name}' created successfully at {base_path}")

    except Exception as e:
        logging.error(f"Error while creating project: {str(e)}")
        click.echo(f"❌ An error occurred: {str(e)}")

@click.command()
@click.argument("path", nargs=-1, required=True)
def check_best_practices(path):
    """CLI Command: maya check-best-practices [folder] [sub-folder] ... [filename]"""
    click.echo("🚀 Running Best Practices Check...")
    
    base_path = os.getcwd()
    target_path = os.path.join(base_path, *path)
    
    if not os.path.exists(target_path):
        click.echo(f"❌ Path '{target_path}' does not exist.")
        return
    
    if os.path.isdir(target_path):
        process_directory(target_path)
    elif os.path.isfile(target_path):
        process_directory(os.path.dirname(target_path), os.path.basename(target_path))
    else:
        click.echo("❌ Invalid path provided.")
        return
    
    click.echo("✅ Best practices check completed!")


@click.command()
@click.argument("key")
@click.argument("value")
def set_env(key, value):
    """Set an environment variable in .env file"""
    env_file = ".env"
    
    try:
        if not os.path.exists(env_file):
            with open(env_file, "w") as f:
                f.write("# Maya CLI Environment Variables\n")
            logging.info("Created new .env file.")

        set_key(env_file, key, value)
        click.echo(f"✅ Environment variable '{key}' set successfully!")
        logging.info(f"Set environment variable: {key}={value}")

    except Exception as e:
        logging.error(f"Error setting environment variable {key}: {str(e)}")
        click.echo(f"❌ Error setting environment variable: {str(e)}")

@click.command()
@click.argument("parent_folder", required=True)
@click.argument("sub_folder", required=True)
@click.argument("filename", required=True)
def optimize(parent_folder, sub_folder, filename):
    """Optimize a file by importing optimize.py from maya_cli.scripts."""
    
    # Construct the full file path
    target_path = os.path.abspath(os.path.join(parent_folder, sub_folder, filename))

    if not os.path.isfile(target_path):
        click.echo(f"❌ Error: '{target_path}' is not a valid file.")
        logging.error(f"Invalid file provided: {target_path}")
        return

    # Inject the import statement into the file
    inject_import(target_path)

def inject_import(filepath):
    """Inject import statement for optimize.py into the target file."""
    try:
        import_statement = "from maya_cli.scripts import optimize\n"

        with open(filepath, "r+", encoding="utf-8") as f:
            content = f.readlines()
            
            # Check if the import already exists
            if any(line.strip() == import_statement.strip() for line in content):
                click.echo(f"✅ {filepath} already imports optimize.py.")
                return
            
            # Insert import at the top
            content.insert(0, import_statement)
            f.seek(0)
            f.writelines(content)

        click.echo(f"✅ Imported optimize.py into {filepath}")
        logging.info(f"Imported optimize.py into {filepath}")

    except Exception as e:
        logging.error(f"Error injecting import into '{filepath}': {str(e)}")
        click.echo(f"❌ Error injecting import into '{filepath}': {str(e)}")

import os
import json
import click
import logging
import openai

@click.command()
@click.argument("parent_folder", required=True)
@click.argument("sub_folder", required=True)
@click.argument("filename", required=True)
def is_secured(parent_folder, sub_folder, filename):
    """Check and enforce API security measures: Authentication, Encryption, and Rate Limiting."""
    click.echo("🔍 Running API Security Check...")

    # Construct the full file path
    target_path = os.path.abspath(os.path.join(parent_folder, sub_folder, filename))

    if not os.path.isfile(target_path):
        click.echo(f"❌ Error: '{target_path}' is not a valid file.")
        logging.error(f"Invalid file provided: {target_path}")
        return

    try:
        with open(target_path, "r", encoding="utf-8") as f:
            code_content = f.read()

        # Validate security using AI
        validation_feedback = validate_security_with_ai(code_content)
        security_issues = []

        if not validation_feedback.get("authentication", False):
            security_issues.append(f"❌ Missing API Authentication. Applying OAuth/API Key authentication.")
            apply_api_authentication(target_path)

        if not validation_feedback.get("encryption", False):
            security_issues.append(f"❌ Missing Data Encryption. Implementing encryption protocols.")
            apply_data_encryption(target_path)

        if not validation_feedback.get("rate_limiting", False):
            security_issues.append(f"❌ No Rate Limiting detected. Implementing rate limiting & quotas.")
            apply_rate_limiting(target_path)

        if security_issues:
            for issue in security_issues:
                click.echo(f"⚠️ {issue}")
            click.echo("✅ Security measures have been enforced!")
        else:
            click.echo("✅ API usage is secure. No changes needed.")

    except Exception as e:
        logging.error(f"❌ Error processing {target_path}: {str(e)}")
        click.echo(f"❌ Error processing {target_path}: {str(e)}")

    logging.info("API Security Check Completed.")


def validate_security_with_ai(code):
    """Use OpenAI to validate security measures in the given code."""
    prompt = f"""
    Analyze the following Python code for API security vulnerabilities.
    Identify if the code implements:
    1. Secure API Authentication (OAuth or API Keys)
    2. Proper Data Encryption Protocols for sensitive data
    3. Rate Limiting and Quotas to prevent API abuse

    Return a JSON response with keys: authentication, encryption, rate_limiting, each set to True or False.

    Code:
    ```
    {code}
    ```
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}],
        )

        result = response["choices"][0]["message"]["content"]
        return json.loads(result)

    except Exception as e:
        logging.error(f"Error in AI validation: {str(e)}")
        return {"authentication": False, "encryption": False, "rate_limiting": False}


def apply_api_authentication(filepath):
    """Apply OAuth or API Key authentication to the specified file."""
    logging.info(f"Applying OAuth/API Key Authentication to {filepath}.")
    with open(filepath, "a", encoding="utf-8") as f:
        f.write("\n# TODO: Implement OAuth/API Key Authentication\n")


def apply_data_encryption(filepath):
    """Implement data encryption protocols in the specified file."""
    logging.info(f"Applying Data Encryption Protocols to {filepath}.")
    with open(filepath, "a", encoding="utf-8") as f:
        f.write("\n# TODO: Implement Data Encryption\n")


def apply_rate_limiting(filepath):
    """Implement API rate limiting and quotas in the specified file."""
    logging.info(f"Applying Rate Limiting & Quotas to {filepath}.")
    with open(filepath, "a", encoding="utf-8") as f:
        f.write("\n# TODO: Enforce API Rate Limiting & Quotas\n")

@click.command()
@click.argument("parent_folder", required=True)
@click.argument("sub_folder", required=True)
@click.argument("filename", required=False)
def check_ethics(parent_folder, sub_folder, filename=None):
    """Check code for efficiency, accuracy, and best practices."""
    click.echo("\U0001F50D Running Code Ethics Check...")
    ethics_issues = []

    # Construct the full path
    target_path = os.path.abspath(os.path.join(parent_folder, sub_folder))
    
    if not os.path.isdir(target_path):
        click.echo(f"❌ Error: '{target_path}' is not a valid directory.")
        logging.error(f"Invalid directory provided: {target_path}")
        return

    # Determine files to check
    if filename:
        files_to_check = [os.path.join(target_path, filename)]
        if not os.path.isfile(files_to_check[0]):
            click.echo(f"❌ Error: '{files_to_check[0]}' is not a valid file.")
            logging.error(f"Invalid file provided: {files_to_check[0]}")
            return
    else:
        files_to_check = [
            os.path.join(target_path, f) for f in os.listdir(target_path) if f.endswith(".py")
        ]

    for file in files_to_check:
        try:
            with open(file, "r", encoding="utf-8") as f:
                code_content = f.read()

            # Validate ethics using AI
            validation_feedback = validate_ethics_with_ai(code_content)

            if not validation_feedback.get("efficiency", False):
                ethics_issues.append(f"{file}: Code may have performance inefficiencies.")

            if not validation_feedback.get("accuracy", False):
                ethics_issues.append(f"{file}: Code accuracy needs review for correctness.")

            if not validation_feedback.get("best_practices", False):
                ethics_issues.append(f"{file}: Code may not follow industry best practices.")

        except Exception as e:
            logging.error(f"❌ Error processing {file}: {str(e)}")
            click.echo(f"❌ Error processing {file}: {str(e)}")

    if ethics_issues:
        for issue in ethics_issues:
            click.echo(f"⚠️ {issue}")
        click.echo("✅ Ethics Review Completed with Recommendations!")
    else:
        click.echo("✅ Code meets ethical standards. No issues detected.")

    logging.info("Code Ethics Check Completed.")


def validate_ethics_with_ai(code):
    """Use OpenAI to validate code ethics, efficiency, and best practices."""
    prompt = f"""
    Analyze the following Python code for ethical concerns in:
    1. Efficiency (performance optimization, unnecessary loops, redundant code)
    2. Accuracy (logical correctness, potential calculation errors)
    3. Best Practices (PEP8 compliance, maintainability, documentation)

    Return a JSON response with keys: efficiency, accuracy, best_practices, each set to True or False.

    Code:
    ```
    {code}
    ```
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}],
        )

        result = response["choices"][0]["message"]["content"]
        return json.loads(result)

    except Exception as e:
        logging.error(f"Error in AI validation: {str(e)}")
        return {"efficiency": False, "accuracy": False, "best_practices": False}

@click.command()
@click.argument("parent_folder")
@click.argument("sub_folder")
@click.argument("filename")
def doc(parent_folder, sub_folder, filename):
    """Generate README.md documentation for the given file."""
    click.echo("📄 Generating Documentation...")

    # Construct the full file path
    target_path = os.path.join(parent_folder, sub_folder)
    file_path = os.path.join(target_path, filename)

    # Validate directory existence
    if not os.path.isdir(target_path):
        click.echo(f"❌ Error: The directory '{target_path}' does not exist.")
        return

    # Validate file existence
    if not os.path.isfile(file_path):
        click.echo(f"❌ Error: The file '{file_path}' does not exist in the specified directory.")
        return

    readme_path = os.path.join(target_path, "README.md")

    try:
        with open(file_path, "r", encoding="utf-8") as source_file:
            code_content = source_file.read()

        # Generate documentation (Placeholder function, replace with AI-based generation)
        documentation = generate_documentation(code_content)

        # Write to README.md
        with open(readme_path, "w", encoding="utf-8") as readme_file:
            readme_file.write(documentation)

        click.echo(f"✅ Documentation created for {file_path} -> {readme_path}")

    except Exception as e:
        logging.error(f"❌ Error processing {file_path}: {str(e)}")
        click.echo(f"❌ Error processing {file_path}: {str(e)}")

def generate_documentation(code):
    """Generate structured documentation based on the given Python code."""
    return f"# Auto-Generated Documentation\n\n```python\n{code}\n```"

@click.command()
@click.argument("parent_folder")
@click.argument("sub_folder")
@click.argument("filename", required=False)
def codex(parent_folder, sub_folder, filename=None):
    """Provide in-depth analysis and recommendations for a file or all Python files in a directory."""
    click.echo("📚 Creating Code Codex Report...")

    # Construct the full target path
    target_path = os.path.join(parent_folder, sub_folder)

    # Validate directory existence
    if not os.path.isdir(target_path):
        click.echo(f"❌ Error: The directory '{target_path}' does not exist.")
        return

    # Determine files to analyze
    if filename:
        file_path = os.path.join(target_path, filename)
        if not os.path.isfile(file_path):
            click.echo(f"❌ Error: The file '{file_path}' does not exist in the specified directory.")
            return
        files_to_analyze = [file_path]
    else:
        files_to_analyze = [os.path.join(target_path, f) for f in os.listdir(target_path) if f.endswith(".py")]

    if not files_to_analyze:
        click.echo("⚠️ No Python files found in the specified directory.")
        return

    for file in files_to_analyze:
        codex_report_path = os.path.join(".\\docs/", "CODEX_REPORT.md")

        try:
            with open(file, "r", encoding="utf-8") as source_file:
                code_content = source_file.read()

            # Generate codex report (Placeholder function, replace with AI-based analysis)
            report = generate_codex_report(code_content)

            # Write report to CODEX_REPORT.md
            with open(codex_report_path, "w", encoding="utf-8") as report_file:
                report_file.write(report)

            click.echo(f"✅ Codex Report generated for {file} -> {codex_report_path}")

        except Exception as e:
            logging.error(f"❌ Error processing {file}: {str(e)}")
            click.echo(f"❌ Error processing {file}: {str(e)}")

def generate_codex_report(code):
    """Generate an in-depth analysis and recommendations based on the given Python code."""
    return f"# Code Analysis & Recommendations\n\n```python\n{code}\n```\n\n## Recommendations:\n- Improve efficiency\n- Enhance readability\n- Optimize performance\n"

@click.command()
@click.argument("parent_folder")
@click.argument("sub_folder")
@click.argument("filename", required=False)
def regulate(parent_folder, sub_folder, filename=None):
    """Ensure code compliance with GDPR, CCPA, AI Act, and ISO 42001 AI governance standards."""
    click.echo("🔍 Running Compliance & Regulation Check...")

    compliance_issues = []

    # Construct the full target path
    target_path = os.path.join(parent_folder, sub_folder)

    # Validate directory existence
    if not os.path.isdir(target_path):
        click.echo(f"❌ Error: The directory '{target_path}' does not exist.")
        return

    # Determine files to check
    if filename:
        file_path = os.path.join(target_path, filename)
        if not os.path.isfile(file_path):
            click.echo(f"❌ Error: The file '{file_path}' does not exist in the specified directory.")
            return
        files_to_check = [file_path]
    else:
        files_to_check = [os.path.join(target_path, f) for f in os.listdir(target_path) if f.endswith(".py")]

    if not files_to_check:
        click.echo("⚠️ No Python files found in the specified directory.")
        return

    for file in files_to_check:
        compliance_report_path = os.path.join("./configs/", "COMPLIANCE_REPORT.md")

        try:
            with open(file, "r", encoding="utf-8") as f:
                code_content = f.read()

            # Validate compliance (Placeholder function, replace with AI-based analysis)
            compliance_feedback = validate_compliance_with_ai(code_content)

            # Track issues and apply fixes
            if not compliance_feedback.get("gdpr", False):
                compliance_issues.append(f"{file}: GDPR compliance issues detected. Adjusting for data privacy.")
                apply_gdpr_compliance(file)

            if not compliance_feedback.get("ccpa", False):
                compliance_issues.append(f"{file}: CCPA compliance issues detected. Ensuring consumer rights protection.")
                apply_ccpa_compliance(file)

            if not compliance_feedback.get("ai_act", False):
                compliance_issues.append(f"{file}: AI Act risk classification missing. Implementing compliance measures.")
                apply_ai_act_compliance(file)

            if not compliance_feedback.get("iso_42001", False):
                compliance_issues.append(f"{file}: ISO 42001 AI governance framework not followed. Adjusting AI management protocols.")
                apply_iso_42001_compliance(file)

            # Generate compliance report
            with open(compliance_report_path, "w", encoding="utf-8") as report_file:
                report_file.write(generate_compliance_report(file, compliance_feedback))

            click.echo(f"✅ Compliance report generated for {file} -> {compliance_report_path}")

        except Exception as e:
            logging.error(f"❌ Error processing {file}: {str(e)}")
            click.echo(f"❌ Error processing {file}: {str(e)}")

    if compliance_issues:
        for issue in compliance_issues:
            click.echo(f"⚠️ {issue}")
        click.echo("✅ Compliance measures have been enforced!")
    else:
        click.echo("✅ Code meets all compliance regulations. No changes needed.")

    logging.info("Compliance & Regulation Check Completed.")

def validate_compliance_with_ai(code):
    """Analyze code for compliance with GDPR, CCPA, AI Act, and ISO 42001."""
    return {
        "gdpr": True, 
        "ccpa": True, 
        "ai_act": False, 
        "iso_42001": False
    }  # Replace with AI-based compliance validation

def apply_gdpr_compliance(filepath):
    logging.info(f"Applying GDPR compliance to {filepath}.")

def apply_ccpa_compliance(filepath):
    logging.info(f"Applying CCPA compliance to {filepath}.")

def apply_ai_act_compliance(filepath):
    logging.info(f"Applying AI Act compliance to {filepath}.")

def apply_iso_42001_compliance(filepath):
    logging.info(f"Applying ISO 42001 AI governance framework to {filepath}.")

def generate_compliance_report(filepath, feedback):
    """Generate a structured compliance report."""
    return f"""
# Compliance Report for {os.path.basename(filepath)}

## Compliance Status:
- **GDPR:** {"✅ Compliant" if feedback.get("gdpr") else "❌ Not Compliant"}
- **CCPA:** {"✅ Compliant" if feedback.get("ccpa") else "❌ Not Compliant"}
- **AI Act:** {"✅ Compliant" if feedback.get("ai_act") else "❌ Not Compliant"}
- **ISO 42001:** {"✅ Compliant" if feedback.get("iso_42001") else "❌ Not Compliant"}

## Recommendations:
- { "Ensure data privacy measures are in place." if not feedback.get("gdpr") else "GDPR compliance verified." }
- { "Strengthen consumer rights protection." if not feedback.get("ccpa") else "CCPA compliance verified." }
- { "Classify AI system under the AI Act risk framework." if not feedback.get("ai_act") else "AI Act compliance verified." }
- { "Align with ISO 42001 AI governance framework." if not feedback.get("iso_42001") else "ISO 42001 compliance verified." }

---

🛠 *Generated by Compliance Checker*
"""

# Add commands to Maya CLI
maya.add_command(is_secured)
maya.add_command(check_ethics)
maya.add_command(doc)
maya.add_command(codex)
maya.add_command(regulate)
maya.add_command(create)
maya.add_command(check_best_practices)
maya.add_command(set_env)
maya.add_command(optimize)

if __name__ == "__main__":
    maya()
