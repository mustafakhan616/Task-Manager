document.addEventListener("DOMContentLoaded", loadTasks);

function loadTasks() {
  fetch("/tasks", { credentials: "same-origin" })
    .then(res => res.json())
    .then(tasks => {
      const list = document.getElementById("taskList");
      list.innerHTML = "";

      let total = tasks.length;
      let completed = 0;

      tasks.forEach(task => {
        if (task.status === "completed") completed++;

        const li = document.createElement("li");

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = task.status === "completed";
        checkbox.onchange = () => toggleStatus(task.id, checkbox.checked);

        const span = document.createElement("span");
        span.innerText = task.title;
        if (task.status === "completed") span.classList.add("completed");

        const del = document.createElement("button");
        del.innerText = "✖";
        del.className = "delete";
        del.onclick = () => deleteTask(task.id);

        li.appendChild(checkbox);
        li.appendChild(span);
        li.appendChild(del);
        list.appendChild(li);
      });

      document.getElementById("total").innerText = total;
      document.getElementById("completed").innerText = completed;
      document.getElementById("pending").innerText = total - completed;
    });
}

function addTask() {
  const title = document.getElementById("taskInput").value;

  fetch("/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({ title })
  }).then(() => {
    taskInput.value = "";
    loadTasks();
  });
}

function toggleStatus(id, checked) {
  fetch(`/tasks/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({
      status: checked ? "completed" : "pending"
    })
  }).then(loadTasks);
}

function deleteTask(id) {
  fetch(`/tasks/${id}`, {
    method: "DELETE",
    credentials: "same-origin"
  }).then(loadTasks);
}

function logout() {
  fetch("/logout", {
    method: "POST",
    credentials: "same-origin"
  }).then(() => window.location.href = "/");
}
