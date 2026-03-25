from __future__ import annotations

from sqlalchemy.orm import Session
import models
from auth import get_password_hash
from database import SessionLocal


def seed_admin(db: Session) -> None:
    """Create default admin user"""

    admin_email = "admin@starterhotel.com"
    existing = db.query(models.User).filter(models.User.email == admin_email).first()
    if existing:
        print(f"Admin already exists: {admin_email}")
        return

    admin = models.User(
        name="Hotel Admin",
        email=admin_email,
        phone="+977-1-4700123",
        usertype="admin",
        password=get_password_hash("admin123"),
    )
    db.add(admin)
    db.commit()
    print(f"✓ Seeded admin user: {admin_email} / admin123")


def seed_rooms(db: Session) -> None:
    """Populate sample rooms with real photos and Kathmandu-themed descriptions"""

    # Check if rooms already exist
    existing_rooms = db.query(models.Room).first()
    if existing_rooms:
        print("Rooms already exist in database, skipping room seeding...")
        return

    rooms_data = [
        {
            "room_title": "Thamel Heritage Suite",
            "image": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80",
            "description": "Experience Nepali elegance in our Heritage Suite overlooking Thamel's vibrant streets. Features a king-size bed with handwoven Dhaka fabric accents, a separate living area with traditional Newari woodwork, and a marble bathroom with rainfall shower.",
            "price": "180",
            "wifi": "yes",
            "room_type": "Suite",
        },
        {
            "room_title": "Himalayan View Deluxe",
            "image": "https://images.unsplash.com/photo-1590490360182-c33d955c7795?w=800&q=80",
            "description": "Wake up to breathtaking views of the Himalayan range from your private balcony. This deluxe room features a queen-size bed, locally crafted furniture, and floor-to-ceiling windows framing the mountain panorama.",
            "price": "150",
            "wifi": "yes",
            "room_type": "Deluxe",
        },
        {
            "room_title": "Durbar Standard Room",
            "image": "https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=800&q=80",
            "description": "A comfortable and tastefully decorated room inspired by Kathmandu's Durbar Square architecture. Queen-size bed, modern en-suite bathroom, writing desk, and all essential amenities for a relaxing stay.",
            "price": "85",
            "wifi": "yes",
            "room_type": "Standard",
        },
        {
            "room_title": "Swayambhu Family Room",
            "image": "https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800&q=80",
            "description": "Spacious family room perfect for exploring Kathmandu together. Two queen-size beds, a cozy sitting area, mini-kitchenette, and child-friendly amenities. Named after the iconic Swayambhunath temple nearby.",
            "price": "200",
            "wifi": "yes",
            "room_type": "Family",
        },
        {
            "room_title": "Backpacker's Comfort Room",
            "image": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800&q=80",
            "description": "Ideal for trekkers and backpackers exploring Thamel. Clean, compact room with a comfortable twin bed, hot shower, luggage storage, and everything you need before your next Himalayan adventure.",
            "price": "45",
            "wifi": "yes",
            "room_type": "Budget",
        },
        {
            "room_title": "Royal Kumari Penthouse",
            "image": "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
            "description": "Our finest accommodation, the Royal Kumari Penthouse offers unparalleled luxury with a 360-degree rooftop terrace, private jacuzzi with mountain views, king-size canopy bed, and personalized butler service.",
            "price": "350",
            "wifi": "yes",
            "room_type": "Penthouse",
        },
        {
            "room_title": "Garden of Dreams Room",
            "image": "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800&q=80",
            "description": "A tranquil retreat overlooking our landscaped garden inspired by Kathmandu's famous Garden of Dreams. Queen-size bed, earthy tones, natural wood finishes, and a private terrace surrounded by greenery.",
            "price": "110",
            "wifi": "yes",
            "room_type": "Standard",
        },
        {
            "room_title": "Everest Business Room",
            "image": "https://images.unsplash.com/photo-1595576508898-0ad5c879a061?w=800&q=80",
            "description": "Designed for business travelers visiting Kathmandu. Ergonomic work desk, high-speed internet, meeting corner, complimentary pressing service, and a comfortable king-size bed for restful nights.",
            "price": "120",
            "wifi": "yes",
            "room_type": "Business",
        },
    ]

    for room_data in rooms_data:
        room = models.Room(**room_data)
        db.add(room)

    db.commit()
    print(f"✓ Seeded {len(rooms_data)} rooms successfully!")


def seed_ratings(db: Session) -> None:
    """Populate sample room ratings"""

    # Check if ratings already exist
    existing_ratings = db.query(models.RoomRating).first()
    if existing_ratings:
        print("Ratings already exist in database, skipping ratings seeding...")
        return

    rooms = db.query(models.Room).all()
    if not rooms:
        print("No rooms found, cannot seed ratings...")
        return

    ratings_data = [
        {
            "room_id": rooms[0].id,
            "username": "Aarav Sharma",
            "email": "aarav@example.com",
            "comment": "Loved the Newari decor and the view of Thamel from the balcony! Best stay in Kathmandu.",
            "rating": 5.0,
            "status": 1,
        },
        {
            "room_id": rooms[1].id,
            "username": "Sophie Anderson",
            "email": "sophie@example.com",
            "comment": "Waking up to see the Himalayas was magical. Perfect room for mountain lovers!",
            "rating": 5.0,
            "status": 1,
        },
        {
            "room_id": rooms[2].id,
            "username": "Rajesh Koirala",
            "email": "rajesh@example.com",
            "comment": "Great value for money in Thamel. Clean, comfortable, and well-located.",
            "rating": 4.0,
            "status": 1,
        },
        {
            "room_id": rooms[3].id,
            "username": "Emily Chen",
            "email": "emily@example.com",
            "comment": "Perfect for our family trip to Nepal! Kids loved the space and the staff was very friendly.",
            "rating": 5.0,
            "status": 1,
        },
        {
            "room_id": rooms[4].id,
            "username": "Marco Rossi",
            "email": "marco@example.com",
            "comment": "Great base for trekking! Hot shower after a long hike felt incredible. Good location in Thamel.",
            "rating": 4.0,
            "status": 1,
        },
        {
            "room_id": rooms[5].id,
            "username": "Priya Adhikari",
            "email": "priya@example.com",
            "comment": "The rooftop jacuzzi with mountain views is absolutely worth it. A once-in-a-lifetime experience!",
            "rating": 5.0,
            "status": 1,
        },
        {
            "room_id": rooms[6].id,
            "username": "James Mitchell",
            "email": "james@example.com",
            "comment": "Such a peaceful room. The garden terrace was my favorite spot for morning tea.",
            "rating": 4.0,
            "status": 1,
        },
        {
            "room_id": rooms[7].id,
            "username": "Sita Thapa",
            "email": "sita@example.com",
            "comment": "Perfect for my business trip. Fast WiFi, quiet room, and excellent location near Durbar Marg.",
            "rating": 4.0,
            "status": 1,
        },
    ]

    for rating_data in ratings_data:
        rating = models.RoomRating(**rating_data)
        db.add(rating)

    db.commit()
    print(f"✓ Seeded {len(ratings_data)} room ratings successfully!")


def seed_bookings(db: Session) -> None:
    """Populate sample bookings"""

    # Check if bookings already exist
    existing_bookings = db.query(models.Booking).first()
    if existing_bookings:
        print("Bookings already exist in database, skipping bookings seeding...")
        return

    rooms = db.query(models.Room).all()
    if not rooms:
        print("No rooms found, cannot seed bookings...")
        return

    bookings_data = [
        {
            "room_id": str(rooms[0].id),
            "name": "Aarav Sharma",
            "email": "aarav@example.com",
            "phone": "+977-9841234567",
            "total_price": 360.00,
            "status": "approved",
            "start_date": "2026-04-01",
            "end_date": "2026-04-03",
        },
        {
            "room_id": str(rooms[1].id),
            "name": "Sophie Anderson",
            "email": "sophie@example.com",
            "phone": "+44-7700-900123",
            "total_price": 450.00,
            "status": "approved",
            "start_date": "2026-04-05",
            "end_date": "2026-04-08",
        },
        {
            "room_id": str(rooms[2].id),
            "name": "Rajesh Koirala",
            "email": "rajesh@example.com",
            "phone": "+977-9801234567",
            "total_price": 255.00,
            "status": "waiting",
            "start_date": "2026-04-10",
            "end_date": "2026-04-13",
        },
        {
            "room_id": str(rooms[3].id),
            "name": "Emily Chen",
            "email": "emily@example.com",
            "phone": "+86-138-0013-8000",
            "total_price": 800.00,
            "status": "approved",
            "start_date": "2026-04-15",
            "end_date": "2026-04-19",
        },
        {
            "room_id": str(rooms[5].id),
            "name": "Priya Adhikari",
            "email": "priya@example.com",
            "phone": "+977-9812345678",
            "total_price": 700.00,
            "status": "paid",
            "start_date": "2026-04-20",
            "end_date": "2026-04-22",
        },
    ]

    for booking_data in bookings_data:
        booking = models.Booking(**booking_data)
        db.add(booking)

    db.commit()
    print(f"✓ Seeded {len(bookings_data)} bookings successfully!")


def seed_gallery(db: Session) -> None:
    """Populate gallery with real hotel/Kathmandu photos"""

    # Check if gallery already exists
    existing_gallery = db.query(models.Gallary).first()
    if existing_gallery:
        print("Gallery already exists in database, skipping gallery seeding...")
        return

    gallery_data = [
        {"image": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80"},
        {"image": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80"},
        {"image": "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800&q=80"},
        {"image": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80"},
        {"image": "https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=800&q=80"},
        {"image": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80"},
        {"image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80"},
        {"image": "https://images.unsplash.com/photo-1605346434674-a440ca4dc4c0?w=800&q=80"},
    ]

    for image_data in gallery_data:
        gallery = models.Gallary(**image_data)
        db.add(gallery)

    db.commit()
    print(f"✓ Seeded {len(gallery_data)} gallery images successfully!")


def seed_contacts(db: Session) -> None:
    """Populate sample contact submissions"""

    # Check if contacts already exist
    existing_contacts = db.query(models.Contact).first()
    if existing_contacts:
        print("Contacts already exist in database, skipping contacts seeding...")
        return

    contacts_data = [
        {
            "name": "Bikram Shrestha",
            "email": "bikram@example.com",
            "phone": "+977-9841111111",
            "message": "I'm planning a honeymoon trip to Kathmandu. Do you have any special packages for the Kumari Penthouse?",
        },
        {
            "name": "Hannah Williams",
            "email": "hannah@example.com",
            "phone": "+1-555-0202",
            "message": "Wonderful experience at your hotel! The staff was incredibly warm and the location in Thamel was perfect for exploring.",
        },
        {
            "name": "Deepak Gurung",
            "email": "deepak@example.com",
            "phone": "+977-9802222222",
            "message": "Do you have corporate rates available for a team of 20 people? We're planning a company retreat in Kathmandu.",
        },
        {
            "name": "Lisa Tanaka",
            "email": "lisa@example.com",
            "phone": "+81-90-1234-5678",
            "message": "The mountain view from the Deluxe room was stunning! Can I book the same room for my next visit in December?",
        },
    ]

    for contact_data in contacts_data:
        contact = models.Contact(**contact_data)
        db.add(contact)

    db.commit()
    print(f"✓ Seeded {len(contacts_data)} contact submissions successfully!")


def seed_blogs(db: Session) -> None:
    """Populate sample blog posts"""

    existing_blogs = db.query(models.Blog).first()
    if existing_blogs:
        print("Blogs already exist in database, skipping blog seeding...")
        return

    blogs_data = [
        {
            "title": "Top 10 Things to Do in Kathmandu Valley",
            "excerpt": "From the ancient temples of Durbar Square to the panoramic views at Nagarkot, discover the must-visit spots in and around Kathmandu that make Nepal truly magical.",
            "content": "Kathmandu Valley is a treasure trove of cultural heritage, natural beauty, and spiritual wonder. Here are the top experiences you shouldn't miss:\n\n1. **Kathmandu Durbar Square** – Marvel at the intricate Newari architecture and the Kumari Ghar, home of the Living Goddess.\n\n2. **Swayambhunath (Monkey Temple)** – Climb the 365 steps for sweeping valley views and encounter playful monkeys along the way.\n\n3. **Boudhanath Stupa** – One of the largest stupas in the world, this is the spiritual heart of Tibetan Buddhism in Nepal.\n\n4. **Pashupatinath Temple** – A sacred Hindu temple on the banks of the Bagmati River, offering a window into Nepal's spiritual traditions.\n\n5. **Thamel** – Kathmandu's vibrant tourist hub, perfect for shopping, dining, and nightlife.\n\n6. **Patan Durbar Square** – Often considered more beautiful than its Kathmandu counterpart, with stunning metalwork and woodcarving.\n\n7. **Bhaktapur** – Step back in time in this remarkably preserved medieval city.\n\n8. **Nagarkot** – A short drive from the city for breathtaking sunrise views over the Himalayas.\n\n9. **Garden of Dreams** – A serene neoclassical garden oasis in the middle of busy Thamel.\n\n10. **Chandragiri Hills** – Take the cable car for panoramic views stretching from Annapurna to Everest on a clear day.",
            "image": "https://images.unsplash.com/photo-1605640840605-14ac1855827b?w=800&q=80",
            "category": "Travel",
            "author": "StarterHotel Team",
        },
        {
            "title": "Preparing for Your First Himalayan Trek",
            "excerpt": "Everything you need to know before trekking in Nepal — from gear essentials and altitude tips to choosing the right route for your fitness level.",
            "content": "Nepal is the ultimate trekking destination, but preparation is key to a safe and enjoyable experience.\n\n**Choosing Your Trek**\nFor beginners, the Poon Hill trek (4-5 days) offers stunning Annapurna views without extreme altitude. The Everest Base Camp trek (12-14 days) is iconic but requires good fitness. The Langtang Valley trek is less crowded and equally beautiful.\n\n**Essential Gear**\n- Quality hiking boots (broken in before your trip)\n- Layered clothing system (base, insulation, waterproof shell)\n- A good backpack (30-40L for teahouse treks)\n- Trekking poles, sunscreen, sunglasses\n- Water purification tablets or a filter\n\n**Altitude Awareness**\nAbove 3,000m, ascend no more than 500m per day. Stay hydrated, watch for headaches or nausea, and never ignore symptoms of altitude sickness.\n\n**Permits & Guides**\nMost treks require TIMS cards and conservation area permits. Hiring a local guide supports the community and adds safety.\n\n**Our Tip**\nStay at StarterHotel before and after your trek — we offer gear storage, hot showers, and the best rest in Thamel!",
            "image": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=800&q=80",
            "category": "Trekking",
            "author": "StarterHotel Team",
        },
        {
            "title": "A Food Lover's Guide to Thamel",
            "excerpt": "Explore the best local eateries, rooftop restaurants, and hidden gems in Thamel — from authentic momos and dal bhat to fusion cuisine and cozy cafés.",
            "content": "Thamel isn't just Kathmandu's tourist hub — it's a food paradise. Here's where to eat:\n\n**Must-Try Nepali Dishes**\n- **Dal Bhat** – The national dish: lentil soup, rice, vegetables, and pickles. You'll find it everywhere and it's endlessly satisfying.\n- **Momos** – Nepali dumplings, steamed or fried, filled with meat or vegetables. Try them at every opportunity.\n- **Newari Khaja Set** – A traditional Newari feast with beaten rice, marinated meats, and local pickles.\n\n**Top Restaurants**\n- **OR2K** – A vegetarian Middle Eastern restaurant with floor seating and great vibes.\n- **Rosemary Kitchen** – Beloved by locals and tourists alike for Nepali and continental food.\n- **Yangling Tibetan Restaurant** – The best thukpa (noodle soup) and momos in Thamel.\n\n**Rooftop Dining**\nMany Thamel restaurants have rooftop terraces — perfect for sunset dinners with views of the surrounding hills.\n\n**Cafés**\nFor coffee lovers, Himalayan Java and Café Soma are great spots to relax after a day of exploring.\n\nPro tip: Ask our front desk for the latest recommendations — Thamel's food scene is always evolving!",
            "image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&q=80",
            "category": "Food",
            "author": "StarterHotel Team",
        },
        {
            "title": "Nepal's Hidden Gems: Beyond Kathmandu",
            "excerpt": "Venture beyond the capital to discover Pokhara's lakeside charm, Lumbini's spiritual peace, and Chitwan's wild jungle adventures.",
            "content": "While Kathmandu is incredible, Nepal has so much more to offer.\n\n**Pokhara**\nNepal's adventure capital sits beside the serene Phewa Lake with the Annapurna range as a backdrop. Try paragliding, visit the World Peace Pagoda, or simply relax lakeside.\n\n**Chitwan National Park**\nA UNESCO World Heritage Site, home to one-horned rhinos, Bengal tigers, and over 500 bird species. Jungle safaris here are unforgettable.\n\n**Lumbini**\nThe birthplace of Lord Buddha. Visit the sacred garden, Mayadevi Temple, and monasteries built by countries from around the world.\n\n**Bandipur**\nA charming hilltop town frozen in time, with traditional Newari architecture and stunning valley views.\n\n**Ilam**\nNepal's tea country in the far east. Rolling green hills, tea gardens, and a peaceful atmosphere reminiscent of Darjeeling.\n\nWe can help arrange transport and accommodation for all these destinations from our front desk in Thamel!",
            "image": "https://images.unsplash.com/photo-1585938389612-a552a28d6914?w=800&q=80",
            "category": "Travel",
            "author": "StarterHotel Team",
        },
        {
            "title": "The Best Seasons to Visit Nepal",
            "excerpt": "Plan your trip around Nepal's seasons — from the crystal-clear autumn skies perfect for trekking to the lush monsoon landscapes ideal for photographers.",
            "content": "Timing your Nepal trip right can make all the difference.\n\n**Autumn (Sep-Nov) — Peak Season**\nClear skies, mild temperatures, and the best mountain views. Ideal for trekking and sightseeing. Book early as hotels fill up fast!\n\n**Spring (Mar-May) — Second Best**\nRhododendrons bloom across the hillsides. Warm days but occasional haze. Great for trekking and cultural festivals like Holi.\n\n**Winter (Dec-Feb) — Budget Season**\nCold but clear at lower altitudes. Fewer tourists mean lower prices and a more authentic experience. High-altitude treks are closed.\n\n**Monsoon (Jun-Aug) — Green Season**\nLush landscapes and dramatic skies. Rain mostly falls at night. Great for photographers and those who don't mind occasional showers. Chitwan and Lumbini are excellent monsoon destinations.\n\nNo matter when you visit, StarterHotel in Thamel is ready to welcome you with warm Nepali hospitality!",
            "image": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=800&q=80",
            "category": "Tips",
            "author": "StarterHotel Team",
        },
    ]

    for blog_data in blogs_data:
        blog = models.Blog(**blog_data)
        db.add(blog)

    db.commit()
    print(f"✓ Seeded {len(blogs_data)} blog posts successfully!")


def main() -> None:
    """Main function to seed all data"""
    db = SessionLocal()
    try:
        print("\n🌱 Starting database seeding...\n")
        seed_admin(db)
        seed_rooms(db)
        seed_ratings(db)
        seed_bookings(db)
        seed_gallery(db)
        seed_contacts(db)
        seed_blogs(db)
        print("\n✅ Database seeding completed successfully!\n")
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}\n")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
