from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class ProjectList(Base):
    __tablename__ = "projects_list"
    id = Column(Integer, index=True, primary_key=True)
    title = Column(String)
    short_desc = Column(String)
    img_url = Column(String)


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    desc = Column(String)
    github = Column(String)
    key_feature = Column(String)
    tech = relationship("Tech", back_populates="project", cascade="all, delete-orphan")
    img = relationship("Image", back_populates="project", cascade="all, delete-orphan")

class Tech(Base):
    __tablename__ = "tech_used"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    tech = Column(String)

    project = relationship("Project", back_populates="tech")

class Image(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=True)
    skill_id = Column(Integer, ForeignKey("skill.id", ondelete="CASCADE"), nullable=True)
    certificate_id = Column(Integer, ForeignKey("certificate.id", ondelete="CASCADE"), nullable=True)
    img_url = Column(String)

    project = relationship("Project", back_populates="img")
    skill = relationship("Skill", back_populates="img_url")
    certificate = relationship("Certificate", back_populates="img_url")


class Certificate(Base):
    __tablename__ = "certificate"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    by = Column(String)
    links = Column(String)
    
    img_url = relationship("Image", back_populates="certificate", cascade="all, delete-orphan")

class Skill(Base):
    __tablename__ = "skill"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    category = Column(String)
    level = Column(Integer)
    desc = Column(String)
    use_case = Column(ARRAY(String))
    link = Column(String)
    learning_difficulity = Column(Integer)

    img_url = relationship("Image", back_populates="skill", cascade="all, delete-orphan")


