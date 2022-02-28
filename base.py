from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine = create_engine('postgres://jiyerqtkdtzmiq:b0b8a7677c2904fe4e37412e1452190cc4368512c9ad0542071835b7ac713ec3@ec2-54-220-243-77.eu-west-1.compute.amazonaws.com:5432/dbh08b84org3rp')
Session = sessionmaker(bind=engine)

Base = declarative_base()