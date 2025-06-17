<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Auth;

class LoginController extends Controller
{
    public function login(Request $request)
    {
        $credentials = $request->only('username', 'password');

        Log::info('Percobaan login:', $credentials);

        $user = User::where('username', $credentials['username'])->first();

        if (!$user) {
            Log::warning('Login gagal: Username tidak ditemukan', ['username' => $credentials['username']]);
            return response()->json(['message' => 'Login gagal: username atau password salah'], 401);
        }

        if (!Hash::check($credentials['password'], $user->password)) {
            Log::warning('Login gagal: Password salah untuk username ' . $credentials['username']);
            return response()->json(['message' => 'Login gagal: username atau password salah'], 401);
        }

        Auth::login($user);

        Log::info('Login berhasil untuk username ' . $credentials['username']);

        return response()->json([
            'message' => 'Login berhasil',
            'user' => $user,
        ]);
    }
}
