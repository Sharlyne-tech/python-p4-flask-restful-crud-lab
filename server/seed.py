#!/usr/bin/env python3

from app import app
from models import db, Plant

from app import app, db
from models import Plant

with app.app_context():
    print("🌱 Seeding data...")
    db.drop_all()
    db.create_all()

    Plant.query.delete()

    aloe = Plant(
        id=1,
        name="Aloe",
        image="./images/aloe.jpg",
        price=11.50,
        is_in_stock=True,
    )

    zz_plant = Plant(
        id=2,
        name="ZZ Plant",
        image="./images/zz-plant.jpg",
        price=25.98,
        is_in_stock=False,
    )
    plants = [
        Plant(name="Aloe", image="./images/aloe.jpg", price=11.50, is_in_stock=True),
        Plant(name="Cactus", image="./images/cactus.jpg", price=7.99, is_in_stock=True),
        Plant(name="Fiddle Leaf Fig", image="./images/fig.jpg", price=25.00, is_in_stock=False),
    ]

    db.session.add_all([aloe, zz_plant])
    db.session.add_all(plants)
    db.session.commit()
    print("✅ Done seeding!")