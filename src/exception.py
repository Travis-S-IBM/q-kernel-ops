"""Exception class for controlling all exceptions."""


def known_exception(runtime_error: str) -> str:
    """Function to check exceptions.

    Args:
        runtime_error: string of the exception

    Return:
        String about the error
    """
    if "413 Client Error" in runtime_error:
        tele_comment = "Payload Too Large"
        print(
            "::set-output name={name}::{value}".format(
                name="Error", value=tele_comment
            )
        )
    elif "Connection broken" in runtime_error and "0 bytes read" in runtime_error:
        tele_comment = "Runtime: Cancelled - Ran too long"
        print(
            "::set-output name={name}::{value}".format(
                name="Error", value=tele_comment
            )
        )

    else:
        tele_comment = "Unknown Error"
        print(
            "::set-output name={name}::{value}".format(
                name="Unknown Error", value=runtime_error
            )
        )

    return tele_comment
