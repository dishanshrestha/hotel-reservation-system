<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class RoomRating extends Model
{
    use HasFactory;

    protected $fillable = ['name', 'email', 'comment', 'rating']; // Ensure these fields match your database

    public function room()
    {
        return $this->belongsTo(Room::class);
    }
}
