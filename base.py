from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgres://wfasqssjtdjinv:e74fce4710d23c30872f19923aecab934c9a7cfd6e2ee02cab3ad49d440cf415@ec2-52-214-125-106.eu-west-1.compute.amazonaws.com:5432/d28lqknqnpun53')
Session = sessionmaker(bind=engine)

Base = declarative_base()
