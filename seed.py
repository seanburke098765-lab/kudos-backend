from sqlalchemy.orm import Session
from database import engine, User, Device, Interaction
from datetime import datetime

def seed_data():
    db = Session(bind=engine)
    try:
        # 1. Clean out any existing test data to start fresh
        db.query(Interaction).delete()
        db.query(Device).delete()
        db.query(User).delete()
        
        print("Seeding initial Kudos ecosystem data...")

        # 2. Create mock entrepreneur profiles
        user_1 = User(
            id="user-alex-99",
            name="Alex Rivera",
            email="alex@riveratech.io",
            company="Rivera Tech Solutions",
            bio="Building next-gen IoT infrastructure for smart warehouses.",
            linkedin_url="https://linkedin.com/in/alexrivera-demo"
        )
        
        user_2 = User(
            id="user-taylor-88",
            name="Taylor Chen",
            email="taylor@chenventures.com",
            company="Chen Ventures",
            bio="Early-stage angel investor looking for hardware ecosystems.",
            linkedin_url="https://linkedin.com/in/taylorchen-demo"
        )
        
        db.add_all([user_1, user_2])
        db.commit() # Save users to get relationships ready

        # 3. Assign a physical wearable to each user
        device_1 = Device(hardware_uuid="kudos-hw-0001", user_id=user_1.id)
        device_2 = Device(hardware_uuid="kudos-hw-0002", user_id=user_2.id)
        
        db.add_all([device_1, device_2])
        
        # 4. Log a physical interaction (Alex's device detected Taylor's device)
        mock_interaction = Interaction(
            host_device_uuid="kudos-hw-0001",  # Alex scanned
            guest_device_uuid="kudos-hw-0002", # Taylor's device
            interacted_at=datetime.utcnow()
        )
        
        db.add(mock_interaction)
        db.commit()
        print("Successfully seeded: 2 Users, 2 Devices, 1 Physical Interaction!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
