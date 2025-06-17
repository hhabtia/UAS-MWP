<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class ProdukScraping extends Model
{
    protected $connection = 'scraping'; // 👈 Penting ini!
    protected $table = 'produk';        // Ganti sesuai tabelmu
    public $timestamps = false;         // Kalau gak pakai created_at/updated_at
}
