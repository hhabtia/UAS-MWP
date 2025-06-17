<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\RegisterController;
use App\Http\Controllers\LoginController;

// Route untuk register (mengarah ke controller)
Route::post('/register', [RegisterController::class, 'register']);

// Route untuk login (HANYA gunakan controller, bukan closure)
Route::post('/login', [LoginController::class, 'login']);

// Optional: route untuk logout & cek user login
Route::post('/logout', [LoginController::class, 'logout']);
Route::get('/me', [LoginController::class, 'me']);
