"""Initial schema for Mastery

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-08-29 04:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # organizations
    op.create_table('organizations',
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('organization_id')
    )
    op.create_index(op.f('ix_organizations_organization_id'), 'organizations', ['organization_id'], unique=False)

    # users
    op.create_table('users',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('organization_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.organization_id']),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=False)

    # courses
    op.create_table('courses',
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('creator_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('mastery_target', sa.Numeric(5, 2), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
        sa.ForeignKeyConstraint(['creator_id'], ['users.user_id']),
        sa.PrimaryKeyConstraint('course_id')
    )
    op.create_index(op.f('ix_courses_course_id'), 'courses', ['course_id'], unique=False)

    # scenarios
    op.create_table('scenarios',
        sa.Column('scenario_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('context', sa.Text(), nullable=False),
        sa.Column('decision_point', sa.Text(), nullable=False),
        sa.Column('scenario_type', sa.String(), nullable=True),
        sa.Column('difficulty', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.ForeignKeyConstraint(['course_id'], ['courses.course_id']),
        sa.PrimaryKeyConstraint('scenario_id')
    )
    op.create_index(op.f('ix_scenarios_scenario_id'), 'scenarios', ['scenario_id'], unique=False)

    # decision_branches
    op.create_table('decision_branches',
        sa.Column('branch_id', sa.Integer(), nullable=False),
        sa.Column('scenario_id', sa.Integer(), nullable=False),
        sa.Column('choice_text', sa.Text(), nullable=False),
        sa.Column('consequence', sa.Text(), nullable=False),
        sa.Column('is_optimal', sa.Boolean(), nullable=True),
        sa.Column('socratic_prompt', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['scenario_id'], ['scenarios.scenario_id']),
        sa.PrimaryKeyConstraint('branch_id')
    )
    op.create_index(op.f('ix_decision_branches_branch_id'), 'decision_branches', ['branch_id'], unique=False)

    # learner_interactions
    op.create_table('learner_interactions',
        sa.Column('interaction_id', sa.Integer(), nullable=False),
        sa.Column('learner_id', sa.Integer(), nullable=False),
        sa.Column('scenario_id', sa.Integer(), nullable=False),
        sa.Column('branch_chosen', sa.Integer(), nullable=False),
        sa.Column('accuracy', sa.Integer(), nullable=True),
        sa.Column('time_spent_seconds', sa.Numeric(10, 2), nullable=True),
        sa.Column('hints_used', sa.String(), nullable=True),
        sa.Column('cognitive_load_signal', sa.String(), nullable=True),
        sa.Column('reflection_text', sa.Text(), nullable=True),
        sa.Column('reflective_writing_score', sa.Numeric(5, 2), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.ForeignKeyConstraint(['branch_chosen'], ['decision_branches.branch_id']),
        sa.ForeignKeyConstraint(['learner_id'], ['users.user_id']),
        sa.ForeignKeyConstraint(['scenario_id'], ['scenarios.scenario_id']),
        sa.PrimaryKeyConstraint('interaction_id')
    )
    op.create_index(op.f('ix_learner_interactions_interaction_id'), 'learner_interactions', ['interaction_id'], unique=False)

    # mastery_progress
    op.create_table('mastery_progress',
        sa.Column('progress_id', sa.Integer(), nullable=False),
        sa.Column('learner_id', sa.Integer(), nullable=False),
        sa.Column('scenario_id', sa.Integer(), nullable=False),
        sa.Column('attempts', sa.Integer(), nullable=True),
        sa.Column('success_rate', sa.Numeric(5, 2), nullable=True),
        sa.Column('last_practiced_at', sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
        sa.Column('mastery_achieved_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['learner_id'], ['users.user_id']),
        sa.ForeignKeyConstraint(['scenario_id'], ['scenarios.scenario_id']),
        sa.PrimaryKeyConstraint('progress_id')
    )
    op.create_index(op.f('ix_mastery_progress_progress_id'), 'mastery_progress', ['progress_id'], unique=False)

    # course_analytics
    op.create_table('course_analytics',
        sa.Column('analytics_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('total_learners', sa.Integer(), nullable=True),
        sa.Column('completion_rate', sa.Numeric(5, 2), nullable=True),
        sa.Column('mastery_rate', sa.Numeric(5, 2), nullable=True),
        sa.Column('average_attempts_to_mastery', sa.Numeric(5, 2), nullable=True),
        sa.Column('drop_off_scenario_id', sa.Integer(), nullable=True),
        sa.Column('cognitive_load_score', sa.Numeric(5, 2), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.course_id']),
        sa.ForeignKeyConstraint(['drop_off_scenario_id'], ['scenarios.scenario_id']),
        sa.PrimaryKeyConstraint('analytics_id')
    )
    op.create_index(op.f('ix_course_analytics_analytics_id'), 'course_analytics', ['analytics_id'], unique=False)


def downgrade() -> None:
    op.drop_table('course_analytics')
    op.drop_table('mastery_progress')
    op.drop_table('learner_interactions')
    op.drop_table('decision_branches')
    op.drop_table('scenarios')
    op.drop_table('courses')
    op.drop_table('users')
    op.drop_table('organizations')
