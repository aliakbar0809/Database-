import asyncio

from logic import registration, login, create_task, get_tasks, update_task,delete_task,get_task_by_id
from database import DatabaseConfig

login_status = False

async def main():
    db = DatabaseConfig(
        user='postgres',
        password='softclub1122',
        db_name='todo'
    )

    await db.connect()
    await db.create_tables()

    while True:
        print("""
        1. Registration
        2. Login
        """)

        choice = input('Choose one: ')
        if choice == '1':
            username = input('Enter your username: ')
            password = input('Enter your password: ')
            await registration(db, username, password)

        elif choice == '2':
            username = input('Enter your username: ')
            password = input('Enter your password: ')
            logged_user_id = await login(db, username, password)
            if logged_user_id:
                login_status = True

            while login_status:
                print("""
                1. Add task
                2. Get all tasks
                3. Update task
                4. Delete task
                5. Logout
                6. Get task by id
                """)

                choice = input('Choose one: ')
                if choice == '1':
                    title = input('Enter your title: ')
                    description = input('Enter your description: ')
                    await create_task(db, title, description, logged_user_id['id'])

                elif choice == '2':
                    tasks = await get_tasks(db, logged_user_id['id'])
                    for i, task in enumerate(tasks, 1):
                        print(f"{i}. {task['id']}) {task['title']} - {task['description']}")

                elif choice == '3':
                    task_id = input('Enter task id: ')
                    title = input('Enter your new title: ')
                    description = input('Enter your new description: ')
                    await update_task(db, task_id, title, description)

                elif choice == '4':
                    task_id = input('Enter task id: ')
                    await delete_task(db, task_id)
                    print('Task deleted!')

                elif choice == '5':
                    print('You logged out!')
                    login_status = False

                elif choice == '6':
                    task_id = input('Enter task id: ')
                    task = await get_task_by_id(db, task_id)
                if task:
                    print(f'Task found: {task['title']} - {task['description']}')
                else:
                    print('Task not found!')

if __name__ == '__main__':
    asyncio.run(main())
