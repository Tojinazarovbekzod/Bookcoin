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


     document.getElementById("loginForm").addEventListener("submit", async function (e) {
        e.preventDefault();

        const data = {
            username: document.getElementById("username").value,
            password: document.getElementById("password").value
        };

        try {
            const response = await fetch("/api/login/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                alert("✅ Login muvaffaqiyatli: " + result.username);
                window.location.href = "/main/";
            } else {
                alert("❌ Xatolik: " + (result.error || "Noto'g'ri ma'lumot"));
            }
        } catch (err) {
            alert("⚠️ Serverga ulanib bo'lmadi!");
            console.error(err);
        }
    });
});

