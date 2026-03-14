<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\Gallary;

class GallarySeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $images = [
            'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=1200',
            'https://images.unsplash.com/photo-1501117716987-c8e6c1abf1f3?w=1200',
            'https://images.unsplash.com/photo-1505691723518-36a0a4a1a7c6?w=1200',
            'https://images.unsplash.com/photo-1496417263034-38ec4f0b665a?w=1200'
        ];

        foreach ($images as $img) {
            Gallary::create(['image' => $img]);
        }
    }
}
