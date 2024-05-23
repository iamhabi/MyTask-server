use rocket::Shutdown;
use rocket::{form::Form, http::Status, serde::json::Json};

use database;
use database::models::*;

#[get("/shutdown")]
pub fn shutdown(shutdown: Shutdown) {
    shutdown.notify();
}

#[get("/groups")]
pub fn get_groups() -> Json<Vec<Group>> {
    let groups = database::get_groups();

    Json(groups)
}

#[post("/groups?<title>")]
pub fn create_group(title: Option<&str>) -> (Status, Json<Group>) {
    let temp = Group {
        id: -1,
        title: String::from("")
    };

    let title: &str = match title {
        Some(t) => t,
        None => {
            return (Status::BadRequest, Json(temp));
        }
    };

    let result = database::create_group(title);

    match result {
        Ok(_) => {
            let created_group = result.unwrap();
            return (Status::Ok, Json(created_group));
        },
        Err(_) => (Status::BadRequest, Json(temp))
    }
}

#[delete("/groups?<id>")]
pub fn delete_group(id: Option<i32>) -> Status {
    let id = match id {
        Some(id) => id,
        None => {
            return Status::BadRequest;
        }
    };

    let result = database::delete_group(id);

    match result {
        Ok(_) => Status::Ok,
        Err(_) => Status::BadRequest
    }
}

#[put("/groups?<id>&<title>")]
pub fn update_group(id: Option<i32>, title: Option<&str>) -> Status {
    let id = match id {
        Some(id) => id,
        None => {
            return Status::BadRequest;
        }
    };

    let new_title: &str = match title {
        Some(t) => t,
        None => {
            return Status::BadRequest;
        }
    };

    let result = database::update_group(id, new_title);

    match result {
        Ok(_) => Status::Ok,
        Err(_) => Status::BadRequest
    }
}

#[get("/tasks?<group_id>")]
pub fn get_tasks(group_id: Option<i32>) -> (Status, Json<Vec<Task>>) {
    let group_id = match group_id {
        Some(g) => g,
        None => {
            return (Status::BadRequest, Json(vec![]));
        }
    };

    let result = database::get_tasks(group_id);

    match result {
        Ok(tasks) => (Status::Ok, Json(tasks)),
        Err(_) => (Status::BadRequest, Json(vec![]))
    }
}

#[get("/tasks/detail?<task_id>")]
pub fn get_task(task_id: Option<i32>) -> (Status, Json<Vec<Task>>) {
    let task_id = match task_id {
        Some(g) => g,
        None => {
            return (Status::BadRequest, Json(vec![]));
        }
    };

    let result = database::get_task(task_id);

    match result {
        Ok(tasks) => (Status::Ok, Json(tasks)),
        Err(_) => (Status::BadRequest, Json(vec![]))
    }
}

#[post("/tasks", format = "multipart/form-data", data = "<form>")]
pub fn create_task(form: Form<NewTask>) -> (Status, Json<Task>) {
    let task = form.into_inner();

    let result = database::create_task(task);

    match result {
        Ok(_) => {
            let created_task = result.unwrap();

            return (Status::Ok, Json(created_task));
        },
        Err(_) => {
            let error = result.err();

            println!("{:?}", error);

            let temp = Task {
                id: -1,
                title: String::from(""),
                is_done: String::from("false"),
                group_id: -1,
                description: String::from(""),
                created: String::from("0"),
                due_date: String::from("0")
            };

            return (Status::BadRequest, Json(temp))
        }
    }
}

#[delete("/tasks?<id>")]
pub fn delete_task(id: Option<i32>) -> Status {
    let id = match id {
        Some(id) => id,
        None => {
            return Status::BadRequest;
        }
    };

    let result = database::delete_task(id);

    match result {
        Ok(_) => Status::Ok,
        Err(_) => Status::BadRequest
    }
}

#[put("/tasks", format = "multipart/form-data", data = "<form>")]
pub fn update_task(form: Form<UpdateTask>) -> Status {
    let task = form.into_inner();

    let result = database::update_task(task);

    match result {
        Ok(_) => Status::Ok,
        Err(_) => Status::BadRequest
    }
}
