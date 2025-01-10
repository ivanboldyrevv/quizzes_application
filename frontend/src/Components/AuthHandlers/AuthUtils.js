function parseJwt (token) {
    let base64Url = token.split(".")[1];
    let base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    let jsonPayload = decodeURIComponent(window.atob(base64).split("").map(function(c) {
        return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(""));

    return JSON.parse(jsonPayload);
}

async function verifyToken (token) {
    const response = await fetch("http://localhost:8080/api/v1/oauth2/verify_token", {
        method: "POST",
        headers: {"Content-Type": "application/json", "Authorization": `Bearer ${token}`}
    });

    console.log(await response.ok);

    if (response.status != 200) {
        return false;
    }
    return true;
}

export { parseJwt, verifyToken }