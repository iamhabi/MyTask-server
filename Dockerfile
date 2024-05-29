FROM rust:1.78

WORKDIR /

RUN cargo install diesel_cli --no-default-features --features postgres &&\
    git clone https://github.com/iamhabi/MyTask-server.git
    
WORKDIR /MyTask-server/database

ENTRYPOINT diesel setup &&\
    cd /MyTask-server &&\
    cargo run --bin server
