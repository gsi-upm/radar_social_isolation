FROM python:3.9-slim-buster

WORKDIR /app

COPY mlp_cl.pkl .
COPY modelo_mlp.pkl .
COPY modelo_vt.pkl .
COPY scaler_mlp.pkl .
COPY scaler_voting_clf.pkl .
COPY scaler_vt.pkl .
COPY scalermlp_cl.pkl .
COPY voting_clf.pkl .