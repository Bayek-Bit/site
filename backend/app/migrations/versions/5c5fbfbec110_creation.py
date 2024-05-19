"""creation

Revision ID: 5c5fbfbec110
Revises: 
Create Date: 2024-05-18 22:39:25.777620

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c5fbfbec110'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('class',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subject',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('father_name', sa.String(), nullable=False),
    sa.Column('class_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teacher',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('father_name', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('homework',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=False),
    sa.Column('class_id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.Column('task', sa.String(length=250), nullable=False),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mark',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.Column('mark', sa.Integer(), nullable=True),
    sa.Column('attendance', sa.String(length=1), nullable=True),
    sa.Column('set_date', sa.DateTime(), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.CheckConstraint('(mark IS NOT NULL AND attendance IS NULL) OR (mark IS NULL AND attendance IS NOT NULL)', name='check_mark_or_attendance'),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teacher_class',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=False),
    sa.Column('class_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teacher_subject',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('timetable',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('day_of_week', sa.String(length=50), nullable=False),
    sa.Column('class_id', sa.Integer(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=False),
    sa.Column('lesson_number', sa.Integer(), nullable=False),
    sa.Column('classroom_number', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.String(length=5), nullable=False),
    sa.Column('end_time', sa.String(length=5), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('timetable')
    op.drop_table('teacher_subject')
    op.drop_table('teacher_class')
    op.drop_table('mark')
    op.drop_table('homework')
    op.drop_table('teacher')
    op.drop_table('student')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('subject')
    op.drop_table('role')
    op.drop_table('class')
    # ### end Alembic commands ###
