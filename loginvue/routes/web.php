<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Http\Response;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

// Route utama
Route::get('/', function () {
    return view('welcome');
});

// ✅ Tambahkan ini untuk mengaktifkan CSRF cookie route (WAJIB untuk login via frontend)

