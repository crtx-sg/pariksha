#!/usr/bin/env python3
"""
Header Management System for Pariksha - Question Paper Drafting System
Provides functionality to create, manage, and format headers for question papers
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path


class HeaderGenerator:
    """Class to generate and manage question paper headers"""

    def __init__(self):
        self.default_templates = {
            "standard": {
                "school_name": "SCHOOL NAME",
                "exam_name": "EXAMINATION NAME",
                "subject": "SUBJECT",
                "class_grade": "CLASS/GRADE",
                "duration": "3 Hours",
                "max_marks": "100",
                "date": "",
                "instructions": [
                    "All questions are compulsory.",
                    "Write your answers in the space provided.",
                    "Use black or blue pen only.",
                    "Read all questions carefully before answering."
                ]
            },
            "university": {
                "university_name": "UNIVERSITY NAME",
                "department": "DEPARTMENT",
                "course_code": "COURSE CODE",
                "course_title": "COURSE TITLE",
                "semester": "SEMESTER",
                "year": "YEAR",
                "duration": "3 Hours",
                "max_marks": "100",
                "date": "",
                "instructions": [
                    "Answer ALL questions.",
                    "All questions carry equal marks unless specified.",
                    "Use of calculator is permitted/not permitted.",
                    "Start each answer on a new page."
                ]
            },
            "board": {
                "board_name": "BOARD OF EDUCATION",
                "examination": "EXAMINATION",
                "subject": "SUBJECT",
                "class_standard": "CLASS/STANDARD",
                "paper_code": "PAPER CODE",
                "duration": "3 Hours",
                "max_marks": "100",
                "date": "",
                "roll_number_section": True,
                "instructions": [
                    "This question paper contains X questions.",
                    "All questions are compulsory.",
                    "Marks are indicated against each question.",
                    "Write your Roll Number in the space provided above."
                ]
            }
        }

    def generate_header_markdown(self, template_type="standard", custom_data=None):
        """Generate header in markdown format"""
        template = self.default_templates.get(template_type, self.default_templates["standard"])

        if custom_data:
            template.update(custom_data)

        # Set default date if not provided
        if not template.get("date"):
            template["date"] = datetime.now().strftime("%B %d, %Y")

        markdown = self._build_markdown_header(template, template_type)
        return markdown

    def _build_markdown_header(self, data, template_type):
        """Build the markdown header based on template type"""
        if template_type == "standard":
            return self._build_standard_header(data)
        elif template_type == "university":
            return self._build_university_header(data)
        elif template_type == "board":
            return self._build_board_header(data)
        else:
            return self._build_standard_header(data)

    def _build_standard_header(self, data):
        """Build standard school header"""
        header = f"""<div style="text-align: center;">
<h1><strong>{data.get('school_name', 'SCHOOL NAME')}</strong></h1>
<h2><strong>{data.get('exam_name', 'EXAMINATION NAME')}</strong></h2>
<h3><strong>Subject: {data.get('subject', 'SUBJECT')}</strong></h3>
</div>

<div style="float: left;">
<strong>Class/Grade:</strong> {data.get('class_grade', 'CLASS/GRADE')}<br>
<strong>Duration:</strong> {data.get('duration', '3 Hours')}<br>
<strong>Date:</strong> {data.get('date', '')}
</div>

<div style="float: right;">
<strong>Maximum Marks:</strong> {data.get('max_marks', '100')}<br>
<strong>Name:</strong> _____________________<br>
<strong>Roll No.:</strong> ___________________
</div>

<div style="overflow: hidden;">
&nbsp;
</div>

---

### General Instructions:
"""

        for instruction in data.get('instructions', []):
            header += f"- {instruction}\n"

        header += "\n---\n\n"
        return header

    def _build_university_header(self, data):
        """Build university-style header"""
        header = f"""<div style="text-align: center;">
<h1><strong>{data.get('university_name', 'UNIVERSITY NAME')}</strong></h1>
<h2><strong>{data.get('department', 'DEPARTMENT')}</strong></h2>
<h3><strong>{data.get('course_code', 'COURSE CODE')}: {data.get('course_title', 'COURSE TITLE')}</strong></h3>
</div>

<div style="float: left;">
<strong>Semester:</strong> {data.get('semester', 'SEMESTER')}<br>
<strong>Year:</strong> {data.get('year', 'YEAR')}<br>
<strong>Duration:</strong> {data.get('duration', '3 Hours')}
</div>

<div style="float: right;">
<strong>Maximum Marks:</strong> {data.get('max_marks', '100')}<br>
<strong>Date:</strong> {data.get('date', '')}<br>
<strong>Student ID:</strong> ___________________
</div>

<div style="overflow: hidden;">
&nbsp;
</div>

---

### Instructions:
"""

        for instruction in data.get('instructions', []):
            header += f"- {instruction}\n"

        header += "\n---\n\n"
        return header

    def _build_board_header(self, data):
        """Build board examination header"""
        header = f"""<div style="text-align: center;">
<h1><strong>{data.get('board_name', 'BOARD OF EDUCATION')}</strong></h1>
<h2><strong>{data.get('examination', 'EXAMINATION')}</strong></h2>
</div>

"""

        if data.get('roll_number_section', True):
            header += """<div style="text-align: center; border: 2px solid black; padding: 10px; margin: 10px 0;">
<strong>Roll Number: ________________________</strong>
</div>

"""

        header += f"""<div style="float: left;">
<strong>Subject:</strong> {data.get('subject', 'SUBJECT')}<br>
<strong>Class/Standard:</strong> {data.get('class_standard', 'CLASS/STANDARD')}<br>
<strong>Paper Code:</strong> {data.get('paper_code', 'PAPER CODE')}
</div>

<div style="float: right;">
<strong>Duration:</strong> {data.get('duration', '3 Hours')}<br>
<strong>Maximum Marks:</strong> {data.get('max_marks', '100')}<br>
<strong>Date:</strong> {data.get('date', '')}
</div>

<div style="overflow: hidden;">
&nbsp;
</div>

---

### Instructions:
"""

        for instruction in data.get('instructions', []):
            header += f"- {instruction}\n"

        header += "\n---\n\n"
        return header

    def save_template(self, template_name, template_data, templates_dir="templates"):
        """Save custom template to file"""
        # Create templates directory if it doesn't exist
        Path(templates_dir).mkdir(exist_ok=True)

        template_file = Path(templates_dir) / f"{template_name}.json"

        with open(template_file, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, indent=4, ensure_ascii=False)

        return str(template_file)

    def load_template(self, template_name, templates_dir="templates"):
        """Load custom template from file"""
        template_file = Path(templates_dir) / f"{template_name}.json"

        if not template_file.exists():
            raise FileNotFoundError(f"Template '{template_name}' not found in {templates_dir}")

        with open(template_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def list_templates(self, templates_dir="templates"):
        """List available custom templates"""
        templates_path = Path(templates_dir)

        if not templates_path.exists():
            return []

        template_files = list(templates_path.glob("*.json"))
        return [f.stem for f in template_files]

    def create_interactive_header(self):
        """Interactive CLI for creating headers"""
        print("🎓 Pariksha Header Generator")
        print("=" * 40)

        # Choose template type
        print("\nAvailable template types:")
        for i, template_type in enumerate(self.default_templates.keys(), 1):
            print(f"{i}. {template_type.title()}")

        try:
            choice = int(input("\nSelect template type (1-3): ")) - 1
            template_types = list(self.default_templates.keys())
            selected_template = template_types[choice]
        except (ValueError, IndexError):
            print("Invalid choice. Using standard template.")
            selected_template = "standard"

        # Get custom data
        custom_data = {}
        template = self.default_templates[selected_template]

        print(f"\n📝 Customizing {selected_template} template:")
        print("(Press Enter to use default values)")

        for key, default_value in template.items():
            if key == "instructions":
                continue  # Handle instructions separately

            if isinstance(default_value, bool):
                continue  # Skip boolean values for now

            display_key = key.replace("_", " ").title()
            user_input = input(f"{display_key} [{default_value}]: ").strip()

            if user_input:
                custom_data[key] = user_input

        # Handle instructions
        print("\nCustomize instructions (press Enter twice to finish):")
        custom_instructions = []
        while True:
            instruction = input("Instruction: ").strip()
            if not instruction:
                break
            custom_instructions.append(instruction)

        if custom_instructions:
            custom_data["instructions"] = custom_instructions

        # Generate header
        header_markdown = self.generate_header_markdown(selected_template, custom_data)

        # Save to file
        output_file = f"header_{selected_template}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(header_markdown)

        print(f"\n✅ Header saved to: {output_file}")
        print("\n📋 Generated Header Preview:")
        print("-" * 40)
        print(header_markdown[:500] + "..." if len(header_markdown) > 500 else header_markdown)

        return output_file


def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(description="Pariksha Header Generator")
    parser.add_argument("--template", "-t", choices=["standard", "university", "board"],
                       default="standard", help="Template type to use")
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Run in interactive mode")
    parser.add_argument("--output", "-o", help="Output file name")
    parser.add_argument("--config", "-c", help="JSON configuration file")

    args = parser.parse_args()

    generator = HeaderGenerator()

    if args.interactive:
        generator.create_interactive_header()
        return

    # Load configuration if provided
    custom_data = {}
    if args.config and os.path.exists(args.config):
        with open(args.config, 'r', encoding='utf-8') as f:
            custom_data = json.load(f)

    # Generate header
    header_markdown = generator.generate_header_markdown(args.template, custom_data)

    # Save to file
    output_file = args.output or f"header_{args.template}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(header_markdown)

    print(f"✅ Header generated and saved to: {output_file}")


if __name__ == "__main__":
    # Ensure Windows compatibility
    if sys.platform.startswith('win'):
        # Set UTF-8 encoding for Windows console
        import locale
        try:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        except locale.Error:
            try:
                locale.setlocale(locale.LC_ALL, 'C.UTF-8')
            except locale.Error:
                pass  # Use system default

    main()