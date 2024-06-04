FROM rust:1.78

WORKDIR /var/MyTask-server

RUN cargo install diesel_cli --no-default-features --features postgres
    
WORKDIR /var/MyTask-server/database

ENTRYPOINT diesel setup &&\
    cargo run --bin server
