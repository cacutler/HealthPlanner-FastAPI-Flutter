import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8080';
  final _storage = const FlutterSecureStorage();
  Future<String?> getToken() => _storage.read(key: 'jwt_totken');
  Future<void> saveToken(String token) =>
      _storage.write(key: 'jwt_token', value: token);
  Future<void> clearToken() => _storage.delete(key: 'jwt_token');
  Future<Map<String, String>> _authHeaders() async {
    final token = await getToken();
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }

  Future<bool> login(String email, String password) async {
    final res = await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );
    if (res.statusCode == 200) {
      final token = jsonDecode(res.body)['access_token'];
      await saveToken(token);
      return true;
    }
    return false;
  }

  Future<bool> register(String email, String password) async {
    final res = await http.post(
      Uri.parse('$baseUrl/auth/register'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );
    return res.statusCode == 201;
  }

  Future<List<dynamic>> getWorkouts() async {
    final res = await http.get(
      Uri.parse('$baseUrl/workouts'),
      headers: await _authHeaders(),
    );
    if (res.statusCode == 200) return jsonDecode(res.body);
    throw Exception('Failed to load workouts');
  }

  Future<Map<String, dynamic>> createWorkout(Map<String, dynamic> data) async {
    final res = await http.post(
      Uri.parse('$baseUrl/workouts'),
      headers: await _authHeaders(),
      body: jsonEncode(data),
    );
    if (res.statusCode == 201) return jsonDecode(res.body);
    throw Exception('Failed to create workout');
  }

  Future<List<dynamic>> getNutritionLogs() async {
    final res = await http.get(
      Uri.parse('$baseUrl/nutrition'),
      headers: await _authHeaders(),
    );
    if (res.statusCode == 200) return jsonDecode(res.body);
    throw Exception('Failed to load nutrition logs');
  }

  Future<List<dynamic>> getWeightLogs() async {
    final res = await http.get(
      Uri.parse('$baseUrl/weight'),
      headers: await _authHeaders(),
    );
    if (res.statusCode == 200) return jsonDecode(res.body);
    throw Exception('Failed to load weight logs');
  }
}
