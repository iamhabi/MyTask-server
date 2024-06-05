FROM rust:1.78

WORKDIR /mytask-server

RUN cargo install diesel_cli --no-default-features --features postgres
    
WORKDIR /mytask-server/database

ENTRYPOINT diesel setup &&\
    cd .. &&\
    cargo run --bin server
