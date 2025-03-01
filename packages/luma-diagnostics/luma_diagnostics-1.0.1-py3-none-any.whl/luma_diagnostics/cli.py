"""Command line interface for LUMA diagnostics."""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
from . import utils
from . import api_tests
from . import messages
from . import wizard
from .case_manager import CaseManager
from rich.console import Console
from PIL import Image
from typing import Optional
import json
from . import __version__

console = Console()

class CaseManager:
    def __init__(self):
        self.current_case = None
        self.cases_dir = utils.get_config_dir() / "cases"

    def create_case(self, title, description):
        case_id = utils.generate_id()
        case_dir = self.cases_dir / case_id
        case_dir.mkdir(parents=True, exist_ok=True)
        with open(case_dir / "case.json", "w") as f:
            json.dump({"title": title, "description": description, "test_results": []}, f)
        messages.print_success(f"Case created: {case_id}")

    def list_cases(self):
        cases = []
        for case_dir in self.cases_dir.iterdir():
            if case_dir.is_dir():
                with open(case_dir / "case.json", "r") as f:
                    case_data = json.load(f)
                    cases.append({"id": case_dir.name, "title": case_data["title"]})
        return cases

    def get_case(self, case_id):
        case_dir = self.cases_dir / case_id
        if case_dir.is_dir():
            with open(case_dir / "case.json", "r") as f:
                return json.load(f)
        return None

    def select_case(self, case_id):
        case = self.get_case(case_id)
        if case:
            self.current_case = case
            return True
        return False

    def add_test_result(self, result):
        if self.current_case:
            case_dir = self.cases_dir / self.current_case["id"]
            with open(case_dir / "case.json", "r+") as f:
                case_data = json.load(f)
                case_data["test_results"].append(result)
                f.seek(0)
                json.dump(case_data, f)
                f.truncate()
            messages.print_success("Test result added to current case")
        else:
            messages.print_error("No case selected")

    def export_case(self, case_id, output_dir):
        case = self.get_case(case_id)
        if case:
            output_file = output_dir / f"{case_id}.json"
            with open(output_file, "w") as f:
                json.dump(case, f)
            return output_file
        raise ValueError("Case not found")

    def format_case_summary(self, case):
        return f"Case ID: {case['id']}\nTitle: {case['title']}\nDescription: {case['description']}\nTest Results: {len(case['test_results'])}"

def validate_image(image_path: str) -> Optional[str]:
    """Validate image file and return error message if invalid."""
    try:
        if not os.path.exists(image_path):
            return "File does not exist"
        
        image = Image.open(image_path)
        image.verify()
        return None
    except Exception as e:
        return str(e)

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="LUMA Diagnostics - Test and validate LUMA API functionality")
    parser.add_argument("--version", action="version", version=f"LUMA Diagnostics v{__version__}")
    parser.add_argument("--wizard", action="store_true", help="Run in interactive wizard mode")
    parser.add_argument("--image", help="Path to image file to test")
    parser.add_argument("--api-key", help="LUMA API key for generation tests")
    parser.add_argument("--case", help="Test case to run")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--output-dir", help="Directory to store results")
    parser.add_argument("--test", action="store_true", help="Run diagnostic tests")
    
    # Case management arguments
    case_group = parser.add_argument_group("Case Management")
    case_group.add_argument("--create-case", help="Create a new case with the given title")
    case_group.add_argument("--case-description", help="Description for the new case")
    case_group.add_argument("--list-cases", action="store_true", help="List all cases")
    case_group.add_argument("--view-case", help="View details of a specific case by ID")
    case_group.add_argument("--select-case", help="Select a case for adding test results")
    case_group.add_argument("--export-case", help="Export a case to a file that can be sent to support")
    
    args = parser.parse_args()
    
    # Initialize case manager
    case_manager = CaseManager()
    
    # Handle case management commands
    if args.create_case:
        description = args.case_description or "No description provided"
        case_manager.create_case(args.create_case, description)
        return
    
    if args.list_cases:
        cases = case_manager.list_cases()
        if not cases:
            messages.print_info("No cases found")
            return
        for case in cases:
            print("\n" + case_manager.format_case_summary(case))
        return
    
    if args.view_case:
        case = case_manager.get_case(args.view_case)
        if not case:
            messages.print_error(f"Case {args.view_case} not found")
            return
        print("\n" + case_manager.format_case_summary(case))
        return
    
    if args.select_case:
        if not case_manager.select_case(args.select_case):
            messages.print_error(f"Case {args.select_case} not found")
            return
    
    if args.export_case:
        try:
            output_dir = args.output_dir or os.getcwd()
            output_file = case_manager.export_case(args.export_case, output_dir)
            messages.print_success(f"Case exported to: {output_file}")
            messages.print_info("You can send this file to support@lumalabs.ai for assistance")
            return
        except ValueError as e:
            messages.print_error(str(e))
            return
    
    # If no case management commands, proceed with normal operation
    try:
        if args.wizard:
            wizard.run_wizard()
        elif args.test or args.image:
            api_key = args.api_key or os.getenv("LUMA_API_KEY")
            if not api_key:
                messages.print_error("No API key provided. Use --api-key or set LUMA_API_KEY environment variable")
                sys.exit(1)
            
            tester = api_tests.LumaAPITester(api_key)
            result = {}
            
            if args.test:
                messages.print_info("Running basic API test...")
                result = tester.test_text_to_image()
                if result["status"] == "success":
                    messages.print_success("Basic API test passed")
                else:
                    messages.print_error(f"Basic API test failed: {result.get('error', 'Unknown error')}")
                    sys.exit(1)
            
            if args.image:
                messages.print_info("Testing with provided image...")
                result = tester.test_image_reference(args.image)
                if result["status"] == "success":
                    messages.print_success("Image test passed")
                else:
                    messages.print_error(f"Image test failed: {result.get('error', 'Unknown error')}")
                    sys.exit(1)
            
            # Add test result to current case if one is selected
            if case_manager.current_case:
                case_manager.add_test_result(result)
            
            # Exit with success if we've run any tests
            if args.test or args.image:
                sys.exit(0)
        else:
            parser.print_help()
            sys.exit(2)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        messages.print_error(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
