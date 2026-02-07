const form = document.getElementById("applyForm");
const response = document.getElementById("response");

form.addEventListener("submit", function(e){
    e.preventDefault();
    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value,
        message: document.getElementById("message").value
    };

    fetch("http://127.0.0.1:5000/apply", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => response.innerText = data.message)
    .catch(err => response.innerText = "Error submitting application");
});