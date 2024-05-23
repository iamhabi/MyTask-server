#[macro_use]
extern crate rocket;

use rocket::{form::Context, fs::{ relative, FileServer }};
use rocket_dyn_templates::Template;

mod api;

#[get("/")]
async fn home() -> Template {
    Template::render("home", &Context::default())
}

#[rocket::launch]
pub fn rocket() -> _ {
    let routes = routes![
        api::shutdown,
        api::get_groups, api::create_group, api::delete_group, api::update_group,
        api::get_tasks, api::get_task, api::create_task, api::delete_task, api::update_task
    ];

    rocket::build()
        .mount("/", routes![home])
        .mount("/api", routes)
        .mount("/static", FileServer::from(relative!("static")))
        .attach(Template::fairing())
}