import argparse

from secretvalidate.env_loader import get_secret_active, get_secret_inactive, get_service

from secretvalidate.azure_storage_account_key_validator import validate_azure_storage_account_key
from secretvalidate.browserstack_validator import validate_browserstack
from secretvalidate.entra_id_validator import validate_entra_id
from secretvalidate.flickr_validator import validate_flickr_api
from secretvalidate.http_validator import validate_http
from secretvalidate.mongodb_validator import validate_mongodb
from secretvalidate.new_relic_validator import validate_new_relic
from secretvalidate.sonarcloud_validator import validate_sonarcloud
from secretvalidate.teams_webhook_validator import validate_teams_webhook


from secretvalidate.utility import format_services, get_version, lowercase_choice, update_tool

# Retrieve the current version from environment variable

CURRENT_VERSION = get_version()


# Custom ArgumentParser to suppress the default usage message
class CustomArgumentParser(argparse.ArgumentParser):
    def print_help(self, file=None):
        self._print_message(self.description, file)
        self._print_message("\n", file)
        self._print_message("Options:\n", file)
        for action in self._actions:
            if action.option_strings:
                option_string = ', '.join(action.option_strings)
                help_text = action.help if action.help else ''
                self._print_message(f"  {option_string}    {help_text}\n", file)


def parse_arguments():
    parser = argparse.ArgumentParser(
    description="Secret Validator Tool\n"
                "Use this tool to validate various types of secrets for different services.",
    formatter_class=argparse.RawTextHelpFormatter)

    # Retrieve choices from environment variable
    services = get_service()
    formatted_services = format_services(services)

    # Define arguments
    parser.add_argument("-service", type=lowercase_choice, choices=services, required=False,
                        help=f"Service / SecretType to validate secrets.\nSupported services:\n{formatted_services}")
    parser.add_argument("-secret", required=False,
                        help="Pass Secrets to be validated")
    parser.add_argument('-r', '--response', action='store_true', 
                        help=f"Prints {get_secret_active()}/ {get_secret_inactive()} upon validating secrets.")
    parser.add_argument('-v', '--version', action='version', version=f'Secret Validator Tool version {CURRENT_VERSION}', 
                        help='Show the version of this tool and exit.')
    parser.add_argument('--update', action='store_true',
                        help='Update the tool to the latest version.')

    return parser.parse_args()


def validate(service, secret, response, blob=''):
    """
    Args:
        blob(string): Can be a base-64 blob with the contents of the file where the harcoded secret was commited,
                        or a plain string with the content of the file.
                        It is used to retrieve the azure connection string to validade the azure_storage_account_key
        service(string): The service to validate the secret against.
        secret(string): The secret to validate.
        response(bool): If True, return the status instead of a message.
    """

    if service not in get_service():
        return f"Unsupported service: {service}. Skipping validation."
    
    match service:
        # please keep alphabetic order, we are civilized :D
        case "azure_storage_account_key":
            if isinstance(blob, dict):
                return validate_azure_storage_account_key(blob, secret, response)
            return "Secret unverified: Blob unavailable."
        case "browserstack_auth_url":
            return validate_browserstack(secret, response)
        case "flickr_api_key":
            return validate_flickr_api(secret, response)
        case "microsoft_azure_entra_id_token":
            return validate_entra_id(service, secret, response)
        case "mongodb":
            return validate_mongodb(secret, response)
        case "new_relic_license_key":
            return validate_new_relic(service, secret,response)
        case "sonarcloud_token":
            return validate_sonarcloud(secret, response)
        case "teams_webhook":
            return validate_teams_webhook(secret, response)
        case _:
            return validate_http(service, secret, response)

def main(args=None):
    if args is None:
        args = parse_arguments()

    if args.update:
        update_tool()
        return

    if not args.service or not args.secret:
        print("Error: The following arguments are required: -service, -secret")
        print("Use '-h' or '--help' for usage information.")
        return

    try:
        # Call the validate function with provided arguments
        result = validate(args.service, args.secret, args.response)
        print(result)
    except Exception as e:
        print(f"Error: {e}")


def main(args=None):
    if args is None:
        args = parse_arguments()

    if args.update:
        update_tool()
        return

    try:
        # Call the validate function with provided arguments
       result = validate(args.service, args.secret, args.response)
       print(result)
    except Exception as e:
        print(f"Error: {e}")
