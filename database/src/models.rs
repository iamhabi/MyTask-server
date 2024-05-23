use diesel::prelude::*;
use rocket::FromForm;
use serde::{Deserialize, Serialize};
use crate::schema::{tasks, groups};

#[derive(Queryable, Selectable, Debug, Serialize, Deserialize, FromForm)]
#[diesel(table_name = tasks)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct Task {
    pub id: i32,
    pub title: String,
    pub is_done: String,
    pub group_id: i32,
    pub description: String,
    pub created: String,
    pub due_date: String,
}

#[derive(Queryable, Selectable, Debug, Serialize, Deserialize, FromForm)]
#[diesel(table_name = groups)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct Group {
    pub id: i32,
    pub title: String
}

#[derive(Debug, Serialize, Deserialize, FromForm)]
#[derive(Insertable)]
#[diesel(table_name = tasks)]
pub struct NewTask<'a> {
    pub title: &'a str,
    pub is_done: String,
    pub group_id: i32,
    pub description: String,
    pub created: String,
    pub due_date: String,
}

#[derive(Debug, Serialize, Deserialize, FromForm)]
pub struct UpdateTask {
    pub id: i32,
    pub title: String,
    pub is_done: String,
    pub description: String,
    pub due_date: String,
}

#[derive(Insertable)]
#[diesel(table_name = groups)]
pub struct NewGroup<'a> {
    pub title: &'a str
}