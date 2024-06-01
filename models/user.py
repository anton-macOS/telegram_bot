from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from db.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    email = Column(String, nullable=False, unique=True)
    discord_nick = Column(String, nullable=False, unique=True)
    postal_address = Column(String, nullable=False)
    adaptation_start_date = Column(Date, nullable=False)
    work_start_date = Column(Date)
    assigned_stream = Column(String)  # example 44.1У or 6.2М...
    dismissal_date = Column(Date)
    admin_id = Column(Integer, ForeignKey('admins.id'))
    work_tg_nick = Column(String, nullable=True, unique=True)
    personal_tg_nick = Column(String, nullable=False, unique=True)
    photo = Column(String, nullable=True)

    onboarding_stages = relationship('OnboardingStage', back_populates='user')
    admin = relationship('Admin', back_populates='users')

    def __repr__(self):
        return f"<User(full_name='{self.full_name}', email='{self.email}')>"


class OnboardingStage(Base):
    __tablename__ = 'onboarding_stages'

    id = Column(Integer, primary_key=True, index=True)
    stage_name = Column(String, nullable=False)
    status = Column(Enum('in_progress', 'completed', name='status_enum'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='onboarding_stages')

    def __repr__(self):
        return f"<OnboardingStage(stage_name='{self.stage_name}', status='{self.status}')>"


class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    full_name = Column(String, nullable=False)
    work_start_date = Column(Date, nullable=False)
    dismissal_date = Column(Date)
    personal_tg_nick = Column(String, nullable=False, unique=True)
    users = relationship('User', back_populates='admin')

    def __repr__(self):
        return f"<Admin(full_name='{self.full_name}', email='{self.email}')>"
