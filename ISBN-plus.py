# Oliver Johnson, Anna George
# CSC28500 Applied Discrete Structure
# ISBN checker
# Last modified 10/24/19

import urllib.request
import json

 
def main():
    # Prompt user for ISBN
    num = input("\nEnter ISBN-13: ")

    # Check for valid input
    if len(num) != 13:  # Check for number of digits
        print("ISBN must be 13 digits.\n")
        return  # End program
    if not validate(num):  # Check that input is a number
        print("Input must be a number.\n")
        return  # End program
    
    # Check Number ISBN
    check_num = get_check(num)  # Calculate check digit
    print("Check digit:", check_num)

    # Validate ISBN
    if int(num[12]) == check_num:  # Compare last digit to check digit
        print("ISBN is valid.")
    else:
        print("ISBN is not valid.\n")
        return  # End program
    
    # Look up ISBN
    api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + num
    open_url = None
    try:
        open_url = urllib.request.urlopen(api_link)
    except:
        help_url = "https://www.dev2qa.com/how-to-fix-python-error-certificate-verify-failed-unable-to-get-local-issuer-certificate-in-mac-os/"
        print("SSL not allowed. If you're using a mac, see this: ", help_url, "\n")
        return  # End program
    if open_url.getcode() != 200:
        print("ISBN not found.\n")
        return  # End program
    json_data = json.loads(open_url.read())
    if json_data["totalItems"] == 0:
        print("No information found.\n")
        return  # End program
    volume_info = json_data["items"][0] 
    authors = json_data["items"][0]["volumeInfo"]["authors"]

    print()
    print("-" * 12, "Book Info", "-" * 12)
    print("Title:", volume_info["volumeInfo"]["title"])
    print("Author(s):", ",".join(authors))
    print("Published:", volume_info["volumeInfo"]["publishedDate"])
    print()


# Validate - check that input is a valid integer
def validate(str_input: str) -> bool:
    try:
        int(str_input)
        return True
    except ValueError:
        return False


# Get Check - return the check digit of an ISBN number
def get_check(str_input: str) -> int:
    sum = 0
    for index, value in enumerate(str_input[:12], 1):
        if (index % 2 == 0):  # when index is even
            sum += int(value) * 3
        else:  # when index is odd
            sum += int(value)
    # if remainder is 0, return 0
    # else return 10 - remainder
    return 10 - sum % 10 if sum % 10 > 0 else 0


if __name__ == "__main__":
    main()