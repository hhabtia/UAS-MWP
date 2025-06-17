<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;
use Illuminate\Validation\ValidationException;

class RegisterController extends Controller
{
    public function register(Request $request)
    {
        try {
            $validated = $request->validate([
                'name' => 'required|string|max:100',
                'username' => 'required|string|max:50|unique:users,username',
                'password' => 'required|string|min:6',
            ]);

            $validated['password'] = bcrypt($validated['password']); // Hash password

            $user = User::create($validated);

            return response()->json([
                'message' => 'Registrasi berhasil',
                'user' => $user,
            ], 201);

        } catch (ValidationException $e) {
            return response()->json([
                'message' => 'Signup gagal: validasi gagal',
                'errors' => $e->errors()
            ], 422);

        } catch (\Exception $e) {
            return response()->json([
                'message' => 'Signup gagal: error server',
                'error' => $e->getMessage()
            ], 500);
        }
    }
}
