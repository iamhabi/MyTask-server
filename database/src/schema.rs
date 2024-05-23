// @generated automatically by Diesel CLI.

diesel::table! {
    groups (id) {
        id -> Int4,
        title -> Text,
    }
}

diesel::table! {
    tasks (id) {
        id -> Int4,
        title -> Text,
        is_done -> Text,
        group_id -> Int4,
        description -> Text,
        created -> Text,
        due_date -> Text,
    }
}
