// If these categories are valid
let validCategories = {
    "username": false,
    "fullname": false,
    "email": false,
    "password": false
}

// Checks if the username is valid
function checkUsername()
{
    document.getElementById("usernameError").innerHTML = "";
    let user = document.getElementsByName("username")[0].value;
    let valid = true;
    if(user.length < 4)
    {
        setButtonDisabled("username:Username too short, must be at least 4 characters long");
        valid = false;
    }
    if(user.length == 0) // TODO Change to check if username exists
    {
        setButtonDisabled("username:Username already exists!");
        valid = false;
    }

    validCategories["username"] = valid;
    checkValid();
}

// Checks if the full name is valid
function checkFullname()
{
    document.getElementById("fullnameError").innerHTML = "";
    let fullname = document.getElementsByName("full_name")[0].value;
    let valid = true;
    if(fullname.length == 0)
    {
        setButtonDisabled("fullname:Must enter in a name");
        valid = false;
    }

    validCategories["fullname"] = valid;
    checkValid();
}

// Checks if the email is valid
function checkEmail()
{
    document.getElementById("emailError").innerHTML = "";
    let email = document.getElementsByName("email")[0].value;
    let valid = true;
    if(!(email.includes("@gmail.com") || email.includes("@yahoo.com") || email.includes("@ku.edu"))) // TODO Add more emails
    {
        setButtonDisabled("email:Email is not supported. PoserRank supports gmail.com, yahoo.com, or ku.edu");
        valid = false;
    }
    else if(email.length == 0) // TODO Change to check if email exists
    {
        setButtonDisabled("email:Email already exists!");
        valid = false;
    }

    validCategories["email"] = valid;
    checkValid();
}

// Checks if the password is valid
function checkPassword()
{
    document.getElementById("passwordError").innerHTML = "";
    let pw = document.getElementsByName("password")[0].value;
    let valid = true;
    if(pw.length < 8)
    {
        setButtonDisabled("password:Password too short, must be at least 8 characters long");
        valid = false;
    }
    if(pw.match(/\d/) == null || pw.match(/[A-Z]/) == null || pw.match(/[a-z]/) == null)
    {
        setButtonDisabled("password:Password must contain one uppercase letter, one lowercase letter, and one number");
        valid = false;
    }

    validCategories["password"] = valid;
    checkValid();
}

// Sets the button to disabled and shows error
function setButtonDisabled(reasonStr)
{
    document.getElementById("submit").disabled = true;
    let reason = reasonStr.split(':');
    document.getElementById(reason[0] + "Error").innerHTML += "Error: " + reason[1] + "<br>";
}

// Checks to see if all categories are valid
function checkValid()
{
    for(let e in validCategories)
    {
        console.log(validCategories[e]);
        if(!validCategories[e])
        {
            return;
        }
    }
    document.getElementById("submit").disabled = false;
}