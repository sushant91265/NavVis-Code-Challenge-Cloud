import concurrent
from concurrent.futures import ThreadPoolExecutor

from db.models import Task, Result


def process_tasks(db, object_storage_service, threads=10):
    tasks = _tasks_to_process(db)
    for task in tasks:
        try:
            filename = task.filename
            print("processing file " + filename)
            lines = object_storage_service.get(filename)
            if not lines:
                continue
        
            n = int(len(lines) / threads)
            chunks = [lines[i: i + n] for i in range(0, len(lines), n)]

            valid_numbers = []
            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = [executor.submit(_extract_numbers, chunk) for chunk in chunks]
                for future in concurrent.futures.as_completed(futures):
                    for number in future.result():
                        valid_numbers.append(number)

            print(
                "Total valid numbers in " + filename + " are " + str(len(valid_numbers))
            )
            _save_processed_numbers(db, task, valid_numbers)

        except Exception as e:
            print(e)


def _tasks_to_process(db):
    with db():
        rows = db.session.query(Task).filter(
            Task.state == "ack" and Task.status == "active"
        )
        ids = [row.id for row in rows]
        print("Picked up tasks " + str(len(ids)))

        table = Task.__table__
        query = (
            table.update()
            .returning(table.c.id)
            .where(table.c.state == "ack")
            .values(state="pending")
        )
        result = db.session.execute(query)
        db.session.commit()

        rows = result.fetchall()
        ids = [row.id for row in rows]
        result = db.session.query(Task).filter(Task.id.in_(ids))
        tasks = [res for res in result]

        print("Processing tasks " + str(len(tasks)))
        return tasks

    return []


def _extract_numbers(lines):
    res = []
    for line in lines:
        remaining = ""
        number = ""
        if line.startswith("0049"):
            remaining = line[4:]
            number = "0049"
        elif line.startswith("+49"):
            remaining = line[3:]
            number = "+49"
        for r in remaining:
            if str(r).isdigit():
                number = number + r
                if len(number) == 15:
                    res.append(number)
                    break

    return list(set(res))


def _save_processed_numbers(db, task, numbers):
    with db():
        rows = db.session.query(Result).filter(Result.phone_number.in_(numbers))
        existing = [row.phone_number for row in rows]
        new = [number for number in numbers if number not in existing]
        for number in new:
            result = Result(phone_number=number, task_id=task.id)
            db.session.add(result)
        db.session.query(Task).filter(Task.id == task.id).update({'state': 'processed'})
        db.session.commit()
