<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\Room;

class RoomSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $rooms = [
            [
                'room_title' => 'Deluxe King Room',
                'image' => 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=1200',
                'description' => 'Spacious room with king bed, free Wi-Fi and great view.',
                'price' => '120',
                'wifi' => 'yes',
                'room_type' => 'deluxe'
            ],
            [
                'room_title' => 'Standard Twin Room',
                'image' => 'https://images.unsplash.com/photo-1505691938895-1758d7feb511?w=1200',
                'description' => 'Comfortable twin beds, ideal for friends or family.',
                'price' => '80',
                'wifi' => 'yes',
                'room_type' => 'standard'
            ],
            [
                'room_title' => 'Suite with Balcony',
                'image' => 'https://images.unsplash.com/photo-1554995207-c18c203602cb?w=1200',
                'description' => 'Luxury suite featuring balcony and premium amenities.',
                'price' => '220',
                'wifi' => 'yes',
                'room_type' => 'suite'
            ],
        ];

        foreach ($rooms as $r) {
            Room::create($r);
        }
    }
}
