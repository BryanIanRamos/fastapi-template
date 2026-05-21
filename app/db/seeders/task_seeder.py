"""Task seeder"""
from app.db.seeders.base_seeder import BaseSeeder
from app.db.factories.factory import fake
from app.models.task import Task
from app.models.user import User


class TaskSeeder(BaseSeeder):
    """Seed tasks table"""
    
    def run(self):
        """Create sample tasks"""
        if self.count(Task) > 0:
            print("⏭️  Tasks table already seeded, skipping...")
            return
        
        users = self.db.query(User).all()
        if not users:
            print("⚠️  No users found. Seed users first.")
            return
        
        statuses = ["pending", "in_progress", "completed"]
        tasks = []
        
        # Example 1: One custom hardcoded task
        tasks.append(Task(
            title="Setup Development Environment",
            description="Install dependencies and configure local environment",
            status="completed",
            user_id=users[0].user_id,
        ))
        
        # Example 2: Generate 15 random tasks with Faker (change the range(15) to generate more)
        for _ in range(15):
            tasks.append(Task(
                title=fake.sentence(nb_words=4),
                description=fake.paragraph(nb_sentences=2),
                status=fake.word() if fake.word() in statuses else "pending",
                user_id=fake.integer(min=0, max=len(users)-1) and users[fake.integer(min=0, max=len(users)-1)].user_id or users[0].user_id,
            ))
        
        # TODO: Add more tasks here by adding more loops or custom entries above
        
        self.db.add_all(tasks)
        self.db.commit()
        print(f"✅ Seeded {len(tasks)} tasks")
