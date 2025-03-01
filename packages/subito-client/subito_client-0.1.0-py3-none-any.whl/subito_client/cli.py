import argparse
import asyncio
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from subito_client import translate
from .configs import PREFIX

def main():
    parser = argparse.ArgumentParser(
        description="Subtitle Translation Client",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Required arguments
    parser.add_argument("file_path", 
                        help="Path to subtitle file for translation")
    
    # Token can come from CLI or environment variable
    parser.add_argument("-t",
                        "--token", 
                        required=False,
                        help="Authentication token (default: $SUBITO_TOKEN)",
                        default=os.environ.get("SUBITO_TOKEN", None))
    
    # Optional arguments
    parser.add_argument("-P",
                        "--max-price", 
                        type=int,
                        help="Maximum acceptable price (toman)",
                        default=None)
    
    # Optional arguments
    parser.add_argument("-p",
                        "--prefix",
                        help='Filename prefix for translations',
                        default=PREFIX)

    args = parser.parse_args()

    # Add this validation check
    if not args.token:
        parser.error("Authentication token required (use --token or set SUBITO_TOKEN environment variable)")

    try:
        asyncio.run(translate(
            path=args.file_path,
            token=args.token,
            max_price=args.max_price,
            prefix=args.prefix
        ))
    except RuntimeError as e:
        print(f"Error: {str(e)}")
        exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled")
        exit(130)

if __name__ == "__main__":
    main()
