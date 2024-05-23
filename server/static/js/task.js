function init() {
    window.onload = getGroups();

    var inputGroup = document.getElementById("create-group");
    var inputTask = document.getElementById("create-task");

    inputGroup.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            createGroup();
        }
    });

    inputTask.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            createTask();
        }
    });
}

function getGroups() {
    fetch("api/groups", {
        method: "GET"
    })
    .then((response) => {
        if (response.status != 200) {
            return;
        }

        return response.json();
    })
    .then((groups) => {
        let list = document.getElementById("groups");

        groups.forEach(group => {
            var li = document.createElement("li");

            li.setAttribute("id", "group" + group.id);
            li.setAttribute("class", "group");
            li.setAttribute("onclick", "getTasks(" + group.id + ")");

            var item = document.createElement("p");

            item.setAttribute("id", group.id);
            item.appendChild(document.createTextNode(group.title));

            li.appendChild(item);

            var btnDelete = document.createElement("button");

            btnDelete.setAttribute("onclick", "deleteGroup(" + group.id + "); event.stopPropagation();");
            btnDelete.appendChild(document.createTextNode("del"));

            li.appendChild(btnDelete);

            list.appendChild(li);
        });
    })
    .catch(error => console.log(error));
}

function createGroup() {
    let input = document.getElementById("create-group");

    let title = input.value;

    fetch("api/groups/create?title=" + title, {
        method: "POST"
    })
    .then((response) => {
        input.value = "";
        location.reload();
    });
}

function deleteGroup(groupId) {
    fetch("api/groups/delete?id=" + groupId, {
        method: "DELETE"
    })
    .then((response) => {
        if (response.status != 200) {
            return;
        }

        if (groupId == currentGroupId) {
            let prevGroup = document.getElementById("group" + currentGroupId);

            prevGroup.classList.remove("active");

            currentGroupId = -1;
        }

        let groups = document.getElementById("groups");
        let group = document.getElementById("group" + groupId);

        groups.removeChild(group);
    })
}

function getTasks(groupId) {
    if (currentGroupId != -1) {
        let prevGroup = document.getElementById("group" + currentGroupId);

        prevGroup.classList.remove("active");
    }

    let group = document.getElementById("group" + groupId);

    group.classList.add("active");

    currentGroupId = groupId;

    fetch("api/tasks?group_id=" + groupId, {
        method: "GET"
    })
    .then((response) => {
        if (response.status != 200) {
            return;
        }

        return response.json();
    })
    .then((tasks) => {
        let list = document.getElementById("tasks");

        list.innerHTML = "";

        tasks.forEach(task => {
            var li = document.createElement("li");

            li.setAttribute("id", "task" + task.id);

            var div = document.createElement("div");

            div.onclick = () => showTaskDetail(task);

            li.appendChild(div);

            var checkBox = document.createElement("input");

            checkBox.setAttribute("id", task.id);
            checkBox.setAttribute("type", "checkbox");
            checkBox.setAttribute("onchange", "toggleTask(this, " + task.id + ")");
            checkBox.setAttribute("onclick", "event.stopPropagation();");

            checkBox.checked = task.is_done;

            div.appendChild(checkBox);

            var title = document.createElement("label");

            title.setAttribute("for", task.id);
            title.appendChild(document.createTextNode(task.title));

            div.appendChild(title);

            var btnDelete = document.createElement("button");

            btnDelete.setAttribute("style", "float: right;");
            btnDelete.setAttribute("onclick", "deleteTask(" + task.id + "); event.stopPropagation();");
            btnDelete.appendChild(document.createTextNode("del"));

            div.appendChild(btnDelete);

            if (task.description != null) {
                var description = document.createElement("p");

                description.appendChild(document.createTextNode(task.description));

                div.appendChild(description);
            }

            var hr = document.createElement("hr");

            div.appendChild(hr)

            list.appendChild(li);
        });
    })
    .catch(error => console.log(error));
}

function createTask() {
    let input = document.getElementById("create-task");

    let title = input.value;

    fetch("api/tasks/create?group_id=" + currentGroupId + "&title=" + title, {
        method: "POST"
    })
    .then((response) => {
        console.log(response);
    })
    .then(() => {
        input.value = "";
        
        getTasks(currentGroupId);
    });
}

function toggleTask(checkBox, id) {
    let isDone = checkBox.checked ? 1 : 0;

    fetch("api/tasks/toggle?id=" + id + "&is_done=" + isDone, {
        method: "PUT"
    })
    .then((response) => {
        console.log(response);
    });
}

function deleteTask(taskId) {
    fetch("/api/tasks/delete?id=" + taskId, {
        method: "DELETE"
    })
    .then((response) => {
        if (response.status != 200) {
            return;
        }

        let tasks = document.getElementById("tasks");
        let task = document.getElementById("task" + taskId);

        tasks.removeChild(task);
    });
}

function showTaskDetail(task) {
    const modalTaskDetail = document.getElementById("dialog_task_detail");
    const btnClose = document.getElementById("btn_close_task_detail");
    const btnOk = document.getElementById("btn_ok");

    const title = document.getElementById("title");
    const description = document.getElementById("description");
    const dueDate = document.getElementById("due_date");

    title.value = task.title;

    if (task.description != null) {
        description.value = task.description;
    }

    dueDate.value = task.due_date == null
        ? new Date().toDateInputValue()
        : new Date(task.due_date).toDateInputValue();

    modalTaskDetail.showModal();

    btnClose.onclick = () => {
        modalTaskDetail.close();
    }

    btnOk.onclick = async () => {
        let dueDateValue = Math.floor(new Date(dueDate.value).getTime());

        const formData = new FormData();

        formData.append("id", task.id);
        formData.append("title", title.value);
        formData.append("description", description.value);
        formData.append("due_date", dueDateValue);

        await fetch("/api/tasks/update", {
            method: "POST",
            body: formData
        })
        .then((response) => {
            console.log(response);

            modalTaskDetail.close();
        });
    }

    window.onclick = (event) => {
        if (event.target == modalTaskDetail) {
            modalTaskDetail.close();
        }        
    }
}

Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0,10);
});