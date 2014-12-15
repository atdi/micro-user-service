"""empty message

Revision ID: 16701869471
Revises: None
Create Date: 2014-12-15 23:13:53.975770

"""

# revision identifiers, used by Alembic.
revision = '16701869471'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('version', mysql.DATETIME(), nullable=True),
    sa.Column('creation_date', mysql.DATETIME(), nullable=True),
    sa.Column('updated_by', mysql.VARCHAR(length=120), nullable=True),
    sa.Column('id', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('first_name', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('last_name', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('phone', mysql.VARCHAR(length=14), nullable=False),
    sa.Column('birth_date', sa.DATE(), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('password', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('admin', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('last_login_at', mysql.DATETIME(), nullable=True),
    sa.Column('current_login_at', mysql.DATETIME(), nullable=True),
    sa.Column('last_login_ip', mysql.VARCHAR(length=16), nullable=True),
    sa.Column('current_login_ip', mysql.VARCHAR(length=16), nullable=True),
    sa.Column('confirmed_at', mysql.DATETIME(), nullable=True),
    sa.Column('login_count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('customer_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )

    op.create_table('roles',
    sa.Column('version', mysql.DATETIME(), nullable=True),
    sa.Column('creation_date', mysql.DATETIME(), nullable=True),
    sa.Column('updated_by', mysql.VARCHAR(length=120), nullable=True),
    sa.Column('id', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=80), nullable=True),
    sa.Column('description', mysql.VARCHAR(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )

    op.create_table('roles_users',
    sa.Column('user_id', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('role_id', mysql.VARCHAR(length=255), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='roles_users_ibfk_2'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='roles_users_ibfk_1'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )

    op.create_table('countries',
    sa.Column('version', mysql.DATETIME(), nullable=True),
    sa.Column('creation_date', mysql.DATETIME(), nullable=True),
    sa.Column('updated_by', mysql.VARCHAR(length=120), nullable=True),
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('code', mysql.VARCHAR(length=3), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )

    op.create_table('regions',
    sa.Column('version', mysql.DATETIME(), nullable=True),
    sa.Column('creation_date', mysql.DATETIME(), nullable=True),
    sa.Column('updated_by', mysql.VARCHAR(length=120), nullable=True),
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('code', mysql.VARCHAR(length=3), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('country_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], name='regions_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )

    op.create_table('cities',
    sa.Column('version', mysql.DATETIME(), nullable=True),
    sa.Column('creation_date', mysql.DATETIME(), nullable=True),
    sa.Column('updated_by', mysql.VARCHAR(length=120), nullable=True),
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('region_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['region_id'], ['regions.id'], name='cities_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )

    op.create_table('customers',
    sa.Column('version', mysql.DATETIME(), nullable=True),
    sa.Column('creation_date', mysql.DATETIME(), nullable=True),
    sa.Column('updated_by', mysql.VARCHAR(length=120), nullable=True),
    sa.Column('id', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('vat_number', mysql.VARCHAR(length=30), nullable=False),
    sa.Column('phone', mysql.VARCHAR(length=14), nullable=False),
    sa.Column('address', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('iban', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('bank', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('swift', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('city_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], name='customers_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )

    ### end Alembic commands ###



def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cities')
    op.drop_table('countries')
    op.drop_table('customers')
    op.drop_table('regions')
    op.drop_table('roles')
    op.drop_table('roles_users')
    op.drop_table('users')
    ### end Alembic commands ###
