import json
import time
from dataclasses import asdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

import requests
from mllm import Router
from shortuuid import uuid
from sqlalchemy import asc
from taskara import ReviewRequirement, Task, TaskStatus
from threadmem import RoleThread

from surfkit.db.conn import WithDB
from surfkit.db.models import SkillRecord
from surfkit.server.models import UserTask, UserTasks, V1Skill, V1UpdateSkill


class SkillStatus(Enum):
    """Skill status"""

    COMPLETED = "completed"
    TRAINING = "training"
    AGENT_TRAINING = "agent_training"  # state change for when generated tasks start assigning to agents
    AGENT_REVIEW = "agent_review"
    DEMO = "demo"
    NEEDS_DEFINITION = "needs_definition"
    CREATED = "created"
    FINISHED = "finished"
    CANCELED = "canceled"
    REVIEW = "review"


class Skill(WithDB):
    """An agent skill"""

    def __init__(
        self,
        description: Optional[str] = None,
        requirements: Optional[list[str]] = None,
        name: Optional[str] = None,
        id: Optional[str] = None,
        status: SkillStatus = SkillStatus.NEEDS_DEFINITION,
        agent_type: Optional[str] = None,
        owner_id: Optional[str] = None,
        example_tasks: Optional[list[str]] = None,
        min_demos: Optional[int] = None,
        demos_outstanding: Optional[int] = None,
        remote: Optional[str] = None,
        kvs: Optional[Dict[str, Any]] = None,
        token: Optional[str] = None,
        max_steps_agent: Optional[int] = None,
        review_requirements: Optional[list[ReviewRequirement]] = None,
    ):
        self.description = description or ""
        self.name = name
        self.generating_tasks = False
        if not name:
            self.name = self._get_name()
        self.status = status
        self.requirements = requirements or []
        self.tasks: List[Task] = []
        self.example_tasks = example_tasks or []
        self.owner_id = owner_id
        self.agent_type = agent_type
        self.max_steps = max_steps_agent if max_steps_agent is not None else 40
        self.review_requirements = review_requirements or []
        if not self.agent_type:
            self.agent_type = "foo"
        self.min_demos = min_demos if min_demos is not None else 100
        self.demos_outstanding = (
            demos_outstanding if demos_outstanding is not None else 5
        )
        self.remote = remote
        self.threads: List[RoleThread] = []
        self.kvs = kvs or {}
        self.id = id or uuid()
        self.created = int(time.time())
        self.updated = int(time.time())
        self.token = token

    def _get_name(self) -> str:
        router = Router(
            [
                "mistral/mistral-medium-latest",
                "mistral/mistral-small-latest",
                "mistral/mistral-large-latest",
            ]
        )
        print("generating Name")
        thread = RoleThread()
        thread.post(
            role="user",
            msg=f"Please generate a name for this skill description that is no longer than 5 words, lowercase and hyphenated as a single word, e.g. 'search-for-stays-on-airbnb': '{self.description}'",
        )
        resp = router.chat(thread, model="mistral/mistral-small-latest")
        print(
            "Get Name Chat response", asdict(resp), flush=True
        )  # TODO test pydantic dump
        return resp.msg.text

    def to_v1(self) -> V1Skill:
        if not hasattr(self, "remote"):
            self.remote = None
        return V1Skill(
            id=self.id,
            name=self.name,  # type: ignore
            description=self.description,
            requirements=self.requirements,
            max_steps=self.max_steps,
            review_requirements=[review.to_v1() for review in self.review_requirements]
            if self.review_requirements
            else [],
            agent_type=self.agent_type,  # type: ignore
            tasks=[task.to_v1() for task in self.tasks],
            threads=[thread.to_v1() for thread in self.threads],
            example_tasks=self.example_tasks,
            status=self.status.value,
            generating_tasks=self.generating_tasks
            if hasattr(self, "generating_tasks")
            else False,
            min_demos=self.min_demos,
            demos_outstanding=self.demos_outstanding,
            owner_id=self.owner_id,
            created=self.created,
            updated=self.updated,
            remote=self.remote,
            kvs=self.kvs,
        )

    @classmethod
    def from_v1(
        cls,
        data: V1Skill,
        owner_id: Optional[str] = None,
        auth_token: Optional[str] = None,
        remote: Optional[str] = None,
    ) -> "Skill":
        skill_status = (
            SkillStatus(data.status) if data.status else SkillStatus.NEEDS_DEFINITION
        )
        out = cls.__new__(cls)
        out.id = data.id
        out.name = data.name
        out.description = data.description
        out.requirements = data.requirements
        out.max_steps = data.max_steps
        out.review_requirements = (
            [ReviewRequirement.from_v1(r) for r in data.review_requirements]
            if data.review_requirements
            else []
        )
        out.agent_type = data.agent_type
        out.owner_id = owner_id
        owners = None
        if not out.owner_id:
            out.owner_id = data.owner_id
        if out.owner_id:
            owners = [out.owner_id]

        if not remote:
            remote = data.remote

        out.tasks = []
        for task in data.tasks:
            found = Task.find(
                id=task.id,
                remote=remote,
                auth_token=auth_token,
                owners=owners,
                owner_id=out.owner_id,
            )
            if found:
                out.tasks.append(found[0])
            else:
                print(
                    f"Task {task.id} not found when searching with owners {owners} and remote {remote} and auth_token {auth_token}",
                    flush=True,
                )

        out.example_tasks = data.example_tasks
        out.threads = []  # TODO: fix if needed
        out.status = skill_status
        out.min_demos = data.min_demos
        out.demos_outstanding = data.demos_outstanding
        out.generating_tasks = data.generating_tasks
        out.created = data.created
        out.updated = data.updated
        out.remote = data.remote
        out.kvs = data.kvs
        return out

    def to_record(self) -> SkillRecord:
        return SkillRecord(
            id=self.id,
            owner_id=self.owner_id,
            name=self.name,
            description=self.description,
            requirements=json.dumps(self.requirements),
            max_steps=self.max_steps,
            review_requirements=json.dumps(self.review_requirements),
            agent_type=self.agent_type,
            threads=json.dumps([thread._id for thread in self.threads]),  # type: ignore
            tasks=json.dumps([task.id for task in self.tasks]),
            example_tasks=json.dumps(self.example_tasks),
            generating_tasks=self.generating_tasks,
            status=self.status.value,
            min_demos=self.min_demos,
            demos_outstanding=self.demos_outstanding,
            kvs=json.dumps(self.kvs),
            created=self.created,
            updated=int(time.time()),
        )

    @classmethod
    def from_record(cls, record: SkillRecord) -> "Skill":
        start_time = time.time()
        thread_ids = json.loads(str(record.threads))
        threads = [RoleThread.find(id=thread_id)[0] for thread_id in thread_ids]
        tasks = []
        task_ids = json.loads(str(record.tasks))

        if task_ids:
            tasks = Task.find_many_lite(task_ids)
            valid_task_ids = []

            if len(tasks) < len(task_ids):
                try:
                    print(f"updating tasks for skill {record.id}", flush=True)
                    task_map = {task.id: task for task in tasks}
                    for task_id in task_ids:
                        if not task_map[task_id]:
                            print(f"Task {task_id} not found, removing from skill")
                            continue

                        valid_task_ids.append(task_id)

                    record.tasks = json.dumps(valid_task_ids)  # type: ignore
                    for db in cls.get_db():
                        db.merge(record)
                        db.commit()
                    print(f"updated tasks for skill {record.id}", flush=True)
                except Exception as e:
                    print(
                        f"Error updating tasks for skill {record.id}: {e}", flush=True
                    )
        print(f"tasks found for skill {record.id} time lapsed: {(time.time() - start_time):.4f}")
        example_tasks = json.loads(str(record.example_tasks))

        requirements = json.loads(str(record.requirements))

        out = cls.__new__(cls)
        out.id = record.id
        out.name = record.name
        out.owner_id = record.owner_id
        out.description = record.description
        out.requirements = requirements
        out.max_steps = record.max_steps
        out.review_requirements = (
            json.loads(str(record.review_requirements))
            if record.review_requirements is not None
            else []
        )
        out.agent_type = record.agent_type
        out.threads = threads
        out.tasks = tasks
        out.example_tasks = example_tasks
        out.generating_tasks = record.generating_tasks
        out.status = SkillStatus(record.status)
        out.min_demos = record.min_demos
        out.demos_outstanding = record.demos_outstanding
        out.kvs = json.loads(str(record.kvs)) if record.kvs else {}  # type: ignore
        out.created = record.created
        out.updated = record.updated
        out.remote = None
        print(f"record composed for skill {record.id} time lapsed: {(time.time() - start_time):.4f}")
        return out

    def save(self):
        """
        Save the current state of the Skill either locally or via the remote API.

        For remote saves:
        - If the skill exists remotely, update it via a PUT request.
        - If the skill does not exist remotely, create it via a POST request.

        For local saves, perform the normal database merge/commit.
        """
        if self.remote:
            skill_url = f"{self.remote}/v1/skills/{self.id}"
            payload = self.to_v1().model_dump()  # Adjust serialization as needed
            try:
                # Check if the skill exists remotely.
                get_resp = requests.get(
                    skill_url, headers={"Authorization": f"Bearer {self.token}"}
                )
                if get_resp.status_code == 404:
                    # The skill does not exist remotely, so create it using POST.
                    create_url = f"{self.remote}/v1/skills"
                    post_resp = requests.post(create_url, json=payload)
                    post_resp.raise_for_status()
                    print(f"Skill {self.id} created remotely", flush=True)
                else:
                    # If found, update the remote record using PUT.
                    put_resp = requests.put(skill_url, json=payload)
                    put_resp.raise_for_status()
                    print(f"Skill {self.id} updated remotely", flush=True)
            except requests.RequestException as e:
                print(f"Error saving skill {self.id} on remote: {e}", flush=True)
            return
        else:
            for db in self.get_db():
                record = self.to_record()
                db.merge(record)
                db.commit()

    @classmethod
    def find(
        cls,
        remote: Optional[str] = None,
        owners: Optional[List[str]] = None,
        token: Optional[str] = None,
        **kwargs,  # type: ignore
    ) -> List["Skill"]:
        print("running find for skills", flush=True)
        start_time = time.time()
        if remote:
            # Prepare query parameters
            params = dict(kwargs)
            if owners:
                # Pass owners as multiple query parameters
                for owner in owners:
                    params.setdefault("owners", []).append(owner)

            print(f"Query params for remote request: {params}", flush=True)

            try:
                resp = requests.get(
                    f"{remote}/v1/skills",
                    params=params,
                    headers={"Authorization": f"Bearer {token}"},
                )
                resp.raise_for_status()
            except requests.RequestException as e:
                print(f"Error fetching skills from remote: {e}", flush=True)
                return []

            skills_json = resp.json()
            skills = [
                cls.from_v1(
                    V1Skill.model_validate(skill_data),
                    auth_token=token,
                    remote=remote,
                )
                for skill_data in skills_json["skills"]
            ]

            # Set remote attribute for each skill
            for skill in skills:
                skill.remote = remote

            return skills

        else:
            out = []
            for db in cls.get_db():
                query = db.query(SkillRecord)

                # Apply owners filter if provided
                if owners:
                    query = query.filter(SkillRecord.owner_id.in_(owners))

                # Apply additional filters from kwargs
                for key, value in kwargs.items():
                    query = query.filter(getattr(SkillRecord, key) == value)

                records = query.order_by(asc(SkillRecord.created)).all()
                print(f"skills found in db {records} time lapsed: {(time.time() - start_time):.4f}", flush=True)
                out.extend([cls.from_record(record) for record in records])
                print(f"skills from_record ran time lapsed: {(time.time() - start_time):.4f}", flush=True)
            return out

    def update(self, data: V1UpdateSkill):
        """
        Update the skill's properties based on the provided data.
        After updating the in-memory attributes, the method calls save() to persist
        changes locally or remotely.
        """
        print(f"updating skill {self.id} data: {data.model_dump_json()}", flush=True)
        if data.name:
            self.name = data.name
        if data.description:
            self.description = data.description
        if data.requirements:
            self.requirements = data.requirements
        if data.threads:
            self.threads = [
                RoleThread.find(id=thread_id)[0] for thread_id in data.threads
            ]
        if data.tasks:
            self.tasks = [Task.find(id=task_id)[0] for task_id in data.tasks]
        if data.example_tasks:
            self.example_tasks = data.example_tasks
        if data.status:
            self.status = SkillStatus(data.status)
        if data.max_steps:
            self.max_steps = data.max_steps
        if data.review_requirements:
            self.review_requirements = [
                ReviewRequirement.from_v1(r) for r in data.review_requirements
            ]
        if data.min_demos:
            self.min_demos = data.min_demos
        if data.demos_outstanding:
            self.demos_outstanding = data.demos_outstanding

        # Save the updated skill, either locally or remotely.
        self.save()

    def set_key(self, key: str, value: str):
        """
        Sets the given key to the specified value.
        If a remote is set, delegate this operation to the remote API.
        """
        if self.remote:
            url = f"{self.remote}/v1/skills/{self.id}/keys"
            payload = {"key": key, "value": value}
            try:
                resp = requests.post(
                    url, json=payload, headers={"Authorization": f"Bearer {self.token}"}
                )
                resp.raise_for_status()
                print(
                    f"Successfully set key '{key}' on remote for skill {self.id}",
                    flush=True,
                )
            except requests.RequestException as e:
                print(
                    f"Error setting key on remote for skill {self.id}: {e}", flush=True
                )
            return
        else:
            self.kvs[key] = value
            self.save()

    def get_key(self, key: str) -> Optional[str]:
        """
        Retrieves the value for the given key.
        If a remote is set, retrieve the value via the remote API.
        """
        if self.remote:
            url = f"{self.remote}/v1/skills/{self.id}/keys/{key}"
            try:
                resp = requests.get(
                    url, headers={"Authorization": f"Bearer {self.token}"}
                )
                resp.raise_for_status()
                data = resp.json()
                value = data.get("value")
                print(
                    f"Successfully retrieved key '{key}' from remote for skill {self.id}",
                    flush=True,
                )
                return value
            except requests.RequestException as e:
                print(
                    f"Error retrieving key on remote for skill {self.id}: {e}",
                    flush=True,
                )
                return None
        else:
            return self.kvs.get(key)

    def delete_key(self, key: str):
        """
        Deletes the given key.
        If a remote is set, perform the deletion via the remote API.
        """
        if self.remote:
            url = f"{self.remote}/v1/skills/{self.id}/keys/{key}"
            try:
                resp = requests.delete(url)
                resp.raise_for_status()
                print(
                    f"Successfully deleted key '{key}' on remote for skill {self.id}",
                    flush=True,
                )
            except requests.RequestException as e:
                print(
                    f"Error deleting key on remote for skill {self.id}: {e}", flush=True
                )
            return
        else:
            if key in self.kvs:
                del self.kvs[key]
                self.save()

    def refresh(self):
        """
        Refresh the object state from the database or remote API.
        """
        if self.remote:
            url = f"{self.remote}/v1/skills/{self.id}"
            try:
                resp = requests.get(
                    url, headers={"Authorization": f"Bearer {self.token}"}
                )
                resp.raise_for_status()
                data = resp.json()
                # Assume that the response data can be used to instantiate a V1Skill.
                # You may need to adjust this based on your actual API response format.
                v1skill = V1Skill(**data)
                new = Skill.from_v1(v1skill, owner_id=self.owner_id)
            except requests.RequestException as e:
                raise ValueError(f"Error refreshing skill from remote: {e}")
        else:
            found = self.find(id=self.id)
            if not found:
                raise ValueError("Skill not found")
            new = found[0]

        # Update the current object's fields with the new data.
        self.name = new.name
        self.description = new.description
        self.requirements = new.requirements
        self.max_steps = new.max_steps
        self.review_requirements = new.review_requirements
        self.threads = new.threads
        self.tasks = new.tasks
        self.example_tasks = new.example_tasks
        self.created = new.created
        self.updated = new.updated
        self.owner_id = new.owner_id
        self.agent_type = new.agent_type
        self.generating_tasks = new.generating_tasks
        self.status = new.status
        self.min_demos = new.min_demos
        self.demos_outstanding = new.demos_outstanding
        self.kvs = new.kvs

        return self

    def set_generating_tasks(self, input: bool):
        if self.generating_tasks != input:
            self.generating_tasks = input
            self.save()

    def get_task_descriptions(self, limit: Optional[int] = None):
        maxLimit = len(self.tasks)
        limit = limit if limit and limit < maxLimit else maxLimit
        return {"tasks": [task.description for task in self.tasks[-limit:]]}

    def generate_tasks(
        self,
        n_permutations: int = 1,
        assigned_to: Optional[str] = None,
        assigned_type: Optional[str] = None,
    ) -> List[Task]:
        self.set_generating_tasks(True)
        router = Router(
            [
                "mistral/mistral-medium-latest",
                "mistral/mistral-small-latest",
                "mistral/mistral-large-latest",
            ]
        )
        current_date = datetime.now().strftime("%B %d, %Y")
        example_str = str(
            "For example, if the skill is 'search for stays on airbnb' "
            "and a requirement is 'find stays within a travel window' then a task "
            "might be 'Find the most popular available stays on Airbnb between October 12th to October 14th' "
        )
        example_schema = '{"tasks": ["Find stays from october 2nd to 3rd", "Find stays from January 15th-17th"]}'
        if self.example_tasks:
            example_str = str(
                f"Some examples of tasks for this skill are: '{json.dumps(self.example_tasks)}'"
            )
            example_schema = str('{"tasks": ' f"{json.dumps(self.example_tasks)}" "}")
        if len(self.requirements) > 0:
            print(
                f"Generating tasks for skill: '{self.description}', skill ID: {self.id} with requirements: {self.requirements}",
                flush=True,
            )
            old_task_str = ""
            old_tasks = self.get_task_descriptions(limit=15000)
            if old_tasks:
                old_task_str = str(
                    "Please do not create any tasks identical to these tasks that have already been created: "
                    f"{old_tasks}"
                )
            thread = RoleThread(
                owner_id=self.owner_id
            )  # TODO is this gonna keep one thread? I don't see a need for a new thread every time
            result: List[Task] = []

            for n in range(n_permutations):
                print(
                    f"task generation interation: {n} for skill ID {self.id}",
                    flush=True,
                )

                prompt = (
                    f"Given the agent skill '{self.description}', and the "
                    f"configurable requirements that the agent skill encompasses '{json.dumps(self.requirements)}', "
                    "Please generate a task that a user could take which will excercise this skill, "
                    "our goal is to train and get good at using a skill "
                    f"Today's date is {current_date}. "
                    f"{example_str} "
                    f"Please return a raw json object that looks like the following example: "
                    f"{example_schema} "
                    f"{old_task_str}"
                    "Please ensure the task parameters are varied. If there are dates or numbers please vary them a little bit."
                )
                print(f"prompt: {prompt}", flush=True)
                thread.post("user", prompt)
                response = router.chat(
                    thread, model="mistral/mistral-medium-latest", expect=UserTasks
                )
                print(f"thread {thread}, response: {response}", flush=True)
                if not response.parsed:
                    self.set_generating_tasks(False)
                    raise ValueError(f"unable to parse response: {response}")

                print(
                    f"Generated tasks: {response.parsed.model_dump_json()} for skill ID {self.id}",
                    flush=True,
                )

                gen_tasks = response.parsed.tasks
                if not gen_tasks:
                    self.set_generating_tasks(False)
                    raise ValueError(f"no tasks generated for skill ID {self.id}")
                gen_tasks = gen_tasks[
                    :1
                ]  # take only one as we are doing this one at a time

                if not self.owner_id:
                    self.set_generating_tasks(False)
                    raise ValueError(
                        f"Owner ID must be set on skill ID {self.id} to generate tasks"
                    )

                for task in gen_tasks:
                    tsk = Task(
                        task,
                        owner_id=self.owner_id,
                        review_requirements=[  # TODO commenting this out for now since we are only doing user tasks
                            # ReviewRequirement(
                            #     number_required=1, users=[self.owner_id]
                            # )  # TODO: make this configurable
                        ],
                        max_steps=self.max_steps,
                        assigned_to=assigned_to if assigned_to else self.owner_id,
                        assigned_type=assigned_type if assigned_type else "user",
                        labels={"skill": self.id},
                        created_by='agenttutor'
                    )
                    tsk.status = TaskStatus.IN_QUEUE
                    self.tasks.append(tsk)
                    tsk.save()
                    print(
                        f"task saved for skill ID: {self.id}",
                        tsk.to_v1().model_dump_json(),
                        flush=True,
                    )
                    result.append(tsk)
                self.save()  # need to save for every iteration as we want tasks to incrementally show up
            self.generating_tasks = False
            self.save()

            return result

        else:
            print(f"Generating tasks for skill: {self.description}", flush=True)
            old_task_str = ""
            old_tasks = self.get_task_descriptions(limit=15000)
            if old_tasks:
                old_task_str = str(
                    "Please do not create any tasks identical to these tasks that have already been created: "
                    f"{old_tasks}"
                )
            prompt = (
                f"Given the agent skill '{self.description}' "
                "Please generate a task that a agent could do which will excercise this skill, "
                "our goal is to test whether the agent can perform the skill "
                f"Today's date is {current_date}. "
                f"{example_str} "
                f"Please return a raw json object that looks like the following example: "
                f"{example_schema} "
                f"{old_task_str} "
                "Please ensure the task parameters are varied. If there are dates or numbers please vary them a little bit."
            )
        thread = RoleThread(owner_id=self.owner_id)
        thread.post("user", prompt)

        response = router.chat(
            thread, model="mistral/mistral-medium-latest", expect=UserTask
        )

        if not response.parsed:
            raise ValueError(f"unable to parse response: {response}")

        if not self.owner_id:
            raise ValueError("Owner ID must be set on story to generate tasks")

        task = Task(
            response.parsed.task,
            owner_id=self.owner_id,
            review_requirements=[  # TODO commenting this out for now since we are only doing user tasks
                # ReviewRequirement(
                #     number_required=1, users=[self.owner_id]
                # )  # TODO: make this configurable
            ],
            max_steps=self.max_steps,
            assigned_to=assigned_to if assigned_to else self.owner_id,
            assigned_type=assigned_type if assigned_type else "user",
            labels={"skill": self.id},
            created_by='agenttutor'
        )
        task.status = TaskStatus.IN_QUEUE
        self.tasks.append(task)
        task.save()
        print("task saved", task.to_v1().model_dump_json(), flush=True)
        self.generating_tasks = False
        self.save()
        print(f"Generated task: {task.id}", flush=True)
        return [task]

    def delete(self, owner_id: str):
        for db in self.get_db():
            record = (
                db.query(SkillRecord).filter_by(id=self.id, owner_id=owner_id).first()
            )
            db.delete(record)
            db.commit()
