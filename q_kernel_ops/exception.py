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
            "::set-output name={name}::{value}".format(name="Error", value=tele_comment)
        )
    elif "ran longer than maximum execution time." in runtime_error:
        tele_comment = "Runtime: Cancelled - Ran too long"
        print(
            "::set-output name={name}::{value}".format(name="Error", value=tele_comment)
        )
    elif "too many 500 error responses" in runtime_error:
        tele_comment = "Network Error"
        print(
            "::set-output name={name}::{value}".format(name="Error", value=tele_comment)
        )
    elif "Unable to retrieve job result" in runtime_error:
        tele_comment = "OOM"
        print(
            "::set-output name={name}::{value}".format(name="Error", value=tele_comment)
        )

    else:
        tele_comment = "Unknown Error"
        print(
            "::set-output name={name}::{value}".format(
                name="Unknown Error", value=runtime_error
            )
        )

    return tele_comment
