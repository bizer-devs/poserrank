function changeProfilPic()
{
    document.getElementById("chooseProfile").innerHTML = `
        <input type="text" id="picInput" placeholder="Picture URL">
        <input type="button" onclick="setProfilPicURL()" value="Submit">
    `;
}

function setProfilPicURL()
{
    let errorMsg = "";
    let picURL = document.getElementById("picInput").value;
    if(picURL == document.getElementsByClassName("user-profilPic")[0].src)
        errorMsg = "This is their picture!";
    else
    {
        try {
            let checker = new XMLHttpRequest();
            checker.open('HEAD', picURL, false);
            checker.send();
            if (checker.status != 404) {
                document.getElementsByClassName("user-profilPic")[0].src = picURL;
                sendHTTPRequest("profilPic", document.getElementsByClassName("user-profilPic")[0].src);
                resetProfilPic();
            }
            else
                errorMsg = "Image doesn't exist"
        }
        catch(e)
        {
            errorMsg = "Image is invalid"
        }
    }

    if(errorMsg != "")
    {
        document.getElementById("chooseProfile").innerHTML = `
            <input type="text" id="picInput" placeholder="Picture URL">
            <input type="button" onclick="setProfilPicURL()" value="Submit"><br>
            <span style="color:red">Error: ` + errorMsg + `</span>
        `;
    }
}

function resetProfilPic()
{
    document.getElementById("chooseProfile").innerHTML = "<a  href=\"javascript:void(0);\" onclick=\"changeProfilPic()\">Change this user's Profile Picture!</a>";
}

function changeSubtitle()
{
    document.getElementById("changeSubtitle").innerHTML = `
        <input type="text" id="subtInput" placeholder="Subtitle">
        <input type="button" onclick="setSubtitle()" value="Submit">
    `;
}

function setSubtitle()
{
    let newSubtitle = document.getElementById("subtInput").value;
    if(newSubtitle != "")
    {
        document.getElementById("subt").innerHTML = "<b>" + newSubtitle + "</b>";
        sendHTTPRequest("subtitle", newSubtitle);
        resetSubtitle();
    }
}

function resetSubtitle()
{
    document.getElementById("changeSubtitle").innerHTML = "<a href=\"javascript:void(0);\" onclick=\"changeSubtitle()\">Change your subtitle!</a>";
}

function sendHTTPRequest(host, info)
{
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open("PATCH", window.location.href, true);
    xmlHttp.send(host + ":" + info);
    return xmlHttp.responseText;
}