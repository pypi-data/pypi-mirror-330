import argparse
import sys
from jasapp.parser.dockerfile import DockerfileParser
from jasapp.parser.kubernetes import KubernetesParser
from jasapp.linter import Linter
from jasapp.scorer import Scorer
from jasapp.rules import all_rules  # Import all rules dynamically
from jasapp.renderers import (
    ConsoleRenderer,
    JSONRenderer,
    CheckstyleRenderer,
    CodeClimateRenderer,
    GitLabCodeClimateRenderer,
    GNURenderer,
    CodacyRenderer,
    SonarQubeRenderer,
    SARIFRenderer)

from jasapp.gemini_integration import generate_corrected_code

# Importer la version depuis __init__.py
from jasapp import __version__


def main():
    """
    Entry point for the command-line interface.
    """
    parser = argparse.ArgumentParser(
        description="Jasapp - A linter for configuration files with scoring capabilities."
    )
    parser.add_argument("file", help="Path to the file to lint.")
    parser.add_argument(
        "--type",
        choices=["dockerfile", "kubernetes"],
        required=True,
        help="Specify the file type (Dockerfile or Kubernetes manifest).",
    )
    parser.add_argument(
        "--score", action="store_true", help="Calculate and display a quality score for the file."
    )
    parser.add_argument(
        "--ignore",
        nargs="*",
        default=[],
        help="List of rule names to ignore (e.g., STX0002).",
    )
    parser.add_argument(
        "--format",
        choices=["console", "json", "checkstyle", "codeclimate", "gitlab_codeclimate", "gnu", "codacy", "sonarqube", "sarif"],
        default="console",
        help="Output format for the errors (default: console).",
    )
    parser.add_argument(
        "--exit-code",
        action="store_true",
        help="Return exit code 1 if any error or warning is found, otherwise return 0."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"Jasapp version {__version__}"
    )
    parser.add_argument(
        "--gemini",
        metavar="API_KEY",
        help="Use Gemini to suggest fixes. Provide your Gemini API key."
    )
    parser.add_argument(
        "--gemini-detailed",
        action="store_true",
        help="Use Gemini to suggest fixes with detailed explanations (requires --gemini).",
    )

    args = parser.parse_args()

    # Select the parser and applicable rules based on the file type
    if args.type == "dockerfile":
        file_parser = DockerfileParser(args.file)
        rules = [rule() for rule_name, rule in all_rules.items() if rule.rule_type == "dockerfile"]

    elif args.type == "kubernetes":
        file_parser = KubernetesParser(args.file)
        rules = [rule() for rule_name, rule in all_rules.items() if rule.rule_type == "kubernetes"]
    else:
        raise ValueError("Unsupported file type. Use --type to specify.")

    # Filter out ignored rules
    if args.ignore:
        rules = [rule for rule in rules if rule.name not in args.ignore]

    # Check if a file is provided or read from stdin
    if args.file == '-':
        # Read from stdin
        content = sys.stdin.read()
        # Modify the parser to accept content from stdin
        instructions = file_parser.parse_from_string(content)
    else:
        # Parse the file
        try:
            instructions = file_parser.parse()
        except FileNotFoundError as e:
            print(f"Error: {e}")
            sys.exit(1)  # Exit with code 1 on file not found
        except Exception as e:
            print(f"Unexpected error while parsing: {e}")
            sys.exit(1)

    # Lint the file
    linter = Linter(rules)
    errors = linter.run(instructions)

    for error in errors:
        error["file"] = args.file

    # Render the errors in the specified format
    if args.format == "console":
        renderer = ConsoleRenderer()
    elif args.format == "json":
        renderer = JSONRenderer()
    elif args.format == "checkstyle":
        renderer = CheckstyleRenderer()
    elif args.format == "codeclimate":
        renderer = CodeClimateRenderer()
    elif args.format == "gitlab_codeclimate":
        renderer = GitLabCodeClimateRenderer()
    elif args.format == "gnu":
        renderer = GNURenderer()
    elif args.format == "codacy":
        renderer = CodacyRenderer()
    elif args.format == "sonarqube":
        renderer = SonarQubeRenderer()
    elif args.format == "sarif":
        renderer = SARIFRenderer()
    renderer.render(errors)

    # Calculate and display the score if requested
    if args.score:
        scorer = Scorer()
        score = scorer.calculate(errors, len(rules))
        print(f"\nFile Quality Score: {score}/100")

        # Gemini integration
        if args.gemini:
            # Read the file content
            try:
                with open(args.file, 'r') as f:
                    file_content = f.read()
            except FileNotFoundError as e:
                print(f"Error: {e}")
                sys.exit(1)
            except Exception as e:
                print(f"Unexpected error while reading file: {e}")
                sys.exit(1)

            # Call the Gemini API function
            corrected_code = generate_corrected_code(args.type, file_content, errors, args.gemini, args.gemini_detailed)

            if corrected_code:
                print("\n--- Gemini Suggested Fixes ---")
                print(corrected_code)
            else:
                print("\n--- Gemini could not generate corrections. ---")

    # Set the exit code based on errors and --exit-code flag
    if args.exit_code and any(error["severity"] in ["warning", "error"] for error in errors):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    if sys.modules.get("jasapp.cli") and sys.modules["jasapp.cli"].__name__ != "__main__":
        raise RuntimeError("`jasapp.cli` is already loaded incorrectly in sys.modules. Ensure you run this as a script.")
    main()
