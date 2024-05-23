use diesel::result::Error;
use diesel::{ Connection, PgConnection, RunQueryDsl, SelectableHelper };
use diesel::prelude::*;
use dotenvy::dotenv;
use std::env;

use self::models::*;

pub mod models;
pub mod schema;

pub fn establish_connection() -> PgConnection {
    dotenv().ok();

    let db_url = env::var("DATABASE_URL")
        .expect("Failed to get url");

    PgConnection::establish(&db_url)
        .unwrap_or_else(|_| panic!("Error connecting to database"))
}

pub fn get_groups() -> Vec<Group> {
    use self::schema::groups::dsl::*;

    let connection = &mut establish_connection();

    groups
        .select(Group::as_select())
        .load(connection)
        .expect("Error loading groups")
}

pub fn create_group(title: &str) -> Result<Group, Error> {
    use crate::schema::groups;

    let connection = &mut establish_connection();

    let group = NewGroup {
        title
    };

    diesel::insert_into(groups::table)
        .values(&group)
        .returning(Group::as_returning())
        .get_result(connection)
}

pub fn update_group(id: i32, title: &str) -> Result<usize, Error> {
    use crate::schema::groups;

    let connection = &mut establish_connection();

    let source = groups::table.filter(groups::id.eq(id));

    diesel::update(source)
        .set(groups::title.eq(title))
        .execute(connection)
}

pub fn delete_group(id: i32) -> Result<usize, Error> {
    use crate::schema::groups;
    use crate::schema::tasks;

    let connection = &mut establish_connection();

    let groups_source = groups::table.filter(groups::id.eq(id));
    let tasks_source = tasks::table.filter(tasks::group_id.eq(id));

    let _ = diesel::delete(tasks_source)
        .execute(connection);

    diesel::delete(groups_source)
        .execute(connection)
}

pub fn get_tasks(group_id: i32) -> Result<Vec<Task>, Error> {
    let connection = &mut establish_connection();

    self::schema::tasks::dsl::tasks
        .select(Task::as_select())
        .filter(schema::tasks::group_id.eq(group_id))
        .load(connection)
}

pub fn get_task(task_id: i32) -> Result<Vec<Task>, Error> {
    let connection = &mut establish_connection();
    
    self::schema::tasks::dsl::tasks
        .select(Task::as_select())
        .filter(schema::tasks::id.eq(task_id))
        .limit(1)
        .load(connection)
}

pub fn create_task(task: NewTask) -> Result<Task, Error> {
    use crate::schema::tasks;

    let connection = &mut establish_connection();

    diesel::insert_into(tasks::table)
        .values(&task)
        .returning(Task::as_returning())
        .get_result(connection)
}

pub fn update_task(task: UpdateTask) -> Result<usize, Error> {
    use crate::schema::tasks;

    let connection = &mut establish_connection();

    let source = tasks::table.filter(schema::tasks::id.eq(task.id));

    diesel::update(source)
        .set((
            schema::tasks::title.eq(task.title),
            schema::tasks::is_done.eq(task.is_done),
            schema::tasks::description.eq(task.description),
            schema::tasks::due_date.eq(task.due_date),
        ))
        .execute(connection)
}

pub fn delete_task(id: i32) -> Result<usize, Error> {
    use crate::schema::tasks;

    let connection = &mut establish_connection();

    let source = tasks::table.filter(schema::tasks::id.eq(id));

    diesel::delete(source)
        .execute(connection)
}