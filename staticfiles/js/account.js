window.addEventListener("load", function () {
    let input = document.getElementById("password");
    let toggle = document.getElementById("toggle");

    toggle.addEventListener("click", () => {
        if (input.type === "password") {
            input.type = "text";
            toggle.src = "/static/images/invisible.png";
        } else {
            input.type = "password"; 
            toggle.src = "/static/images/view.png";
        }
        toggle.style.width = "40px";
        toggle.style.height = "40px";

    });
    document.getElementById("registerForm").addEventListener("submit", async function (e) {
        e.preventDefault();

        const data = {
            username: document.getElementById("username").value,
            surname: document.getElementById("surname").value,
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        };

        try {
            const response = await fetch("/api/signup/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                alert("✅Ro'yxatdan o'tish muvaffaqiyatli!");
                window.location.href = "/login/";
            } else {
                alert("❌Xatolik: " + (result.error || "Notog'ri ma'lumot"));
            }
        } catch (err) {
            alert("Server bilan bog'lanishda xato");
            console.error(err);
        }
    });
    
});

