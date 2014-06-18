"""empty message

Revision ID: 1e1a3cb99a90
Revises: None
Create Date: 2014-03-25 20:48:09.030044

"""

# revision identifiers, used by Alembic.
revision = '1e1a3cb99a90'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('version', sa.DateTime, nullable=False),
        sa.Column('creation_date', sa.DateTime, nullable=False),
        sa.Column('updated_by', sa.String(120), nullable=True),
        sa.Column('first_name', sa.String(50), nullable=False),
        sa.Column('last_name', sa.String(50), nullable=False),
        sa.Column('birth_date', sa.Date, nullable=False),
        sa.Column('email', sa.String(50), unique=True),
        sa.Column('password', sa.String(20), nullable=False),
        sa.Column('active', sa.Boolean, default=False),
        sa.Column('admin', sa.Boolean, default=False),
        sa.Column('last_login_at', sa.DateTime, nullable=True),
        sa.Column('current_login_at', sa.DateTime, nullable=True),
        sa.Column('last_login_ip', sa.String(16), nullable=True),
        sa.Column('current_login_ip', sa.String(16), nullable=True),
        sa.Column('confirmed_at', sa.DateTime, nullable=True),
        sa.Column('login_count', sa.Integer, nullable=True),
    )

    op.create_table(
        'roles',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('version', sa.DateTime, nullable=False),
        sa.Column('creation_date', sa.DateTime, nullable=False),
        sa.Column('updated_by', sa.String(120), nullable=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.String(200), nullable=True),
    )

    op.create_table(
        'roles_users',
        sa.Column('user_id', sa.Integer,
                  sa.ForeignKey('roles.id', name='fk_role_user_role_id'),
                  nullable=False),
        sa.Column('role_id', sa.Integer,
                  sa.ForeignKey('users.id', name='fk_role_user_user_id'),
                  nullable=False),
        sa.UniqueConstraint('user_id', 'role_id', name="roles_users_uk")
    )


def downgrade():
    op.drop_table('roles_users')
    op.drop_table('users')
    op.drop_table('roles')
