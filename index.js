function login(e) {
  e.preventDefault();
  const p1 = document.getElementById("partner1").value;
  const p2 = document.getElementById("partner2").value;
  const pwd = document.getElementById("password").value;

  if (pwd === "143") {
    localStorage.setItem("coupleNames", `${p1} ❤️ ${p2}`);
    window.location.href = "modules.html";
  } else {
    document.getElementById("message").textContent = "Oops! Wrong code 😢";
    document.getElementById("message").style.color = "red";
  }
}
