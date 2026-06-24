from typing import Optional
import datetime
import decimal
import uuid

from sqlalchemy import (
    Boolean,
    CHAR,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKeyConstraint,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    String,
    Table,
    Text,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Coupons(Base):
    __tablename__ = "coupons"
    __table_args__ = (
        CheckConstraint(
            "discount_type::text = ANY (ARRAY['percent'::character varying::text, 'fixed'::character varying::text])",
            name="coupons_discount_type_check",
        ),
        CheckConstraint(
            "discount_value > 0::numeric", name="coupons_discount_value_check"
        ),
        CheckConstraint(
            "max_redemptions IS NULL OR max_redemptions >= 0",
            name="coupons_max_redemptions_check",
        ),
        PrimaryKeyConstraint("id", name="coupons_pkey"),
        UniqueConstraint("code", name="coupons_code_key"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    discount_type: Mapped[str] = mapped_column(String(20), nullable=False)
    discount_value: Mapped[decimal.Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    is_first_purchase_only: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("true")
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("now()")
    )
    description: Mapped[Optional[str]] = mapped_column(Text)
    max_redemptions: Mapped[Optional[int]] = mapped_column(Integer)
    starts_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ends_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    subscriptions: Mapped[list["Subscriptions"]] = relationship(
        "Subscriptions", back_populates="applied_coupon"
    )
    coupon_redemptions: Mapped[list["CouponRedemptions"]] = relationship(
        "CouponRedemptions", back_populates="coupon"
    )


class Profiles(Base):
    __tablename__ = "profiles"
    __table_args__ = (
        CheckConstraint(
            "questions_create_limit >= 0", name="profiles_questions_create_limit_check"
        ),
        PrimaryKeyConstraint("id", name="profiles_pkey"),
        UniqueConstraint("name", name="profiles_name_key"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("now()")
    )
    questions_create_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    subscriptions: Mapped[list["Subscriptions"]] = relationship(
        "Subscriptions", back_populates="profile"
    )


class QuestionAssets(Base):
    __tablename__ = "question_assets"
    __table_args__ = (
        CheckConstraint(
            "\"position\"::text = ANY (ARRAY['before_statement'::character varying, 'after_statement'::character varying]::text[])",
            name="question_assets_position_check",
        ),
        CheckConstraint(
            "asset_type::text = ANY (ARRAY['text'::character varying, 'table'::character varying, 'chart'::character varying, 'image'::character varying, 'map'::character varying, 'diagram'::character varying, 'infographic'::character varying]::text[])",
            name="question_assets_asset_type_check",
        ),
        CheckConstraint(
            "rendering_mode::text = ANY (ARRAY['inline_text'::character varying, 'structured_data'::character varying, 'generated_image'::character varying]::text[])",
            name="question_assets_rendering_mode_check",
        ),
        CheckConstraint(
            "storage_status::text = ANY (ARRAY['not_required'::character varying, 'pending_storage_configuration'::character varying, 'stored'::character varying, 'generation_failed'::character varying]::text[])",
            name="question_assets_storage_status_check",
        ),
        PrimaryKeyConstraint("id", name="question_assets_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    asset_type: Mapped[str] = mapped_column(String(20), nullable=False)
    rendering_mode: Mapped[str] = mapped_column(String(20), nullable=False)
    position: Mapped[str] = mapped_column(String(30), nullable=False)
    display_order: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )
    storage_status: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        server_default=text("'not_required'::character varying"),
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("now()")
    )
    title: Mapped[Optional[str]] = mapped_column(Text)
    caption: Mapped[Optional[str]] = mapped_column(Text)
    alt_text: Mapped[Optional[str]] = mapped_column(Text)
    source_label: Mapped[Optional[str]] = mapped_column(Text)
    content: Mapped[Optional[str]] = mapped_column(Text)
    storage_provider: Mapped[Optional[str]] = mapped_column(String(30))
    storage_key: Mapped[Optional[str]] = mapped_column(Text)
    public_url: Mapped[Optional[str]] = mapped_column(Text)
    mime_type: Mapped[Optional[str]] = mapped_column(String(100))
    metadata_: Mapped[Optional[dict]] = mapped_column("metadata", JSONB)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    question_asset_questions: Mapped[list["QuestionAssetQuestions"]] = relationship(
        "QuestionAssetQuestions", back_populates="question_asset"
    )


class Questions(Base):
    __tablename__ = "questions"
    __table_args__ = (
        CheckConstraint(
            "correct_answer = ANY (ARRAY['A'::bpchar, 'B'::bpchar, 'C'::bpchar, 'D'::bpchar, 'E'::bpchar])",
            name="questions_correct_answer_check",
        ),
        PrimaryKeyConstraint("id", name="questions_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    topic: Mapped[str] = mapped_column(String(100), nullable=False)
    subtopic: Mapped[str] = mapped_column(Text, nullable=False)
    subtopic_description: Mapped[str] = mapped_column(Text, nullable=False)
    diversity_mode: Mapped[str] = mapped_column(Text, nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer_a: Mapped[str] = mapped_column(Text, nullable=False)
    answer_b: Mapped[str] = mapped_column(Text, nullable=False)
    answer_c: Mapped[str] = mapped_column(Text, nullable=False)
    answer_d: Mapped[str] = mapped_column(Text, nullable=False)
    explanation_a: Mapped[str] = mapped_column(Text, nullable=False)
    explanation_b: Mapped[str] = mapped_column(Text, nullable=False)
    explanation_c: Mapped[str] = mapped_column(Text, nullable=False)
    explanation_d: Mapped[str] = mapped_column(Text, nullable=False)
    correct_answer: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("now()")
    )
    answer_e: Mapped[Optional[str]] = mapped_column(Text)
    explanation_e: Mapped[Optional[str]] = mapped_column(Text)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    user: Mapped[list["Users"]] = relationship(
        "Users", secondary="favorite_questions", back_populates="question"
    )
    question_answers: Mapped[list["QuestionAnswers"]] = relationship(
        "QuestionAnswers", back_populates="question"
    )
    question_asset_questions: Mapped[list["QuestionAssetQuestions"]] = relationship(
        "QuestionAssetQuestions", back_populates="question"
    )
    question_feedbacks: Mapped[list["QuestionFeedbacks"]] = relationship(
        "QuestionFeedbacks", back_populates="question"
    )


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="users_pkey"),
        UniqueConstraint("cpf_hash", name="users_cpf_hash_key"),
        UniqueConstraint("email_hash", name="users_email_hash_key"),
        UniqueConstraint("nickname_hash", name="users_nickname_hash_key"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    cpf: Mapped[str] = mapped_column(Text, nullable=False)
    nickname: Mapped[str] = mapped_column(Text, nullable=False)
    email_hash: Mapped[str] = mapped_column(CHAR(64), nullable=False)
    cpf_hash: Mapped[str] = mapped_column(CHAR(64), nullable=False)
    nickname_hash: Mapped[str] = mapped_column(CHAR(64), nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    global_role: Mapped[str] = mapped_column(
        String(50), nullable=False, server_default=text("'User'::character varying")
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("now()")
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    question: Mapped[list["Questions"]] = relationship(
        "Questions", secondary="favorite_questions", back_populates="user"
    )
    question_answers: Mapped[list["QuestionAnswers"]] = relationship(
        "QuestionAnswers", back_populates="user"
    )
    subscriptions: Mapped[list["Subscriptions"]] = relationship(
        "Subscriptions", back_populates="user"
    )
    user_feedback: Mapped[list["UserFeedback"]] = relationship(
        "UserFeedback", back_populates="user"
    )
    coupon_redemptions: Mapped[list["CouponRedemptions"]] = relationship(
        "CouponRedemptions", back_populates="user"
    )


t_favorite_questions = Table(
    "favorite_questions",
    Base.metadata,
    Column("user_id", Uuid, primary_key=True),
    Column("question_id", Uuid, primary_key=True),
    ForeignKeyConstraint(
        ["question_id"], ["questions.id"], name="favorite_questions_question_id_fkey"
    ),
    ForeignKeyConstraint(
        ["user_id"], ["users.id"], name="favorite_questions_user_id_fkey"
    ),
    PrimaryKeyConstraint("user_id", "question_id", name="favorite_questions_pkey"),
)


class QuestionAnswers(Base):
    __tablename__ = "question_answers"
    __table_args__ = (
        CheckConstraint(
            "answer = ANY (ARRAY['A'::bpchar, 'B'::bpchar, 'C'::bpchar, 'D'::bpchar, 'E'::bpchar])",
            name="question_answers_answer_check",
        ),
        ForeignKeyConstraint(
            ["question_id"], ["questions.id"], name="question_answers_question_id_fkey"
        ),
        ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="question_answers_user_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="question_answers_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    question_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    answer: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("now()")
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    question: Mapped["Questions"] = relationship(
        "Questions", back_populates="question_answers"
    )
    user: Mapped["Users"] = relationship("Users", back_populates="question_answers")


class QuestionAssetQuestions(Base):
    __tablename__ = "question_asset_questions"
    __table_args__ = (
        ForeignKeyConstraint(
            ["question_asset_id"],
            ["question_assets.id"],
            ondelete="CASCADE",
            name="question_asset_questions_question_asset_id_fkey",
        ),
        ForeignKeyConstraint(
            ["question_id"],
            ["questions.id"],
            ondelete="CASCADE",
            name="question_asset_questions_question_id_fkey",
        ),
        PrimaryKeyConstraint(
            "question_id", "question_asset_id", name="question_asset_questions_pkey"
        ),
    )

    question_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    question_asset_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("now()")
    )

    question_asset: Mapped["QuestionAssets"] = relationship(
        "QuestionAssets", back_populates="question_asset_questions"
    )
    question: Mapped["Questions"] = relationship(
        "Questions", back_populates="question_asset_questions"
    )


class QuestionFeedbacks(Base):
    __tablename__ = "question_feedbacks"
    __table_args__ = (
        ForeignKeyConstraint(
            ["question_id"],
            ["questions.id"],
            name="question_feedbacks_question_id_fkey",
        ),
        PrimaryKeyConstraint("id", name="question_feedbacks_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    question_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    is_liked: Mapped[bool] = mapped_column(Boolean, nullable=False)
    feedback: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("now()")
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    question: Mapped["Questions"] = relationship(
        "Questions", back_populates="question_feedbacks"
    )


class Subscriptions(Base):
    __tablename__ = "subscriptions"
    __table_args__ = (
        CheckConstraint(
            "questions_generated_in_cycle <= questions_limit",
            name="subscriptions_questions_generated_within_limit_check",
        ),
        CheckConstraint(
            "questions_generated_in_cycle >= 0",
            name="subscriptions_questions_generated_in_cycle_check",
        ),
        CheckConstraint(
            "questions_limit >= 0", name="subscriptions_questions_limit_check"
        ),
        CheckConstraint(
            "status::text = ANY (ARRAY['active'::character varying::text, 'failed_payment'::character varying::text, 'canceled'::character varying::text, 'incomplete'::character varying::text, 'trialing'::character varying::text])",
            name="subscriptions_status_check",
        ),
        ForeignKeyConstraint(
            ["applied_coupon_id"],
            ["coupons.id"],
            name="subscriptions_applied_coupon_id_fkey",
        ),
        ForeignKeyConstraint(
            ["profile_id"], ["profiles.id"], name="subscriptions_profile_id_fkey"
        ),
        ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="subscriptions_user_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="subscriptions_pkey"),
        UniqueConstraint(
            "stripe_subscription_id", name="subscriptions_stripe_subscription_id_key"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    profile_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    stripe_subscription_id: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    price_id: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("now()")
    )
    questions_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    questions_generated_in_cycle: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )
    applied_coupon_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    stripe_customer_id: Mapped[Optional[str]] = mapped_column(Text)
    current_period_end: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    questions_generation_cycle_end: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    applied_coupon: Mapped[Optional["Coupons"]] = relationship(
        "Coupons", back_populates="subscriptions"
    )
    profile: Mapped["Profiles"] = relationship(
        "Profiles", back_populates="subscriptions"
    )
    user: Mapped["Users"] = relationship("Users", back_populates="subscriptions")
    coupon_redemptions: Mapped[Optional["CouponRedemptions"]] = relationship(
        "CouponRedemptions", uselist=False, back_populates="subscription"
    )


class UserFeedback(Base):
    __tablename__ = "user_feedback"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="user_feedback_user_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="user_feedback_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    text_feedback: Mapped[str] = mapped_column(Text, nullable=False)

    user: Mapped["Users"] = relationship("Users", back_populates="user_feedback")


class CouponRedemptions(Base):
    __tablename__ = "coupon_redemptions"
    __table_args__ = (
        ForeignKeyConstraint(
            ["coupon_id"], ["coupons.id"], name="coupon_redemptions_coupon_id_fkey"
        ),
        ForeignKeyConstraint(
            ["subscription_id"],
            ["subscriptions.id"],
            name="coupon_redemptions_subscription_id_fkey",
        ),
        ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="coupon_redemptions_user_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="coupon_redemptions_pkey"),
        UniqueConstraint(
            "coupon_id", "user_id", name="coupon_redemptions_coupon_user_key"
        ),
        UniqueConstraint(
            "subscription_id", name="coupon_redemptions_subscription_id_key"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    coupon_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    redeemed_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("now()")
    )
    subscription_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    discount_amount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))

    coupon: Mapped["Coupons"] = relationship(
        "Coupons", back_populates="coupon_redemptions"
    )
    subscription: Mapped[Optional["Subscriptions"]] = relationship(
        "Subscriptions", back_populates="coupon_redemptions"
    )
    user: Mapped["Users"] = relationship("Users", back_populates="coupon_redemptions")
