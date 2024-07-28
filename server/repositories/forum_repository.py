from datetime import datetime

from sqlmodel import Session, col, select
from server.models.database.forum_db_model import ForumPost, MobileUser

class ForumRepository:
    @staticmethod
    def create(
        *, input: ForumPost,
        session: Session
    ) -> ForumPost:
        new_post = input
        new_post.created_at = datetime.now()
        new_post.report_count = 0
        # new_post.reported_users = []

        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        return new_post


    @staticmethod
    def get_all_posts(*,class_id: int, session: Session) -> list[ForumPost]:
        statement = select(ForumPost).where(col(ForumPost.class_id)==class_id)
        posts = session.exec(statement).all()
        return list(posts)
    
    @staticmethod
    def get_post_by_id(*,post_id: int, session: Session) -> ForumPost:
        statement = select(ForumPost).where(col(ForumPost.id)==post_id)
        post = session.exec(statement).first()
        return post
    
    @staticmethod
    def update_forum_report_count(*, post_id:int , mobile_user_id: int , session:Session) -> ForumPost:
        statement = select(ForumPost).where(col(ForumPost.id)==post_id)
        post = session.exec(statement).first()

        # user_statement = select(MobileUser).where(col(MobileUser.id)==mobile_user_id)
        # reported_mobile_user = session.exec(user_statement).first()
        post.report_count += 1

        session.add(post)
        session.commit()
        session.refresh(post)

        return post
