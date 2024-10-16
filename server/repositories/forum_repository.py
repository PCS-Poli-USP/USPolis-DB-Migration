from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, col, select
from server.models.database.forum_db_model import ForumPost 
from server.models.database.forum_post_report_link import ForumPostReportLink


class ForumRepository:
    @staticmethod
    def create(*, input: ForumPost, session: Session) -> ForumPost:
        new_post = input
        new_post.created_at = datetime.now()
        new_post.report_count = 0

        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        return new_post

    @staticmethod
    def get_all_posts(*, subject_id: int, session: Session) -> list[ForumPost]:
        statement = select(ForumPost).where(
            col(ForumPost.subject_id)==subject_id, 
            col(ForumPost.reply_of_post_id)==None,
            col(ForumPost.enabled) == True)
        posts = session.exec(statement).all()
        return list(posts)

    @staticmethod
    def get_post_by_id(*, post_id: int, session: Session) -> ForumPost:
        statement = select(ForumPost).where(col(ForumPost.id) == post_id, col(ForumPost.enabled) == True)
        post = session.exec(statement).one()
        return post

    @staticmethod
    def disable_post(*, post_id: int, session: Session):
        statement = select(ForumPost).where(col(ForumPost.id) == post_id)
        post = session.exec(statement).one()
        
        post.enabled = False

        session.add(post)
        session.commit()

    @staticmethod
    def update_forum_report_count(
        *, post_id: int, mobile_user_id: int, session: Session
    ) -> ForumPost:
        statement = select(ForumPost).where(col(ForumPost.id) == post_id)

        user_statement = select(ForumPostReportLink).where(
            col(ForumPostReportLink.mobile_user_id)==mobile_user_id,
            col(ForumPostReportLink.forum_post_id)==post_id)
            
        post = session.exec(statement).one()
        reported_post = session.exec(user_statement).first()

        if reported_post == None :
            # Did NOT found a report for this user and post!

            # Count reports for this post
            reports_statement = select(ForumPostReportLink).where(
                col(ForumPostReportLink.forum_post_id)==post_id)
            reports_count = len(list(session.exec(reports_statement).all())) + 1 # Adds the current report to counter
            post.report_count = reports_count
            
            # Create new report for this post and user
            new_reported_post = ForumPostReportLink(forum_post_id=post_id, mobile_user_id=mobile_user_id)

            session.add(new_reported_post)
            session.add(post)
            session.commit()
            session.refresh(post)

        return post

    @staticmethod
    def create_reply(*, input: ForumPost, session: Session):
        try:
            # Gets, and counts, all replies from this post (except this new one)
            replies_statement = select(ForumPost).where(col(ForumPost.reply_of_post_id) == input.reply_of_post_id)
            replies_count = len(list(session.exec(replies_statement).all())) + 1 # Adds the current reply to counter
            post = session.exec(select(ForumPost).where(col(ForumPost.id) == input.reply_of_post_id)).first()
            
            post.replies_count = replies_count
            
            input.created_at = datetime.now()
            
            session.add(input)
            session.add(post)
            session.commit()
        except IntegrityError:
            raise PostNotFoundException(input.reply_of_post_id)

        session.refresh(input)
        return input

    @staticmethod
    def get_all_replies(*, post_id: int ,session: Session):
        statement = select(ForumPost).where(
            col(ForumPost.reply_of_post_id)==post_id,
            col(ForumPost.enabled) == True)
        replies = session.exec(statement).all()
        return list(replies)

class PostNotFoundException(HTTPException):
    def __init__(self, post_id: int) -> None:
        super().__init__(
            status.HTTP_404_NOT_FOUND, f"Forum Post {post_id} does not exists"
        )
