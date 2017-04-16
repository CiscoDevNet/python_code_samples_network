from ciscosparkapi import CiscoSparkAPI

if __name__=='__main__':
    # Use ArgParse to retrieve command line parameters.
    from argparse import ArgumentParser
    parser = ArgumentParser("Spark Check In")

    # Retrieve the Spark Token and Destination Email
    parser.add_argument(
        "-t", "--token", help="Spark Authentication Token", required=True
    )
    # Retrieve the Spark Token and Destination Email
    parser.add_argument(
        "-e", "--email", help="Email to Send to", required=True
    )

    args = parser.parse_args()

    token = args.token
    email = args.email 
    message = "**Alert:** Config Changed"

    api = CiscoSparkAPI(access_token=token)
    api.messages.create(toPersonEmail=email, markdown=message)

