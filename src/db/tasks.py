from src.db.schemas import Task, UserTask
from sqlalchemy.orm import Session as DBSession


# Functions used for managing tasks that are available for users to choose.
# --------------------------------------------------------------------------------------
def add_task(db_session: DBSession, description: str, reward: int) -> Task:
    """Add a task to the database."""
    task = Task(description=description, reward=reward)
    db_session.add(task)
    db_session.commit()
    return task


def remove_task(db_session: DBSession, task_id: int) -> None:
    """Remove a task from the database."""
    task = db_session.query(Task).filter(Task.id == task_id).first()
    if task is None:
        return
    db_session.delete(task)
    db_session.commit()
    return


def get_all_tasks(db_session: DBSession) -> list[Task]:
    """Get all tasks."""
    return db_session.query(Task).all()


def get_task_by_id(db_session: DBSession, task_id: int) -> Task | None:
    """Get a task by its ID."""
    return db_session.query(Task).filter(Task.id == task_id).first()


# Functions for managing tasks that users have chosen.
# --------------------------------------------------------------------------------------
def add_user_task(db_session: DBSession, user_id: int, task_id: int) -> UserTask:
    """Add a task to a user."""
    user_task = UserTask(user=user_id, task=task_id, completed=False)
    db_session.add(user_task)
    db_session.commit()
    return user_task


def get_user_task_by_id(db_session: DBSession, user_task_id: int) -> UserTask | None:
    """Get a user task by its ID."""
    return db_session.query(UserTask).filter(UserTask.id == user_task_id).first()


def set_user_task_completed(db_session: DBSession, user_task_id: int) -> None:
    """Mark a user task as completed."""
    user_task = db_session.query(UserTask).filter(UserTask.id == user_task_id).first()
    if user_task is None:
        return  # TODO Probably raise an error here.
    user_task.completed = True
    db_session.commit()
    return


def user_has_completed_task(db_session: DBSession, user_id: int, task_id: int) -> bool:
    """Check if a user has completed a task."""
    return (
        db_session.query(UserTask)
        .filter(
            UserTask.user == user_id,
            UserTask.task == task_id,
            UserTask.completed == True,
        )
        .count()
        == 1
    )


def recommended_tasks_for_user(
    db_session: DBSession, user_id: int, min_amount: int
) -> list[Task]:
    """Get the recommended tasks for a user.

    Puts the tasks that the user has not completed at the top.
    """
    # Return tasks that the user has not completed.
    user_tasks = db_session.query(UserTask).filter(UserTask.user == user_id).all()
    user_tasks = [user_task.task for user_task in user_tasks]
    tasks = db_session.query(Task).filter(Task.id.notin_(user_tasks)).all()
    if len(tasks) >= min_amount:
        return tasks

    # Return tasks that the user has completed.
    return db_session.query(Task).filter(Task.id.in_(user_tasks)).all()
